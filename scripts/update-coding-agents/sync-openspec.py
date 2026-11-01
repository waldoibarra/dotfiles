#!/usr/bin/env python3
"""Refresh native OpenSpec skills only when upstream reports changes."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys

from importlib.util import module_from_spec, spec_from_file_location


def main():
    root = Path(__file__).resolve().parents[2]
    env = dict(os.environ, OPENSPEC_TELEMETRY="0")
    module_spec = spec_from_file_location("skill_sync", Path(__file__).with_name("sync-skills.py"))
    skill_sync = module_from_spec(module_spec)
    module_spec.loader.exec_module(skill_sync)
    declaration = skill_sync.manifest()
    home = Path.home()
    skill_sync.preflight(declaration, home)
    generated = root / ".agents/skills"
    skill_sync.safe_parents(generated / "entry", root)
    missing = [
        name for name in skill_sync.OPEN_SPEC
        if not skill_sync.usable_skill(generated / name, name)
    ]
    for name in missing:
        if (generated / name / "SKILL.md").exists():
            raise ValueError(
                "Invalid OpenSpec skill %s; preserve content and repair manually" % name
            )
    fresh = len(missing) == len(skill_sync.OPEN_SPEC)
    if fresh:
        subprocess.run(
            ["openspec", "init", "--tools", "agents", "--no-animation", str(root)],
            env=env, check=True, stdin=subprocess.DEVNULL,
        )
    preview = subprocess.run(
        ["openspec", "update", "--dry-run", "--json", str(root)],
        env=env, check=True, capture_output=True, text=True,
    )
    plan = json.loads(preview.stdout)
    if plan.get("failures"):
        raise RuntimeError(f"OpenSpec update blocked: {plan['failures']}")
    if "changes" not in plan or not isinstance(plan["changes"], list):
        raise RuntimeError("Unrecognized OpenSpec update preview; no files changed.")
    if plan["changes"]:
        additions = {
            str(Path(".agents/skills") / name / "SKILL.md") for name in missing
        }
        only_missing = (not fresh and missing and
                        {change.get("path") for change in plan["changes"]} == additions and
                        all(change.get("action") == "add" for change in plan["changes"]))
        if only_missing:
            with tempfile.TemporaryDirectory(prefix="openspec-repair-") as scratch:
                staging = Path(scratch)
                config = root / "openspec/config.yaml"
                if config.is_file():
                    destination = staging / "openspec/config.yaml"
                    destination.parent.mkdir(parents=True)
                    shutil.copy2(config, destination)
                subprocess.run(["openspec", "init", "--tools", "agents", "--no-animation",
                                str(staging)], env=env, check=True, stdin=subprocess.DEVNULL)
                staged = staging / ".agents/skills"
                for name in skill_sync.OPEN_SPEC:
                    if name not in missing and (generated / name / "SKILL.md").read_bytes() != (
                            staged / name / "SKILL.md").read_bytes():
                        raise RuntimeError(
                            "OpenSpec generated content differs; retry native update"
                        )
                for name in missing:
                    destination = generated / name / "SKILL.md"
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(staged / name / "SKILL.md", destination)
        else:
            subprocess.run(
                ["openspec", "update", str(root)], env=env, check=True,
                stdin=subprocess.DEVNULL,
            )
    else:
        print("OpenSpec skills already current.")
    for name in skill_sync.OPEN_SPEC:
        generated = root / ".agents/skills" / name
        if not skill_sync.usable_skill(generated, name):
            raise RuntimeError("OpenSpec did not generate valid %s" % name)
        for client in skill_sync.CLIENTS:
            skill_sync.link_missing(home / skill_sync.CLIENTS[client] / name, generated)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"OpenSpec synchronization failed: {error}", file=sys.stderr)
        sys.exit(1)
