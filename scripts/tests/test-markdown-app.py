"""Exercise the Markdown association script without changing LaunchServices."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/configure-markdown-app.sh"
BASH = shutil.which("bash")


class MarkdownAppTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="markdown-app-")
        self.addCleanup(self.scratch.cleanup)
        self.home = Path(self.scratch.name)
        self.config = self.home / ".config/duti/markdown.duti"
        self.config.parent.mkdir(parents=True)
        self.config.write_text("fixture.cursor .md all\n")
        self.bin = self.home / "bin"
        self.bin.mkdir()
        fixtures = {
            "uname": "print(os.environ.get('TEST_OS', 'Darwin'))\n",
            "osascript": (
                "if os.environ.get('QUERY_EXIT'):\n"
                " sys.exit(int(os.environ['QUERY_EXIT']))\n"
                "assert sys.argv[-1] == 'fixture.cursor'\n"
                "print(os.environ.get('APP_AVAILABLE', 'true'))\n"
            ),
            "duti": (
                "state = Path.home() / 'handler.txt'\n"
                "if sys.argv[1] == '-x':\n"
                " if os.environ.get('HANDLER_QUERY_EXIT'): sys.exit(29)\n"
                " if state.exists() and os.environ.get('POST_QUERY_EXIT'): sys.exit(29)\n"
                " handler = state.read_text() if state.exists() else 'fixture.previous'\n"
                " print('Fixture\\n/Applications/Fixture.app\\n' + handler)\n"
                " sys.exit(0)\n"
                "with (Path.home() / 'calls.jsonl').open('a') as out:\n"
                " out.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if os.environ.get('DUTI_EXIT'): sys.exit(int(os.environ['DUTI_EXIT']))\n"
                "if not os.environ.get('PENDING_APPROVAL'): state.write_text('fixture.cursor')\n"
            ),
        }
        for name, body in fixtures.items():
            executable = self.bin / name
            executable.write_text(
                f"#!{sys.executable}\nimport json, os, sys\nfrom pathlib import Path\n" + body
            )
            executable.chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.home), PATH=str(self.bin))

    def run_script(self):
        return subprocess.run(
            [BASH, str(SCRIPT)], env=self.env, capture_output=True, text=True
        )

    def calls(self):
        capture = self.home / "calls.jsonl"
        return [json.loads(line) for line in capture.read_text().splitlines()] \
            if capture.exists() else []

    def test_non_macos_skips_before_reading_configuration(self):
        self.env["TEST_OS"] = "Linux"
        self.config.rename(self.home / "unused-config")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [])

    def test_unavailable_app_skips_without_applying(self):
        self.env["APP_AVAILABLE"] = "false"
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [])

    def test_missing_duti_fails(self):
        (self.bin / "duti").rename(self.home / "unused-duti")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duti", result.stderr)
        self.assertEqual(self.calls(), [])

    def test_missing_configuration_fails(self):
        self.config.rename(self.home / "unused-config")
        self.assertNotEqual(self.run_script().returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_application_query_failure_propagates(self):
        self.env["QUERY_EXIT"] = "17"
        self.assertEqual(self.run_script().returncode, 17)
        self.assertEqual(self.calls(), [])

    def test_apply_failure_propagates(self):
        self.env["DUTI_EXIT"] = "23"
        self.assertEqual(self.run_script().returncode, 23)

    def test_repeated_application_skips_already_selected_handler(self):
        for _ in range(2):
            result = self.run_script()
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [[str(self.config)]])
        self.assertIn("no change requested", result.stdout)

    def test_failed_handler_precheck_never_invokes_setter(self):
        self.env["HANDLER_QUERY_EXIT"] = "1"
        self.assertEqual(self.run_script().returncode, 29)
        self.assertEqual(self.calls(), [])

    def test_failed_postcheck_is_not_reported_as_pending_consent(self):
        self.env["POST_QUERY_EXIT"] = "1"
        result = self.run_script()
        self.assertEqual(result.returncode, 29)
        self.assertNotIn("macOS prompt", result.stderr)
        self.assertEqual(self.calls(), [[str(self.config)]])

    def test_pending_approval_is_not_success_and_does_not_retry(self):
        self.env["PENDING_APPROVAL"] = "1"
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("macOS prompt", result.stderr)
        self.assertEqual(self.calls(), [[str(self.config)]])


if __name__ == "__main__":
    unittest.main()
