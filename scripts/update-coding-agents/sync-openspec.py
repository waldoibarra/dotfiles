#!/usr/bin/env python3
"""Refresh native OpenSpec skills only when upstream reports changes."""

import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[2]
    env = dict(os.environ, OPENSPEC_TELEMETRY="0")
    preview = subprocess.run(
        ["openspec", "update", "--dry-run", "--json", str(root)],
        env=env, check=True, capture_output=True, text=True,
    )
    plan = json.loads(preview.stdout)
    if plan.get("failures"):
        raise RuntimeError(f"OpenSpec update blocked: {plan['failures']}")
    if "changes" not in plan or not isinstance(plan["changes"], list):
        raise RuntimeError("Unrecognized OpenSpec update preview; no files changed.")
    if not plan["changes"]:
        print("OpenSpec skills already current.")
        return
    subprocess.run(["openspec", "update", str(root)], env=env, check=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"OpenSpec synchronization failed: {error}", file=sys.stderr)
        sys.exit(1)
