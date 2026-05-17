# Dotfiles

My personal OS **configuration files**, currently using **MacOS**.

## Project Structure

The idea is simple, the [home/](home/) directory in this repository mirrors the actual
directory structure of `$HOME` in the OS.

It can also be easily seen by looking at the [install.conf.yaml](install.conf.yaml)
file, in the `link` directive.

## Initial Setup

A fresh OS installation might not have `git` available, so you must install it manually to clone
this repository. You can do that by running:

- MacOS: `xcode-select --install`\
- Linux (Debian): `sudo apt-get install -y git`

To install this dotfiles configuration on a new machine, run these 3 commands:

```bash
git clone --recurse-submodules https://github.com/waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./scripts/install-dotfiles.sh
```

> On machines where you have **SSH configured** with GitHub (for write access ease), you can clone
> via SSH instead:
>
> ```bash
> git clone --recurse-submodules git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
> ```

Run these commands only 1 time; after the initial setup, use the commands below.

## Sync

This command is idempotent, it can be ran many times.

```bash
just sync
```

What it does:

- Use [DotBot](https://github.com/anishathalye/dotbot), a dotfiles bootstrapper, to update the
  symlinks and ensure all OS packages are installed. It uses the [install.conf.yaml](install.conf.yaml)
  file.
- Use [Homebrew](https://brew.sh/) to upgrade apps, libraries, or dev tools (but prefer Mise for dev
  tools). Installed Brew packages are defined in the global [~/.Brewfile](home/.Brewfile).
- Use [mise](https://github.com/jdx/mise), the language agnostic dev tools manager to update global
  default tool versions that are defined in [~/.config/mise/config.toml](home/.config/mise/config.toml),
  they define which version is active when no project-level file overrides it.
- Update coding agents configuration by running the [scripts/update-coding-agents.sh](scripts/update-coding-agents.sh)
  script.

## Utility Scripts

There is a `scripts/` directory, read its [documentation](scripts/README.md).
