"""Exercise Pi settings delivery with isolated sources and homes."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/update-coding-agents/sync-pi-settings.py"
SPEC = importlib.util.spec_from_file_location("pi_settings", SCRIPT)
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


class PiSettingsTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.source = self.root / "source.json"
        self.target = self.root / "home/.pi/agent/settings.json"
        self.defaults = {
            "defaultModel": "managed", "terminal": {"images": "kitty"},
            "packages": ["npm:example"],
        }
        self.source.write_text(json.dumps(self.defaults))

    def seed_local(self, settings):
        self.target.parent.mkdir(parents=True, exist_ok=True)
        self.target.write_text(json.dumps(settings))

    def sync(self):
        return SYNC.sync_settings(self.source, self.target)

    def test_fresh_install_and_repeat_preserve_bytes_mode_mtime(self):
        self.assertTrue(self.sync())
        self.assertFalse(self.target.is_symlink())
        self.assertEqual(json.loads(self.target.read_text()), self.defaults)
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o600)
        before = (self.target.read_bytes(), self.target.stat())
        self.assertFalse(self.sync())
        self.assertEqual(self.target.read_bytes(), before[0])
        self.assertEqual(self.target.stat().st_mtime_ns, before[1].st_mtime_ns)
        self.assertEqual(self.target.stat().st_mode, before[1].st_mode)

    def test_migration_preserves_marker_and_does_not_write_source(self):
        self.defaults["lastChangelogVersion"] = "1.5.0"
        self.source.write_text(json.dumps(self.defaults))
        original = self.source.read_bytes()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.source)
        self.assertTrue(self.sync())
        self.assertEqual(self.source.read_bytes(), original)
        self.assertFalse(self.target.is_symlink())
        del self.defaults["lastChangelogVersion"]
        self.source.write_text(json.dumps(self.defaults))
        self.assertFalse(self.sync())
        self.assertEqual(json.loads(self.target.read_text())["lastChangelogVersion"], "1.5.0")
        local = json.loads(self.target.read_text())
        local["lastChangelogVersion"] = "1.6.0"
        self.target.write_text(json.dumps(local))
        self.assertEqual(json.loads(self.source.read_text()), self.defaults)
        self.assertFalse(self.sync())

    def test_managed_values_replace_nested_objects_and_arrays(self):
        self.seed_local({
            "terminal": {"images": False, "showImages": False},
            "packages": ["npm:removed"], "defaultModel": "local",
            "lastChangelogVersion": "1.5.0", "theme": "dark",
        })
        self.target.chmod(0o640)
        self.assertTrue(self.sync())
        expected = {**self.defaults, "lastChangelogVersion": "1.5.0", "theme": "dark"}
        self.assertEqual(json.loads(self.target.read_text()), expected)
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o640)

    def test_invalid_inputs_fail_without_replacing_files(self):
        for which in ("source", "target"):
            for invalid in ("{", "[]", "null"):
                with self.subTest(which=which, invalid=invalid):
                    self.source.write_text(json.dumps(self.defaults))
                    self.seed_local({"theme": "dark"})
                    getattr(self, which).write_text(invalid)
                    before = (self.source.read_bytes(), self.target.read_bytes())
                    with self.assertRaises(ValueError):
                        self.sync()
                    self.assertEqual((self.source.read_bytes(), self.target.read_bytes()), before)
                    self.assertFalse(self.target.with_suffix(".json.lock").exists())

    def test_locked_settings_fail_then_retry(self):
        self.seed_local({"lastChangelogVersion": "1.5.0"})
        before = self.target.read_bytes()
        lock = self.target.with_suffix(".json.lock")
        lock.mkdir()
        with self.assertRaisesRegex(ValueError, "locked"):
            self.sync()
        self.assertEqual(self.target.read_bytes(), before)
        self.assertTrue(lock.exists())
        lock.rmdir()
        self.assertTrue(self.sync())

    def test_unrelated_and_dangling_links_fail_unchanged(self):
        self.target.parent.mkdir(parents=True)
        other = self.root / "other.json"
        for exists in (False, True):
            if exists:
                other.write_text("{}")
            self.target.symlink_to(other)
            with self.assertRaisesRegex(ValueError, "unrelated"):
                self.sync()
            self.assertTrue(self.target.is_symlink())
            self.target.unlink()

    def test_failed_replace_preserves_link_and_allows_retry(self):
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.source)
        before = self.source.read_bytes()
        with patch.object(SYNC.os, "replace", side_effect=OSError("fixture failure")):
            with self.assertRaises(OSError):
                self.sync()
        self.assertTrue(self.target.is_symlink())
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual(list(self.target.parent.glob(".settings-*")), [])
        self.assertFalse(self.target.with_suffix(".json.lock").exists())
        self.assertTrue(self.sync())

    def test_same_file_and_hard_links_are_rejected(self):
        with self.assertRaises(ValueError):
            SYNC.sync_settings(self.source, self.source)
        self.target.parent.mkdir(parents=True)
        os.link(self.source, self.target)
        with self.assertRaisesRegex(ValueError, "hard links"):
            self.sync()

    def test_cli_uses_normal_home_and_ignores_trial_profile(self):
        env = dict(
            os.environ, HOME=str(self.root / "home"),
            PI_CODING_AGENT_DIR=str(self.root / "unused-trial"),
        )
        result = subprocess.run([sys.executable, str(SCRIPT), "--source", str(self.source)],
                                env=env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.target.is_file())
        self.assertFalse((self.root / "unused-trial").exists())

    def test_dotbot_settings_step_runs_idempotently(self):
        sys.path.insert(0, str(ROOT / "dotbot/lib/pyyaml/lib"))
        import yaml

        config = yaml.safe_load((ROOT / "install.conf.yaml").read_text())
        steps = [
            step for block in config for step in block.get("shell", [])
            if "sync-pi-settings.py" in step.get("command", "")
        ]
        self.assertEqual(len(steps), 1)
        fixture = self.root / "install.yaml"
        fixture.write_text(yaml.safe_dump([{"shell": steps}]))
        env = dict(os.environ, HOME=str(self.root / "home"))
        command = [
            sys.executable, str(ROOT / "dotbot/bin/dotbot"),
            "-c", str(fixture), "-d", str(ROOT),
        ]
        for run in range(2):
            result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse(self.target.is_symlink())
            self.assertEqual(
                json.loads(self.target.read_text()),
                json.loads((ROOT / "home/.pi/agent/settings.json").read_text()),
            )
            if run == 0:
                first_mtime = self.target.stat().st_mtime_ns
            else:
                self.assertEqual(self.target.stat().st_mtime_ns, first_mtime)

    def test_delivery_is_wired_before_packages_and_not_linked(self):
        entrypoint = (ROOT / "scripts/update-coding-agents/entrypoint.sh").read_text()
        main = entrypoint.split("main() {", 1)[1]
        self.assertLess(main.index("sync-pi-settings.py"), main.index("install_pi_packages"))
        config = (ROOT / "install.conf.yaml").read_text()
        self.assertNotIn("~/.pi/agent/settings.json:", config)
        self.assertIn("command: python3 scripts/update-coding-agents/sync-pi-settings.py", config)


if __name__ == "__main__":
    unittest.main()
