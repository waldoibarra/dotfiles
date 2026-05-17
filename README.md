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
git clone --recurse-submodules https://github.com/waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles

# Only run this Shell script directly on a fresh OS (when the OS does not have Brew/Mise/just).
# Run with `just sync` for all subsequent runs.
./scripts/install-dotfiles.sh
```

> **On machines where you have SSH configured with GitHub**, you can clone via SSH instead:
>
> ```bash
> git clone --recurse-submodules git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
> ```

Run these commands only 1 time; after the initial setup, use the commands below.

### One-time Setup

Run after cloning to set Homebrew zsh as the default shell, install local project tools, and
install Git hooks. May prompt for a password.

```bash
just setup
```

### Customization

Edit the [install.conf.yaml](install.conf.yaml) file and sync the configuration by running:

```bash
# Runs Dotbot, upgrades Brew packages, Mise tools, and coding agents.
just sync
```

The [Dotbot](https://github.com/anishathalye/dotbot) script is idempotent and can be run many times.

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
