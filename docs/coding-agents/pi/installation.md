# Pi installation and sync

Pi provisioning runs through the existing `dots` workflow. Mise owns the binary; Dotbot owns the
instruction, role, and preference links; the coding-agent updater reconciles declared packages.
[Configuration](configuration.md) lists the linked files and ownership boundaries.

## Provisioning sequence

[Dotbot](../../../install.conf.yaml) creates the real Pi directories and links `AGENTS.md`,
`settings.json`, `models.json`, `keybindings.json`, `mcp.json`, and `extensions/subagent/config.json`.
It links shared roles individually; credentials and sessions remain separate.
Pi files do not use the managed-copy helper.

The updater reconciles shared personal MCP definitions with Claude's user registry first.
Read [personal MCP setup](../mcp.md) before changing or verifying those registrations.

The [agent updater](../../../scripts/update-coding-agents/entrypoint.sh) then runs
`pi install <configured-runner-source> --no-approve`, then `pi update --extensions --no-approve`
from `$HOME`. The runner source comes from linked settings, keeping its pin in one place.
Explicit installation is required because Pi's update command skips pinned npm packages, even when missing.
The package filter object remains intact when installing the same source.

Both commands use `PI_CODING_AGENT_DIR="$HOME/.pi/agent"` without `OPENAI_API_KEY`.
Inherited trial profiles and project-local packages do not change this target.
Only packages are reconciled; Mise remains responsible for the Pi binary.

The original trial used `pi install npm:pi-live-codex --no-approve`. Both operations use Pi's
[package mechanism](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).
An install/update failure stops the updater with an error. Configuration may already be linked;
a later successful run reconciles the packages. Neither operation starts a model conversation or
opens the microphone.

The existing `dots` alias runs `just sync`; it can remove undeclared packages, and the skill updater
can commit and push changes, including earlier unpushed commits. It is not a harmless validation
command. See [sync boundaries](../../tooling.md#sync-the-workstation) before applying workstation
changes, and [workstation setup](../../setup.md) for the complete fresh-machine sequence.

## RTK, Herdr and Moshi extensions

The same agent updater installs these native extensions in `~/.pi/agent/extensions`, outside Git.
None of their installers changes Pi's linked preferences.

| Integration | Installer | Purpose |
| --- | --- | --- |
| RTK | `rtk init -g --agent pi` | Rewrites supported Bash commands. |
| Herdr | `herdr integration install pi` | Reports session and lifecycle state inside Herdr. |
| Moshi | `moshi-hook install --target pi` | Sends session and completion events to Moshi's local daemon. |

The updater uses RTK's dry run and Herdr's integration status to avoid rewriting current files.
Moshi's installer is rerun because it exposes no equivalent per-target status check. Moshi pairing
and daemon/service setup remain machine-local; hooks alone do not establish phone delivery.
Restart Pi after changes. [Agent integrations](../../agent-integrations.md) documents the native
installers, data sent by Moshi, environment requirements, and verification limits.

## Authentication and billing

Pi's `/login openai-codex` handles subscription authentication. Device-code login is available in
the inspected Pi version, with browser authorization as another supported route. Waldo completed
login and verified text and voice access; the exact login method used was not recorded. First-run
login and macOS microphone permission remain interactive user actions.

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
| `python3 scripts/tests/test-agent-harness.py` | Isolated links, role settings, and updater success/failure behavior. |
| `pi --version` | Installed Pi resolution and version. |
| `pi list --no-approve` | Configured package declarations. |
| `pi --list-models openai-codex --offline` | Loaded model metadata and context-window overrides, without inference. |
| Fresh interactive Pi and `/hotkeys` | Package loading and shortcut registration. |
| `/live spruce` | A user-run spoken check of the selected voice. |

Provisioning changes are smoke-tested in a disposable home, without a microphone or model call.
Read [Pi delegation](delegation.md#install-and-verify) before testing role/model execution.
Waldo performs the spoken check. `pi --continue` resumes coding context but does not repair the known
[voice-context limitation](limitations.md).

## Upstream references

- [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).
- [Pi authentication](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md).
