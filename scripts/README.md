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

1. Copy the four managed agent configs. This runs first because it replaces Claude settings.
2. Clear stale OpenCode plugin-cache entries when a newer upstream version is detected.
3. Refresh the RTK OpenCode plugin when its dry run lists pending changes.
4. Refresh Herdr's OpenCode plugin and Claude hook unless integration status reports them current.
5. Install missing lockfile skills, update global skills, then **commit and push** a changed lockfile.

RTK and Herdr steps skip their integrations when the respective binary is missing.
See [coding agents](/docs/coding-agents.md) for copied file ownership, failure handling
and publication risks. Moshi installation is not part of this updater.

## Shared helpers and checks

[`lib/shell-helpers.sh`](/scripts/lib/shell-helpers.sh) supplies `print_separator`.
Updater helpers live beside their entrypoint under `scripts/update-coding-agents/`.

Run `just lint-sh` after shell changes. It checks selected entrypoints and follows sourced helpers
where configured; it does not execute installation behavior. Exercise changed behavior in an
isolated environment, never by running a real machine sync as a test.
