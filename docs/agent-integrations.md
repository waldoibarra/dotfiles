# Agent integrations

Read [Coding agents](coding-agents/README.md) before editing tracked settings, and
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running the updater.
Keep machine-local hooks, plugins and service configuration outside the repository.

## RTK

Read the [RTK command reference](/home/.agents/RTK.md) before using or diagnosing RTK.
The shared global instructions load that reference on demand.

| Agent | Integration and owner |
| --- | --- |
| Claude Code | Tracked Bash hook runs `rtk hook claude`. |
| Pi (`pi`) | If `pi` exists, updater refreshes `~/.pi/agent/extensions/rtk.ts` with `rtk init -g --agent pi`. |

The updater refreshes Pi's file only when dry runs list pending
`[dry-run] would …` changes. Dry runs always print `Nothing written`; that line does not mean
an integration is current. A failed RTK step warns and lets the remaining updater steps run.

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
| Pi | `~/.pi/agent/extensions/herdr-agent-state.ts`. |

Pi's integration is installed only when `pi` exists. Its native installer requires the extension
directory to exist, so the updater creates it when needed. The installer writes only the extension
file; it does not modify Pi's linked JSON settings. Pi discovers the file on startup. Restart Pi
after installation or updates.

The extensions report session references and lifecycle state to Herdr's local socket when
`HERDR_ENV=1`, `HERDR_SOCKET_PATH`, and `HERDR_PANE_ID` identify a Herdr pane. They are inactive
outside Herdr. Pi's integration gates reporting on TUI mode. Installation status does not prove
a live pane's state display is correct.

Herdr can add an absolute-path duplicate hook to the installed Claude settings copy. The next
updater run resets it from the tracked source. That machine-specific mutation is why Claude uses
a copy; it is not a reason to copy Pi's JSON files. If Herdr changes the Claude hook command,
review the installed entry and port it into the tracked `$HOME` form.

