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
                        os.environ, PATH=f"{directory}:{os.environ['PATH']}",
                        CAPTURE=str(capture),
                        PREVIEW=preview if isinstance(preview, str) else json.dumps(preview),
                        PREVIEW_EXIT=str(preview_exit), UPDATE_EXIT=str(update_exit),
                    )
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT)], env=env,
                        capture_output=True, text=True, timeout=15,
                    )
                    self.assertEqual(result.returncode, expected_exit, result.stderr)
                    calls = [json.loads(line) for line in capture.read_text().splitlines()]
                    self.assertEqual(len(calls), expected_calls)
                    self.assertEqual(calls[0], ["update", "--dry-run", "--json", str(ROOT)])
                    if expected_calls == 2:
                        self.assertEqual(calls[1], ["update", str(ROOT)])


if __name__ == "__main__":
    unittest.main()
