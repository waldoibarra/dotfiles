# Scripts

This directory contains scripts to:

- Idempotently install the dotfiles configuration ([install-dotfiles.sh](install-dotfiles.sh))
- Install Homebrew (and its packages), Mise (and its tools), Git hooks, and sets Zsh (from Brew) as
  default Shell ([install-os-packages.sh](install-os-packages.sh))
- Update coding agents ([update-coding-agents.sh](update-coding-agents.sh))

## Install Dotfiles

It is a slightly modified copy of the DotBot install script, it calls the DotBot installer with the
[install.config.yaml](/install.config.yaml) configuration file; it then will:

- Manage the dotfiles symlinks.
- Run the `install-os-packages.sh` script.

This `install-dotfiles.sh` script is ran with the `just sync` command.

## Install OS Packages

What this script does:

- Ensure Homebrew and its dependencies are installed.
- Ensure Homebrew packages are installed.
- Ensure Mise tools are installed.
- Ensure this repo's Git hooks are installed.
- Ensure `zsh` (from brew) is the default shell.

This `install-os-packages.sh` script is used by `install-dotfiles.sh` script, which is ran with the
`just sync` command.

## Update Coding Agents

It will update the following:

- [Globally installed skills](https://skills.sh/)

This script is used automatically by the `just sync` command.