See [Herdr's integrations reference](https://herdr.dev/docs/integrations/) for upstream behavior.

## Moshi

Homebrew owns `moshi-hook`. The coding-agent updater uses its native `install --target` command
for Pi when both Moshi and `pi` exist. The installer creates the directories
and writes the generated extensions; no tracked extension copy or custom hook is needed.

| Agent | Integration and owner |
| --- | --- |
| Claude Code | Tracked settings call `'/opt/homebrew/bin/moshi-hook' claude-hook`, assuming Homebrew's Apple Silicon prefix. |
| Pi | Updater runs `moshi-hook install --target pi`; writes `~/.pi/agent/extensions/moshi-hooks.ts`. |

The installed Moshi 0.4.18 CLI has no per-target dry run or version-status command. The updater
reruns its native installer; repeated installs produce the same extension contents. It does not
modify Pi's linked JSON preferences, Herdr/RTK extensions, pairing, or daemon service configuration.
Restart Pi to load the extension.

### First-run settings during sync

Moshi's native installer can open a **First-run settings** menu in an interactive terminal. This
is Moshi setup, not Herdr, even when it appears just after Herdr's status output. Cancelling saves
nothing, but hook installation continues.

The updater redirects each Moshi installer's stdin from `/dev/null`. An attached-terminal smoke
test confirmed hooks install without showing the menu or writing preference files. Sync does
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
user prompts, settled completions, and shutdown. Pi's current extension does not register approval handlers;
installing it is not proof of phone-based approval support. Herdr pane identity comes from the
pane environment, so these hooks can coexist with Herdr's own state-reporting extensions.

Events include session/transcript references, working directory, model and context metadata, and
clipped prompt/completion text. The paired daemon can relay events to the phone; installation is
not a claim that conversation content stays on the host. Socket failures are ignored by the native
hooks so an absent daemon does not interrupt an agent turn.

Pairing and daemon/LaunchAgent setup remain machine-local and are not provisioned by `dots`.
`moshi-hook probe --json` checks the local daemon and gateway without changing them; it does not
prove phone delivery. Waldo reports missing Pi phone notifications despite installed hooks;
that diagnosis is deferred. On another computer, use [Moshi's setup guide](https://getmoshi.app/docs/install-moshi-hook)
for pairing and service setup, then restart agents and verify a harmless completion in the app.
For daemon failures, inspect the service environment: launchd does not inherit the interactive
shell's Mise PATH. [Moshi's hook reference](https://getmoshi.app/docs/hooks) describes upstream support.

## Lens

[Pi Lens](https://github.com/waldoibarra/pi-lens) and
[Claude Lens](https://github.com/waldoibarra/claude-lens)
target matching display-only transcript views.
Pi is the primary coding agent. Each sibling documents its supported behavior and host limitations.

### Pi Lens

The tracked Pi settings declare `git:github.com/waldoibarra/pi-lens@latest` with empty `skills`
and `prompts` filters. The existing updater runs `pi update --extensions --no-approve` against the
normal profile, so no separate installer loop is needed for the Git package.

Lens `v0.2.0` is verified with Pi `1.1.0` and `1.2.0`; unrecognized UI layouts retain native rendering.
Mise follows Pi `latest`; Lens no longer rejects hosts by version number.
Future Pi versions still require compatibility verification.
Check `pi --version` and `/lens` after sync. Credentials, sessions, and package caches remain machine-local.
Clipboard previews and composer attribution require compatible host patches.
The Lens package does not install them.

Read [Pi Lens](https://github.com/waldoibarra/pi-lens) before changing its package declaration.
Local validation does not require `dots`, package publication, or replacing the normal Pi runtime.

### Release deployment

Pi's binary remains on Mise `latest`. Both Lens deployments follow their GitHub `latest` tags.
There is no release branch. Versioned release tags remain immutable; only `latest` moves.

Read [Pi publishing](https://github.com/waldoibarra/pi-lens/blob/main/docs/how-to/contribute.md)
before publishing Pi Lens or moving its `latest` alias.
Read [Claude publishing](https://github.com/waldoibarra/claude-lens/blob/main/docs/development.md)
before publishing Claude Lens or moving its `latest` alias.

1. Publish and verify an immutable version; update `latest` through that product's release procedure.
2. Keep Pi's package-source tag and Claude's marketplace `source.ref` set to `latest`.
3. Run the harness tests, lint, and native installation checks against the released commit.
4. Refresh installed packages on each machine and open a fresh agent.

Moving `latest` does not reload running sessions. Verify installed commits after refresh.
For rollback, select a previous immutable version in settings; never move versioned release tags.
No credentials, sessions, or development checkouts are copied between machines.

### Claude Lens

The tracked Claude settings declare Lens in two keys:

- `extraKnownMarketplaces.claude-lens` points at `waldoibarra/claude-lens`, with `source.ref: latest`.
- `autoUpdate` refreshes that source; releases advance the GitHub `latest` tag.
- `enabledPlugins` enables `lens@claude-lens` and disables the old `lens@claude-code-lens` identity.

The updater copies the settings, and Claude Code clones the marketplace and installs the plugin
in the background at the next session start. No install command or trust prompt is needed for a
GitHub source declared in user settings.

To use it before the next sync, install it into the current settings copy:

```sh
claude plugin marketplace add waldoibarra/claude-lens@latest
claude plugin install lens@claude-lens
```

Both commands write the same two keys into the installed copy, and the next updater run replaces
that copy with the tracked source. Edit the tracked keys, never the installed copy, to change the
source or disable the plugin. `claude plugin list` shows the installed version and whether it is
enabled.

Existing machines may retain the old marketplace cache.
The explicit disabled entry prevents duplicate rendering after sync.
Read [Claude Lens migration](https://github.com/waldoibarra/claude-lens#install)
before switching an existing installation.
Use native plugin and marketplace commands; do not edit Claude's package cache by hand.

Lens's clicks need the fullscreen interface that the tracked `"tui": "fullscreen"` setting turns
on. Read [Develop Lens locally](/docs/tooling.md#claude-lens) before working from the Lens
working tree; `just claude-lens-dev` disables the installed copy for that session.
