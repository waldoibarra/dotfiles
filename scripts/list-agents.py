#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich>=13"]
# ///
"""Print every live Herdr agent as one table.

Columns: workspace, tab, pane (agent name, or pane ID when unnamed), agent
(harness and model when the screen footer shows one), directory, last screen line.
On a terminal the Markdown table is rendered with rich; when piped it is raw Markdown, so
agents can paste it. `--md` forces raw Markdown.

Filters: every positional word must appear, case-insensitively, somewhere in a row;
`--here` keeps rows whose directory is the current directory or inside it.
Requires a running Herdr server, the `herdr` CLI, and `uv` for the rich dependency.
"""

import json
import pathlib
import re
import subprocess
import sys

HEADERS = ["Workspace", "Tab", "Pane", "Agent", "Directory", "Description"]

HOME = str(pathlib.Path.home())
MODEL_RE = re.compile(r"(gpt-[\w.-]+|claude-[\w.-]+|[a-z]+-\d[\w.-]*)")


def herdr(*args: str) -> dict:
    out = subprocess.run(["herdr", *args], capture_output=True, text=True, check=True).stdout
    return json.loads(out)["result"]


def tail_lines(target: str, lines: int = 12) -> list[str]:
    cmd = ["herdr", "agent", "read", target, "--source", "recent"]
    cmd += ["--lines", str(lines), "--format", "text"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def describe(agent: dict) -> tuple[str, str]:
    """Return (model, description) from the pane's recent screen lines."""
    lines = tail_lines(agent["pane_id"])
    model = ""
    for line in reversed(lines):
        match = MODEL_RE.search(line)
        if match and ("•" in line or "(sub)" in line or "model" in line.lower()):
            model = match.group(1)
            break
    chrome = ("↑", "~", "$", "─", "━")
    content = [l for l in lines if not l.startswith(chrome) and len(l) > 20]
    description = content[-1] if content else agent.get("terminal_title_stripped", "")
    return model, description[:110]


def keep(row: list[str], terms: list[str], here: bool) -> bool:
    text = " ".join(row).lower()
    if any(t not in text for t in terms):
        return False
    if here:
        cwd = str(pathlib.Path.cwd()).replace(HOME, "~")
        return row[4] == cwd or row[4].startswith(cwd + "/")
    return True


def main() -> None:
    args = sys.argv[1:]
    terms = [a.lower() for a in args if not a.startswith("--")]
    agents = herdr("agent", "list")["agents"]
    labels = {}
    for ws in {a["workspace_id"] for a in agents}:
        for tab in herdr("tab", "list", "--workspace", ws)["tabs"]:
            labels[tab["tab_id"]] = tab["label"]
        labels[ws] = next(
            w["label"] for w in herdr("workspace", "list")["workspaces"] if w["workspace_id"] == ws
        )
    rows = []
    for a in sorted(agents, key=lambda x: (x["workspace_id"], x["tab_id"])):
        model, description = describe(a)
        harness = a["agent"]
        if model:
            harness = f"{harness}, {model}"
        pane = a.get("name") or a["pane_id"]
        status = a["agent_status"] + (", focused" if a.get("focused") else "")
        cwd = a["cwd"].replace(HOME, "~")
        ws = labels.get(a["workspace_id"], a["workspace_id"])
        tab = labels.get(a["tab_id"], a["tab_id"])
        row = [ws, tab, pane, harness, cwd, f"{status}. {description}"]
        if keep(row, terms, "--here" in args):
            rows.append(row)
    text = markdown(rows)
    if "--md" in args or not sys.stdout.isatty():
        print(text)
        return
    from rich.console import Console
    from rich.markdown import Markdown

    Console().print(Markdown(text))


def markdown(rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(HEADERS) + " |", "| " + " | ".join("---" for _ in HEADERS) + " |"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]} | `{r[2]}` | {r[3]} | `{r[4]}` | {r[5]} |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
