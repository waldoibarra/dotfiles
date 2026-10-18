"""Exercise profile links in disposable homes; never run workstation updates."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "update-coding-agents/sync-life-profile.sh"


class ProfileLinks(unittest.TestCase):
    def setUp(self):
        self.fixture = tempfile.TemporaryDirectory(prefix="life-profile-")
        self.addCleanup(self.fixture.cleanup)
        self.home = Path(self.fixture.name).resolve()
        self.links = self.home / ".agents"

    def run_sync(self, profile=None):
        env = dict(os.environ, HOME=str(self.home))
        env.pop("LIFE_PROFILE", None)
        if profile is not None:
            env["LIFE_PROFILE"] = profile
        return subprocess.run(
            ["bash", str(SCRIPT)], env=env, capture_output=True, text=True, timeout=10
        )

    def add_profile(self, profile):
        root = self.home / "life/people" / profile
        root.mkdir(parents=True)
        (root / "README.md").write_text("Profile\n")
        (root / "agent-identity.md").write_text("Identity\n")
        return root

    def test_no_vault_and_missing_selection(self):
        self.assertEqual(self.run_sync().stderr, "")
        self.add_profile("waldo")
        for profile in (None, ""):
            result = self.run_sync(profile)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Warning:", result.stderr)
            self.assertFalse(self.links.exists())

    def test_idempotence_switch_and_missing_selection_preserves_links(self):
        waldo = self.add_profile("waldo")
        lluvia = self.add_profile("lluvia")
        self.assertEqual(self.run_sync("waldo").returncode, 0)
        link = self.links / "personal-context.md"
        inode = link.lstat().st_ino
        self.assertEqual(link.resolve(), waldo / "README.md")
        self.assertEqual(self.run_sync("waldo").returncode, 0)
        self.assertEqual(inode, link.lstat().st_ino)
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(link.resolve(), waldo / "README.md")
        self.assertEqual(self.run_sync("lluvia").returncode, 0)
        self.assertEqual(link.resolve(), lluvia / "README.md")
        self.assertEqual((self.links / "agent-identity.md").resolve(), lluvia / "agent-identity.md")

    def test_invalid_and_missing_source_leave_links_unchanged(self):
        root = self.add_profile("waldo")
        self.assertEqual(self.run_sync("waldo").returncode, 0)
        for profile in ("../waldo", "Waldo", "two words", "missing"):
            self.assertNotEqual(self.run_sync(profile).returncode, 0)
        (root / "agent-identity.md").unlink()
        self.assertNotEqual(self.run_sync("waldo").returncode, 0)
        self.assertEqual(os.readlink(self.links / "personal-context.md"), str(root / "README.md"))

    def test_regular_file_preflight_preserves_both_destinations(self):
        self.add_profile("waldo")
        self.links.mkdir()
        context = self.links / "personal-context.md"
        context.symlink_to("old-target")
        identity = self.links / "agent-identity.md"
        identity.write_text("Do not overwrite\n")
        self.assertNotEqual(self.run_sync("waldo").returncode, 0)
        self.assertEqual(os.readlink(context), "old-target")
        self.assertEqual(identity.read_text(), "Do not overwrite\n")

    def test_directory_and_dangling_symlink(self):
        self.add_profile("waldo")
        self.links.mkdir()
        context = self.links / "personal-context.md"
        context.mkdir()
        self.assertNotEqual(self.run_sync("waldo").returncode, 0)
        context.rmdir()
        context.symlink_to("missing")
        self.assertEqual(self.run_sync("waldo").returncode, 0)
        self.assertTrue(context.is_file())


if __name__ == "__main__":
    unittest.main()
