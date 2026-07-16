# Scripts

This directory contains scripts to:

- Idempotently install the dotfiles configuration ([install-dotfiles.sh](install-dotfiles.sh))
- Install Homebrew (and its packages) and Mise (and its tools) ([install-os-packages.sh](install-os-packages.sh))
- Set the Homebrew Zsh as the default shell ([set-brew-zsh-as-default-shell.sh](set-brew-zsh-as-default-shell.sh))
- Update coding agents ([update-coding-agents/entrypoint.sh](update-coding-agents/entrypoint.sh))

## Install Dotfiles

It is a slightly modified copy of the DotBot install script, it calls the DotBot installer with the
[install.conf.yaml](/install.conf.yaml) configuration file; it then will:

- Manage the dotfiles symlinks.
- Run the `install-os-packages.sh`, `set-brew-zsh-as-default-shell.sh`, and `setup-repo.sh` scripts.

This `install-dotfiles.sh` script is ran with the `just sync` command.

## Install OS Packages

What this script does:

- Ensure Homebrew and its dependencies are installed.
- Ensure Homebrew packages are installed.
- Ensure Mise tools are installed.
- Ensure WezTerm terminfo entry is installed (macOS only).

This `install-os-packages.sh` script is used by `install-dotfiles.sh` script, which is ran with the
`just sync` command.

## Configure Touch ID for Sudo

What this script does:

- Ensure `/etc/pam.d/sudo_local` enables Touch ID (`pam_tid.so`) so the terminal
authenticates via Touch ID instead of a password prompt. macOS only — the script
no-ops on Linux.

This `configure-touch-id-for-sudo.sh` script is used by `install-dotfiles.sh` script, which is ran
with the `just sync` command.

## Set Brew Zsh as Default Shell

What this script does:

- Ensure `zsh` (from Brew) is the default shell.

This `set-brew-zsh-as-default-shell.sh` script is used by `install-dotfiles.sh` script, which is
ran with the `just sync` command.

## Update Coding Agents

It will update the following:

- OpenCode's plugin cache, clearing only the entries for plugins with a newer version available
  upstream so OpenCode reinstalls just those on next launch
- [Globally installed skills](https://skills.sh/)
- RTK OpenCode plugin (`~/.config/opencode/plugins/rtk.ts`) via `rtk init -g --opencode`

This script is used automatically by the `just sync` command.
