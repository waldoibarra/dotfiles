"""Exercise the personal Sheets launcher using disposable homes and fake uvx."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "home/.local/bin/google-sheets-personal-mcp"


class PersonalGoogleSheetsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sheets-mcp-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.uvx = self.bin / "uvx"
        self.uvx.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                            "print(json.dumps({'args':sys.argv[1:], 'env':dict(os.environ)}))\n"
                            "sys.exit(int(os.environ.get('FAKE_EXIT','0')))\n")
        self.uvx.chmod(0o755)
        self.client_dir = self.home / ".config/mcp-google-sheets/personal"
        self.client_dir.mkdir(parents=True)
        (self.client_dir / "client.json").write_text(json.dumps({"installed": {
            "client_id": "test-id", "client_secret": "test-secret",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }}))
        self.cwd = self.base / "outside"
        self.cwd.mkdir()
        self.env = dict(os.environ, HOME=str(self.home), PATH=f"{self.bin}:{os.environ['PATH']}",
                        CREDENTIALS_CONFIG="hostile", SERVICE_ACCOUNT_PATH="hostile",
                        GOOGLE_APPLICATION_CREDENTIALS="hostile", DRIVE_FOLDER_ID="hostile",
                        CREDENTIALS_PATH="hostile", TOKEN_PATH="hostile",
                        ENABLED_TOOLS="share_spreadsheet")

    def run_launcher(self, cwd=None):
        return subprocess.run([sys.executable, str(LAUNCHER)], cwd=cwd or self.cwd,
                              env=self.env, capture_output=True, text=True)

    def test_exact_isolated_launch_and_private_token_directory(self):
        result = self.run_launcher()
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(observed["args"], [
            "--python", "3.12", "--with", "mcp==1.30.0", "mcp-google-sheets==0.6.3",
            "--transport", "stdio",
            "--include-tools",
            "get_sheet_data,get_sheet_formulas,list_sheets,update_cells,batch_update,"
            "create_spreadsheet,copy_sheet",
        ])
        env = observed["env"]
        self.assertEqual(env["CREDENTIALS_CONFIG"], "")
        self.assertEqual(env["SERVICE_ACCOUNT_PATH"], "")
        self.assertEqual(env["GOOGLE_APPLICATION_CREDENTIALS"], os.devnull)
        self.assertEqual(env["DRIVE_FOLDER_ID"], "")
        self.assertEqual(env["CREDENTIALS_PATH"], str((self.client_dir / "client.json").resolve()))
        token = self.home / ".local/state/mcp-google-sheets/personal/token.json"
        self.assertEqual(env["TOKEN_PATH"], str(token.resolve()))
        self.assertEqual(token.parent.stat().st_mode & 0o777, 0o700)

    def test_missing_and_malformed_oauth_fail_without_uvx(self):
        client = self.client_dir / "client.json"
        original = client.read_text()
        client.unlink()
        result = self.run_launcher()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn(str(client), result.stderr)
        for invalid in (
            '{"web": {"client_id": "wrong"}}', '{"installed": null}',
            '{"installed": []}', '{"installed": "secret-sentinel"}', '{broken',
            '{"installed": {"client_id": "id", "client_secret": "secret-sentinel"}}',
        ):
            client.write_text(invalid)
            result = self.run_launcher()
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn(str(client), result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertNotIn("secret-sentinel", result.stderr)
        client.write_text(original)

    def test_work_directory_and_symlink_rejected(self):
        work = self.home / "projects/work/private"
        work.mkdir(parents=True)
        link = self.base / "work-link"
        link.symlink_to(work)
        for target in (work, link):
            result = self.run_launcher(target)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")

    def test_existing_token_permissions_are_restricted(self):
        token = self.home / ".local/state/mcp-google-sheets/personal/token.json"
        token.parent.mkdir(parents=True)
        token.parent.chmod(0o755)
        token.write_text("fixture-token")
        token.chmod(0o644)
        result = self.run_launcher()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(token.parent.stat().st_mode & 0o777, 0o700)
        self.assertEqual(token.stat().st_mode & 0o777, 0o600)
        self.assertEqual(token.read_text(), "fixture-token")

    @unittest.skipUnless(os.environ.get("MCP_SHEETS_PACKAGE_CHECK") == "1",
                        "opt-in package contract check")
    def test_upstream_honors_authentication_paths_and_tool_filter(self):
        observed = json.loads(self.run_launcher().stdout)
        # Inspect the installed package without starting its OAuth lifespan or contacting Google.
        check = """
import asyncio, os
from unittest.mock import patch
import google.auth
from google.auth.exceptions import DefaultCredentialsError
from mcp_google_sheets import server
assert server.CREDENTIALS_CONFIG == ''
assert server.SERVICE_ACCOUNT_PATH == ''
assert server.CREDENTIALS_PATH == os.environ['CREDENTIALS_PATH']
assert server.TOKEN_PATH == os.environ['TOKEN_PATH']
assert server.DRIVE_FOLDER_ID == ''
expected = {'get_sheet_data', 'get_sheet_formulas', 'list_sheets', 'update_cells',
            'batch_update', 'create_spreadsheet', 'copy_sheet'}
assert server.ENABLED_TOOLS == expected
assert {tool.name for tool in asyncio.run(server.mcp.list_tools())} == expected
with patch('socket.socket.connect', side_effect=AssertionError('network forbidden')):
    try:
        google.auth.default(scopes=server.SCOPES)
    except DefaultCredentialsError:
        pass
    else:
        raise AssertionError('ADC must fail with explicit null-file credentials')
"""
        result = subprocess.run(
            [shutil.which("uvx"), *observed["args"][:4], "--from", observed["args"][4],
              "python", "-c", check, *observed["args"][5:]],
            cwd=self.cwd, env=observed["env"], capture_output=True, text=True, timeout=180,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_exit_code_propagates(self):
        self.env["FAKE_EXIT"] = "23"
        self.assertEqual(self.run_launcher().returncode, 23)

    def test_project_configuration_does_not_shadow_the_local_server(self):
        for relative in (".pi/mcp.json", ".mcp.json"):
            config = ROOT / relative
            if config.exists():
                servers = json.loads(config.read_text()).get("mcpServers", {})
                self.assertNotIn("google-sheets-personal", servers, relative)

    def test_manifest_and_dotbot_launcher_link(self):
        manifest = json.loads((ROOT / "home/.agents/mcp.json").read_text())
        server = manifest["mcpServers"]["google-sheets-personal"]
        self.assertEqual(server["command"], "google-sheets-personal-mcp")
        self.assertIn("context7", manifest["mcpServers"])
        config = (ROOT / "install.conf.yaml").read_text()
        self.assertIn(
            "~/.local/bin/google-sheets-personal-mcp: home/.local/bin/google-sheets-personal-mcp",
            config,
        )


if __name__ == "__main__":
    unittest.main()
