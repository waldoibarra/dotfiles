"""Check Cursor rule rendering in disposable homes without launching Cursor."""

import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MARKER = b"@~/.agents/AGENTS.md"


class CursorRuleTest(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.script = self.root / "scripts/update-coding-agents/sync-cursor-rule.sh"
        self.script.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "scripts/update-coding-agents/sync-cursor-rule.sh", self.script)
        self.template = self.root / "home/.cursor/rules/global-instructions.mdc"
        self.template.parent.mkdir(parents=True)
        self.env = dict(os.environ, HOME=str(self.root))
        self.template.write_bytes(b"---\nalwaysApply: true\n---\n\n@~/.agents/AGENTS.md\n")
        self.instructions = self.root / ".agents/AGENTS.md"
        self.instructions.parent.mkdir()
        self.instructions.write_bytes(b"# Instructions\nKeep $HOME and @other literal.\n")
        self.target = self.root / ".cursor/rules/global-instructions.mdc"

    def sync(self):
        subprocess.run(
            ["bash", str(self.script)], env=self.env, check=True,
            capture_output=True, text=True, timeout=10,
        )

    def test_render_repeat_and_refresh(self):
        self.sync()
        expected = self.template.read_bytes().replace(
            MARKER, self.instructions.read_bytes()
        )
        self.assertEqual(self.target.read_bytes(), expected)
        self.assertFalse(self.target.is_symlink())
        self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o644)
        before = self.target.stat()
        self.sync()
        after = self.target.stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.instructions.write_bytes(b"Updated instructions\n")
        self.sync()
        self.assertIn(b"Updated instructions\n", self.target.read_bytes())

    def test_literal_bytes_and_trailing_newlines_are_preserved(self):
        for ending in (b"", b"\n", b"\n\n"):
            self.template.write_bytes(b"---\nalwaysApply: true\n---\n" + MARKER + ending)
            self.instructions.write_bytes(b"Literal & \\ $HOME @other" + ending)
            self.sync()
            self.assertEqual(
                self.target.read_bytes(),
                self.template.read_bytes().replace(MARKER, self.instructions.read_bytes()),
            )

    def test_symlink_migration_preserves_template_and_other_rules(self):
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.template)
        other = self.target.parent / "other.mdc"
        other.write_bytes(b"unrelated")
        original = self.template.read_bytes()
        self.sync()
        self.assertFalse(self.target.is_symlink())
        self.assertEqual(self.template.read_bytes(), original)
        self.assertEqual(other.read_bytes(), b"unrelated")

    def test_invalid_inputs_preserve_existing_rule(self):
        self.sync()
        original = self.target.read_bytes()
        for template in (b"no marker", MARKER * 2):
            self.template.write_bytes(template)
            with self.assertRaises(subprocess.CalledProcessError):
                self.sync()
            self.assertEqual(self.target.read_bytes(), original)
        self.template.write_bytes(MARKER)
        self.instructions.unlink()
        with self.assertRaises(subprocess.CalledProcessError):
            self.sync()
        self.assertEqual(self.target.read_bytes(), original)

    def test_failed_replace_cleans_staging_and_allows_retry(self):
        self.sync()
        original = self.target.read_bytes()
        entries = set(self.target.parent.iterdir())
        self.instructions.write_bytes(b"Updated\n")
        binary_dir = self.root / "bin"
        binary_dir.mkdir()
        fake_mv = binary_dir / "mv"
        fake_mv.write_text("#!/bin/sh\nexit 23\n")
        fake_mv.chmod(0o755)
        self.env["PATH"] = f"{binary_dir}:{os.environ['PATH']}"
        with self.assertRaises(subprocess.CalledProcessError):
            self.sync()
        fake_mv.unlink()
        self.assertEqual(self.target.read_bytes(), original)
        self.assertEqual(set(self.target.parent.iterdir()), entries)
        self.sync()
        self.assertIn(b"Updated\n", self.target.read_bytes())

    def test_permissions_repaired_without_content_replacement(self):
        self.sync()
        self.target.chmod(0o600)
        before = self.target.stat()
        self.sync()
        self.assertEqual(self.target.stat().st_ino, before.st_ino)
        self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o644)


if __name__ == "__main__":
    unittest.main()
