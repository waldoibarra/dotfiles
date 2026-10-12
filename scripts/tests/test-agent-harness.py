"""Check shared role delivery and Pi provisioning without touching the workstation."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dotbot/lib/pyyaml/lib"))
import yaml  # noqa: E402 - use Dotbot's existing parser, not another dependency


class AgentHarnessTest(unittest.TestCase):
    def test_laptop_images_use_native_kitty_protocol(self):
        settings = json.loads((ROOT / "home/.pi/agent/settings.json").read_text())
        self.assertEqual(settings["terminal"]["images"], "kitty")
        self.assertTrue(settings["terminal"].get("showImages", True))

    def test_shared_roles_and_pi_overrides(self):
        roles = ROOT / "home/.agents/roles"
        settings = json.loads((ROOT / "home/.pi/agent/settings.json").read_text())
        config = settings["subagents"]
        expected = {"plan-reviewer", "code-auditor", "implementer", "browser-tester", "docs-writer"}
        self.assertEqual({p.stem for p in roles.glob("*.md")}, expected)
        self.assertEqual(set(config["agentOverrides"]), expected)
        self.assertEqual(config["agentScanDirs"], ["~/.agents/roles"])
        self.assertTrue(config["disableBuiltins"])
        for name in expected:
            frontmatter = yaml.safe_load((roles / f"{name}.md").read_text().split("---", 2)[1])
            self.assertEqual(set(frontmatter), {"name", "description"})
            self.assertEqual(frontmatter["name"], name)
            override = config["agentOverrides"][name]
            self.assertEqual(override["systemPromptMode"], "append")
            for key in ("inheritGlobalContext", "inheritProjectContext", "inheritSkills"):
                self.assertTrue(override[key], (name, key))
            self.assertNotIn("model", override)
        for name in ("plan-reviewer", "code-auditor"):
            tools = config["agentOverrides"][name]["tools"]
            self.assertIsInstance(tools, list)
            self.assertNotIn("write", tools)
            self.assertNotIn("edit", tools)
            self.assertIn("bash", tools)

    def test_runner_is_pinned_and_optional_resources_are_off(self):
        settings = json.loads((ROOT / "home/.pi/agent/settings.json").read_text())
        package = next(
            p for p in settings["packages"]
            if isinstance(p, dict) and p["source"].startswith("npm:pi-subagents@")
        )
        self.assertEqual(package["source"], "npm:pi-subagents@0.77.0")
        self.assertEqual(package["skills"], [])
        self.assertEqual(package["prompts"], [])
        config = json.loads((ROOT / "home/.pi/agent/extensions/subagent/config.json").read_text())
        self.assertIn("agent-management", config["disabledFeatures"])
        self.assertIn("workflow-scripts", config["disabledFeatures"])
        self.assertFalse(config["scheduledRuns"]["enabled"])
        self.assertFalse(config["missions"]["enabled"])

    def test_dotbot_links_shared_bytes_idempotently(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-harness-") as scratch:
            home = Path(scratch)
            env = dict(os.environ, HOME=str(home))
            command = [
                sys.executable, str(ROOT / "dotbot/bin/dotbot"),
                "-d", str(ROOT), "-c", str(ROOT / "install.conf.yaml"),
                "--only", "create", "link",
            ]
            for _ in range(2):
                subprocess.run(command, env=env, check=True, capture_output=True, text=True)
                for source in (ROOT / "home/.agents/roles").glob("*.md"):
                    for directory in (".agents/roles", ".claude/agents"):
                        self.assertEqual((home / directory / source.name).resolve(), source)
                for relative in (".agents/AGENTS.md", ".pi/agent/AGENTS.md"):
                    self.assertEqual((home / relative).resolve(), ROOT / "home/.agents/AGENTS.md")
                for relative in (".agents/RTK.md", ".claude/RTK.md"):
                    self.assertEqual((home / relative).resolve(), ROOT / "home/.agents/RTK.md")
                config = home / ".pi/agent/extensions/subagent/config.json"
                self.assertEqual(
                    config.resolve(), ROOT / "home/.pi/agent/extensions/subagent/config.json"
                )
                self.assertTrue((home / ".claude/agents").is_dir())
                self.assertFalse((home / ".claude/agents").is_symlink())

    def test_package_reconciliation_uses_normal_profile_and_propagates_failure(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-packages-") as scratch:
            home = Path(scratch)
            binary_dir = home / "bin"
            binary_dir.mkdir()
            # A standalone fixture avoids shell -c and never invokes real Pi.
            fake_pi = binary_dir / "pi"
            fake_pi.write_text(
                "#!/usr/bin/env python3\nimport json, os, sys\n"
                "from pathlib import Path\n"
                "with Path(os.environ['CAPTURE']).open('a') as capture:\n"
                " capture.write(json.dumps({\n"
                "'argv': sys.argv[1:], 'cwd': os.getcwd(),\n"
                "'profile': os.environ.get('PI_CODING_AGENT_DIR'),\n"
                "'api_key_present': 'OPENAI_API_KEY' in os.environ}) + '\\n')\n"
                "key = 'INSTALL_EXIT' if sys.argv[1] == 'install' else 'UPDATE_EXIT'\n"
                "sys.exit(int(os.environ.get(key, '0')))\n"
            )
            fake_pi.chmod(0o755)
            driver = home / "reconcile.sh"
            driver.write_text(
                f"#!/usr/bin/env bash\nset -euo pipefail\n"
                f"source '{ROOT}/scripts/update-coding-agents/entrypoint.sh'\n"
                "install_pi_packages\n"
            )
            profile = home / ".pi/agent"
            profile.mkdir(parents=True)
            (profile / "settings.json").write_text(
                (ROOT / "home/.pi/agent/settings.json").read_text())
            capture = home / "capture.json"
            env = dict(
                os.environ, HOME=str(home), PATH=f"{binary_dir}:{os.environ['PATH']}",
                PI_CODING_AGENT_DIR="/unused/trial", OPENAI_API_KEY="fixture-only",
                CAPTURE=str(capture),
            )
            for install_exit, update_exit, expected in ((0, 0, 0), (19, 0, 1), (0, 19, 19)):
                capture.write_text("")
                env.update(INSTALL_EXIT=str(install_exit), UPDATE_EXIT=str(update_exit))
                result = subprocess.run(["bash", str(driver)], env=env, capture_output=True,
                                        text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                calls = [json.loads(line) for line in capture.read_text().splitlines()]
                self.assertEqual(
                    calls[0]["argv"], ["install", "npm:pi-subagents@0.77.0", "--no-approve"]
                )
                self.assertEqual(len(calls), 1 if install_exit else 2)
                if not install_exit:
                    self.assertEqual(
                        calls[1]["argv"], ["update", "--extensions", "--no-approve"]
                    )
                for observed in calls:
                    self.assertEqual(Path(observed["cwd"]).resolve(), home.resolve())
                    self.assertEqual(observed["profile"], str(profile))
                    self.assertFalse(observed["api_key_present"])


if __name__ == "__main__":
    unittest.main()
