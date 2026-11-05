#!/usr/bin/env python3
"""Exercise Cursor hook reconciliation without changing workstation configuration."""

from pathlib import Path
import subprocess
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = ROOT / "scripts/update-coding-agents/entrypoint.sh"


class CursorHerdrTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        for name in ("dirname", "grep", "mkdir"):
            (self.bin / name).symlink_to(shutil.which(name))
        self.env = {
            "HOME": str(self.home), "PATH": str(self.bin),
            "CURSOR_CONFIG_DIR": str(self.home / "cursor config"),
        }
        self.config = Path(self.env["CURSOR_CONFIG_DIR"])
        self.executable("cursor-agent", "#!/bin/sh\nexit 0\n")
        self.executable("herdr", '''#!/bin/sh
if [ "$*" = "integration status" ]; then
  if [ -f "$HOME/current" ]; then
    echo 'cursor: current (v1)'
  else
    echo 'cursor: outdated (v0 < v1)'
  fi
elif [ "$*" = "integration install cursor" ]; then
  test -d "$CURSOR_CONFIG_DIR" || exit 9
  echo install >> "$HOME/installs"
  printf hook > "$CURSOR_CONFIG_DIR/herdr-agent-state.sh"
  test ! -f "$HOME/fail" || exit 7
  printf current > "$HOME/current"
else
  exit 8
fi
''')

    def executable(self, name, script):
        target = self.bin / name
        target.write_text(script)
        target.chmod(0o755)

    def reconcile(self):
        return subprocess.run(
            ["/bin/bash"], input=f'source "{ENTRYPOINT}"\ninstall_herdr_integration cursor\n',
            text=True, capture_output=True, env=self.env, timeout=10,
        )

    def test_missing_cursor_skips_without_writes(self):
        (self.bin / "cursor-agent").unlink()
        result = self.reconcile()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("cursor-agent not found", result.stdout)
        self.assertFalse(self.config.exists())
        self.assertFalse((self.home / "installs").exists())

    def test_missing_herdr_skips_without_writes(self):
        (self.bin / "herdr").unlink()
        result = self.reconcile()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Herdr not found", result.stdout)
        self.assertFalse(self.config.exists())

    def test_install_and_repeat_preserve_files(self):
        self.config.mkdir()
        settings = self.config / "hooks.json"
        settings.write_text('{"version":1,"hooks":{"stop":[]}}\n')
        settings.chmod(0o600)
        before = (settings.read_bytes(), settings.stat())
        first = self.reconcile()
        self.assertEqual(first.returncode, 0, first.stderr)
        hook = self.config / "herdr-agent-state.sh"
        installed = (hook.read_bytes(), hook.stat())
        second = self.reconcile()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("already up to date", second.stdout)
        self.assertEqual((self.home / "installs").read_text(), "install\n")
        for target, snapshot in ((settings, before), (hook, installed)):
            self.assertEqual(target.read_bytes(), snapshot[0])
            self.assertEqual(target.stat().st_mtime_ns, snapshot[1].st_mtime_ns)
            self.assertEqual(target.stat().st_mode, snapshot[1].st_mode)

    def test_failure_then_retry_creates_config_directory(self):
        failure = self.home / "fail"
        failure.touch()
        self.assertNotEqual(self.reconcile().returncode, 0)
        self.assertFalse((self.home / "current").exists())
        failure.unlink()
        result = self.reconcile()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / "installs").read_text(), "install\ninstall\n")

    def test_default_config_directory(self):
        self.env.pop("CURSOR_CONFIG_DIR")
        self.executable("herdr", '''#!/bin/sh
if [ "$*" = "integration status" ]; then
  echo 'cursor: not installed'
else
  test "$*" = 'integration install cursor' && test -d "$HOME/.cursor"
fi
''')
        result = self.reconcile()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / ".cursor").is_dir())


if __name__ == "__main__":
    unittest.main()
