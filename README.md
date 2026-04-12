# Dotfiles

My personal OS **configuration files**, currently using **MacOS**.

## Project Structure

The idea is simple, the [home/](home/) directory in this repository mirrors the actual
directory structure of `$HOME` in the OS.

It can also be easily seen by looking at the [install.conf.yaml](install.conf.yaml)
file, in the `link` directive.

## Setup

Install this dotfiles configuration on a new machine.

```bash
git clone --recurse-submodules git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles

# Use `just install` for all subsequent runs.
./scripts/install-dotfiles.sh
```

> Might need to set Zsh as default shell and restart machine (I need to test this in the future).

### Customization

Edit the [install.conf.yaml](install.conf.yaml) file and re-run the script.

```bash
just install
```

The [Dotbot](https://github.com/anishathalye/dotbot)'s script is idempotent, can be ran many times.

## Managing Developer Tools

Use [mise](https://github.com/jdx/mise), the language agnostic dev tools manager. Global default
tool versions are defined in [~/.config/mise/config.toml](home/.config/mise/config.toml), they
define which version is active when no project-level file overrides it.

```bash
mise ls
```

To override a tool version, simply create a config/version file in the project root.

```bash
# Any of these work.
my-awesome-project
├── mise.toml
├── .node-version
└── .python-version
```

## Managing Brew Packages

Install/uninstall a package, then update the global [~/.Brewfile](home/.Brewfile).

```bash
# Brew bundle: dump, cleanup, upgrade.
just brew
```

## Utility Scripts

There is a `scripts/` directory, read its [documentation](scripts/README.md).
