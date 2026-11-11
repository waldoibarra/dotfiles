#!/usr/bin/env python3
"""Bounded local tests for the livestream recorder. No network media is acquired."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/.agents/skills/video-analysis/scripts/record_livestream.py"
SPEC = importlib.util.spec_from_file_location("recorder", SCRIPT)
assert SPEC and SPEC.loader
recorder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = recorder
SPEC.loader.exec_module(recorder)

FAKE = """#!/usr/bin/env python3
import pathlib, sys, time
mode, segment = sys.argv[1], pathlib.Path(sys.argv[2])
if mode == 'access':
    print('HTTP Error 403: Forbidden', flush=True)
    raise SystemExit(1)
if mode == 'access-delayed':
    print('HTTP Error 403: Forbidden', flush=True)
    time.sleep(1)
if mode == 'transient-403':
    print('HTTP Error 403: Forbidden. Retrying fragment 5 (1/10)...')
if mode == 'fail':
    (segment / 'video.part').write_bytes(b'video')
    (segment / 'audio.part').write_bytes(b'audio')
    raise SystemExit(1)
if mode == 'video-only':
    (segment / 'capture.f140.m4a.part').write_bytes(b'initial-audio')
    for _ in range(30):
        with (segment / 'capture.f137.mp4.part').open('ab') as handle: handle.write(b'x')
        time.sleep(.03)
if mode == 'combined-growing':
    for _ in range(30):
        with (segment / 'capture.mp4.part').open('ab') as handle: handle.write(b'x')
        time.sleep(.03)
if mode in ('merge-after-tracks', 'merge-with-intermediates', 'merge-frozen'):
    for name in ('capture.f137.mp4.part', 'capture.f140.m4a.part'):
        (segment / name).write_bytes(b'initial')
    time.sleep(.2)
    if mode == 'merge-after-tracks':
        for name in ('capture.f137.mp4.part', 'capture.f140.m4a.part'):
            (segment / name).unlink()
    if mode == 'merge-frozen':
        (segment / 'capture.mp4.part').write_bytes(b'beginning')
        time.sleep(2)
    else:
        for _ in range(30):
            with (segment / 'capture.mp4.part').open('ab') as handle: handle.write(b'x')
            time.sleep(.03)
    raise SystemExit(1)
if mode in ('audio-frozen-static-meta', 'audio-frozen-combined-growing'):
    (segment / 'capture.f140.m4a.part').write_bytes(b'initial-audio')
    (segment / 'capture.f137.mp4.part').write_bytes(b'initial-video')
    if mode == 'audio-frozen-static-meta':
        (segment / 'capture.meta').write_bytes(b'static')
    for _ in range(40):
        with (segment / 'capture.f137.mp4.part').open('ab') as handle: handle.write(b'x')
        if mode == 'audio-frozen-combined-growing':
            with (segment / 'capture.temp.mp4').open('ab') as handle: handle.write(b'x')
        time.sleep(.05)
if mode == 'both-growing':
    for _ in range(30):
        for name in ('capture.f137.mp4.part', 'capture.f140.m4a.part'):
            with (segment / name).open('ab') as handle: handle.write(b'x')
        time.sleep(.03)
if mode == 'churn':
    for index in range(30):
        fragment = segment / f'video.part-Frag{index}'
        fragment.write_bytes(b'x')
        fragment.unlink()
        time.sleep(.01)
if mode == 'sleep':
    time.sleep(30)
if mode == 'child-exits-grandchild':
    import subprocess
    grandchild = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(30)'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    (segment / 'grandchild.pid').write_text(str(grandchild.pid))
    time.sleep(.1)
    raise SystemExit(1)
if mode == 'success':
    (segment / 'video.part').write_bytes(b'video')
    (segment / 'audio.part').write_bytes(b'audio')
