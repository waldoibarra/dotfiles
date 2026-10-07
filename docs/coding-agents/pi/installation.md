# Pi installation and sync

Pi provisioning runs through the existing `dots` workflow. Mise owns the binary; Dotbot owns the
instruction and preference links; the coding-agent updater reconciles the voice package.
[Configuration](configuration.md) lists the linked files and ownership boundaries.

## Provisioning sequence

[Dotbot](../../../install.conf.yaml) creates the real Pi directories and links `AGENTS.md`,
`settings.json`, `models.json`, and `keybindings.json`. Credentials and sessions remain separate.
Pi files do not use the managed-copy helper.

The [agent updater](../../../scripts/update-coding-agents/entrypoint.sh) then runs
`pi update npm:pi-live-codex --no-approve` from `$HOME`. Pi installs a missing
package and updates it when a newer release is available. The command uses
`PI_CODING_AGENT_DIR="$HOME/.pi/agent"` and removes `OPENAI_API_KEY` from that subprocess.
Inherited trial profiles and project-local packages do not change this target. The updater does
not call `pi update` without a package target; Mise remains responsible for the Pi binary.

The original trial used `pi install npm:pi-live-codex --no-approve`. Both operations use Pi's
[package mechanism](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).
An install/update failure stops the updater with an error. Configuration may already be linked;
a later successful run reconciles the package. Neither operation starts a model conversation or
opens the microphone.

The existing `dots` alias runs `just sync`; it can remove undeclared packages, and the skill updater
can commit and push changes, including earlier unpushed commits. It is not a harmless validation
command. See [sync boundaries](../../tooling.md#sync-the-workstation) before applying workstation
changes, and [workstation setup](../../setup.md) for the complete fresh-machine sequence.

## RTK and Herdr extensions

The same agent updater installs RTK with `rtk init -g --agent pi` and Herdr with
`herdr integration install pi`. RTK rewrites supported Bash commands; Herdr reports session and
lifecycle state when Pi runs inside a Herdr pane. Both generated extensions live in
`~/.pi/agent/extensions`, outside Git, and neither installer changes Pi's linked preferences.

The updater uses RTK's dry run and Herdr's integration status to avoid rewriting current files.
Restart Pi after changes. [Agent integrations](../../agent-integrations.md) documents the native
installers, paths, environment requirements, and verification limits.

## Authentication and billing

Pi's `/login openai-codex` handles subscription authentication. Device-code login is available in
the inspected Pi version, with browser authorization as another supported route. Waldo completed
login and verified text and voice access; the exact login method used was not recorded. First-run
login and macOS microphone permission remain interactive user actions.

The chosen billing route is subscription-backed Codex access. There is no authorized API-key
fallback, credit purchase, or automatic top-up. Device codes, tokens, callback URLs, and credential
files must not appear in repository documentation or logs. Existing Codex CLI or OMP credentials
are not copied into Pi.

The extension's experimental signaling and attestation behavior is documented under
[live voice](live-voice.md#connection-and-access-boundary). An access rejection is not permission
to alter identity or attestation or switch billing routes.

## Verification

| Check | What it establishes |
| --- | --- |
| `just lint` | Repository formatting and source checks. |
| `pi --version` | Installed Pi resolution and version. |
| `pi list --no-approve` | Configured package declarations. |
| `pi --list-models openai-codex --offline` | Loaded model metadata and context-window overrides, without inference. |
| Fresh interactive Pi and `/hotkeys` | Package loading and shortcut registration. |
| `/live spruce` | A user-run spoken check of the selected voice. |

Provisioning changes are smoke-tested in a disposable home, without a microphone or model call.
Waldo performs the spoken check. `pi --continue` resumes coding context but does not repair the known
[voice-context limitation](limitations.md).

## Upstream references

- [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).
- [Pi authentication](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md).
