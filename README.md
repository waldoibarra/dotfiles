# Dotfiles

My personal OS **configuration files**, currently using **MacOS**.

## Project Structure

The idea is simple, the [home/](home/) directory in this repository mirrors the actual
directory structure of `$HOME` in the OS.

It can also be easily seen by looking at the [install.conf.yaml](install.conf.yaml)
file, in the `link` directive.

## Initial Setup

Install this dotfiles configuration on a new machine.

```bash
git clone --recurse-submodules git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles

# Only run this Shell script directly on a fresh OS (when the OS does not have Brew/Mise/just).
# Run with `just sync` for all subsequent runs.
./scripts/install-dotfiles.sh
```

Run these commands only 1 time; after the initial setup, use the commands below.

> Might need to set Zsh as default shell and restart machine (I need to test this in the future).

### Customization

Edit the [install.conf.yaml](install.conf.yaml) file and sync the configuration by running:

```bash
just sync
```

The [Dotbot](https://github.com/anishathalye/dotbot)'s script is idempotent, can be ran many times.

## Managing Developer Tools

Use [mise](https://github.com/jdx/mise), the language agnostic dev tools manager. Global default
tool versions are defined in [~/.config/mise/config.toml](home/.config/mise/config.toml), they
define which version is active when no project-level file overrides it.

```bash
# Upgrade outdated tools.
just mise-up
```

## Managing Homebrew Packages

Use [Homebrew](https://brew.sh/) to install apps, libraries, or dev tools (but prefer Mise for dev
tools). Installed Brew packages are defined in the global [~/.Brewfile](home/.Brewfile).

```bash
# Brew bundle: dump, cleanup, upgrade.
just brew
```

## Utility Scripts

There is a `scripts/` directory, read its [documentation](scripts/README.md).
