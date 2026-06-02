# Coding Agents

Configuration files for Claude Code and OpenCode are tracked in this repo and symlinked into
`$HOME` via Dotbot.

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
