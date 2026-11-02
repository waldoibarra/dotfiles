# Agent coordination

**Run, name, brief, and read agents across Claude Code and Pi from one terminal.**
Herdr is the current terminal backend; the purpose, names, and briefs would survive replacing it.
These pages own the procedures and conventions.
The [shared orchestration
reference](/home/.agents/references/orchestration.md#coordinate-across-harnesses)
owns the coordination rules and approval boundaries; nothing here restates them.
[Agent integrations](/docs/agent-integrations.md#herdr) owns installation and state-reporting
diagnosis.

Read `herdr --skill` before any control command. The skill file is Herdr's own contract.

## Choose a task

| Need | Read |
| --- | --- |
| See every live agent in one table, or a filtered subset | [List agents](listing.md) |
| Pick or change an agent's name, or label a tab or workspace | [Name agents, tabs, and workspaces](naming.md) |
| Start a worker in a disposable workspace, or close one | [Spawn and close a worker](spawning.md) |
| Write the first message a worker receives | [Brief a worker](briefing.md) |
| Fix state reporting or hooks | [Agent integrations](/docs/agent-integrations.md#herdr) |

## How it fits

Herdr hosts one agent per pane and reports its lifecycle state: idle, working, blocked, or unknown.
A lead session talks to other agents through `herdr agent` commands, never through raw pane input.
Workers reply the same way. Chat output in a worker's own pane reaches nobody.
Every command in these pages was exercised on 2026-11-01 with Herdr 0.9.5 unless a step says
"inspected".

**Relation to firstmate.** The spawning convention mirrors firstmate's one-task container, one
workspace with one tab and one pane per worker. Adopting firstmate replaces [spawning](spawning.md)
and [briefing](briefing.md) with its own scripts and task records; naming and listing stay ours.
Read the [glossary](/GLOSSARY.md#agent-coordination) for the role names both setups share.
