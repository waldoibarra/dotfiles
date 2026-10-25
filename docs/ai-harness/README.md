# AI harness

**Use shared instructions and skills across coding clients without duplicating their policy.**
Pi, Claude Code, and Cursor retain native settings, permissions, credentials, and session state.
Worker support and instruction delivery differ between clients.

Start with [session workflow](session-workflow.md) to direct work, approve changes, and review
results.
For a new workstation, follow [setup](/docs/setup.md) before configuring clients.

## How the pieces fit

| Layer | Responsibility | Owner |
| --- | --- | --- |
| Global instructions | Shared boundaries and task-based reading routes | [Agent instructions](/docs/agent-instructions.md) |
| References | On-demand communication, coordination, and integration guidance | [Shared references](/home/.agents/references) |
| Skills | Specialist procedures and verification | [Agent skills](/docs/agent-skills.md) |
| Roles | Bounded worker responsibilities; the lead retains decisions and Git delivery | [Role selection](/home/.agents/references/delegation.md) |
| Native configuration | Client mechanics, tools, and runtime state | [Configuration and delivery](configuration.md) |

Read [architecture](/docs/architecture.md) before changing configuration, project knowledge, or
shared-memory ownership.
These guides describe workstation maintenance; portable runtime instructions have their own
installed reading routes.

## Choose a task

| Need | Guide |
| --- | --- |
| Start, direct, or close a session | [Session workflow](session-workflow.md) |
| Improve prompts or clarify a request | [Prompting](/docs/prompting.md) |
| Change shared rules or personal instruction loading | [Agent instructions](/docs/agent-instructions.md) |
| Configure Pi or use subscription voice | [Pi and live voice](pi/README.md) |
| Delegate with an explicit role and model | [Pi delegation](pi/delegation.md) |
| Configure personal MCP servers | [Personal MCP servers](mcp.md) |
| Install or maintain skills | [Agent skills](/docs/agent-skills.md) |
| Plan and deliver a durable change | [OpenSpec integration](openspec.md) |
| Check delivery, loading, or behavior | [Harness verification](harness-verification.md) |
| Maintain writing profiles | [Ghostwriter profiles](ghostwriter.md) |
| Diagnose RTK, Herdr, Moshi, or Lens | [Agent integrations](/docs/agent-integrations.md) |
| Configure design tools | [UI design tools](/docs/agent-ui-design-tools.md) |
| Compare personal and work behavior | [Work harness parity](work-parity.md) |

## File ownership

**Edit tracked sources under `home/`, not installed copies.**
Follow [configuration ownership](configuration.md#file-ownership) for links, managed copies, and
rendered files.
Linked-file edits also change the repository; credentials and runtime state remain client-local.

**Publication risk:** `just update-ca`, and therefore `just sync`, can commit and push a changed
skill lockfile, publishing other unpushed commits on the branch too. Read
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running either.

## Copy-managed files

[Claude settings delivery](configuration.md#copy-managed-files) explains replacement behavior and
machine-local hooks.

## Cursor global instructions

[Cursor rendering](configuration.md#cursor-global-instructions) explains the template, targeted
refresh, and verification limits.

## Ghostwriter voice

[Ghostwriter profiles](ghostwriter.md) owns audience routing, linked files, and private-sample
boundaries.
