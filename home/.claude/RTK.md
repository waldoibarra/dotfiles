# RTK

RTK filters supported command output and records usage statistics. Savings depend on the
command and output; use local analytics rather than assuming a fixed percentage.

## Commands

Call these directly:

```sh
rtk gain              # Recorded token-savings summary
rtk gain --history    # Recent command history
rtk gain --daily      # Daily breakdown
rtk gain --weekly     # Weekly breakdown
rtk discover          # Missed opportunities in this project's Claude Code history
rtk proxy <command>   # Run without filtering; still records usage
```

`rtk discover --all` scans all projects. Read the installed command's `--help` for other options.
`rtk proxy` executes the supplied command with its normal side effects; it is not a dry run.

## Agent integration

The tracked Claude Code settings register `rtk hook claude` for `PreToolUse` on `Bash`.
The coding-agent updater refreshes OpenCode's machine-local plugin with `rtk init -g --opencode`.
These integrations rewrite supported commands, such as `git status` to `rtk git status`;
they do not wrap every command or every tool call. Other agents need their own integration.

To inspect support without executing a command, use `rtk rewrite "git status"` and inspect the
printed rewrite. This checks RTK's mapping, not whether an agent loaded its hook or plugin.

This reference is maintained in dotfiles and linked to `~/.claude/RTK.md`. Running `rtk init`
can change installed integration files; it is not a read-only configuration check.
