# Coding Agents

This is a dotfiles repo — its primary purpose is managing configuration files for the current
machine. The global configuration files for Claude Code and OpenCode are tracked here and symlinked
into `$HOME` via DotBot, the same way every other dotfile is.

## Tracked files

| Tool | Repo path | `$HOME` path |
| --- | --- | --- |
| Claude Code | `home/.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Claude Code | `home/.claude/settings.json` | `~/.claude/settings.json` |
| Claude Code | `home/.claude/statusline.sh` | `~/.claude/statusline.sh` |
| OpenCode | `home/.config/opencode/AGENTS.md` | `~/.config/opencode/AGENTS.md` |
| OpenCode | `home/.config/opencode/opencode.json` | `~/.config/opencode/opencode.json` |
| OpenCode | `home/.config/opencode/tui.json` | `~/.config/opencode/tui.json` |
| RTK | `home/.claude/RTK.md` | `~/.claude/RTK.md` |
| RTK | `home/.config/rtk/config.toml` | `~/Library/Application Support/rtk/config.toml` (macOS), `~/.config/rtk/config.toml` (Linux) |
| RTK | `home/.config/rtk/filters.toml` | same pattern as `config.toml` |

## RTK integration

`RTK.md` is placed in `~/.claude/` by `rtk init -g` because RTK injects context only into Claude
Code. Both `CLAUDE.md` and `AGENTS.md` reference `~/.claude/RTK.md` directly, so OpenCode also
benefits from the same file without duplicating it.

`RTK.md` is maintained manually — its content may diverge from what `rtk init -g` generates by
default.

The OpenCode plugin (`~/.config/opencode/plugins/rtk.ts`) is intentionally not tracked in the
table above. RTK embeds the plugin at compile time and is the authoritative source for the correct
version. It is installed and kept current by `rtk init -g --opencode`, which runs automatically
via `update-coding-agents/entrypoint.sh` on every `just sync`.

## Global skills lockfile

`scripts/update-coding-agents/sync-global-skills-from-lock.sh` keeps globally installed Claude Code
/ OpenCode skills in sync with [`home/.agents/.skill-lock.json`](/home/.agents/.skill-lock.json): it
installs any skill listed there that isn't already present, runs `npx skills update -g` to update
all of them, then **commits and pushes the lockfile to the repo's remote** if the update changed its
content. It runs automatically via `update-coding-agents/entrypoint.sh` on every `just sync`.

## Repo-managed skills

Most global skills are installed and pinned by the lockfile (see [Global skills
lockfile](#global-skills-lockfile)). Two skills are instead **authored as source**
in the repo and edited here directly — never installed, never in the lockfile:

| Skill | Repo source | Symlinked to |
| --- | --- | --- |
| [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) | `home/.agents/skills/shell-scripting` | `~/.agents/skills/` **and** `~/.claude/skills/` (shared source via two Dotbot globs) |
| [`non-vision-image-reader`](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) | `home/.config/opencode/skills/non-vision-image-reader` | `~/.config/opencode/skills/` (opencode global skills) |

Dotbot relinks these on every `just sync`, so edits in the repo are picked up
once the tool reloads its config (restart opencode / Claude Code). Because they
are symlink targets, **never edit them under `~/.agents/skills/`,
`~/.claude/skills/`, or `~/.config/opencode/skills/`** — always edit the repo
source under `home/`.

## Global instructions

[`AGENTS.md`](/home/.config/opencode/AGENTS.md) is the single source of truth for global
instructions. [`CLAUDE.md`](/home/.claude/CLAUDE.md) is a one-line `@`-import of it:

```md
@~/.config/opencode/AGENTS.md
```

This is the [pattern Claude Code recommends](https://code.claude.com/docs/en/memory.md#import-additional-files)
for repos that keep instructions in `AGENTS.md`. Edit `AGENTS.md` only — `CLAUDE.md` auto-imports
it, so there is nothing to mirror.

## Local project instructions

Like any other repo, this dotfiles repo has its own local agent instruction files:

- [`AGENTS.md`](/AGENTS.md) — the source of truth for both tools, committed to the repo.
- [`CLAUDE.md`](/CLAUDE.md) — a committed file that uses Claude Code's `@`-include syntax (`@AGENTS.md`)
  to pull in the full content of `AGENTS.md` at load time.

Claude Code picks up `CLAUDE.md` (which includes `AGENTS.md` via `@`).
OpenCode picks up `AGENTS.md` directly. `AGENTS.md` remains the single source of truth.

## Preventing double-injection of global instruction files

The global instruction files tracked in this repo —
[`home/.claude/CLAUDE.md`](/home/.claude/CLAUDE.md) and
[`home/.config/opencode/AGENTS.md`](/home/.config/opencode/AGENTS.md) — live
inside the project tree. Without exclusion, both tools load them **twice**: once
as the global instruction file (via the symlink to `$HOME`) and again as a
project-level file discovered by traversing the repo.

### Claude Code

Claude Code solves this with `claudeMdExcludes` in the project-level
[`.claude/settings.json`](/.claude/settings.json):

```json
{
  "claudeMdExcludes": [
    "**/home/.claude/CLAUDE.md"
  ]
}
```

This prevents the global `CLAUDE.md` source file from being injected as a
project-level instruction when working in this repo.

### OpenCode

OpenCode has **no equivalent** of `claudeMdExcludes`. The `instructions` field in
`opencode.json` is additive only — it cannot suppress the default `AGENTS.md`
discovery. Feature requests have been filed repeatedly and consistently closed as
"not planned" ([#17990](https://github.com/anomalyco/opencode/issues/17990),
[#31697](https://github.com/anomalyco/opencode/issues/31697)); community PRs to
implement exclusion
([#17980](https://github.com/anomalyco/opencode/pull/17980),
[#20784](https://github.com/anomalyco/opencode/pull/20784)) were abandoned.

Until an exclusion mechanism lands upstream, `home/.config/opencode/AGENTS.md`
will be double-injected when working in this repo. A potential workaround would
be a plugin using the `experimental.chat.system.transform` hook to strip the
duplicate at runtime, but this has not been implemented.

## How symlinks are managed

Dotbot uses glob patterns in `install.conf.yaml` to symlink every file inside each directory:

```yaml
~/.claude/:
  glob: true
  path: home/.claude/*
~/.config/opencode/:
  glob: true
  path: home/.config/opencode/*
```

Any new file added to `home/.claude/` or `home/.config/opencode/` will be automatically symlinked
on the next `just sync`.
