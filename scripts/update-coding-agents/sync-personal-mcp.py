#!/usr/bin/env python3
"""Register canonical personal MCP servers with Claude Code without editing its registry."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def load_json(file_path, label):
    try:
        with file_path.open(encoding="utf-8") as source_file:
            return json.load(source_file)
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Cannot read {label} {file_path}: {error}")


def normalize(config):
    normalized = dict(config)
    if normalized.get("type", "stdio") == "stdio":
        normalized.pop("type", None)
        if normalized.get("args") == []:
            normalized.pop("args")
        if normalized.get("env") == {}:
            normalized.pop("env")
    return normalized


def validate_servers(manifest):
    servers = manifest.get("mcpServers") if isinstance(manifest, dict) else None
    if not isinstance(servers, dict):
        fail("Invalid personal MCP manifest: top-level mcpServers must be an object")
    for name, config in servers.items():
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
            fail(f"Invalid personal MCP server name: {name!r}")
        if not isinstance(config, dict):
            fail(f"Invalid configuration for MCP server {name}: expected an object")
        kind = config.get("type", "stdio")
        if kind == "stdio":
            if not isinstance(config.get("command"), str) or not config["command"]:
                fail(f"Invalid stdio configuration for MCP server {name}: command is required")
            if "args" in config and (not isinstance(config["args"], list) or
                                      not all(isinstance(arg, str) for arg in config["args"])):
                fail(f"Invalid stdio configuration for MCP server {name}: args must be strings")
            if "env" in config and (not isinstance(config["env"], dict) or
                                    not all(isinstance(key, str) and isinstance(value, str)
                                            for key, value in config["env"].items())):
                fail(f"Invalid stdio configuration for MCP server {name}: env must contain strings")
        elif kind in ("http", "streamable-http"):
            if not isinstance(config.get("url"), str) or not config["url"]:
                fail(f"Invalid {kind} configuration for MCP server {name}: url is required")
        else:
            fail(f"Invalid configuration for MCP server {name}: unsupported type {kind!r}")
    return servers


def main():
    home = Path.home()
    servers = validate_servers(load_json(home / ".agents/mcp.json", "personal MCP manifest"))
    registry_path = home / ".claude.json"
    registry = load_json(registry_path, "Claude registry") if registry_path.exists() else {}
    if not isinstance(registry, dict):
        fail(f"Invalid Claude registry {registry_path}: expected an object")
    installed = registry.get("mcpServers", {})
    if not isinstance(installed, dict):
        fail(f"Invalid Claude registry {registry_path}: mcpServers must be an object")

    missing = []
    for name, config in servers.items():
        if name not in installed:
            missing.append((name, config))
        elif (not isinstance(installed[name], dict)
              or normalize(installed[name]) != normalize(config)):
            fail(f"MCP server conflict for {name}; inspect the Claude user entry manually")

    environment = os.environ.copy()
    environment.pop("CLAUDE_CONFIG_DIR", None)
    for name, config in missing:
        command = [
            "claude", "mcp", "add-json", "--scope", "user", name, json.dumps(config)
        ]
        try:
            result = subprocess.run(command, cwd=home, env=environment,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    check=False)
        except OSError as error:
            fail(f"Could not register MCP server {name}: {error}")
        if result.returncode:
            fail(f"Failed to register MCP server {name} (exit code {result.returncode})")
    print(f"Personal MCP: {len(missing)} registered; {len(servers) - len(missing)} unchanged.")


if __name__ == "__main__":
    main()
