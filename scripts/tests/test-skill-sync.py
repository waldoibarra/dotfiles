#!/usr/bin/env python3
"""Exercise skill declaration, migration, and recovery in isolated homes."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = "https://github.com/example/skills.git"


class SkillSyncTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="skill-sync-")
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)
        self.root = self.base / "checkout"
        script_dir = self.root / "scripts/update-coding-agents"
        script_dir.mkdir(parents=True)
        shutil.copy2(
            ROOT / "scripts/update-coding-agents/sync-skills.py", script_dir / "sync-skills.py",
        )
        declared = self.root / "home/.agents"
        declared.mkdir(parents=True)
        (declared / "skills-manifest.json").write_text(json.dumps({
            "version": 1, "clients": ["pi", "claude-code", "cursor"],
            "skills": [{"name": "sample", "source": SOURCE}],
        }))
        self.home = self.base / "other-user"
        self.home.mkdir()
        binary = self.base / "bin"
        binary.mkdir()
        npx = binary / "npx"
        npx.write_text(
            "#!" + sys.executable + "\n"
            "import json, os, sys\nfrom pathlib import Path\n"
            "home=Path(os.environ['HOME']); args=sys.argv[1:]\n"
            "if 'CALLS' in os.environ:\n"
            " with Path(os.environ['CALLS']).open('a') as stream:\n"
            "  stream.write(json.dumps(args)+'\\n')\n"
            "if args[2]=='add':\n"
            " name=args[args.index('--skill')+1]\n"
            " skill=home/'.agents/skills'/name; skill.mkdir(parents=True,exist_ok=True)\n"
            " (skill/'SKILL.md').write_text('---\\nname: '+name+'\\n---\\n\\nsample skill\\n')\n"
            " (skill/'reference.txt').write_text('reference\\n')\n"
            " if os.environ.get('FAIL_ADD'): sys.exit(31)\n"
            " lock=home/'.agents/.skill-lock.json'\n"
            " value=json.loads(lock.read_text()) if lock.exists() else "
            "{'version':1,'skills':{},'lastSelectedAgents':[],'dismissed':[]}\n"
            " value['skills'][name]={'sourceUrl':args[3]+'.git'}\n"
            " lock.write_text(json.dumps(value))\n"
        )
        npx.chmod(0o755)
        self.calls = self.base / "calls"
        self.env = dict(
            os.environ, HOME=str(self.home), XDG_CONFIG_HOME=str(self.home / ".config"),
            CLAUDE_CONFIG_DIR=str(self.home / ".claude"),
            PATH=str(binary)+os.pathsep+os.environ["PATH"],
            CALLS=str(self.calls), CI="1", DISABLE_TELEMETRY="1",
        )
        self.script = script_dir / "sync-skills.py"

    def run_sync(self, *arguments):
        return subprocess.run([sys.executable, str(self.script), *arguments], env=self.env,
                              cwd=self.base, capture_output=True, text=True, timeout=15)

    def recorded_source(self):
        lock = json.loads((self.home / ".agents/.skill-lock.json").read_text())
        return lock["skills"]["sample"]["sourceUrl"]

    def test_fresh_and_repeated_run_repairs_only_missing_client_link(self):
        local = self.home / ".agents/skills/local-only"
        local.mkdir(parents=True)
        (local / "SKILL.md").write_text("personal\n")
        local_time = (local / "SKILL.md").stat().st_mtime_ns
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)
        skill = self.home / ".agents/skills/sample"
        claude = self.home / ".claude/skills/sample"
        cursor = self.home / ".cursor/skills/sample"
        self.assertEqual(claude.resolve(), skill.resolve())
        self.assertEqual(cursor.resolve(), skill.resolve())
        self.assertEqual(self.recorded_source(), SOURCE)
        snapshot = [
            (p.read_bytes(), p.stat().st_mtime_ns, p.stat().st_mode) for p in skill.iterdir()
        ]
        lock = self.home / ".agents/.skill-lock.json"
        lock_snapshot = (lock.read_bytes(), lock.stat().st_mtime_ns, lock.stat().st_mode)
        link_time = claude.lstat().st_mtime_ns
        cursor.unlink()
        second = self.run_sync()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(claude.lstat().st_mtime_ns, link_time)
        self.assertEqual(
            (lock.read_bytes(), lock.stat().st_mtime_ns, lock.stat().st_mode), lock_snapshot,
        )
        self.assertEqual(cursor.resolve(), skill.resolve())
        self.assertEqual(snapshot, [
            (p.read_bytes(), p.stat().st_mtime_ns, p.stat().st_mode) for p in skill.iterdir()
        ])
        self.assertEqual(sum('add' in line for line in self.calls.read_text().splitlines()), 1)
        self.assertEqual((local / "SKILL.md").read_text(), "personal\n")
        self.assertEqual((local / "SKILL.md").stat().st_mtime_ns, local_time)
        self.assertFalse((self.root / "home/.agents/.skill-lock.json").exists())

    def test_known_legacy_link_migrates_without_modifying_source(self):
        original = self.root / "home/.agents/.skill-lock.json"
        original.write_text(json.dumps({
            "version": 1, "skills": {}, "dismissed": [], "lastSelectedAgents": [],
        }))
        installed = self.home / ".agents/.skill-lock.json"
        installed.parent.mkdir(parents=True)
        installed.symlink_to(original)
        before = original.read_bytes()
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(installed.is_file())
        self.assertFalse(installed.is_symlink())
        self.assertEqual(original.read_bytes(), before)

    def test_regular_lock_preserves_unrelated_entries(self):
        lock = self.home / ".agents/.skill-lock.json"
        lock.parent.mkdir(parents=True)
        lock.write_text(json.dumps({
            "version": 1, "skills": {"personal": {"sourceUrl": "local"}},
            "lastSelectedAgents": [], "dismissed": [],
        }))
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(lock.read_text())["skills"]["personal"], {"sourceUrl": "local"},
        )
        self.assertEqual(self.recorded_source(), SOURCE)
        self.assertFalse(lock.is_symlink())

    def test_unknown_broken_link_blocks_preflight_without_mutation(self):
        link = self.home / ".claude/skills/sample"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.base / "unknown")
        result = self.run_sync("--preflight")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(link.is_symlink())
        self.assertFalse(self.calls.exists())

    def test_unknown_broken_lock_link_survives_installer_preflight(self):
        self.prepare_sync_fixture()
        lock = self.home / ".agents/.skill-lock.json"
        lock.parent.mkdir(parents=True)
        lock.symlink_to(self.base / "unknown-lock")
        installer = subprocess.run(
            ["bash", str(self.root / "scripts/install-dotfiles.sh"), "--dry-run"],
            env=self.env, cwd=self.base, capture_output=True, text=True, timeout=15,
        )
        self.assertNotEqual(installer.returncode, 0)
        self.assertIn("Unknown lockfile link", installer.stderr)
        self.assertTrue(lock.is_symlink())
        self.assertFalse((self.home / "dotbot-ran").exists())

    def test_source_conflict_and_invalid_manifest_block_before_install(self):
        lock = self.home / ".agents/.skill-lock.json"
        lock.parent.mkdir(parents=True)
        lock.write_text(json.dumps({
            "skills": {"sample": {"sourceUrl": "https://github.com/other/skills.git"}},
        }))
        self.assertIn("Source conflict", self.run_sync("--preflight").stderr)
        self.assertFalse(self.calls.exists())
        lock.unlink()
        manifest = self.root / "home/.agents/skills-manifest.json"
        declaration = json.loads(manifest.read_text())
        declaration["skills"].append(declaration["skills"][0])
        manifest.write_text(json.dumps(declaration))
        self.assertIn("duplicate", self.run_sync().stderr)
        declaration["skills"].pop()
        declaration["clients"] = ["pi", "claude-code", "unknown"]
        manifest.write_text(json.dumps(declaration))
        self.assertIn("clients", self.run_sync().stderr)
        declaration["clients"] = ["pi", "claude-code", "cursor"]
        owned = self.root / "home/.agents/skills/sample"
        owned.mkdir(parents=True)
        manifest.write_text(json.dumps(declaration))
        self.assertIn("Repository-owned", self.run_sync().stderr)
        self.assertFalse(self.calls.exists())

    def test_alias_recipe_runs_skill_reconciliation_in_two_isolated_checkouts(self):
        for machine in range(2):
            with self.subTest(machine=machine):
                if machine:
                    self.root = self.base / "second-checkout"
                    self.home = self.base / "second-user"
                    self.home.mkdir()
                    self.env.update(HOME=str(self.home), XDG_CONFIG_HOME=str(self.home / ".config"),
                                    CLAUDE_CONFIG_DIR=str(self.home / ".claude"))
                    if self.calls.exists():
                        self.calls.unlink()
                self.prepare_sync_fixture()
                if machine == 1:
                    declared = self.root / "home/.agents/skills-manifest.json"
                    declared.write_bytes(published_manifest)
                if machine == 0:
                    original = self.root / "home/.agents/.skill-lock.json"
                    original.write_text(json.dumps({
                        "version": 1, "skills": {}, "lastSelectedAgents": [], "dismissed": [],
                    }))
                    lock = self.home / ".agents/.skill-lock.json"
                    lock.parent.mkdir(parents=True)
                    lock.symlink_to(original)
                alias = self.home / "aliases"
                dots_alias = next(
                    line for line in (ROOT / "home/.zshrc").read_text().splitlines()
                    if line.startswith("alias dots=")
                )
                alias.write_text(dots_alias + "\n")
                (self.home / ".dotfiles").symlink_to(self.root)
                run = subprocess.run(
                    ["zsh", "-f", "-c", 'source "$HOME/aliases"; eval dots'],
                    env=self.env, cwd=self.base, capture_output=True, text=True, timeout=25,
                )
                self.assertEqual(run.returncode, 0, run.stderr)
                git_calls = (self.home / "git-calls").read_text().splitlines()
                self.assertTrue(any(call == "pull" for call in git_calls))
                self.assertFalse(any(call.startswith(("commit", "push")) for call in git_calls))
                self.assertEqual(self.recorded_source(), SOURCE)
                for client in (".agents/skills", ".claude/skills", ".cursor/skills"):
                    if machine == 1:
                        self.assertTrue((self.home / client / "new-sample" / "SKILL.md").is_file())
                    self.assertTrue((self.home / client / "sample" / "SKILL.md").is_file())
                    openspec = self.home / client / "openspec-propose" / "SKILL.md"
                    self.assertTrue(openspec.is_file())
                if machine == 0:
                    self.assertFalse((self.home / ".agents/.skill-lock.json").is_symlink())
                    declared = self.root / "home/.agents/skills-manifest.json"
                    shared = json.loads(declared.read_text())
                    shared["skills"].append({"name": "new-sample", "source": SOURCE})
                    declared.write_text(json.dumps(shared))
                    published_manifest = declared.read_bytes()
                    updated = subprocess.run(
                        [
                            "just", "--justfile", str(self.root / "justfile"),
                            "--working-directory", str(self.root), "update-ca",
                        ],
                        env=self.env, capture_output=True, text=True, timeout=20,
                    )
                    self.assertEqual(updated.returncode, 0, updated.stderr)
                    self.assertTrue((self.home / ".cursor/skills/new-sample/SKILL.md").is_file())

    def test_installer_rejects_unknown_broken_link_before_dotbot(self):
        self.prepare_sync_fixture()
        conflict = self.home / ".claude/skills/sample"
        conflict.parent.mkdir(parents=True)
        conflict.symlink_to(self.base / "unknown")
        installer = subprocess.run(
            ["bash", str(self.root / "scripts/install-dotfiles.sh"), "--dry-run"],
            env=self.env, cwd=self.base, capture_output=True, text=True, timeout=15,
        )
        self.assertNotEqual(installer.returncode, 0)
        self.assertIn("Conflicting skill destination", installer.stderr)
        self.assertTrue(conflict.is_symlink())
        self.assertFalse((self.home / "dotbot-ran").exists())
        self.assertFalse(self.calls.exists())

    def test_installer_bootstraps_before_standalone_agent_provisioning(self):
        self.prepare_sync_fixture()
        installer = subprocess.run(
            ["bash", str(self.root / "scripts/install-dotfiles.sh"), "--dry-run"],
            env=self.env, cwd=self.base, capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(installer.returncode, 0, installer.stderr)
        self.assertFalse((self.home / ".agents/skills/sample").exists())
        self.assertFalse(self.calls.exists())
        updater = subprocess.run(
            [
                "just", "--justfile", str(self.root / "justfile"),
                "--working-directory", str(self.root), "update-ca",
            ],
            env=self.env, cwd=self.base, capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(updater.returncode, 0, updater.stderr)
        self.assertEqual(self.recorded_source(), SOURCE)
        self.assertTrue((self.home / ".cursor/skills/openspec-propose/SKILL.md").is_file())

    def prepare_sync_fixture(self):
        updater = self.root / "scripts/update-coding-agents"
        updater.mkdir(parents=True, exist_ok=True)
        for name in ("sync-skills.py", "sync-openspec.py"):
            shutil.copy2(ROOT / "scripts/update-coding-agents" / name, updater / name)
        manifest = self.root / "home/.agents/skills-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({
            "version": 1, "clients": ["pi", "claude-code", "cursor"],
            "skills": [{"name": "sample", "source": SOURCE}],
        }))
        shutil.copy2(ROOT / "justfile", self.root / "justfile")
        shutil.copy2(
            ROOT / "scripts/install-dotfiles.sh", self.root / "scripts/install-dotfiles.sh",
        )
        entrypoint = (ROOT / "scripts/update-coding-agents/entrypoint.sh").read_text()
        first = entrypoint.index("install_pi_packages() (")
        last = entrypoint.index("\n)\n\nmain()", first) + 2
        entrypoint_stub = updater / "entrypoint.sh"
        entrypoint = entrypoint[:first] + "install_pi_packages() { :; }" + entrypoint[last:]
        start = entrypoint.index(
            '  bash "${ENTRYPOINT_DIR}/sync-life-profile.sh"', entrypoint.index("main() {")
        )
        finish = entrypoint.index('  python3 "${ENTRYPOINT_DIR}/sync-skills.py"', start)
        entrypoint_stub.write_text(entrypoint[:start] + entrypoint[finish:])
        entrypoint_stub.chmod(0o755)
        (updater / "sync-managed-configs.sh").write_text("sync_managed_configs() { :; }\n")
        helpers = self.root / "scripts/lib/shell-helpers.sh"
        helpers.parent.mkdir(parents=True, exist_ok=True)
        helpers.write_text("print_separator() { :; }\n")
        for relative in (
            "scripts/update-coding-agents/sync-life-profile.sh",
            "scripts/update-coding-agents/sync-cursor-rule.sh",
            "scripts/update-coding-agents/sync-personal-mcp.py",
            "scripts/sync-packages.py", "scripts/obsidian.py",
        ):
            stub = self.root / relative
            stub.parent.mkdir(parents=True, exist_ok=True)
            stub.write_text("# isolated no-op\n" if stub.suffix == ".py" else
                            "#!/bin/sh\nexit 0\n")
        dotbot = self.root / "dotbot/bin/dotbot"
        dotbot.parent.mkdir(parents=True, exist_ok=True)
        dotbot.write_text('#!/bin/sh\ntouch "$HOME/dotbot-ran"\nexit 0\n')
        dotbot.chmod(0o755)
        binary = Path(self.env["PATH"].split(os.pathsep)[0])
        git = binary / "git"
        git.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$HOME/git-calls"\n')
        git.chmod(0o755)
        hk = binary / "hk"
        hk.write_text("#!/bin/sh\nexit 0\n")
        hk.chmod(0o755)
        openspec = binary / "openspec"
        openspec.write_text(
            "#!" + sys.executable + "\n"
            "import json, sys\nfrom pathlib import Path\n"
            "args=sys.argv[1:]; root=Path(args[-1])\n"
            "if args[0]=='init':\n"
            " for name in ('apply-change','archive-change','explore',"
            "'propose','sync-specs','update-change'):\n"
            "  target=root/'.agents/skills'/('openspec-'+name)\n"
            "  target.mkdir(parents=True,exist_ok=True)\n"
            "  (target/'SKILL.md').write_text('---\\nname: openspec-'+name+'\\n---\\n\\n'+name)\n"
            "elif '--dry-run' in args: print(json.dumps({'changes':[],'failures':[]}))\n"
        )
        openspec.chmod(0o755)

    def test_dotbot_clean_would_delete_undeclared_broken_repo_link(self):
        orphan = self.home / ".agents/skills/local-only"
        orphan.parent.mkdir(parents=True)
        orphan.symlink_to(self.root / "home/.agents/skills/removed")
        unrelated = self.home / ".agents/skills/private"
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("private")
        config = self.base / "clean.yaml"
        config.write_text('- clean:\n    ~/.agents/skills:\n')
        command = [
            str(ROOT / "dotbot/bin/dotbot"), "-d", str(self.root), "-c", str(config),
        ]
        self.assertIn("Unknown broken repository skill link", self.run_sync("--preflight").stderr)
        self.assertTrue(orphan.is_symlink())
        actual = subprocess.run(command, env=self.env, capture_output=True, text=True, timeout=15)
        self.assertEqual(actual.returncode, 0, actual.stderr)
        self.assertFalse(orphan.is_symlink())
        self.assertEqual((unrelated / "SKILL.md").read_text(), "private")

    def test_symlinked_parents_and_authored_conflict_block_preflight(self):
        for parent in (
            ".agents", ".claude", ".cursor", ".agents/skills",
            ".claude/skills", ".cursor/skills",
        ):
            with self.subTest(parent=parent):
                redirected = self.home / parent
                redirected.parent.mkdir(parents=True, exist_ok=True)
                redirected.symlink_to(self.base / "outside")
                result = self.run_sync("--preflight")
                self.assertIn("Unsafe skill parent", result.stderr)
                self.assertTrue(redirected.is_symlink())
                redirected.unlink()
        authored = self.root / "home/.agents/skills/docs"
        authored.mkdir(parents=True)
        link = self.home / ".cursor/skills/docs"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.base / "outside")
        self.assertIn("Conflicting skill destination", self.run_sync("--preflight").stderr)
        link.unlink()
        link.symlink_to(authored)
        self.assertEqual(self.run_sync("--preflight").returncode, 0)
        authored.rmdir()
        authored.parent.rmdir()
        for parent in (".agents", ".agents/skills", "home/.agents/skills"):
            with self.subTest(source_parent=parent):
                generated = self.root / parent
                generated.parent.mkdir(parents=True, exist_ok=True)
                generated.symlink_to(self.base / "outside")
                self.assertIn("Unsafe skill parent", self.run_sync("--preflight").stderr)
                generated.unlink()
        manifest = self.root / "home/.agents/skills-manifest.json"
        manifest.unlink()
        manifest.symlink_to(self.base / "outside")
        self.assertIn("Unsafe skills manifest", self.run_sync("--preflight").stderr)

    def test_missing_or_malformed_content_with_lock_is_never_linked(self):
        self.assertEqual(self.run_sync().returncode, 0)
        installed = self.home / ".agents/skills/sample/SKILL.md"
        link = self.home / ".claude/skills/sample"
        link.unlink()
        for content in (None, "", "sample skill", "---\nname: wrong\n---\n\nbody"):
            with self.subTest(content=content):
                if content is None:
                    installed.unlink(missing_ok=True)
                else:
                    installed.write_text(content)
                result = self.run_sync()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Incomplete skill", result.stderr)
                self.assertFalse(link.is_symlink())
        self.assertEqual(self.recorded_source(), SOURCE)

    def test_mixed_install_and_adoption_preserve_latest_lock(self):
        manifest = self.root / "home/.agents/skills-manifest.json"
        data = json.loads(manifest.read_text())
        data["skills"].append({"name": "adopted", "source": SOURCE})
        manifest.write_text(json.dumps(data))
        installed = self.home / ".agents/skills/adopted"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("---\nname: adopted\n---\n\nsample skill\n")
        (installed / "reference.txt").write_text("reference\n")
        lock = self.home / ".agents/.skill-lock.json"
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text(json.dumps({"version": 1, "skills": {"personal": {"sourceUrl": "local"}},
                                    "dismissed": ["keep"], "lastSelectedAgents": []}))
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(lock.read_text())
        self.assertEqual(set(state["skills"]), {"personal", "sample", "adopted"})
        self.assertEqual(state["dismissed"], ["keep"])

    def test_colored_zero_exit_failure_and_missing_native_metadata(self):
        binary = Path(self.env["PATH"].split(os.pathsep)[0]) / "npx"
        original = binary.read_text()
        binary.write_text(original.replace(
            "if args[2]=='add':",
            "if args[2]=='add':\n print('\\x1b[31mError: unavailable\\x1b[0m'); sys.exit(0)",
        ))
        result = self.run_sync()
        self.assertIn("Native skills command reported failure", result.stderr)
        self.assertFalse((self.home / ".claude/skills/sample").is_symlink())
        binary.write_text(original.replace(
            " lock.write_text(json.dumps(value))", " pass # no lock entry",
        ))
        result = self.run_sync()
        self.assertIn("missing matching source metadata", result.stderr)
        self.assertFalse((self.home / ".claude/skills/sample").is_symlink())

    def test_native_adoption_requires_full_tree_and_native_metadata(self):
        manifest = self.root / "home/.agents/skills-manifest.json"
        manifest.write_text(json.dumps({
            "version": 1, "clients": ["pi", "claude-code", "cursor"],
            "skills": [{
                "name": "find-skills", "source": "https://github.com/vercel-labs/skills.git",
            }],
        }))
        env = dict(
            self.env, PATH=os.environ["PATH"], npm_config_cache=str(self.base / "npm-cache"),
        )
        installed = subprocess.run(
            [
                "npx", "-y", "skills", "add", "https://github.com/vercel-labs/skills",
                "--skill", "find-skills", "-a", "pi", "-a", "claude-code", "-a", "cursor",
                "-g", "-y",
            ],
            env=env, capture_output=True, text=True, timeout=100,
        )
        self.assertEqual(installed.returncode, 0, installed.stderr)
        lock = self.home / ".agents/.skill-lock.json"
        native_entry = json.loads(lock.read_text())["skills"]["find-skills"]
        self.assertEqual(
            native_entry["sourceUrl"], "https://github.com/vercel-labs/skills.git",
        )
        tree = self.home / ".agents/skills/find-skills"
        snapshot = {
            str(p.relative_to(tree)): p.read_bytes() for p in tree.rglob("*") if p.is_file()
        }
        lock.unlink()
        adopted = subprocess.run(
            [sys.executable, str(self.script)], env=env,
            capture_output=True, text=True, timeout=110,
        )
        self.assertEqual(adopted.returncode, 0, adopted.stderr)
        self.assertEqual(
            {str(p.relative_to(tree)): p.read_bytes()
            for p in tree.rglob("*") if p.is_file()}, snapshot,
        )
        self.assertEqual(
            json.loads(lock.read_text())["skills"]["find-skills"]["sourceUrl"],
            native_entry["sourceUrl"],
        )
        lock.unlink()
        document = tree / "SKILL.md"
        document.write_bytes(document.read_bytes() + b"\nmodified\n")
        mismatch = subprocess.run(
            [sys.executable, str(self.script)], env=env,
            capture_output=True, text=True, timeout=110,
        )
        self.assertIn("Source conflict", mismatch.stderr)
        self.assertIn(b"modified", document.read_bytes())
        self.assertFalse(lock.exists())

    def test_interrupted_install_recovers_without_rewriting_content(self):
        self.env["FAIL_ADD"] = "1"
        interrupted = self.run_sync()
        self.assertNotEqual(interrupted.returncode, 0)
        installed = self.home / ".agents/skills/sample/SKILL.md"
        self.assertTrue(installed.is_file())
        unchanged = installed.stat().st_mtime_ns
        del self.env["FAIL_ADD"]
        retry = self.run_sync()
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(installed.stat().st_mtime_ns, unchanged)
        self.assertEqual(self.recorded_source(), SOURCE)

    def test_unrecorded_content_is_adopted_only_after_full_tree_match(self):
        installed = self.home / ".agents/skills/sample"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("---\nname: sample\n---\n\nsample skill\n")
        (installed / "reference.txt").write_text("reference\n")
        marker = (installed / "reference.txt").stat().st_mtime_ns
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((installed / "reference.txt").stat().st_mtime_ns, marker)
        self.assertEqual(self.recorded_source(), SOURCE)
        (installed / "reference.txt").write_text("modified\n")
        (self.home / ".agents/.skill-lock.json").unlink()
        result = self.run_sync()
        self.assertIn("Source conflict", result.stderr)
        self.assertEqual((installed / "reference.txt").read_text(), "modified\n")
        self.assertFalse((self.home / ".agents/.skill-lock.json").exists())


if __name__ == "__main__":
    unittest.main()
