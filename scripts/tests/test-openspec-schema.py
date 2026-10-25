#!/usr/bin/env python3
"""Exercise the real OpenSpec schema lifecycle in disposable homes and projects."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "openspec/schemas/session-workflow"
GUIDE = ROOT / "docs/ai-harness/session-workflow.md"

PROPOSAL = """# Proposal

## Why

Fixture users need a stable response for this isolated lifecycle check.

## What Changes

- Add a predictable response.

## Capabilities

- fixture-response: A stable observable response.

## Impact

Disposable fixtures only.
"""
SPEC = """# Spec Delta

## Purpose

Provide a stable fixture response for testing the native change lifecycle without external services.

## ADDED Requirements

### Requirement: Stable response

The fixture SHALL return the agreed response.

#### Scenario: Successful request

- **WHEN** the fixture receives a request
- **THEN** it returns the agreed response
"""


def executable(name):
    """Resolve Mise tools before replacing HOME in fixture subprocesses."""
    if shutil.which("mise"):
        found = subprocess.run(
            ["mise", "which", name], capture_output=True, text=True, timeout=15,
        )
        if found.returncode == 0:
            return found.stdout.strip()
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f"Missing required tool: {name}")
    return found


class OpenSpecSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = executable("openspec")
        cls.node_directory = str(Path(executable("node")).parent)

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="openspec-schema-")
        self.addCleanup(self.scratch.cleanup)
        base = Path(self.scratch.name)
        self.home = base / "home"
        self.project = base / "project"
        self.project.mkdir()
        self.home.mkdir()
        config = self.home / ".config/openspec/config.json"
        config.parent.mkdir(parents=True)
        config.write_bytes((ROOT / "home/.config/openspec/config.json").read_bytes())
        user_schema = self.home / ".local/share/openspec/schemas/session-workflow"
        user_schema.parent.mkdir(parents=True)
        user_schema.symlink_to(SCHEMA)
        workflow = self.home / ".agents/references/session-workflow.md"
        workflow.parent.mkdir(parents=True)
        workflow.symlink_to(GUIDE)
        self.env = dict(
            os.environ, HOME=str(self.home),
            XDG_CONFIG_HOME=str(self.home / ".config"),
            XDG_DATA_HOME=str(self.home / ".local/share"),
            XDG_CACHE_HOME=str(self.home / ".cache"),
            PATH=f"{self.node_directory}:{os.environ['PATH']}",
            OPENSPEC_TELEMETRY="0", CI="1", NO_COLOR="1",
        )
        self.command("init", "--tools", "none", "--no-animation")
        (self.project / "openspec/config.yaml").write_text("schema: session-workflow\n")

    def command(self, *arguments, succeeds=True):
        result = subprocess.run(
            [self.binary, *arguments], cwd=self.project, env=self.env,
            capture_output=True, text=True, timeout=30,
        )
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def response(self, *arguments):
        return json.loads(self.command(*arguments, "--json").stdout)

    def new_change(self, name="fixture-change", schema=None):
        arguments = ["new", "change", name]
        if schema:
            arguments.extend(["--schema", schema])
        self.command(*arguments)
        return self.project / "openspec/changes" / name

    def write_plan(self, change, done=False):
        (change / "proposal.md").write_text(PROPOSAL)
        marker = "x" if done else " "
        (change / "tasks.md").write_text(
            f"# Tasks\n\n## 1. Fixture\n\n- [{marker}] 1.1 Verify the fixture response.\n"
        )

    def test_user_schema_resolution_and_portable_instructions(self):
        self.command("schema", "validate", "session-workflow")
        resolution = self.response("schema", "which", "session-workflow")
        self.assertEqual(resolution["source"], "user")
        self.assertEqual(Path(resolution["path"]).resolve(), SCHEMA)
        self.new_change()
        state = self.response("status", "--change", "fixture-change")
        self.assertEqual(state["schemaName"], "session-workflow")
        self.assertEqual(
            {artifact["id"] for artifact in state["artifacts"]},
            {"proposal", "specs", "tasks"},
        )
        instructions = self.response("instructions", "proposal", "--change", "fixture-change")
        self.assertIn("~/.agents/references/session-workflow.md", instructions["instruction"])
        self.assertEqual(
            (self.home / ".agents/references/session-workflow.md").resolve(), GUIDE
        )
        self.assertFalse((self.project / "docs").exists())

    def test_skip_specs_keeps_proposal_dependency_and_archives_without_specs(self):
        change = self.new_change()
        metadata = change / ".openspec.yaml"
        metadata.write_text(metadata.read_text() + "skip_specs: true\n")
        state = self.response("status", "--change", "fixture-change")
        artifacts = {item["id"]: item for item in state["artifacts"]}
        self.assertEqual(artifacts["tasks"]["status"], "blocked")
        (change / "proposal.md").write_text(PROPOSAL)
        state = self.response("status", "--change", "fixture-change")
        artifacts = {item["id"]: item for item in state["artifacts"]}
        self.assertEqual(artifacts["tasks"]["status"], "ready")
        self.write_plan(change, done=True)
        self.command("validate", "fixture-change", "--strict", "--no-interactive")
        self.command("archive", "fixture-change", "--yes")
        self.assertFalse(change.exists())
        self.assertFalse(list((self.project / "openspec/specs").rglob("spec.md")))
        self.assertEqual(
            len(list((self.project / "openspec/changes/archive").glob("*-fixture-change"))), 1
        )

    def test_behavior_change_requires_specs_and_tracks_real_progress(self):
        change = self.new_change()
        self.write_plan(change)
        self.command("validate", "fixture-change", "--strict", "--no-interactive", succeeds=False)
        spec = change / "specs/fixture-response/spec.md"
        spec.parent.mkdir(parents=True)
        spec.write_text(SPEC)
        self.command("validate", "fixture-change", "--strict", "--no-interactive")
        state = self.response("instructions", "apply", "--change", "fixture-change")
        self.assertEqual(state["progress"]["total"], 1)
        self.assertEqual(state["progress"]["complete"], 0)
        self.assertIn("explicit approval", state["instruction"])
        self.write_plan(change, done=True)
        state = self.response("instructions", "apply", "--change", "fixture-change")
        self.assertEqual(state["progress"]["complete"], 1)
        self.command("archive", "fixture-change", "--yes")
        maintained = self.project / "openspec/specs/fixture-response/spec.md"
        self.assertIn("### Requirement: Stable response", maintained.read_text())
        self.command("validate", "--specs", "--strict", "--no-interactive")

    def test_existing_selection_survives_a_default_change(self):
        config = self.project / "openspec/config.yaml"
        config.write_text("schema: spec-driven\n")
        self.new_change("existing-change")
        config.write_text("schema: session-workflow\n")
        existing = self.response("status", "--change", "existing-change")
        self.assertEqual(existing["schemaName"], "spec-driven")
        self.assertIn("design", {item["id"] for item in existing["artifacts"]})
        self.new_change("new-change")
        selected = self.response("status", "--change", "new-change")
        self.assertEqual(selected["schemaName"], "session-workflow")
        self.assertNotIn("design", {item["id"] for item in selected["artifacts"]})

    def test_project_local_schema_takes_precedence(self):
        local = self.project / "openspec/schemas/session-workflow"
        shutil.copytree(SCHEMA, local)
        resolution = self.response("schema", "which", "session-workflow")
        self.assertEqual(resolution["source"], "project")
        self.assertEqual(Path(resolution["path"]).resolve(), local.resolve())


if __name__ == "__main__":
    unittest.main()
