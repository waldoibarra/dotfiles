# Scripts

Read this before changing installer or sync behavior. These scripts modify the workstation;
use [tooling](/docs/tooling.md) to choose the narrowest operation.

## Installation

[`install-dotfiles.sh`](/scripts/install-dotfiles.sh) initializes the Dotbot submodule and runs
[install.conf.yaml](/install.conf.yaml) from the repository root. It forwards arguments to Dotbot.
The configuration updates submodules from their remotes, manages links and runs these scripts:

| Script | Behavior |
| --- | --- |
| [configure-touch-id-for-sudo.sh](/scripts/configure-touch-id-for-sudo.sh) | On macOS, build `/etc/pam.d/sudo_local` from Apple's template if Touch ID is not enabled; set mode `444`. Skip other systems; fail if the template is missing. |
| [install-os-packages.sh](/scripts/install-os-packages.sh) | Install Homebrew if needed, check/install its global bundle, trust/install Mise tools, and install missing WezTerm terminfo on macOS when WezTerm is available. |
| [set-brew-zsh-as-default-shell.sh](/scripts/set-brew-zsh-as-default-shell.sh) | Register Homebrew Zsh in `/etc/shells` and select it with `chsh`, unless `$SHELL` already matches. |

Installation does not run the coding-agent updater, prune tools or install this checkout's hooks.
`just sync` runs the installer, then those additional management steps.

## Coding-agent updates

[`update-coding-agents/entrypoint.sh`](/scripts/update-coding-agents/entrypoint.sh) runs these steps
in order through `just update-ca` and `just sync`:

1. Copy the two managed agent configs before refreshing Claude hooks.
2. Register missing shared personal MCP servers through Claude's native user-scope command.
3. Install the configured pinned subagent runner, then update declared Pi packages in the normal profile.
4. Refresh RTK's Pi extension when its dry run lists changes.
5. Refresh Herdr's Claude and Pi integrations unless status reports them current.
6. Install Moshi's Pi extension non-interactively with its native target-specific installer.
7. Install missing lockfile skills, update global skills, then **commit and push** a changed lockfile.

RTK, Herdr and Moshi steps skip their integrations when the respective binary is missing. Their Pi
steps also require the `pi` binary. Herdr's native installer requires an extension directory;
the updater creates it when needed. Generated extensions stay outside Git.
Read [Coding agents](../docs/coding-agents/README.md) before editing copied configs or running updates;
it lists ownership and publication risks. Read [Agent integrations](/docs/agent-integrations.md)
before diagnosing hooks or plugins. Moshi's Pi hook file is refreshed on each run; pairing and
daemon/service setup remain outside this updater. Redirecting installer
stdin from `/dev/null` prevents interactive first-run settings prompts during sync without saving
choices. Use [Moshi's separate setup](../docs/agent-integrations.md#first-run-settings-during-sync)
for those machine-local preferences.

[`sync-personal-mcp.py`](/scripts/update-coding-agents/sync-personal-mcp.py) can run separately
with `python3`, without package upgrades or publication. It preserves matching registrations and
fails on conflicts; read [personal MCP setup](/docs/coding-agents/mcp.md) before applying changes.

Pi binary installation belongs to Mise. Package reconciliation reads the runner pin from linked
settings, explicitly installs it, then runs `pi update --extensions --no-approve` from `$HOME`.
Pi's update command skips pinned npm packages even when missing, so installation cannot be omitted.
Both calls use the normal profile, exclude project packages, and omit `OPENAI_API_KEY`.
Failures stop the updater. No model, microphone, or authentication call is requested.

Pi's preferences and subagent configuration are Dotbot links, not managed copies.
Credentials, sessions, and locks are separate and untouched.
[Pi configuration](../docs/coding-agents/pi/configuration.md) lists the ownership boundaries.

## Shared helpers and checks

[`lib/shell-helpers.sh`](/scripts/lib/shell-helpers.sh) supplies `print_separator`.
Updater helpers live beside their entrypoint under `scripts/update-coding-agents/`.

Run `just lint-sh` after shell changes. It checks selected entrypoints and follows sourced helpers
where configured; it does not execute installation behavior. Exercise changed behavior in an
isolated environment, never by running a real machine sync as a test.

Run `python3 scripts/tests/test-agent-harness.py` to check shared-role links, Pi settings, and
package reconciliation. It uses temporary homes and a fake Pi executable; no inference or sync runs.
Run `python3 scripts/tests/test-personal-mcp.py` for isolated MCP registration and linking checks.
