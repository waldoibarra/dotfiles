# Agent integrations

Read [Coding agents](coding-agents/README.md) before editing tracked settings, and
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
| Pi (`pi`) | If `pi` exists, updater refreshes `~/.pi/agent/extensions/rtk.ts` with `rtk init -g --agent pi`. |

The updater refreshes the OpenCode, OMP and Pi files only when dry runs list pending
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

When Herdr is available, the updater checks `herdr integration status` and installs missing or
outdated integrations through `herdr integration install TARGET`. Herdr owns the generated files;
no custom hook implementation or checked-in extension copy is needed.

| Agent | Generated integration |
| --- | --- |
| Claude Code | `~/.claude/hooks/herdr-agent-state.sh`; tracked `SessionStart` hook uses the `$HOME` path. |
| OpenCode | `~/.config/opencode/plugins/herdr-agent-state.js`. |
| OMP | `~/.omp/agent/extensions/herdr-omp-agent-state.ts`. |
| Pi | `~/.pi/agent/extensions/herdr-agent-state.ts`. |

OMP and Pi are installed only when their binaries exist. Their native installers require the
extension directory to exist, so the updater creates it when needed. These installers write only
the extension files; they do not modify Pi's linked JSON settings. Both agents discover the files
on startup. Restart them after installation or updates.

The extensions report session references and lifecycle state to Herdr's local socket when
`HERDR_ENV=1`, `HERDR_SOCKET_PATH`, and `HERDR_PANE_ID` identify a Herdr pane. They are inactive
outside Herdr. Pi's integration gates reporting on TUI mode; OMP also excludes nested sessions
marked by `OMPCODE=1`. Installation status does not prove a live pane's state display is correct.

Herdr can add an absolute-path duplicate hook to the installed Claude settings copy. The next
updater run resets it from the tracked source. That machine-specific mutation is why Claude uses
a copy; it is not a reason to copy Pi's JSON files. If Herdr changes the Claude hook command,
review the installed entry and port it into the tracked `$HOME` form.

See [Herdr's integrations reference](https://herdr.dev/docs/integrations/) for upstream behavior.

## Moshi

Tracked Claude settings call `'/opt/homebrew/bin/moshi-hook' claude-hook`, which assumes
Homebrew's Apple Silicon prefix. Moshi's OpenCode plugin and daemon/LaunchAgent are machine-local;
the coding-agent updater does not install them. `moshi-hook install --target opencode` owns the plugin.

For daemon failures, inspect the service environment: launchd does not inherit the interactive
shell's mise PATH.
