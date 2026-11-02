# Agent coordination

**Run, name, brief, and read agents across Claude Code and Pi from one terminal.**
Herdr is the current terminal backend; the purpose, names, and briefs would survive replacing it.
This manual owns the procedures and conventions.
The [shared orchestration
reference](/home/.agents/references/orchestration.md#coordinate-across-harnesses)
owns the coordination rules and approval boundaries; nothing here restates them.
[Agent integrations](/docs/agent-integrations.md#herdr) owns installation and state-reporting
diagnosis.

Read `herdr --skill` before any control command. The skill file is Herdr's own contract.

## Choose a task

| Need | Read |
| --- | --- |
| See every live agent in one table | [List agents](#list-agents) |
| Pick or change an agent's name | [Name agents](#name-agents) |
| Start a worker in its own workspace | [Spawn a worker](#spawn-a-worker) |
| Write the assignment a worker receives | [Brief a worker](#brief-a-worker) |
| Fix state reporting or hooks | [Agent integrations](/docs/agent-integrations.md#herdr) |

## How it fits

Herdr hosts one agent per pane and reports its lifecycle state: idle, working, blocked, or unknown.
A lead session talks to other agents through `herdr agent` commands, never through raw pane input.
Workers reply the same way. Chat output in a worker's own pane reaches nobody.
Every command here was exercised on 2026-11-01 with Herdr 0.9.5 unless a step says "inspected".

## List agents

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

## Name agents

**Name every agent `<context>-<model>[-<role>]`.** Peers address a name, not a pane ID.
Pane IDs change occupants; a name follows the agent until it exits.

| Context | Source | Examples |
| --- | --- | --- |
| Linear issue | Issue key in the tab label | `roy-92-fable`, `roy-92-astra` |
| Repository without an issue | Directory name, shortened | `melodix-api-fable`, `kh-astra` |
| Learning or personal project | Topic slug | `info-arch-astra`, `life-fable` |
| Same model twice in one context | Add a role suffix | `kh-astra-docs`, `kh-astra-review` |

- Lowercase and hyphens only; Herdr accepts `[a-z][a-z0-9_-]{0,31}`.
- Always keep the model suffix (`fable`, `astra`, `opus`); it tells peers which harness answers.
- Add a role suffix only when context plus model would collide.
- Names are unique per Herdr server, so choose a specific context.

```sh
herdr agent rename <pane-or-name> roy-92-astra
herdr agent list   # the `name` field confirms it
```

## Spawn a worker

Use this when the operator asks to spawn a worker, an independent reviewer, or a peer agent.
Say "spawn a worker" or "spawn an independent reviewer"; add "with Astra" or "with Claude" to pick
the harness. Without a harness, use Pi, because a different model gives a more independent read.

**Each worker gets a disposable workspace holding one tab with one pane.** This mirrors
firstmate's one-task container, so adopting it later changes nothing. Split the lead's tab only
when the operator says "split", "beside me", or "in this tab".

Each layer answers one question, so the sidebar identifies the work without opening it:

| Layer | Question | Label | Example |
| --- | --- | --- | --- |
| Workspace | What task? | Task in two to four words, Title case | `Glossary proposal` |
| Tab | What role? | The glossary role, plus the deliverable when several | `Independent reviewer` |
| Agent and pane | Who? | The [agent name](#name-agents) | `harness-glossary-astra` |

1. Resolve the lead's own pane and name with `herdr agent list`.
2. Write the [brief](#brief-a-worker) to a file before starting the worker.
3. Create the workspace without taking focus, passing the worker's directory and the task label.
  The result's `root_pane.pane_id` and `tab.tab_id` are the new pane and tab.
4. Rename the tab to the role and the pane to the worker's name.
5. Start the worker under that name. Use `--kind claude` for Claude Code. Native agent flags go
  after `--`.
6. Wait for idle once, after start. Then send the first message, written with the
  [AIM template](/docs/prompting.md#prompt-template); a bare "read the brief at a path" is not a
  prompt. Never add `--wait`.
7. Do not wait again. The reply arrives as a prompt in the lead's session; a second wait blocks
  the lead while that message is already queued. Verify the reply's claims against files.
8. Close the worker's workspace once its deliverable is verified, unless the operator asked to
  keep it. Close only containers this lead created. Closing ends the agent; say so in the reply.

```sh
herdr workspace create --cwd <dir> --label "<Task label>" --no-focus                 # step 3
herdr tab rename <new-tab-id> "<Role>"                                               # step 4
herdr pane rename <new-pane-id> <name>
herdr agent start <name> --kind pi --pane <new-pane-id> --timeout 60000              # step 5
herdr agent wait <name> --until idle --timeout 60000                                 # step 6
herdr agent prompt <name> "$(cat <first-message-file>)"                              # step 6
herdr workspace close <new-workspace-id>                                             # step 8
```

On request, replace steps 3 and 4 with a split of the lead's pane; `pane.pane_id` is the new pane:

```sh
herdr pane split <lead-pane-id> --direction right --ratio 0.5 --cwd <dir> --no-focus
herdr pane close <new-pane-id>   # when finished
```

Workspace, tab, and pane creation, renames, and closes were exercised on 2026-11-01.
Starting an agent and sending prompts keep their usual approval boundaries.

## Brief a worker

**The first message to any agent follows the [prompting guide](/docs/prompting.md).** Its AIM
template names the actor, input, mission, actions, constraints, output, clarification, and
verification. Send that message itself; a path to a file is input, not a prompt. Save the message
under the session's scratch directory so it can be sent verbatim and kept as evidence.

```markdown
**Actor:** You are the worker `<name>`, an <role>. Your lead is `<lead-name>` (Herdr agent name).
**Reply:** `herdr agent prompt <lead-name> "<text>"` without `--wait`. Chat output reaches nobody.

## Mission
<Outcome> for <audience>. Why it matters in one sentence.

## Input
- Files and directories to read, with paths.
- The lead's draft or position to challenge, when one exists.

## Actions and constraints
- Allowed operations and tools. Directories that must not be edited.
- Sentences of at most 17 words. House conventions that apply.

## Output
Write `<path>` containing <format>. Answer first, then rationale and evidence.

## Clarification and verification
Ask the lead about missing information that would change the result. Name assumptions.
Support each major claim with a source the lead can open.

## Stop condition
When `<path>` exists, send one reply naming the path and the <n> most contested choices. Then stop.
```

- Mission, Output, and Stop condition are mandatory. Prune fields that cannot change the result.
- The lead closes the worker's workspace after verification; the stop condition ends the worker's
  turn, not its container.
- Keep approval boundaries explicit: a worker never gains the lead's Git, publication, or model
  authority.
- Reuse focused context for follow-ups; do not resend the whole history.
