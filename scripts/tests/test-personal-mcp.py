"""Check personal MCP linking and native registration in disposable homes."""

import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "scripts/update-coding-agents/sync-personal-mcp.py"
SERVER = {"command": "npx", "args": ["-y", "example-mcp@1.0.0"]}


class PersonalMcpTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="personal-mcp-")
        self.addCleanup(self.scratch.cleanup)
        self.home = Path(self.scratch.name)
        (self.home / ".agents").mkdir()
        self.source = self.home / ".agents/mcp.json"
        self.source.write_text(json.dumps({"mcpServers": {"context7": SERVER}}))
        self.registry = self.home / ".claude.json"
        self.initial = {
            "mcpServers": {"unrelated": {"command": "private-tool"}},
            "projects": {"/private/work": {"mcpServers": {"work-only": {"url": "private"}}}},
            "privateState": "preserve-this",
        }
        self.registry.write_text(json.dumps(self.initial))
        binary_dir = self.home / "bin"
        binary_dir.mkdir()
        fake = binary_dir / "claude"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\nfrom pathlib import Path\n"
            "home = Path.home()\n"
            "with (home / 'calls.jsonl').open('a') as out:\n"
            " out.write(json.dumps({'args': sys.argv[1:], "
            "'alternate': os.environ.get('CLAUDE_CONFIG_DIR')}) + '\\n')\n"
            "if os.environ.get('MCP_EXIT'): sys.exit(int(os.environ['MCP_EXIT']))\n"
            "assert sys.argv[1:5] == ['mcp', 'add-json', '--scope', 'user']\n"
            "registry = home / '.claude.json'\n"
            "settings = json.loads(registry.read_text()) if registry.exists() else {}\n"
            "servers = settings.setdefault('mcpServers', {})\n"
            "name, config = sys.argv[5:7]\n"
            "if name in servers: sys.exit(4)\n"
            "servers[name] = json.loads(config)\n"
            "registry.write_text(json.dumps(settings))\n"
        )
        fake.chmod(0o755)
        self.env = dict(
            os.environ, HOME=str(self.home),
            PATH=f"{binary_dir}:{os.environ['PATH']}", CLAUDE_CONFIG_DIR="/unused/trial",
        )

    def run_adapter(self):
        return subprocess.run(
            [sys.executable, str(ADAPTER)], env=self.env, cwd=self.home,
            capture_output=True, text=True,
        )

    def calls(self):
        captured = self.home / "calls.jsonl"
        return [json.loads(line) for line in captured.read_text().splitlines()] \
            if captured.exists() else []

    def test_adds_missing_user_server_and_preserves_other_state(self):
        result = self.run_adapter()
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = json.loads(json.dumps(self.initial))
        expected["mcpServers"]["context7"] = SERVER
        self.assertEqual(json.loads(self.registry.read_text()), expected)
        self.assertEqual(len(self.calls()), 1)
        self.assertIsNone(self.calls()[0]["alternate"])

    def test_second_run_is_noop_and_explicit_stdio_type_matches(self):
        self.initial["mcpServers"]["context7"] = {**SERVER, "type": "stdio", "env": {}}
        self.registry.write_text(json.dumps(self.initial))
        before = self.registry.read_bytes()
        for _ in range(2):
            result = self.run_adapter()
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.registry.read_bytes(), before)
        self.assertEqual(self.calls(), [])

    def test_conflict_fails_before_registering_any_servers(self):
        self.source.write_text(json.dumps({"mcpServers": {
            "missing": SERVER, "unrelated": SERVER,
        }}))
        before = self.registry.read_bytes()
        result = self.run_adapter()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflict", result.stderr.lower())
        self.assertEqual(self.registry.read_bytes(), before)
        self.assertEqual(self.calls(), [])

    def test_malformed_manifest_fails_without_native_calls(self):
        for manifest in (
            {"mcpServers": []}, {"mcpServers": {"--bad": SERVER}},
            {"mcpServers": {"context7": "not-a-config"}},
            {"mcpServers": {"context7": {"type": "sse", "url": "https://example.com"}}},
        ):
            self.source.write_text(json.dumps(manifest))
            self.assertNotEqual(self.run_adapter().returncode, 0)
            self.assertEqual(self.calls(), [])

    def test_native_failure_propagates_without_registry_changes(self):
        self.env["MCP_EXIT"] = "23"
        before = self.registry.read_bytes()
        result = self.run_adapter()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("23", result.stderr)
        self.assertEqual(self.registry.read_bytes(), before)

    @unittest.skipUnless(os.environ.get("MCP_NATIVE_CHECK") == "1", "opt-in native CLI check")
    def test_native_concurrent_adds_preserve_unrelated_records(self):
        native = shutil.which("claude")
        self.assertIsNotNone(native)
        environment = dict(os.environ, HOME=str(self.home))
        environment.pop("CLAUDE_CONFIG_DIR", None)
        children = []
        try:
            for name in ("fixture-a", "fixture-b"):
                children.append(subprocess.Popen(
                    [
                        native, "mcp", "add-json", "--scope", "user", name,
                        json.dumps({"command": "fixture-only-no-server-start"}),
                    ],
                    cwd=self.home, env=environment,
                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
                ))
            for child in children:
                _, error = child.communicate(timeout=30)
                self.assertEqual(child.returncode, 0, error)
        finally:
            for child in children:
                if child.poll() is None:
                    child.kill()
                    child.communicate()
        observed = json.loads(self.registry.read_text())
        self.assertEqual(observed["projects"], self.initial["projects"])
        self.assertEqual(observed["privateState"], self.initial["privateState"])
        self.assertEqual(
            observed["mcpServers"]["unrelated"], self.initial["mcpServers"]["unrelated"]
        )
        for name in ("fixture-a", "fixture-b"):
            self.assertEqual(
                observed["mcpServers"][name]["command"], "fixture-only-no-server-start"
            )

    def test_dotbot_links_one_canonical_definition(self):
        result = subprocess.run(
            [
                sys.executable, str(ROOT / "dotbot/bin/dotbot"), "-d", str(ROOT),
                "-c", str(ROOT / "install.conf.yaml"), "--only", "create", "link",
            ],
            env=self.env, check=True, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)
        source = ROOT / "home/.agents/mcp.json"
        for relative in (".agents/mcp.json", ".pi/agent/mcp.json", ".cursor/mcp.json"):
            self.assertEqual((self.home / relative).resolve(), source)
        self.assertEqual(json.loads(self.registry.read_text()), self.initial)


if __name__ == "__main__":
    unittest.main()
