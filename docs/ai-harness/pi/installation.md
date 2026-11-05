# Pi installation and sync

**Ownership:** Pi provisioning runs through `dots`.
Mise owns the binary; Dotbot links instructions, roles, and most preferences.
Settings delivery merges tracked defaults into a local writable file before package reconciliation.
Read [editing settings](configuration.md#edit-persistent-settings) before changing Pi defaults.

## Provisioning sequence

[Dotbot](../../../install.conf.yaml) creates the real Pi directories and links `AGENTS.md`,
`models.json`, `keybindings.json`, and `mcp.json`.
It also links `APPEND_SYSTEM.md` for Pi-specific skill compatibility and installs shared roles individually.
Credentials and sessions remain separate.
Dotbot runs the targeted settings sync instead of linking `settings.json`.
The updater repeats that idempotent step before package reconciliation.
[Settings ownership](configuration.md#merge-ownership) defines merge, migration, and recovery behavior.

The updater reconciles shared personal MCP definitions with Claude's user registry first.
Read [personal MCP setup](../mcp.md) before changing or verifying those registrations.

The [agent updater](../../../scripts/update-coding-agents/entrypoint.sh) then runs
`pi update --extensions --no-approve` from `$HOME` for every declared package.

`pi update --extensions` reconciles the remaining declared packages, including the Pi Lens Git
source, from the local normal-profile settings. Its empty `skills` and `prompts` filters are part
of the tracked package declaration and should be preserved.

The command uses `PI_CODING_AGENT_DIR="$HOME/.pi/agent"` without `OPENAI_API_KEY`.
Inherited trial profiles and project-local packages do not change this target.
Only packages are reconciled; Mise remains responsible for the Pi binary and remains on `latest`.

Reconciliation uses Pi's [package mechanism](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).
Homebrew does not own another Pi installation.
The shell alias `pi='caffeinate -i pi'` keeps the workstation awake during interactive use.
An install/update failure stops the updater with an error. Configuration may already be linked;
a later successful run reconciles the packages. Reconciliation never starts a model conversation or
opens the microphone.

The `dots` alias runs `just sync`, which can remove undeclared packages.
The updater does not commit or push local changes.
Do not use `dots` as a validation command.
Read [sync boundaries](../../tooling.md#sync-the-workstation) before applying workstation
changes, and [workstation setup](../../setup.md) for the complete fresh-machine sequence.

## RTK, Herdr and Moshi extensions

The same agent updater installs these native extensions in `~/.pi/agent/extensions`, outside Git.
Generated extensions remain separate from tracked Pi defaults.

| Integration | Installer | Purpose |
| --- | --- | --- |
| RTK | `rtk init -g --agent pi` | Rewrites supported Bash commands. |
| Herdr | `herdr integration install pi` | Reports session and lifecycle state inside Herdr. |
| Moshi | `moshi-hook install --target pi` | Sends session and completion events to Moshi's local daemon. |

The updater uses RTK's dry run and Herdr's integration status to avoid rewriting current files.
Moshi's installer is rerun because it exposes no equivalent per-target status check. Moshi pairing
and daemon/service setup remain machine-local; hooks alone do not establish phone delivery.
Restart Pi after changes. [Agent integrations](../integrations.md) documents the native
installers, data sent by Moshi, environment requirements, and verification limits.

## Authentication and billing

Pi's `/login openai-codex` handles subscription authentication without requiring the Codex CLI.
First-run login and macOS microphone permission remain interactive user actions.
Earlier text and voice access succeeded; those results do not establish current account access.

The chosen billing route is subscription-backed Codex access. There is no authorized API-key
fallback, credit purchase, or automatic top-up. Device codes, tokens, callback URLs, and credential
files must not appear in repository documentation or logs. No other agent's credentials are
copied into Pi.

The extension's experimental signaling and attestation behavior is documented under
[live voice](live-voice.md#connection-and-access-boundary). An access rejection is not permission
to alter identity or attestation or switch billing routes.

## Verification

| Check | What it establishes |
| --- | --- |
| `just lint` | Repository formatting and source checks. |
| `python3 scripts/tests/test-pi-settings.py` | Isolated settings migration, preservation, idempotency, and failure recovery. |
| `python3 scripts/tests/test-agent-harness.py` | Isolated links, role settings, and updater success/failure behavior. |
| `pi --version` | Installed Pi resolution and version. |
| `pi list --no-approve` | Configured package declarations. |
| `pi --list-models openai-codex --offline` | Loaded model metadata and context-window overrides, without inference. |
| Fresh interactive Pi and `/hotkeys` | Package loading and shortcut registration. |
| `/live spruce` | A user-run spoken check of the selected voice. |

The provisioning suite uses a disposable home, without a microphone or model call.
Read [Agent coordination](../agent-coordination/spawning.md) before testing worker execution.
The user performs the spoken check.
`pi --continue` resumes coding context but does not repair the known [voice-context limitation](limitations.md).

## Upstream references

- [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).
- [Pi authentication](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md).
