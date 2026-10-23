"""Test package coordination with isolated executables, never real package managers."""

import json
import os
import selectors
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "sync-packages.py"
FAKE = r'''
import json, os, sys, time
from pathlib import Path
root = Path(os.environ["FIXTURE"])
name = Path(sys.argv[0]).name
args = sys.argv[1:]
with (root / "events").open("a") as stream:
  stream.write(json.dumps([name, args, os.environ.get("HOMEBREW_BUNDLE_BREW_SKIP")]) + "\n")
if name == "brew":
  if args[0] == "list":
    if os.environ.get("PROBE_FAIL"): sys.exit(7)
    if not os.environ.get("MISSING"): print("mise 1.0")
  elif args[0] == "--prefix": print(root)
  elif os.environ.get("UPGRADE_FAIL"): sys.exit(8)
elif name == "just" and args[0] in ("brew-apply", "mise-sync"):
  lane = args[0]
  (root / lane).touch()
  print(f"{lane}: standard output", flush=True)
  print(f"{lane}: diagnostic", file=sys.stderr, flush=True)
  print(f"{lane}: progress\r{lane}: complete", flush=True)
  if os.environ.get("BLOCK"):
    (root / (lane + ".pid")).write_text(str(os.getpid()))
    time.sleep(30)
  if not os.environ.get("MISSING") and os.environ.get("DOTS_SEQUENTIAL") != "1":
    peer = "mise-sync" if lane == "brew-apply" else "brew-apply"
    deadline = time.monotonic() + 3
    while not (root / peer).exists():
      if time.monotonic() > deadline: sys.exit(9)
      time.sleep(0.01)
  if os.environ.get("FAIL") == lane: sys.exit(10)
  (root / (lane + ".done")).touch()
elif name == "just" and args[0] == "brew-clean":
  assert (root / "brew-apply.done").exists()
  assert (root / "mise-sync.done").exists()
'''


class PackageSyncTest(unittest.TestCase):
  def setUp(self):
    self.scratch = tempfile.TemporaryDirectory(prefix="package-sync-")
    self.addCleanup(self.scratch.cleanup)
    self.root = Path(self.scratch.name)
    self.bin = self.root / "bin"
    self.bin.mkdir()
    for name in ("brew", "mise", "just"):
      executable = self.bin / name
      executable.write_text(f"#!{sys.executable}\n" + FAKE)
      executable.chmod(0o755)
    self.env = dict(os.environ, PATH=str(self.bin), FIXTURE=str(self.root))
    for key in ("DOTS_SEQUENTIAL", "HOMEBREW_BUNDLE_BREW_SKIP"):
      self.env.pop(key, None)

  def run_sync(self, **env):
    return subprocess.run(
      [sys.executable, str(SCRIPT)], env=dict(self.env, **env),
      capture_output=True, text=True, timeout=10
    )

  def events(self):
    return [json.loads(line) for line in (self.root / "events").read_text().splitlines()]

  def test_parallel_repeat_and_scoped_exclusion(self):
    for _ in range(2):
      for marker in self.root.glob("*.done"):
        marker.unlink()
      for lane in ("brew-apply", "mise-sync"):
        (self.root / lane).unlink(missing_ok=True)
      result = self.run_sync(HOMEBREW_BUNDLE_BREW_SKIP="other")
      self.assertEqual(result.returncode, 0, result.stderr)
      events = self.events()
      apply = [event for event in events if event[1] == ["brew-apply"]][-1]
      self.assertEqual(apply[2], "other mise")
      self.assertEqual(events[-1], ["just", ["brew-clean"], "other"])
      self.assertLess(
        next(i for i, event in enumerate(events) if event[1] == ["upgrade", "mise"]),
        next(i for i, event in enumerate(events) if event[1] == ["brew-apply"])
      )

  def test_labels_both_output_streams_and_progress_lines(self):
    result = self.run_sync()
    self.assertEqual(result.returncode, 0, result.stderr)
    for label, lane in (("brew", "brew-apply"), ("mise", "mise-sync")):
      for message in ("standard output", "diagnostic", "progress", "complete"):
        self.assertIn(f"[{label}] {lane}: {message}\n", result.stdout)
    self.assertNotIn("diagnostic", result.stderr)

  def test_output_is_visible_while_both_jobs_are_still_running(self):
    process = subprocess.Popen(
      [sys.executable, str(SCRIPT)], env=dict(self.env, BLOCK="1"),
      stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    captured = b""
    try:
      deadline = time.monotonic() + 5
      while not all(
        message in captured for message in
        (b"[brew] brew-apply: diagnostic", b"[mise] mise-sync: diagnostic")
      ):
        self.assertLess(time.monotonic(), deadline, captured.decode())
        for key, _ in selector.select(timeout=0.1):
          chunk = os.read(key.fileobj.fileno(), 4096)
          self.assertTrue(chunk, captured.decode())
          captured += chunk
      self.assertIsNone(process.poll())
    finally:
      if process.poll() is None:
        process.terminate()
      process.wait(timeout=7)
      selector.close()
      process.stdout.close()

  def test_bootstrap_and_explicit_sequential(self):
    for env in ({"MISSING": "1"}, {"DOTS_SEQUENTIAL": "1"}):
      with self.subTest(env=env):
        result = self.run_sync(**env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
          [event[1] for event in self.events() if event[0] == "just"][-2:],
          [["brew"], ["mise-sync"]]
        )

  def test_either_failure_waits_and_prevents_cleanup_then_retry_succeeds(self):
    for lane in ("brew-apply", "mise-sync"):
      with self.subTest(lane=lane):
        (self.root / "events").unlink(missing_ok=True)
        result = self.run_sync(FAIL=lane)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(["brew-clean"], [event[1] for event in self.events()])
        peer = "mise-sync" if lane == "brew-apply" else "brew-apply"
        self.assertTrue((self.root / (peer + ".done")).exists())
        self.assertEqual(self.run_sync().returncode, 0)

  def test_preflight_failures_stop_before_parallel_work(self):
    for env in ({"PROBE_FAIL": "1"}, {"UPGRADE_FAIL": "1"}):
      (self.root / "events").unlink(missing_ok=True)
      self.assertNotEqual(self.run_sync(**env).returncode, 0)
      self.assertFalse(any(event[0] == "just" for event in self.events()))

  def test_interrupt_stops_both_children(self):
    process = subprocess.Popen(
      [sys.executable, str(SCRIPT)], env=dict(self.env, BLOCK="1"),
      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
      deadline = time.monotonic() + 5
      while len(list(self.root.glob("*.pid"))) < 2:
        self.assertLess(time.monotonic(), deadline)
        time.sleep(0.01)
      process.send_signal(signal.SIGTERM)
      self.assertEqual(process.wait(timeout=7), 143)
      for pid_file in self.root.glob("*.pid"):
        with self.assertRaises(ProcessLookupError):
          os.kill(int(pid_file.read_text()), 0)
    finally:
      if process.poll() is None:
        process.terminate()
        process.wait(timeout=7)


if __name__ == "__main__":
  unittest.main()
