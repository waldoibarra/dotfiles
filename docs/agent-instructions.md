# Agent instructions

Read [Coding agents](coding-agents/README.md) before choosing which tracked file to edit.
Restart agents after changing loaded instructions, then check the active session's context.
A file or symlink on disk does not prove that an agent loaded it.

## Global rules

[`home/.agents/AGENTS.md`](/home/.agents/AGENTS.md) owns shared preferences. Dotbot links it to
`~/.agents/AGENTS.md` and each agent's global path. Keep it usable across projects;
repository-specific rules belong in the root [`AGENTS.md`](/AGENTS.md).

Read the [harness design policy](/home/.agents/AGENTS.md#harness-design) before changing shared
configuration or adding a harness-specific adapter.

| Agent | Global loader |
| --- | --- |
| Claude Code | Copied `~/.claude/CLAUDE.md` imports `@~/.agents/AGENTS.md` |
| Pi (`pi`) | `~/.pi/agent/AGENTS.md` links to the tracked source |

Claude Code has no user-level `AGENTS.md`. Keep its adapter's one-line import and edit shared
rules in the source `AGENTS.md`. The adapter is user-level, not a repository wrapper.

**Cursor** support is planned, not configured. Cursor reads project `AGENTS.md` and
`.cursor/rules/*.mdc`; its user rules live in its settings UI.

## Pi personal instructions

Pi loads the linked global rules and walks ancestor directories for context files. Personal
`~/AGENTS.md` therefore applies to projects under `$HOME`. Projects elsewhere need their own
personal-context arrangement. Profile `AGENTS.override.md` takes priority over the linked global
file; project overrides affect only their directory's context.

Pi discovers `~/.agents/skills` natively. No shared instruction or skill copy is installed into a
second directory. These rules configure the coding agent, not the extension's separate voice
prompt; see [Pi and live voice](coding-agents/pi/README.md).

## Project rules

This repository uses root `AGENTS.md` without a root `CLAUDE.md` wrapper. The user-level Claude
import remains separate. [`.claude/settings.json`](/.claude/settings.json) excludes
`**/home/.claude/CLAUDE.md` from project discovery so the tracked adapter does not load again
as local guidance.

Pi reads `AGENTS.md` along the path to its working directory. Working inside `home/.agents/` can
therefore load the tracked global source twice. Check loaded context; do not assume deduplication.

## Shared role agents

[`home/.agents/roles/`](/home/.agents/roles) owns the five role prompts: `plan-reviewer`,
`code-auditor`, `implementer`, `browser-tester`, and `docs-writer`. Each file contains only
name/description frontmatter and shared instructions. Roles do not pin a provider or model.

Dotbot links each file into `~/.agents/roles/` and `~/.claude/agents/`; no prompts are copied
or generated. Claude Code inherits its session's model and tools unless dispatch overrides them.
Its reviewer restrictions are instructions, not enforced tool allowlists.

Pi uses `pi-subagents` with the shared directory configured as an additional scan root.
Pi-specific context inheritance and tool selection stay in Pi settings.
Read [Pi delegation](coding-agents/pi/delegation.md) before selecting roles/models or changing the runner.
The main session owns orchestration and Git writes; unsupported harnesses use the documented
sequential fallback, not a claimed independent review.

## Shared references

[`home/.agents/RTK.md`](/home/.agents/RTK.md) owns the RTK reference. Dotbot links it into
`~/.agents/RTK.md` and the compatibility path `~/.claude/RTK.md`.

## Claude response styles

Claude Code defaults to `Spartan` through
[`home/.claude/settings.json`](/home/.claude/settings.json). `/output-style` selects a style;
change the tracked `outputStyle` to preserve a global default across updater runs.
Project-local settings can override it.

A style shapes only the main Claude Code session's replies. The shared rules' **Communication**
section carries the writing rules to every harness, sub-agents and written artifacts included.
Keep writing rules there, not in a style.

The three tracked styles are verbatim [Attention Span](https://github.com/alexgreensh/attention-span)
copies, separate from the shared global rules:

| Style | Format |
| --- | --- |
| `Attention-kind` | Plain English, front-loaded, warm |
| `Spartan` | Blunt, compact arrow points |
| `Rundown` | TL;DR and status checklists |

Each retains `keep-coding-instructions: true` and upstream attribution. Compare its version comment
with [upstream releases](https://github.com/alexgreensh/attention-span/releases) before replacing it.
Preserve the [AGPL-3.0 license](https://github.com/alexgreensh/attention-span/blob/main/LICENSE);
this repository does not relicense the copies.
