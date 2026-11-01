#!/usr/bin/env python3
"""Exercise OpenSpec update decisions without changing workstation state."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/update-coding-agents/sync-openspec.py"


class OpenSpecSyncTests(unittest.TestCase):
    def test_generated_document_links_block_every_generation_path_before_native_writes(self):
        names = (
            "apply-change", "archive-change", "explore", "propose",
            "sync-specs", "update-change",
        )
        for generation in ("partial-repair", "bootstrap", "version-update"):
            for target_exists in (False, True):
                with self.subTest(generation=generation, target_exists=target_exists):
                    with tempfile.TemporaryDirectory(prefix="openspec-link-guard-") as scratch:
                        base = Path(scratch)
                        checkout = base / "checkout"
                        updater = checkout / "scripts/update-coding-agents"
                        updater.mkdir(parents=True)
                        for script in ("sync-openspec.py", "sync-skills.py"):
                            (updater / script).write_bytes((SCRIPT.parent / script).read_bytes())
                        manifest = checkout / "home/.agents/skills-manifest.json"
                        manifest.parent.mkdir(parents=True)
                        manifest.write_text(json.dumps({
                            "version": 1, "clients": ["pi", "claude-code", "cursor"],
                            "skills": [],
                        }))
                        generated = checkout / ".agents/skills"
                        if generation != "bootstrap":
                            for name in names:
                                skill = generated / ("openspec-" + name)
                                skill.mkdir(parents=True)
                                (skill / "SKILL.md").write_text(
                                    "---\nname: openspec-" + name + "\n---\n\n" + name
                                )
                        document = generated / "openspec-propose/SKILL.md"
                        document.parent.mkdir(parents=True, exist_ok=True)
                        if document.exists():
                            document.unlink()
                        outside = base / "outside.md"
                        if target_exists:
                            outside.write_text("outside sentinel\n")
                        document.symlink_to(outside)
                        link_target = os.readlink(document)
                        marker = base / "native-ran"
                        binary = base / "openspec"
                        binary.write_text(
                            "#!" + sys.executable + "\n"
                            "import os\nfrom pathlib import Path\n"
                            "Path(os.environ['NATIVE_MARKER']).write_text('native called')\n"
                        )
                        binary.chmod(0o755)
                        home = base / "home"
                        home.mkdir()
                        env = dict(
                            os.environ, HOME=str(home),
                            PATH=str(base) + os.pathsep + os.environ["PATH"],
                            NATIVE_MARKER=str(marker),
                        )
                        for script, arguments in (("sync-skills.py", ["--preflight"]),
                                                  ("sync-openspec.py", [])):
                            result = subprocess.run(
                                [sys.executable, str(updater / script), *arguments],
                                env=env, capture_output=True, text=True, timeout=15,
                            )
                            self.assertNotEqual(result.returncode, 0)
                            self.assertIn("Conflicting generated skill document", result.stderr)
                            self.assertIn(str(document), result.stderr)
                            self.assertFalse(marker.exists())
                            self.assertTrue(document.is_symlink())
                            self.assertEqual(os.readlink(document), link_target)
                            self.assertEqual(outside.exists(), target_exists)
                            if target_exists:
                                self.assertEqual(outside.read_text(), "outside sentinel\n")
                            self.assertFalse((home / ".agents/skills/openspec-propose").exists())

    def test_native_partial_repair_preserves_authored_files_and_healthy_skills(self):
        with tempfile.TemporaryDirectory(prefix="openspec-native-partial-") as scratch:
            root = Path(scratch) / "checkout"
            (root / "openspec/specs").mkdir(parents=True)
            (root / "openspec/schemas").mkdir()
            (root / "openspec/config.yaml").write_text("schema: session-workflow\n")
            (root / "openspec/specs/example.md").write_text("sentinel\n")
            (root / "openspec/schemas/example.yaml").write_text("sentinel\n")
            updater = root / "scripts/update-coding-agents"
            updater.mkdir(parents=True)
            for name in ("sync-openspec.py", "sync-skills.py"):
                (updater / name).write_bytes((SCRIPT.parent / name).read_bytes())
            manifest = root / "home/.agents/skills-manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "version": 1, "clients": ["pi", "claude-code", "cursor"], "skills": [],
            }))
            home = Path(scratch) / "home"
            home.mkdir()
            env = dict(os.environ, HOME=str(home), OPENSPEC_TELEMETRY="0")
            initial = subprocess.run(
                [sys.executable, str(updater / "sync-openspec.py")],
                env=env, capture_output=True, text=True, timeout=50,
            )
            self.assertEqual(initial.returncode, 0, initial.stderr)
            missing = root / ".agents/skills/openspec-propose/SKILL.md"
            missing.unlink()
            before = {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
                      for p in root.rglob("*") if p.is_file()}
            repaired = subprocess.run([sys.executable, str(updater / "sync-openspec.py")],
                                      env=env, capture_output=True, text=True, timeout=50)
            self.assertEqual(repaired.returncode, 0, repaired.stderr)
            self.assertTrue(missing.is_file())
            for relative, snapshot in before.items():
                path = root / relative
                if relative == ".agents/skills/.openspec-target":
                    continue
                self.assertEqual(
                    (path.read_bytes(), path.stat().st_mtime_ns), snapshot, relative,
                )

    def test_missing_generation_bootstraps_then_links_all_clients(self):
        with tempfile.TemporaryDirectory(prefix="openspec-bootstrap-") as scratch:
            base = Path(scratch)
            checkout = base / "checkout"
            updater = checkout / "scripts/update-coding-agents"
            updater.mkdir(parents=True)
            for name in ("sync-openspec.py", "sync-skills.py"):
                (updater / name).write_bytes((SCRIPT.parent / name).read_bytes())
            manifest = checkout / "home/.agents/skills-manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "version": 1, "clients": ["pi", "claude-code", "cursor"], "skills": [],
            }))
            home = base / "home"
            home.mkdir()
            openspec = base / "openspec"
            openspec.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\nfrom pathlib import Path\n"
                "args=sys.argv[1:]; root=Path(args[-1])\n"
                "with Path(os.environ['CAPTURE']).open('a') as log:\n"
                "  log.write(json.dumps(args)+'\\n')\n"
                "if args[0]=='init':\n"
                " if os.environ.get('INIT_FAIL'): sys.exit(7)\n"
                " for name in ('apply-change','archive-change','explore',"
                "'propose','sync-specs','update-change'):\n"
                "  target=root/'.agents/skills'/('openspec-'+name)\n"
                "  target.mkdir(parents=True,exist_ok=True)\n"
                "  (target/'SKILL.md').write_text("
                "'---\\nname: openspec-'+name+'\\n---\\n\\n'+name)\n"
                "elif '--dry-run' in args: print(json.dumps({'changes':[], 'failures':[]}))\n"
            )
            openspec.chmod(0o755)
            capture = base / "calls"
            env = dict(
                os.environ, HOME=str(home), PATH=str(base)+os.pathsep+os.environ["PATH"],
                CAPTURE=str(capture),
            )
            failed = subprocess.run(
                [sys.executable, str(updater / "sync-openspec.py")],
                env=dict(env, INIT_FAIL="1"), capture_output=True, text=True, timeout=15,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertFalse((home / ".agents/skills/openspec-propose").is_symlink())
            capture.write_text("")
            for run_number in range(2):
                result = subprocess.run([sys.executable, str(updater / "sync-openspec.py")],
                                        env=env, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                calls = [json.loads(line) for line in capture.read_text().splitlines()]
                self.assertEqual(sum(call[0] == "init" for call in calls), 1)
                current = []
                for name in (
                    "apply-change", "archive-change", "explore", "propose",
                    "sync-specs", "update-change",
                ):
                    skill = "openspec-" + name
                    source = checkout / ".agents/skills" / skill
                    document = source / "SKILL.md"
                    current.append((document.read_bytes(), document.stat().st_mtime_ns,
                                    document.stat().st_mode))
                    for client in (".agents/skills", ".claude/skills", ".cursor/skills"):
                        link = home / client / skill
                        self.assertEqual(link.resolve(), source.resolve())
                        current.append((os.readlink(link), link.lstat().st_mtime_ns,
                                        link.lstat().st_mode))
                if run_number:
                    self.assertEqual(current, first_snapshot)
                else:
                    first_snapshot = current

    def test_preview_gates_updates_and_propagates_failures(self):
        cases = [
            ({"changes": [], "failures": []}, 0, 0, 0, 1),
            ({"changes": [{"type": "update"}], "failures": []}, 0, 0, 0, 2),
            ({"changes": [], "failures": ["conflict"]}, 0, 0, 1, 1),
            ({}, 0, 0, 1, 1),
            ({"changes": "invalid"}, 0, 0, 1, 1),
            ({"changes": []}, 7, 0, 1, 1),
            ({"changes": [{"type": "update"}]}, 0, 9, 1, 2),
            ("invalid-json", 0, 0, 1, 1),
        ]
        with tempfile.TemporaryDirectory(prefix="openspec-sync-") as scratch:
            directory = Path(scratch)
            checkout = directory / "checkout"
            updater = checkout / "scripts/update-coding-agents"
            updater.mkdir(parents=True)
            for name in ("sync-openspec.py", "sync-skills.py"):
                (updater / name).write_bytes((SCRIPT.parent / name).read_bytes())
            manifest = checkout / "home/.agents/skills-manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "version": 1, "clients": ["pi", "claude-code", "cursor"], "skills": [],
            }))
            for name in (
                "apply-change", "archive-change", "explore", "propose",
                "sync-specs", "update-change",
            ):
                generated = checkout / ".agents/skills" / ("openspec-" + name)
                generated.mkdir(parents=True)
                (generated / "SKILL.md").write_text(
                    "---\nname: openspec-" + name + "\n---\n\n" + name)
            home = directory / "home"
            home.mkdir()
            binary = directory / "openspec"
            binary.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                "from pathlib import Path\n"
                "with Path(os.environ['CAPTURE']).open('a') as log:\n"
                "    log.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if '--dry-run' in sys.argv:\n"
                "    print(os.environ['PREVIEW'])\n"
                "    sys.exit(int(os.environ['PREVIEW_EXIT']))\n"
                "sys.exit(int(os.environ['UPDATE_EXIT']))\n"
            )
            binary.chmod(0o755)
            capture = directory / "calls.jsonl"
            for preview, preview_exit, update_exit, expected_exit, expected_calls in cases:
                with self.subTest(
                    preview=preview, preview_exit=preview_exit, update_exit=update_exit
                ):
                    capture.write_text("")
                    env = dict(
                        os.environ, HOME=str(home), PATH=f"{directory}:{os.environ['PATH']}",
                        CAPTURE=str(capture),
                        PREVIEW=preview if isinstance(preview, str) else json.dumps(preview),
                        PREVIEW_EXIT=str(preview_exit), UPDATE_EXIT=str(update_exit),
                    )
                    result = subprocess.run(
                        [sys.executable, str(updater / "sync-openspec.py")], env=env,
                        capture_output=True, text=True, timeout=15,
                    )
                    self.assertEqual(result.returncode, expected_exit, result.stderr)
                    calls = [json.loads(line) for line in capture.read_text().splitlines()]
                    self.assertEqual(len(calls), expected_calls)
                    self.assertEqual(calls[0], [
                        "update", "--dry-run", "--json", str(checkout.resolve()),
                    ])
                    if expected_calls == 2:
                        self.assertEqual(calls[1], ["update", str(checkout.resolve())])


if __name__ == "__main__":
    unittest.main()
