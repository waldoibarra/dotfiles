# Coding Agents

This is a dotfiles repo — its primary purpose is managing configuration files for the current
machine. The global configuration files for Claude Code and OpenCode are tracked here and symlinked
into `$HOME` via DotBot, the same way every other dotfile is.

## Tracked files

| Tool | Repo path | `$HOME` path |
| --- | --- | --- |
| Claude Code | `home/.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Claude Code | `home/.claude/settings.json` | `~/.claude/settings.json` |
| OpenCode | `home/.config/opencode/AGENTS.md` | `~/.config/opencode/AGENTS.md` |
| OpenCode | `home/.config/opencode/opencode.json` | `~/.config/opencode/opencode.json` |
| OpenCode | `home/.config/opencode/tui.json` | `~/.config/opencode/tui.json` |

## Keeping prompts in sync

[`CLAUDE.md`](/home/.claude/CLAUDE.md) and [`AGENTS.md`](/home/.config/opencode/AGENTS.md) are
effectively the same prompt — any change to one must be mirrored to the other. The only intentional
difference is the contextual skills loading section: each tool references available skills differently
based on its own system prompt format.

## Local project instructions

Like any other repo, this dotfiles repo has its own local agent instruction files:

- [`AGENTS.md`](/AGENTS.md) — the source of truth for both tools, committed to the repo.
- [`CLAUDE.md`](/CLAUDE.md) — a symlink to `AGENTS.md`, gitignored, created by [`scripts/setup-repo.sh`](/scripts/setup-repo.sh).

Claude Code picks up `CLAUDE.md` and OpenCode picks up `AGENTS.md` automatically at the project
root. Both point to the same content via the symlink.

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
