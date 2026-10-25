"""Exercise raw-source exclusions without touching retained source material."""

import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class LintExclusionsTest(unittest.TestCase):
    def setUp(self):
        for executable in ("markdownlint-cli2", "editorconfig-checker", "yamlfmt", "hk"):
            self.assertIsNotNone(shutil.which(executable), f"Missing prerequisite: {executable}")
        self.scratch = tempfile.TemporaryDirectory(prefix="dotfiles-lint-exclusions-")
        self.addCleanup(self.scratch.cleanup)
        self.cwd = Path(self.scratch.name)
        (self.cwd / "raw/nested").mkdir(parents=True)
        (self.cwd / "docs").mkdir()

    def run_tool(self, *command, env=None):
        return subprocess.run(
            command, cwd=self.cwd, env=env, capture_output=True, text=True, timeout=30
        )

    def assert_excluded_but_control_checked(self, command, filename, invalid, env=None):
        source = self.cwd / "raw/nested" / filename
        source.write_bytes(invalid)
        before = (source.read_bytes(), source.stat().st_mtime_ns)
        for _ in range(2):
            result = self.run_tool(*command, env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((source.read_bytes(), source.stat().st_mtime_ns), before)
        (self.cwd / "docs" / filename).write_bytes(invalid)
        result = self.run_tool(*command, env=env)
        self.assertNotEqual(result.returncode, 0, "Invalid maintained content must fail")
        self.assertIn(filename, result.stdout + result.stderr)
        self.assertEqual((source.read_bytes(), source.stat().st_mtime_ns), before)

    def test_markdown_configs_preserve_raw(self):
        for source in (
            ROOT / ".markdownlint-cli2.yaml",
            ROOT / "home/.agents/skills/start-project/assets/markdownlint-cli2.yaml",
        ):
            with self.subTest(config=str(source)):
                (self.cwd / "docs/bad.md").unlink(missing_ok=True)
                shutil.copyfile(source, self.cwd / ".markdownlint-cli2.yaml")
                self.assert_excluded_but_control_checked(
                    ("markdownlint-cli2", "--fix", "**/*.md"), "bad.md",
                    b"# Bad!\n\nhttps://example.com/\n" + b"long sentence " * 20 + b"\n",
                )

    def test_editorconfig_exclusion_preserves_raw(self):
        shutil.copyfile(ROOT / ".editorconfig", self.cwd / ".editorconfig")
        shutil.copyfile(
            ROOT / ".editorconfig-checker.json", self.cwd / ".editorconfig-checker.json"
        )
        self.assert_excluded_but_control_checked(
            ("editorconfig-checker", "raw/nested/bad.txt", "docs"),
            "bad.txt", b"invalid trailing whitespace  ",
        )

    def test_yaml_recipe_preserves_raw(self):
        recipe = (ROOT / "justfile").read_text().split("lint-yaml:\n", 1)[1]
        command = shlex.split(recipe.splitlines()[0].strip())
        self.assert_excluded_but_control_checked(command, "bad.yaml", b"broken: [\n")

    def test_yaml_global_fallback_preserves_raw(self):
        config_home = self.cwd / "config"
        target = config_home / "yamlfmt/.yamlfmt"
        target.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "home/.config/yamlfmt/.yamlfmt", target)
        env = dict(os.environ, XDG_CONFIG_HOME=str(config_home))
        for arguments in (("-dstar", "**/*.yaml"), (".",)):
            with self.subTest(arguments=arguments):
                (self.cwd / "docs/bad.yaml").unlink(missing_ok=True)
                self.assert_excluded_but_control_checked(
                    ("yamlfmt", *arguments), "bad.yaml", b"broken: [\n", env=env,
                )

    def test_global_yaml_link_delivery_is_idempotent(self):
        home = self.cwd / "home"
        home.mkdir()
        env = dict(os.environ, HOME=str(home))
        command = [
            "python3", str(ROOT / "dotbot/bin/dotbot"),
            "-d", str(ROOT), "-c", str(ROOT / "install.conf.yaml"),
            "--only", "create", "link",
        ]
        target = home / ".config/yamlfmt/.yamlfmt"
        source = ROOT / "home/.config/yamlfmt/.yamlfmt"
        previous = None
        for _ in range(2):
            result = self.run_tool(*command, env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), source)
            self.assertEqual(target.read_bytes(), source.read_bytes())
            current = target.lstat().st_mtime_ns
            if previous is not None:
                self.assertEqual(current, previous)
            previous = current

    def test_hook_configs_exclude_raw_inputs(self):
        subprocess.run(["git", "init", "--quiet", str(self.cwd)], check=True)
        for source in (
            ROOT / "hk.pkl",
            ROOT / "home/.agents/skills/start-project/assets/hk.pkl",
        ):
            with self.subTest(config=str(source)):
                shutil.copyfile(source, self.cwd / "hk.pkl")
                for filename in ("raw/nested/bad.md", "docs/maintained.md"):
                    (self.cwd / filename).write_text("# Example\n")
                for inputs, expected in (
                    (["raw/nested/bad.md"], 0),
                    (["raw/nested/bad.md", "docs/maintained.md"], 1),
                ):
                    result = self.run_tool(
                        "hk", "run", "pre-commit", "--plan", "--json", *inputs,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    steps = json.loads(result.stdout)["steps"]
                    self.assertTrue(steps)
                    counts = [step["fileCount"] for step in steps]
                    self.assertEqual(max(counts), expected)
                    self.assertTrue(all(count <= expected for count in counts))


if __name__ == "__main__":
    unittest.main()
