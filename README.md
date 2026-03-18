# Dotfiles

My personal OS configuration files, currently using MacOS.

## Project Structure

The idea is simple, it mirrors the actual directory structure of `$HOME/`.
Just adding a leading dot for files in the root directory.

> ⚠️ There might be exceptions that don't follow the structure; there are
`README.md` files in such directories specifying this deviation.

It can also be easily seen by looking at the [install.conf.yaml](install.conf.yaml)
file, in the `link` directive.

## Setup

To install your dotfiles on a new machine or after updates:

```bash
git clone git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./install
```

The [Dotbot](https://github.com/anishathalye/dotbot)'s script is idempotent, can be ran many times.

## Customization

Edit the [install.conf.yaml](install.conf.yaml) file and re-run the [install](install) script.

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

## Updating packages

### Brew

```bash
# Install a package.
brew install <package_name>

# Update all supported packages into a single file (~/.Brewfile).
brew bundle dump --global --force --describe

# Upgrade all items in the Brewfile.
brew bundle upgrade --global
```

## The Complete Z Shell Load Order

> Just a reminder: when you open a new terminal window, Zsh reads configuration files in this specific sequence.

1. `~/.zshenv`: Always loaded first for every Zsh session (including scripts).
2. `~/.zprofile`: Loaded only for login shells. On macOS, every new terminal window is treated as a login shell by default.
3. `~/.zshrc`: Loaded for interactive shells. This is where most of your day-to-day configuration lives.
4. `~/.zlogin`: Loaded last, but only for login shells.
