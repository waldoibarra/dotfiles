# Dotfiles

My personal OS **configuration files**, currently using **MacOS**.

## Project Structure

The idea is simple, the [home/](/home/) directory in this repository mirrors the actual
directory structure of `$HOME/` in the OS.

It can also be easily seen by looking at the [install.conf.yaml](install.conf.yaml)
file, in the `link` directive.

## Setup

To install your dotfiles on a new machine or after updates:

```bash
git clone --recurse-submodules git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./scripts/install-dotfiles.sh
```

After the first run, use `just install` for all subsequent runs.

> Might need to set Zsh as default shell and restart machine.

The [Dotbot](https://github.com/anishathalye/dotbot)'s script is idempotent, can be ran many times.

### Customization

Edit the [install.conf.yaml](install.conf.yaml) file and re-run:

```bash
just install
```

## Installing Latest Node.js / Python

```bash
# Install latest Long Term Support (LTS) version of Node.js using NVM.
nvm install --lts
nvm use --lts
nvm ls

# Install latest stable Python 3 release.
pyenv install 3
pyenv global 3
pyenv versions
```

## Updating Brew Packages

Install, dump, clean up, and upgrade.

```bash
brew install <package_name>
just brew

# Or run them one by one.

just brew-dump
just brew-cleanup
just brew-upgrade
```

## The Complete Z Shell Load Order

> Just a reminder: when you open a terminal window, Zsh reads configuration files in this
> specific sequence.

1. `~/.zshenv`: Always loaded first for every Zsh session (including scripts).
2. `~/.zprofile`: Loaded only for login shells. On macOS, every new terminal window is treated as a
   login shell by default.
3. `~/.zshrc`: Loaded for interactive shells. This is where most of your day-to-day configuration
   lives.
4. `~/.zlogin`: Loaded last, but only for login shells.

## Utility Scripts

There is a `scripts/` directory, read its [documentation](/scripts/README.md).
