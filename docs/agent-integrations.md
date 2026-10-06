# Agent integrations

Read [Coding agents](/docs/coding-agents.md) before editing tracked settings, and
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running the updater.
Keep machine-local hooks, plugins and service configuration outside the repository.

## RTK

Read the [RTK command reference](/home/.claude/RTK.md) before using or diagnosing RTK.
The shared global instructions load that reference on demand.

| Agent | Integration and owner |
| --- | --- |
| Claude Code | Tracked Bash hook runs `rtk hook claude`. |
| OpenCode | Updater refreshes the untracked, RTK-generated plugin with `rtk init -g --opencode`. |
| OMP | If `omp` exists, updater refreshes `~/.omp/agent/extensions/rtk.ts` with `rtk init -g --agent omp`. |
| Codex | Tracked [`home/.codex/hooks.json`](/home/.codex/hooks.json) runs `rtk hook codex`; Dotbot links it to `~/.codex/hooks.json`. |
| Pi (`pi`) | Not configured. |

The updater refreshes the OpenCode and OMP files only when dry runs list pending
`[dry-run] would …` changes. Dry runs always print `Nothing written`; that line does not mean
an integration is current. A failed RTK step warns and lets the remaining updater steps run.

Do not run `rtk init -g --codex`: it appends an `@RTK.md` reference to `~/.codex/AGENTS.md`,
which links to the shared global instructions. Codex 0.160.1 loads the symlinked hook file,
but commands run without RTK until the non-managed hook is trusted through `/hooks`.
Trust is required once per machine and again after an edit changes the hook's hash.

The tracked RTK config enables usage tracking and telemetry, and keeps tee output for failures.
`filters.toml` contains a commented example, not an active custom filter. Neither a configured
hook nor a supported rewrite proves a live session used it.

## Herdr

When Herdr is available, the updater checks `herdr integration status` and installs stale or
missing Claude and OpenCode integrations. The binary owns the untracked scripts and plugins.
Claude's tracked `SessionStart` hook uses `$HOME/.claude/hooks/herdr-agent-state.sh`.

Herdr can add an absolute-path duplicate hook to the installed Claude settings copy. The next
updater run resets it from the tracked source. If Herdr changes the hook command, review the
installed entry and port it into the tracked `$HOME` form.

## Moshi

Tracked Claude settings call `'/opt/homebrew/bin/moshi-hook' claude-hook`, which assumes
Homebrew's Apple Silicon prefix. Moshi's OpenCode plugin and daemon/LaunchAgent are machine-local;
the coding-agent updater does not install them. `moshi-hook install --target opencode` owns the plugin.

For daemon failures, inspect the service environment: launchd does not inherit the interactive
shell's mise PATH.