"""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RecorderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.fake = self.base / "fake.py"
        self.fake.write_text(FAKE, encoding="utf-8")
        self.fake.chmod(0o755)
        self.invocations: list[
            tuple[list[str], subprocess.CompletedProcess[str]]
        ] = []

    def tearDown(self) -> None:
        outcome = getattr(self, "_outcome", None)
        result = getattr(outcome, "result", None)
        if result is not None and any(
            case is self for case, _ in result.failures + result.errors
        ):
            print(self.diagnostics(), file=sys.stderr, flush=True)
        self.temp.cleanup()

    def command(self, mode: str, name: str, *extra: str) -> list[str]:
        return [
            sys.executable, str(SCRIPT), "https://www.youtube.com/watch?v=fixture",
            str(self.base / name), "--downloader", str(self.fake),
            "--capture-seconds", "1", "--stall-seconds", "0.15",
            "--request-seconds", "1", "--max-bytes", "10000", "--min-free-bytes", "1", *extra,
        ]

    def environment(self, mode: str) -> dict[str, str]:
        return {**os.environ, "RECORDER_TEST_COMMAND": mode}

    def invoke(self, mode: str, name: str, *extra: str) -> subprocess.CompletedProcess[str]:
        command = self.command(mode, name, *extra)
        completed = subprocess.run(
            command, text=True, capture_output=True, timeout=5,
            env=self.environment(mode),
        )
        self.invocations.append((command, completed))
        return completed

    def diagnostics(self) -> str:
        runs = []
        for command, completed in self.invocations:
            run = Path(command[3])
            files = {}
            for filename in ("status.json", "events.jsonl", "segment-000/downloader.log"):
                candidate = run / filename
                files[filename] = (
                    candidate.read_text(errors="replace") if candidate.exists() else None
                )
            runs.append({
                "command": command, "returncode": completed.returncode,
                "stdout": completed.stdout, "stderr": completed.stderr, "files": files,
            })
        processes = subprocess.run(
            ["ps", "-axo", "pid=,ppid=,pgid=,command="],
            capture_output=True, text=True, timeout=3, check=False,
        )
        owned = [
            line for line in processes.stdout.splitlines()
            if str(self.base) in line and "ps -axo" not in line
        ]
        return json.dumps({"test": self.id(), "runs": runs, "owned_processes": owned}, indent=2)

    def status(self, name: str) -> dict:
        return json.loads((self.base / name / "status.json").read_text(encoding="utf-8"))

    def child_pid(self, name: str) -> int | None:
        events = self.base / name / "events.jsonl"
        if not events.exists():
            return None
        for line in events.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event") == "child-start":
                return event["pid"]
        return None

    def wait_for_capturing(self, name: str, process: subprocess.Popen[str]) -> int:
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            status_path = self.base / name / "status.json"
            child_pid = self.child_pid(name)
            if child_pid is not None and status_path.exists():
                try:
                    current = self.status(name)
                except (OSError, json.JSONDecodeError):
                    current = {}
                if current.get("state") == "capturing" and current.get("pid") == child_pid:
                    return child_pid
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                self.fail(
                    f"recorder exited before capturing: {process.returncode}; "
                    f"{stdout!r}; {stderr!r}"
                )
            time.sleep(0.02)
        self.fail(f"recorder never reported capturing; child_pid={self.child_pid(name)}")

    def stop_fixture(self, process: subprocess.Popen[str], child_pid: int | None) -> None:
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=5)
        if child_pid is not None:
            try:
                os.killpg(child_pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

    def test_r1_r2_default_failure_never_starts_second_from_start(self) -> None:
        result = self.invoke("fail", "default", "--from-start")
        self.assertNotEqual(result.returncode, 0)
        run = self.base / "default"
        video = run / "segment-000/video.part"
        expected = hashlib.sha256(b"video").hexdigest()
        self.assertEqual(expected, digest(video))
        self.assertFalse((run / "segment-001").exists())
        events = (run / "events.jsonl").read_text(encoding="utf-8")
        self.assertEqual(events.count('child-start'), 1)
        self.assertEqual(self.status("default")["state"], "partial")

    def test_r3_r4_failure_stops_partial_without_lossy_fallback(self) -> None:
        result = self.invoke("fail", "safe-stop", "--from-start")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.base / "safe-stop/segment-001").exists())
        self.assertEqual(self.status("safe-stop")["state"], "partial")

    def test_r5_maps_yt_dlp_format_intermediates_to_tracks(self) -> None:
        segment = self.base / "formats"
        segment.mkdir()
        (segment / "capture.f14.mp4.part").write_bytes(b"video")
        (segment / "capture.f140.m4a.part").write_bytes(b"audio")
        self.assertEqual(recorder.media_sizes(segment, "14", "140"), {"video": 5, "audio": 5})

    def test_r5_per_track_stall_detects_frozen_audio(self) -> None:
        result = self.invoke(
            "video-only", "stall", "--video-format", "137", "--audio-format", "140"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status("stall")["reason"], "per-track stall")

    def test_r5_both_selected_tracks_growing_avoid_stall(self) -> None:
        result = self.invoke(
            "both-growing", "both", "--video-format", "137", "--audio-format", "140"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(self.status("both")["reason"], "per-track stall")

    def test_combined_output_without_track_provenance_stops_safely(self) -> None:
        result = self.invoke(
            "combined-growing", "combined", "--video-format", "137", "--audio-format", "140",
            "--stall-seconds", "0.3", "--capture-seconds", "2",
        )
        self.assertEqual(result.returncode, 1, self.diagnostics())
        self.assertEqual(
            self.status("combined")["reason"],
            "per-track progress unavailable: combined output", self.diagnostics(),
        )
        self.assertTrue((self.base / "combined/segment-000/capture.mp4.part").exists())

    def test_merge_progress_does_not_false_stall_after_both_tracks(self) -> None:
        result = self.invoke(
            "merge-after-tracks", "merging", "--video-format", "137", "--audio-format", "140",
            "--stall-seconds", "0.3", "--capture-seconds", "3",
        )
        self.assertEqual(result.returncode, 1, self.diagnostics())
        self.assertNotIn(
            self.status("merging")["reason"],
            {"per-track stall", "merge stall", "per-track progress unavailable: combined output"},
            self.diagnostics(),
        )

    def test_merge_with_retained_intermediates_avoids_false_stall(self) -> None:
        result = self.invoke(
            "merge-with-intermediates", "merge-retained", "--video-format", "137",
            "--audio-format", "140", "--stall-seconds", "0.4", "--capture-seconds", "3",
        )
        self.assertEqual(result.returncode, 1, self.diagnostics())
        self.assertNotEqual(
            self.status("merge-retained")["reason"], "per-track stall", self.diagnostics()
        )
        self.assertTrue(
            (self.base / "merge-retained/segment-000/capture.f137.mp4.part").exists()
        )

    def test_frozen_merge_with_retained_intermediates_stops_owned_child(self) -> None:
        result = self.invoke(
            "merge-frozen", "merge-frozen", "--video-format", "137",
            "--audio-format", "140", "--stall-seconds", "0.4", "--capture-seconds", "3",
        )
        child_pid = self.child_pid("merge-frozen")
        try:
            self.assertEqual(result.returncode, 1, self.diagnostics())
            self.assertEqual(
                self.status("merge-frozen")["reason"], "merge stall", self.diagnostics()
            )
            self.assertIsNotNone(child_pid, self.diagnostics())
            with self.assertRaises(ProcessLookupError):
                os.kill(child_pid, 0)
        finally:
            if child_pid is not None:
                try:
                    os.killpg(child_pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def test_one_frozen_track_stalls_despite_other_files(self) -> None:
        for mode in ("audio-frozen-static-meta", "audio-frozen-combined-growing"):
            with self.subTest(mode=mode):
                result = self.invoke(
                    mode, mode, "--video-format", "137", "--audio-format", "140",
                    "--stall-seconds", "0.4", "--capture-seconds", "3",
                )
                child_pid = self.child_pid(mode)
                try:
                    self.assertEqual(result.returncode, 1, self.diagnostics())
                    self.assertEqual(
                        self.status(mode)["reason"], "per-track stall", self.diagnostics()
                    )
                    self.assertIsNotNone(child_pid)
                    with self.assertRaises(ProcessLookupError):
                        os.kill(child_pid, 0)
                finally:
                    if child_pid is not None:
                        try:
                            os.killpg(child_pid, signal.SIGTERM)
                        except ProcessLookupError:
                            pass

    def test_r6_churn_never_leaves_capturing_status(self) -> None:
        result = self.invoke("churn", "churn", "--stall-seconds", "2")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.status("churn")["state"], "partial")

    def test_r6_signal_stops_owned_child(self) -> None:
        process = subprocess.Popen(
            self.command("sleep", "signal"), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=self.environment("sleep"),
        )
        child_pid = None
        try:
            child_pid = self.wait_for_capturing("signal", process)
            process.send_signal(signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=5)
            self.assertNotEqual(process.returncode, 0, (stdout, stderr))
            self.assertEqual(self.status("signal")["reason"], "cancelled", (stdout, stderr))
            with self.assertRaises(ProcessLookupError):
                os.kill(child_pid, 0)
            self.assertFalse((self.base / "signal/segment-001").exists())
        finally:
            self.stop_fixture(process, child_pid or self.child_pid("signal"))

    def test_r6_deadline_stops_owned_child(self) -> None:
        result = self.invoke(
            "sleep", "deadline", "--capture-seconds", "0.2", "--stall-seconds", "2"
        )
        child_pid = self.child_pid("deadline")
        try:
            self.assertNotEqual(result.returncode, 0, (result.stdout, result.stderr))
            self.assertEqual(
                self.status("deadline")["reason"], "capture deadline",
                (result.stdout, result.stderr),
            )
            self.assertIsNotNone(child_pid)
            with self.assertRaises(ProcessLookupError):
                os.kill(child_pid, 0)
        finally:
            if child_pid is not None:
                try:
                    os.killpg(child_pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def test_child_exit_stops_owned_group_descendant(self) -> None:
        result = self.invoke(
            "child-exits-grandchild", "descendant", "--stall-seconds", "2",
            "--capture-seconds", "3",
        )
        child_pid = self.child_pid("descendant")
        grandchild_file = self.base / "descendant/segment-000/grandchild.pid"
        try:
            self.assertTrue(grandchild_file.exists(), self.diagnostics())
            grandchild_pid = int(grandchild_file.read_text())
            self.assertEqual(result.returncode, 1, self.diagnostics())
            with self.assertRaises(ProcessLookupError):
                os.kill(grandchild_pid, 0)
        finally:
            if child_pid is not None:
                try:
                    os.killpg(child_pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def test_r7_byte_and_disk_reasons_are_enforced(self) -> None:
        byte = self.invoke("sleep", "byte-live", "--max-bytes", "1", "--stall-seconds", "2")
        self.assertNotEqual(byte.returncode, 0)
        self.assertEqual(self.status("byte-live")["reason"], "byte budget")
        reserve = self.invoke(
            "sleep", "reserve-live", "--min-free-bytes", str(10**30),
            "--stall-seconds", "2",
        )
        self.assertNotEqual(reserve.returncode, 0)
        self.assertEqual(self.status("reserve-live")["reason"], "disk reserve")

    def test_sigkill_leaves_stale_status_until_external_cleanup(self) -> None:
        process = subprocess.Popen(
            self.command("sleep", "sigkill"), text=True, start_new_session=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=self.environment("sleep"),
        )
        child_pid = None
        try:
            child_pid = self.wait_for_capturing("sigkill", process)
            process.kill()
            stdout, stderr = process.communicate(timeout=5)
            self.assertEqual(self.status("sigkill")["state"], "capturing", (stdout, stderr))
            os.kill(child_pid, 0)
        finally:
            self.stop_fixture(process, child_pid or self.child_pid("sigkill"))

    def test_r7_byte_and_disk_boundaries(self) -> None:
        byte = self.invoke("success", "byte", "--max-bytes", "1")
        self.assertNotEqual(byte.returncode, 0, self.diagnostics())
        self.assertEqual(self.status("byte")["reason"], "byte budget", self.diagnostics())
        self.assertFalse((self.base / "byte/segment-001").exists())
        reserve = self.invoke("success", "reserve", "--min-free-bytes", str(10**30))
        self.assertNotEqual(reserve.returncode, 0, self.diagnostics())
        self.assertEqual(self.status("reserve")["reason"], "disk reserve", self.diagnostics())
        self.assertFalse((self.base / "reserve/segment-001").exists())

    def test_r8_metadata_requires_current_positive_end_signal(self) -> None:
        self.assertEqual(recorder.classify_metadata({"is_live": True}), "live")
        self.assertEqual(recorder.classify_metadata({"live_status": "post_live"}), "ended")
        self.assertEqual(recorder.classify_metadata({"live_status": "was_live"}), "ended")
        self.assertEqual(recorder.classify_metadata({}), "unknown")
        self.assertEqual(recorder.classify_metadata(None), "unknown")
        metadata = self.base / "metadata.py"
        metadata.write_text(
            "#!/usr/bin/env python3\nprint('{\\\"live_status\\\": \\\"post_live\\\"}')\n",
            encoding="utf-8",
        )
        metadata.chmod(0o755)
        self.assertTrue(
            recorder.confirmed_end("https://www.youtube.com/watch?v=fixture", str(metadata), 1)
        )

    def test_r9_access_restriction_stops_without_fallback(self) -> None:
        result = self.invoke("access", "access")
        self.assertNotEqual(result.returncode, 0, self.diagnostics())
        self.assertEqual(self.status("access")["state"], "stopped", self.diagnostics())
        self.assertFalse((self.base / "access/segment-001").exists())

    def test_r9_access_denial_wins_after_stall_guard(self) -> None:
        result = self.invoke(
            "access-delayed", "access-delayed", "--stall-seconds", "0.5",
            "--capture-seconds", "2",
        )
        self.assertNotEqual(result.returncode, 0, self.diagnostics())
        self.assertEqual(
            self.status("access-delayed")["state"], "stopped", self.diagnostics()
        )
        self.assertEqual(
            self.status("access-delayed")["reason"], "access restriction",
            self.diagnostics(),
        )

    def test_r9_transient_403_retry_log_is_not_terminal_access_denial(self) -> None:
        result = self.invoke("transient-403", "transient")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(self.status("transient")["state"], "stopped")

    def test_complete_requires_mocked_end_and_playable_audiovisual_output(self) -> None:
        live = self.base / "live.py"
        live.write_text(
            "#!/usr/bin/env python3\n"
            "import pathlib, subprocess, sys, time\n"
            "if '--skip-download' in sys.argv:\n"
            "    print('{\\\"live_status\\\": \\\"post_live\\\"}')\n"
            "else:\n"
            "    output = pathlib.Path(sys.argv[sys.argv.index('-o') + 1]"
            ".replace('%(ext)s', 'mp4'))\n"
            "    video = output.parent / 'capture.fvideo.mp4.part'\n"
            "    audio = output.parent / 'capture.faudio.m4a.part'\n"
            "    video.write_bytes(b'video-progress')\n"
            "    audio.write_bytes(b'audio-progress')\n"
            "    time.sleep(.3)\n"
            "    video.unlink()\n"
            "    audio.unlink()\n"
            "    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', "
            "'-i', 'testsrc=size=32x32:rate=5', '-f', 'lavfi', '-i', "
            "'sine=frequency=1000', '-t', '0.4', '-c:v', 'mpeg4', "
            "'-c:a', 'aac', str(output)], check=True)\n",
            encoding="utf-8",
        )
        live.chmod(0o755)
        run = self.base / "complete"
        command = [
            sys.executable, str(SCRIPT), "https://www.youtube.com/watch?v=fixture", str(run),
            "--downloader", str(live), "--video-format", "video", "--audio-format", "audio",
            "--capture-seconds", "3", "--stall-seconds", "1", "--request-seconds", "3",
            "--max-bytes", "100000", "--min-free-bytes", "1",
        ]
        result = subprocess.run(command, text=True, capture_output=True, timeout=10)
        self.invocations.append((command, result))
        self.assertEqual(result.returncode, 0, self.diagnostics())
        self.assertEqual(self.status("complete")["state"], "complete")
        self.assertIn("sampled", self.status("complete")["reason"])
        coverage = self.status("complete")["coverage"]
        self.assertEqual(coverage["broadcast_complete"], "unknown")
        self.assertEqual(coverage["captured"], "unknown")
        self.assertGreater(coverage["duration_seconds"], 0)
        self.assertGreater(coverage["decoded_seconds"], 0)

    def test_r10_atomic_status_never_claims_complete(self) -> None:
        result = self.invoke("success", "status")
        state = self.status("status")["state"]
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertEqual(state, "partial", (result.stdout, result.stderr))
        self.assertFalse((self.base / "status/status.json.tmp").exists())

    def test_r11_no_deletion_api_exists(self) -> None:
        self.assertNotIn("unlink(", SCRIPT.read_text(encoding="utf-8"))
        self.assertNotIn("rmtree(", SCRIPT.read_text(encoding="utf-8"))

    def test_r12_fixture_decode_uses_temporary_files(self) -> None:
        media = self.base / "fixture.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=32x32:rate=5",
            "-f", "lavfi", "-i", "sine=frequency=1000", "-t", "0.4", "-c:v", "mpeg4",
            "-c:a", "aac", str(media),
        ], check=True, timeout=10)
        self.assertTrue(recorder.probe_and_decode(media, 5)[0])
        self.assertTrue(str(media).startswith(self.temp.name))

    def test_partial_tracks_probe_selected_audio_and_video(self) -> None:
        segment = self.base / "partial-tracks"
        segment.mkdir()
        video = segment / "capture.f137.mp4"
        audio = segment / "capture.f140.m4a"
        subprocess.run([
            "ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i",
            "testsrc=size=32x32:rate=5", "-t", "0.4", "-an", "-c:v", "mpeg4", str(video),
        ], check=True, capture_output=True, timeout=5)
        subprocess.run([
            "ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i",
            "sine=frequency=1000", "-t", "0.4", "-vn", "-c:a", "aac", str(audio),
        ], check=True, capture_output=True, timeout=5)
        args = recorder.parser().parse_args([
            "https://www.youtube.com/watch?v=fixture", str(self.base / "unused"),
            "--video-format", "137", "--audio-format", "140", "--request-seconds", "3",
        ])
        result = recorder.Recorder(args).inspect_partial(segment)
        self.assertCountEqual(
            result["playable_outputs"], [video.name, audio.name]
        )
        self.assertEqual(result["unverified_outputs"], [])
        for interval in result["sampled_intervals"].values():
            self.assertEqual(interval["start_seconds"], 0)
            self.assertEqual(interval["requested_end_seconds"], 1)
            self.assertGreater(interval["measured_end_seconds"], 0)

    def test_partial_probe_has_one_wall_deadline(self) -> None:
        segment = self.base / "partial-timeout"
        segment.mkdir()
        for number in range(5):
            (segment / f"capture.f137.{number}.part").write_bytes(b"partial")
        fake_bin = self.base / "bin"
        fake_bin.mkdir()
        ffprobe = fake_bin / "ffprobe"
        ffprobe.write_text(
            "#!/usr/bin/env python3\nimport time\ntime.sleep(2)\n"
        )
        ffprobe.chmod(0o755)
        args = recorder.parser().parse_args([
            "https://www.youtube.com/watch?v=fixture", str(self.base / "unused"),
            "--video-format", "137", "--audio-format", "140", "--request-seconds", "0.2",
        ])
        with mock.patch.dict(
            os.environ, PATH=f"{fake_bin}{os.pathsep}{os.environ['PATH']}"
        ):
            started = time.monotonic()
            result = recorder.Recorder(args).inspect_partial(segment)
            elapsed = time.monotonic() - started
        self.assertLess(elapsed, 1)
        self.assertEqual(len(result["unverified_outputs"]), 5)

    def test_unsupported_host_is_rejected_before_acquisition(self) -> None:
        command = self.command("success", "host")
        command[2] = "https://example.invalid/live"
        result = subprocess.run(command, text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.base / "host").exists())

    def test_nonfinite_capture_request_and_stall_limits_are_rejected(self) -> None:
        for option in ("--capture-seconds", "--request-seconds", "--stall-seconds"):
            for value in ("nan", "inf", "-inf"):
                with self.subTest(option=option, value=value):
                    name = f"invalid-{option[2:]}-{value}"
                    arguments = (
                        (f"{option}={value}",) if value.startswith("-") else (option, value)
                    )
                    result = self.invoke("success", name, *arguments)
                    self.assertEqual(result.returncode, 2, self.diagnostics())
                    self.assertIn("finite and positive", result.stderr)
                    self.assertFalse((self.base / name).exists())

    def test_existing_run_directory_is_rejected(self) -> None:
        run = self.base / "existing"
        run.mkdir()
        result = self.invoke("success", "existing")
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
