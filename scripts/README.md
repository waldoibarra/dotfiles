# Scripts

This directory contains scripts to:

- Idempotently install the dotfiles configuration ([install-dotfiles.sh](install-dotfiles.sh))
- Install Homebrew (and its packages) and Mise (and its tools) ([install-os-packages.sh](install-os-packages.sh))
- Set up the machine environment ([setup-env.sh](setup-env.sh))
- Set up the repo environment ([setup-repo.sh](setup-repo.sh))
- Update coding agents ([update-coding-agents.sh](update-coding-agents.sh))

## Install Dotfiles

It is a slightly modified copy of the DotBot install script, it calls the DotBot installer with the
[install.conf.yaml](/install.conf.yaml) configuration file; it then will:

- Manage the dotfiles symlinks.
- Run the `install-os-packages.sh`, `setup-env.sh`, and `setup-repo.sh` scripts.

This `install-dotfiles.sh` script is ran with the `just sync` command.

## Install OS Packages

What this script does:

- Ensure Homebrew and its dependencies are installed.
- Ensure Homebrew packages are installed.
- Ensure Mise tools are installed.

This `install-os-packages.sh` script is used by `install-dotfiles.sh` script, which is ran with the
`just sync` command.

## Setup Env

What this script does:

- Ensure `zsh` (from Brew) is the default shell.

This `setup-env.sh` script is used by `install-dotfiles.sh` script, which is ran with the
`just sync` command.

## Setup Repo

What this script does:

- Ensure this repo's Git hooks are installed.

This `setup-repo.sh` script is used by `install-dotfiles.sh` script, which is ran with the
`just sync` command.

## Update Coding Agents

It will update the following:

- [Globally installed skills](https://skills.sh/)

This script is used automatically by the `just sync` command.
