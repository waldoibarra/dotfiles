# List agents

Back to [agent coordination](README.md).

**Default output when someone asks for the agents, peers, workers, or sessions.**
The `agents` alias runs [list-agents.py](/scripts/list-agents.py) through `uv`, which supplies
the `rich` renderer. On a terminal the table renders as Markdown; piped, it prints raw Markdown
for agents to paste. `--md` forces raw Markdown.

```sh
agents                                   # everyone
agents astra                             # rows containing "astra" anywhere
agents royalytics idle                   # every word must match
agents --here                            # directory is the current one or inside it
uv run --quiet --script ~/.dotfiles/scripts/list-agents.py   # when the alias is not loaded
```

When the operator asks for a subset, such as "the idle Pi agents" or "agents on ROY-92", pass
the words as filters rather than pruning the table by hand.

| Workspace | Tab | Pane | Agent | Directory | Description |
| --- | --- | --- | --- | --- | --- |
| Royalytics | ROY-92 | `roy-92-astra` | pi, gpt-6-astra | `~/work/…` | idle. Last line. |

- Pane shows the agent name, or the pane ID when the agent is unnamed.
- Agent is the harness plus the model when the pane footer shows one. Claude Code shows no model.
- Description is the last substantive screen line. Herdr stores no description field.
- Workspaces without recognized agents are omitted. Plain shells are not agents.
