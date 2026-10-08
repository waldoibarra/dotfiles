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

Homebrew owns `moshi-hook`. The coding-agent updater uses its native `install --target` command
for OMP and Pi when both Moshi and the agent binary exist. The installer creates the directories
and writes the generated extensions; no tracked extension copy or custom hook is needed.

| Agent | Integration and owner |
| --- | --- |
| Claude Code | Tracked settings call `'/opt/homebrew/bin/moshi-hook' claude-hook`, assuming Homebrew's Apple Silicon prefix. |
| OpenCode | Machine-local plugin owned by `moshi-hook install --target opencode`; not installed by this updater. |
| OMP | Updater runs `moshi-hook install --target omp`; writes `~/.omp/agent/extensions/moshi-hooks.ts` for the default profile. |
| Pi | Updater runs `moshi-hook install --target pi`; writes `~/.pi/agent/extensions/moshi-hooks.ts`. |

The installed Moshi 0.4.18 CLI has no per-target dry run or version-status command. The updater
reruns its native installer; repeated installs produce the same extension contents. It does not
modify Pi's linked JSON preferences, Herdr/RTK extensions, pairing, or daemon service configuration.
Restart the agents to load the extensions.

### First-run settings during sync

Moshi's native installer can open a **First-run settings** menu in an interactive terminal. This
is Moshi setup, not Herdr, even when it appears just after Herdr's status output. Cancelling saves
nothing, but hook installation continues. Because OMP and Pi are separate installer calls, cancelling
the first menu can produce the same prompt again for the second target.

The updater redirects each Moshi installer's stdin from `/dev/null`. An attached-terminal smoke
test confirmed both hooks install without showing the menu or writing preference files. Sync does
not accept the preselected choices for you. Skipping the menu does not disable Moshi's defaults.
Choose those machine-local preferences separately in an interactive terminal:

```sh
moshi-hook set --first-run
```

The menu controls background discovery, usage collection, nested-agent notifications, and push
suppression while the Mac is unlocked. `moshi-hook set` lists the settings for later review.
These choices stay outside dotfiles.

### Events and delivery

The generated hooks send events directly to the local Moshi socket. Pi reports session starts,
user prompts, settled completions, and shutdown. OMP also handles session switching and native
approval-request/resolution events. Pi's current extension does not register approval handlers;
installing it is not proof of phone-based approval support. Herdr pane identity comes from the
pane environment, so these hooks can coexist with Herdr's own state-reporting extensions.

Events include session/transcript references, working directory, model and context metadata, and
clipped prompt/completion text. The paired daemon can relay events to the phone; installation is
not a claim that conversation content stays on the host. Socket failures are ignored by the native
hooks so an absent daemon does not interrupt an agent turn.

Pairing and daemon/LaunchAgent setup remain machine-local and are not provisioned by `dots`.
`moshi-hook probe --json` checks the local daemon and gateway without changing them; it does not
prove phone delivery. Waldo reports missing Pi/OMP phone notifications despite installed hooks;
that diagnosis is deferred. On another computer, use [Moshi's setup guide](https://getmoshi.app/docs/install-moshi-hook)
for pairing and service setup, then restart agents and verify a harmless completion in the app.
For daemon failures, inspect the service environment: launchd does not inherit the interactive
shell's Mise PATH. [Moshi's hook reference](https://getmoshi.app/docs/hooks) describes upstream support.

## Lens

[Lens](https://github.com/waldoibarra/claude-code-lens) is a Claude Code plugin that redraws the
transcript in normal, clean and raw views. Its repository documents what it does and how to
develop it; this section covers only how the workstation installs it.

The tracked Claude settings declare it in two keys:

- `extraKnownMarketplaces.claude-code-lens` points at the `waldoibarra/claude-code-lens` GitHub
  repository with `autoUpdate` on, so new releases install on startup.
- `enabledPlugins` turns on `lens@claude-code-lens`.

The updater copies the settings, and Claude Code clones the marketplace and installs the plugin
in the background at the next session start. No install command or trust prompt is needed for a
GitHub source declared in user settings.

To use it before the next sync, install it into the current settings copy:

```sh
claude plugin marketplace add waldoibarra/claude-code-lens
claude plugin install lens@claude-code-lens
```

Both commands write the same two keys into the installed copy, and the next updater run replaces
that copy with the tracked source. Edit the tracked keys, never the installed copy, to change the
source or disable the plugin. `claude plugin list` shows the installed version and whether it is
enabled.

Lens's clicks need the fullscreen interface that the tracked `"tui": "fullscreen"` setting turns
on. When developing Lens from its working tree, disable the installed copy for that session with
`claude plugin disable lens@claude-code-lens` so two copies do not draw at once, then enable it
again.
