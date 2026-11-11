#!/usr/bin/env python3
"""Capture one bounded YouTube livestream attempt without checkpoint recovery."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

ACCESS_PATTERN = re.compile(
    r"(?:login required|sign in to confirm|bot challenge|\bDRM\b|"
    r"HTTP Error (?:401|403): (?:Forbidden|Unauthorized))", re.I
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def atomic_json(path: Path, data: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def append_event(run_dir: Path, event: str, **details: object) -> None:
    with (run_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps({"at": utc_now(), "event": event, **details}, sort_keys=True) + "\n"
        )


def size_of(path: Path) -> int:
    try:
        return path.stat().st_size if path.is_file() else 0
    except FileNotFoundError:
        return 0


def media_sizes(segment: Path, video_format: str, audio_format: str) -> dict[str, int]:
    """Read selected yt-dlp fragment files without prefix collisions or churn failures."""
    def selected(format_id: str) -> int:
        if not format_id:
            return 0
        return sum(size_of(item) for item in segment.glob(f"capture.f{format_id}.*"))
    return {"video": selected(video_format), "audio": selected(audio_format)}


def total_bytes(segment: Path) -> int:
    return sum(size_of(item) for item in segment.rglob("*") if item.is_file())


def combined_bytes(segment: Path) -> int:
    """Track merged output separately; it cannot prove both original tracks progressed."""
    extensions = (".mp4", ".mkv", ".webm", ".ts", ".m4a", ".part")
    return sum(
        size_of(item) for item in segment.glob("capture.*")
        if not item.name.startswith("capture.f") and item.name.endswith(extensions)
    )


def group_stop(process: subprocess.Popen[str], grace: float = 2.0) -> None:
    """Stop the owned process group, including descendants after the direct child exits."""
    def group_exists() -> bool:
        try:
            os.killpg(process.pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            if process.poll() is None:
                raise
            return False

    if not group_exists():
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + grace
    try:
        process.wait(timeout=max(0.001, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        pass
    while group_exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    if group_exists():
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=1)


def classify_metadata(value: object) -> str:
    if not isinstance(value, dict):
        return "unknown"
    if value.get("is_live") is True:
        return "live"
    return (
        "ended" if value.get("live_status") in {"post_live", "was_live"} else "unknown"
    )


def has_access_restriction(output: str) -> bool:
    return any(
        ACCESS_PATTERN.search(line) and "retry" not in line.lower()
        for line in output.splitlines()
    )


def confirmed_end(source: str, downloader: str, timeout: float) -> bool:
    try:
        result = subprocess.run(
            [
                downloader, "--ignore-config", "--no-playlist", "--skip-download",
                "--dump-single-json", source,
            ],
            capture_output=True, text=True, timeout=timeout, check=False, stdin=subprocess.DEVNULL,
        )
        return result.returncode == 0 and classify_metadata(json.loads(result.stdout)) == "ended"
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return False


def probe_and_decode(media: Path, timeout: float) -> tuple[bool, dict[str, object]]:
    deadline = time.monotonic() + timeout
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(media)],
            capture_output=True, text=True,
            timeout=max(0.001, deadline - time.monotonic()),
            check=False, stdin=subprocess.DEVNULL,
        )
        document = json.loads(probe.stdout) if probe.returncode == 0 else {}
        kinds = {stream.get("codec_type") for stream in document.get("streams", [])}
        duration = float(document.get("format", {}).get("duration", 0))
        if not {"audio", "video"}.issubset(kinds) or duration <= 0:
            return False, {"duration_seconds": duration, "decoded_seconds": 0}
        decoded = min(duration, 1.0)
        for selector in ("0:v:0", "0:a:0"):
            if (remaining := deadline - time.monotonic()) <= 0:
                return False, {"duration_seconds": duration, "decoded_seconds": 0}
            decode = subprocess.run(
                [
                    "ffmpeg", "-nostdin", "-v", "error", "-t", str(decoded),
                    "-i", str(media), "-map", selector, "-f", "null", "-",
                ],
                capture_output=True, text=True, timeout=remaining,
                check=False, stdin=subprocess.DEVNULL,
            )
            if decode.returncode != 0:
                return False, {"duration_seconds": duration, "decoded_seconds": 0}
        return True, {"duration_seconds": duration, "decoded_seconds": decoded}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError, ValueError):
        return False, {"duration_seconds": 0, "decoded_seconds": 0}


@dataclass(frozen=True)
class Limits:
    capture_seconds: float
    request_seconds: float
    stall_seconds: float
    max_bytes: int
    min_free_bytes: int


class Recorder:
    def __init__(self, arguments: argparse.Namespace) -> None:
        self.args = arguments
        self.run_dir = Path(arguments.run_dir)
        self.limits = Limits(
            arguments.capture_seconds, arguments.request_seconds, arguments.stall_seconds,
            arguments.max_bytes, arguments.min_free_bytes,
        )
        self.active: subprocess.Popen[str] | None = None
        self.cancelled = False

    def status(self, state: str, reason: str, **details: object) -> None:
        atomic_json(
            self.run_dir / "status.json",
            {"at": utc_now(), "state": state, "reason": reason, **details},
        )
        append_event(self.run_dir, "status", state=state, reason=reason, **details)

    def prepare(self) -> None:
        parsed = urlparse(self.args.source)
        if parsed.scheme != "https" or parsed.hostname not in {
            "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be",
        }:
            raise ValueError("source must be an approved YouTube URL")
        if not os.environ.get("RECORDER_TEST_COMMAND") and not (
            self.args.video_format and self.args.audio_format
        ):
            raise ValueError("video and original-audio format identifiers are required")
        if self.run_dir.exists() or any(
            value <= 0 or (isinstance(value, float) and not math.isfinite(value))
            for value in asdict(self.limits).values()
        ):
            raise ValueError("run directory must be new and limits must be finite and positive")
        for executable in (self.args.downloader, "ffmpeg", "ffprobe"):
            if shutil.which(executable) is None:
                raise ValueError(f"required executable is unavailable: {executable}")
        self.run_dir.mkdir(parents=True, exist_ok=False)
        agreement = {
            "created_at": utc_now(), "source": self.args.source,
            "from_start": self.args.from_start, "limits": asdict(self.limits),
            "checkpoint_recovery": "unsupported and disabled",
            "track_ids": {"video": self.args.video_format, "audio": self.args.audio_format},
        }
        atomic_json(self.run_dir / "agreement.json", agreement)
        append_event(self.run_dir, "prepared", **agreement)

    def command(self, segment: Path) -> list[str]:
        test_mode = os.environ.get("RECORDER_TEST_COMMAND")
        if test_mode:
            return [self.args.downloader, test_mode, str(segment)]
        result = [
            self.args.downloader, "--ignore-config", "--no-playlist", "--no-continue",
            "--no-overwrites", "--socket-timeout", str(self.limits.request_seconds),
            "-o", str(segment / "capture.%(ext)s"), "-f",
            f"{self.args.video_format}+{self.args.audio_format}",
        ]
        result.append("--live-from-start" if self.args.from_start else "--no-live-from-start")
        return [*result, self.args.source]

    def capture(self, segment: Path) -> tuple[bool, str]:
        segment.mkdir()
        command = self.command(segment)
        log_path = segment / "downloader.log"
        with log_path.open("w", encoding="utf-8") as log:
            self.active = subprocess.Popen(
                command, stdout=log, stderr=subprocess.STDOUT, text=True,
                start_new_session=True, stdin=subprocess.DEVNULL,
            )
        append_event(
            self.run_dir, "child-start", command=command,
            pid=self.active.pid, segment=segment.name,
        )
        started = time.monotonic()
        previous = media_sizes(segment, self.args.video_format, self.args.audio_format)
        progressed = {name: started for name in previous}
        combined_previous = 0
        combined_progress = started
        last_heartbeat = 0.0
        try:
            while self.active.poll() is None:
                time.sleep(0.1)
                now = time.monotonic()
                sizes = media_sizes(segment, self.args.video_format, self.args.audio_format)
                growing_tracks = {
                    name for name, value in sizes.items() if value > previous[name]
                }
                for name in growing_tracks:
                    progressed[name] = now
                previous = sizes
                merged = combined_bytes(segment)
                if merged > combined_previous:
                    combined_progress = now
                combined_previous = merged
                selected_seen = all(when > started for when in progressed.values())
                combined_only = merged > 0 and not any(sizes.values())
                reason = ""
                if self.cancelled:
                    reason = "cancelled"
                elif now - started > self.limits.capture_seconds:
                    reason = "capture deadline"
                elif total_bytes(self.run_dir) > self.limits.max_bytes:
                    reason = "byte budget"
                elif shutil.disk_usage(self.run_dir).free < self.limits.min_free_bytes:
                    reason = "disk reserve"
                elif combined_only and not selected_seen:
                    reason = "per-track progress unavailable: combined output"
                elif merged > 0 and selected_seen and not growing_tracks:
                    if (
                        now - max(combined_progress, *progressed.values())
                        > self.limits.stall_seconds
                    ):
                        reason = "merge stall"
                elif any(now - value > self.limits.stall_seconds for value in progressed.values()):
                    reason = "per-track stall"
                if now - last_heartbeat >= 1:
                    self.status(
                        "capturing", "heartbeat", pid=self.active.pid,
                        track_bytes=sizes, total_bytes=total_bytes(self.run_dir),
                    )
                    last_heartbeat = now
                if reason:
                    group_stop(self.active)
                    if has_access_restriction(
                        log_path.read_text(encoding="utf-8", errors="replace")
                    ):
                        return False, "access restriction"
                    return False, reason
            code = self.active.returncode
            output = log_path.read_text(encoding="utf-8")
            if has_access_restriction(output):
                return False, "access restriction"
            if total_bytes(self.run_dir) > self.limits.max_bytes:
                return False, "byte budget"
            return code == 0, "downloader exited"
        except Exception as error:
            return False, f"supervision error: {type(error).__name__}"
        finally:
            if self.active is not None:
                group_stop(self.active)
            self.active = None

    def inspect_partial(self, segment: Path) -> dict[str, object]:
        playable: list[str] = []
        unverified: list[str] = []
        sampled_intervals: dict[str, dict[str, float | None]] = {}
        try:
            items = list(segment.iterdir())
        except FileNotFoundError:
            return {
                "playable_outputs": playable, "unverified_outputs": unverified,
                "sampled_intervals": sampled_intervals,
            }
        deadline = time.monotonic() + self.limits.request_seconds
        for item in items:
            if not item.is_file() or item.name == "downloader.log":
                continue
            if item.name.startswith(f"capture.f{self.args.video_format}."):
                selector = "v"
            elif item.name.startswith(f"capture.f{self.args.audio_format}."):
                selector = "a"
            else:
                unverified.append(item.name)
                continue
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                unverified.append(item.name)
                continue
            try:
                probe = subprocess.run(
                    [
                        "ffprobe", "-v", "error", "-select_streams", f"{selector}:0",
                        "-show_entries", "stream=codec_type:format=duration",
                        "-of", "json", str(item),
                    ],
                    capture_output=True, text=True, timeout=remaining,
                    check=False, stdin=subprocess.DEVNULL,
                )
                report = json.loads(probe.stdout) if probe.returncode == 0 else {}
                valid = bool(report.get("streams", []))
                if valid and (remaining := deadline - time.monotonic()) > 0:
                    decode = subprocess.run(
                        [
                            "ffmpeg", "-nostdin", "-v", "error", "-t", "1",
                            "-i", str(item), "-map", f"0:{selector}:0", "-f", "null", "-",
                        ],
                        capture_output=True, text=True, timeout=remaining,
                        check=False, stdin=subprocess.DEVNULL,
                    )
                    valid = decode.returncode == 0
                    if valid:
                        raw_duration = report.get("format", {}).get("duration")
                        try:
                            duration = float(raw_duration)
                        except (TypeError, ValueError):
                            duration = None
                        sampled_intervals[item.name] = {
                            "start_seconds": 0,
                            "requested_end_seconds": 1,
                            "measured_end_seconds": (
                                min(1, duration) if duration and duration > 0 else None
                            ),
                        }
                else:
                    valid = False
            except (FileNotFoundError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
                valid = False
            (playable if valid else unverified).append(item.name)
        return {
            "playable_outputs": playable, "unverified_outputs": unverified,
            "sampled_intervals": sampled_intervals,
        }

    def run(self) -> int:
        self.prepare()
        signal.signal(signal.SIGINT, lambda *_: setattr(self, "cancelled", True))
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, "cancelled", True))
        segment = self.run_dir / "segment-000"
        success, reason = self.capture(segment)
        if not success:
            self.status(
                "stopped" if reason == "access restriction" else "partial",
                reason, **self.inspect_partial(segment),
            )
            return 1
        self.status("verifying", "downloader exited")
        deadline = time.monotonic() + self.limits.request_seconds
        verified, coverage = False, {"duration_seconds": 0, "decoded_seconds": 0}
        for path in segment.glob("capture.*"):
            if (
                path.is_file() and not path.name.endswith(".part")
                and (remaining := deadline - time.monotonic()) > 0
            ):
                verified, coverage = probe_and_decode(path, remaining)
                if verified:
                    break
        remaining = deadline - time.monotonic()
        ended = (
            False if os.environ.get("RECORDER_TEST_COMMAND") or remaining <= 0
            else confirmed_end(self.args.source, self.args.downloader, remaining)
        )
        details = {
            "decodable": verified, "source_ended": ended,
            "coverage": {"captured": "unknown", "broadcast_complete": "unknown", **coverage},
        }
        if verified and ended:
            self.status("complete", "confirmed end and sampled audiovisual decode", **details)
            return 0
        self.status("partial", "end confirmation or media verification failed", **details)
        return 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("source")
    result.add_argument("run_dir")
    result.add_argument("--downloader", default="yt-dlp")
    result.add_argument("--from-start", action="store_true")
    result.add_argument("--video-format", default="")
    result.add_argument("--audio-format", default="")
    result.add_argument("--capture-seconds", type=float, default=300)
    result.add_argument("--request-seconds", type=float, default=30)
    result.add_argument("--stall-seconds", type=float, default=60)
    result.add_argument("--max-bytes", type=int, default=1_000_000_000)
    result.add_argument("--min-free-bytes", type=int, default=1_000_000_000)
    return result


def main(argv: Iterable[str] | None = None) -> int:
    try:
        return Recorder(parser().parse_args(argv)).run()
    except (ValueError, FileNotFoundError, OSError, subprocess.TimeoutExpired) as error:
        print(f"record_livestream: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
