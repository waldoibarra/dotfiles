"""Exercise bootstrap boundaries without installing packages or changing the host."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
BASH = "/bin/bash"
FAKE = r'''
import json, os, shutil, sys
from pathlib import Path
root = Path(os.environ["FIXTURE"])
name = Path(sys.argv[0]).name
args = sys.argv[1:]
with (root / "events").open("a") as stream:
  stream.write(json.dumps([name, args]) + "\n")
if name == "brew":
  if args[:2] == ["bundle", "check"]:
    assert "--no-upgrade" in args
    sys.exit(0 if (root / "packages").exists() else 1)
  if args[:2] == ["bundle", "install"]:
    assert "--no-upgrade" in args
    if os.environ.get("FAIL_INSTALL"): sys.exit(17)
    if not (root / "packages").exists(): (root / "packages").write_text("installed")
    shutil.copy2(root / "mise-stub", root / "brew-bin/mise")
elif name == "mise":
  if args[0] == "install":
    if os.environ.get("FAIL_MISE"): sys.exit(18)
    if not (root / "tools").exists(): (root / "tools").write_text("installed")
  elif args[0] == "activate": print(":")
elif name == "python3":
  sys.exit(int(os.environ.get("PYTHON_EXIT", "0")))
elif name == "uname": print(os.environ.get("TEST_OS", "Darwin"))
'''


class BootstrapTest(unittest.TestCase):
  def setUp(self):
    self.scratch = tempfile.TemporaryDirectory(prefix="package-bootstrap-")
    self.addCleanup(self.scratch.cleanup)
    self.root = Path(self.scratch.name)
    self.bin = self.root / "bin"
    self.bin.mkdir()
    (self.root / "brew-bin").mkdir()
    self.env = dict(os.environ, HOME=str(self.root), PATH=str(self.bin), FIXTURE=str(self.root))
    self.env.pop("DOTS_DEFER_MISE_INSTALL", None)
    for name in ("brew-stub", "mise-stub", "git", "python3", "uname"):
      target = self.root / name if name.endswith("-stub") else self.bin / name
      target.write_text(f"#!{sys.executable}\n" + FAKE)
      target.chmod(0o755)
    # Preserve executable names when copied into the simulated Homebrew prefix.
    for name in ("dirname", "cp"):
      (self.bin / name).symlink_to(shutil.which(name))
    self.driver = self.root / "bootstrap.sh"
    self.driver.write_text(
      f'source "{ROOT / "scripts/install-os-packages.sh"}"\n'
      # Replace only host detection and the external Homebrew installation boundary.
      'is_brew_installed() { command -v brew >/dev/null 2>&1; }\n'
      'install_brew_deps() { echo prerequisites >> "$FIXTURE/bootstrap-events"; }\n'
      'run_brew_install_script() {\n'
      '  echo install-brew >> "$FIXTURE/bootstrap-events"\n'
      '  cp "$FIXTURE/brew-stub" "$FIXTURE/brew-bin/brew"\n'
      '}\n'
      'add_brew_to_path() { export PATH="$FIXTURE/brew-bin:$PATH"; }\n'
      'install_wezterm_terminfo() { :; }\n'
      'main\n'
    )

  def run_bootstrap(self, **env):
    return subprocess.run(
      [BASH, str(self.driver)], env=dict(self.env, **env),
      capture_output=True, text=True, timeout=5
    )

  def events(self):
    return [json.loads(line) for line in (self.root / "events").read_text().splitlines()]

  def test_fresh_install_without_brew_mise_or_just_and_repeat(self):
    self.assertFalse((self.bin / "just").exists())
    first = self.run_bootstrap()
    self.assertEqual(first.returncode, 0, first.stderr)
    self.assertEqual((self.root / "bootstrap-events").read_text(), "prerequisites\ninstall-brew\n")
    events = self.events()
    self.assertLess(
      next(i for i, event in enumerate(events) if event[0] == "brew"),
      next(i for i, event in enumerate(events) if event[0] == "mise")
    )
    snapshots = {name: (self.root / name).stat().st_mtime_ns for name in ("packages", "tools")}
    # A subsequent login has Homebrew on PATH; no bootstrap or package reinstall is needed.
    self.env["PATH"] = str(self.root / "brew-bin") + os.pathsep + str(self.bin)
    second = self.run_bootstrap()
    self.assertEqual(second.returncode, 0, second.stderr)
    for name, timestamp in snapshots.items():
      self.assertEqual((self.root / name).stat().st_mtime_ns, timestamp)
    installs = [args for name, args in self.events() if name == "brew" and args[1] == "install"]
    self.assertEqual(len(installs), 1)
    self.assertEqual((self.root / "bootstrap-events").read_text(), "prerequisites\ninstall-brew\n")

  def test_sync_defers_mise_tools_but_still_bootstraps_brew_packages(self):
    result = self.run_bootstrap(DOTS_DEFER_MISE_INSTALL="1")
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertTrue((self.root / "packages").exists())
    self.assertFalse((self.root / "tools").exists())
    self.assertEqual(
      [args for name, args in self.events() if name == "mise"],
      [["trust", "--yes", "--quiet"]]
    )

  def test_brew_failure_stops_before_mise_and_retry_succeeds(self):
    failed = self.run_bootstrap(FAIL_INSTALL="1")
    self.assertEqual(failed.returncode, 17, failed.stderr)
    self.assertFalse(any(name == "mise" for name, _ in self.events()))
    self.assertEqual(self.run_bootstrap().returncode, 0)

  def test_mise_failure_propagates(self):
    failed = self.run_bootstrap(FAIL_MISE="1")
    self.assertEqual(failed.returncode, 18, failed.stderr)

  def wrapper(self, **env):
    checkout = self.root / "checkout"
    (checkout / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "scripts/install-dotfiles.sh", checkout / "scripts/install-dotfiles.sh")
    dotbot = checkout / "dotbot/bin/dotbot"
    dotbot.parent.mkdir(parents=True, exist_ok=True)
    dotbot.write_text('#!/bin/bash\nprintf "%s" "$PATH" > "$FIXTURE/dotbot-path"\n')
    dotbot.chmod(0o755)
    return subprocess.run(
      [BASH, str(checkout / "scripts/install-dotfiles.sh")],
      env=dict(self.env, **env), capture_output=True, text=True, timeout=5
    )

  def test_dotbot_inherits_brew_path_on_supported_platforms(self):
    for system, prefix in (("Darwin", "/opt/homebrew"), ("Linux", "/home/linuxbrew/.linuxbrew")):
      result = self.wrapper(TEST_OS=system)
      self.assertEqual(result.returncode, 0, result.stderr)
      entries = (self.root / "dotbot-path").read_text().split(os.pathsep)
      self.assertIn(prefix + "/bin", entries)
      self.assertIn(prefix + "/sbin", entries)

  def test_missing_git_stops_before_dotbot(self):
    (self.bin / "git").unlink()
    result = self.wrapper()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("Git", result.stderr)
    self.assertFalse((self.root / "dotbot-path").exists())

  def test_missing_python_stops_before_dotbot(self):
    (self.bin / "python3").unlink()
    result = self.wrapper()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("Python", result.stderr)
    self.assertFalse((self.root / "dotbot-path").exists())

  def test_old_python_stops_before_dotbot(self):
    result = self.wrapper(PYTHON_EXIT="1")
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("Python", result.stderr)
    self.assertFalse((self.root / "dotbot-path").exists())


if __name__ == "__main__":
  unittest.main()
