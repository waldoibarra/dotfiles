# Agent instructions

Read [Coding agents](/docs/coding-agents.md) before choosing which tracked file to edit.
Restart agents after changing loaded instructions, then check the active session's context.
A file or symlink on disk does not prove that an agent loaded it.

## Global rules

[`home/.agents/AGENTS.md`](/home/.agents/AGENTS.md) owns shared preferences. Dotbot links it to
`~/.agents/AGENTS.md` and each agent's global path. Keep it usable across projects;
repository-specific rules belong in the root [`AGENTS.md`](/AGENTS.md).

| Agent | Global loader |
| --- | --- |
| Claude Code | Copied `~/.claude/CLAUDE.md` imports `@~/.agents/AGENTS.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` links to the tracked source |
| Codex | `~/.codex/AGENTS.md` links to the tracked source |
| Oh My Pi (`omp`) | `~/.omp/agent/AGENTS.md` links to the tracked source |

Claude Code has no user-level `AGENTS.md`. Keep its adapter's one-line import and edit shared
rules in the source `AGENTS.md`. The adapter is user-level, not a repository wrapper.
Leave `~/.codex/AGENTS.override.md` absent unless you intend to replace Codex's global rules.

Codex is installed only to sign in to the OpenAI subscription so OpenUsage can read its auth
token. It is not used for coding. Its instruction link exists for consistency, and its
[RTK hook](/docs/agent-integrations.md#rtk) is pre-installed in case that changes.
No skills are configured for it.

## OMP personal instructions

OMP loads one user-level context file from the highest-priority source: `~/.omp/agent/`, then
`~/.claude/`, then `~/.agents/`. The explicit OMP link makes the shared source load once.

For the default profile, `~/.omp/agent/APPEND_SYSTEM.md` links to the machine-local `~/AGENTS.md`,
which must already exist. Append text has no file-path wrapper; keep `~/AGENTS.md` in its heading
to identify the source in session context. A project append file or `--append-system-prompt`
can override it.

These rules apply to the coding session. Read [OMP live voice](/docs/omp-live-voice.md) before
diagnosing missing personal instructions in `/live`.

## Project rules

This repository uses root `AGENTS.md` without a root `CLAUDE.md` wrapper. The user-level Claude
import remains separate. [`.claude/settings.json`](/.claude/settings.json) excludes
`**/home/.claude/CLAUDE.md` from project discovery so the tracked adapter does not load again
as local guidance.

OMP skips standalone context files whose parent directory starts with `.`. Because this checkout
is named `.dotfiles`, [`.omp/AGENTS.md`](/.omp/AGENTS.md) links to `../AGENTS.md` for native discovery.
The root file remains the single source; the relative link also works in other checkout locations.

Codex and OpenCode read `AGENTS.md` along the path to their working directory. OMP also reads
`.agents/AGENTS.md` there. Working inside `home/` or `home/.agents/` can therefore load the
tracked global source again. OpenCode's `instructions` setting is additive, with no exclusion
configured here for that source. Check loaded context instead of assuming deduplication.

## Claude response styles

Claude Code defaults to `Spartan` through
[`home/.claude/settings.json`](/home/.claude/settings.json). `/output-style` selects a style;
change the tracked `outputStyle` to preserve a global default across updater runs.
Project-local settings can override it.

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
