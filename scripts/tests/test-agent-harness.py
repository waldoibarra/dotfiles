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
    def test_pi_binary_tracks_latest(self):
        config = (ROOT / "home/.config/mise/config.toml").read_text()
        self.assertRegex(
            config, r'(?m)^"npm:@earendil-works/pi-coding-agent"\s*=\s*"latest"$'
        )

    def test_laptop_images_use_native_kitty_protocol(self):
        settings = json.loads((ROOT / "home/.pi/agent/settings.json").read_text())
        self.assertEqual(settings["terminal"]["images"], "kitty")
        self.assertTrue(settings["terminal"].get("showImages", True))

    def test_worker_scope_rejects_lead_inheritance(self):
        settings = json.loads((ROOT / "home/.pi/agent/settings.json").read_text())
        scope = settings["subagents"]["modelScope"]
        self.assertTrue(scope["enforce"])
        self.assertTrue(scope["strict"])
        self.assertNotIn("inherit", scope["allow"])
        self.assertNotIn("scoped", scope["allow"])
        self.assertTrue(scope["allow"])
        for model in scope["allow"]:
            self.assertTrue(model.startswith("openai-codex/"))
            self.assertNotIn("astra", model)
            self.assertNotIn("fable", model)
            self.assertNotIn("*", model)
        self.assertNotIn("modelScope", settings)
        self.assertEqual(settings["steeringMode"], "all")

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
        lens_package = next(
            p for p in settings["packages"]
            if isinstance(p, dict) and p["source"].startswith("git:github.com/waldoibarra/pi-lens@")
        )
        self.assertEqual(lens_package["source"], "git:github.com/waldoibarra/pi-lens@latest")
        self.assertEqual(lens_package["skills"], [])
        self.assertEqual(lens_package["prompts"], [])
        config = json.loads((ROOT / "home/.pi/agent/extensions/subagent/config.json").read_text())
        self.assertIn("agent-management", config["disabledFeatures"])
        self.assertIn("workflow-scripts", config["disabledFeatures"])
        self.assertFalse(config["scheduledRuns"]["enabled"])
        self.assertFalse(config["missions"]["enabled"])

    def test_claude_lens_uses_one_renamed_marketplace(self):
        settings = json.loads((ROOT / "home/.claude/settings.json").read_text())
        self.assertTrue(settings["enabledPlugins"]["lens@claude-lens"])
        self.assertFalse(settings["enabledPlugins"]["lens@claude-code-lens"])
        marketplaces = settings["extraKnownMarketplaces"]
        self.assertNotIn("claude-code-lens", marketplaces)
        self.assertEqual(
            marketplaces["claude-lens"]["source"],
            {"source": "github", "repo": "waldoibarra/claude-lens", "ref": "latest"},
        )

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

    def test_development_recipe_loads_local_sources_and_installed_voice(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-pi-dev-") as scratch:
            home = Path(scratch) / "home with spaces"
            workspace = home / "workspace"
            binary_dir = home / "bin"
            workspace.mkdir(parents=True)
            binary_dir.mkdir()
            sources = [
                home / "projects/personal/pi/packages/coding-agent/dist/bundle/cli.js",
                home / "projects/personal/pi-lens/src/index.ts",
                home / "projects/personal/pi-subagents/index.ts",
                home / ".pi/agent/npm/node_modules/pi-live-codex/index.ts",
            ]
            for source in sources:
                source.parent.mkdir(parents=True, exist_ok=True)
                source.touch()
            capture = home / "launch.json"
            fake_node = binary_dir / "node"
            fake_node.write_text(
                "#!/usr/bin/env python3\nimport json, os, sys\n"
                "from pathlib import Path\n"
                "Path(os.environ['CAPTURE']).write_text(json.dumps({"
                "'argv': sys.argv[1:], 'cwd': os.getcwd()}))\n"
            )
            fake_node.chmod(0o755)
            env = dict(
                os.environ, HOME=str(home), CAPTURE=str(capture),
                PATH=f"{binary_dir}:{os.environ['PATH']}",
            )
            command = ["just", "--justfile", str(ROOT / "justfile"), "pi-lens-dev"]
            result = subprocess.run(command, cwd=workspace, env=env, capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            launch = json.loads(capture.read_text())
            base_argv = [
                str(sources[0]), "--no-extensions", "-e", str(sources[1]),
                "-e", str(sources[2]), "-e", str(sources[3]),
            ]
            self.assertEqual(launch["argv"], base_argv)
            self.assertEqual(Path(launch["cwd"]).resolve(), workspace.resolve())

            cases = [
                ["--continue"],
                ["--no-session"],
                ["--session-dir", "sessions with spaces", "literal $HOME; $(printf unsafe)"],
            ]
            for args in cases:
                with self.subTest(args=args):
                    capture.unlink()
                    result = subprocess.run(command + args, cwd=workspace, env=env,
                                            capture_output=True, text=True, timeout=10)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    launch = json.loads(capture.read_text())
                    self.assertEqual(launch["argv"], base_argv + args)
                    self.assertEqual(Path(launch["cwd"]).resolve(), workspace.resolve())
            for source in sources:
                with self.subTest(missing=source.name):
                    capture.unlink(missing_ok=True)
                    source.unlink()
                    try:
                        result = subprocess.run(command, cwd=workspace, env=env,
                                                capture_output=True, text=True, timeout=10)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn(f"Missing development file: {source}", result.stderr)
                        self.assertFalse(capture.exists())
                    finally:
                        source.touch()

    def test_documented_repository_guard_rejects_wrong_root(self):
        guide = (ROOT / "docs/coding-agents/pi/delegation.md").read_text()
        guard = guide.split("```sh\nactual_root=", 1)[1].split("```", 1)[0]
        with tempfile.TemporaryDirectory(prefix="dotfiles-repo-guard-") as scratch:
            expected = Path(scratch) / "expected repo"
            wrong = Path(scratch) / "wrong repo"
            driver = Path(scratch) / "guard.sh"
            driver.write_text("actual_root=" + guard)
            env = dict(os.environ, EXPECTED_REPO_ROOT=str(expected.resolve()))
            env.pop("GIT_DIR", None)
            env.pop("GIT_WORK_TREE", None)
            for directory, code in ((expected, 0), (wrong, 1)):
                directory.mkdir()
                subprocess.run(["git", "init", "--quiet", str(directory)], env=env,
                                check=True, capture_output=True, timeout=10)
                result = subprocess.run(["sh", str(driver)], cwd=directory, env=env,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, code, result.stderr)
                if code:
                    self.assertIn("Repository mismatch", result.stderr)

    @unittest.skipUnless(os.environ.get("PI_PACKAGE_DIR"), "set PI_PACKAGE_DIR for host checks")
    def test_compiled_host_persists_and_resumes_session_offline(self):
        result = subprocess.run(
            ["node", str(ROOT / "scripts/tests/check-pi-session-persistence.mjs")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("persisted and resumed the synthetic session", result.stdout)

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
                "settings_path = Path(os.environ['PI_CODING_AGENT_DIR'], 'settings.json')\n"
                "with settings_path.open() as settings_file:\n"
                " settings = json.load(settings_file)\n"
                "with Path(os.environ['CAPTURE']).open('a') as capture:\n"
                " capture.write(json.dumps({\n"
                "'argv': sys.argv[1:], 'cwd': os.getcwd(),\n"
                "'profile': os.environ.get('PI_CODING_AGENT_DIR'),\n"
                "'packages': settings['packages'],\n"
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
                if not install_exit:
                    lens_package = next(
                        p for p in calls[1]["packages"]
                        if isinstance(p, dict)
                        and p["source"] == "git:github.com/waldoibarra/pi-lens@latest"
                    )
                    self.assertEqual(lens_package["skills"], [])
                    self.assertEqual(lens_package["prompts"], [])


if __name__ == "__main__":
    unittest.main()
