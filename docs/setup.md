# Set up a workstation

Read this before installing these dotfiles on a new machine. The repository contains personal
configuration for macOS and Debian; review and adapt it before applying it to your own account.

## Before you start

- Review [install.conf.yaml](/install.conf.yaml) for managed paths and installation actions.
  The [home directory](/home/) mirrors `$HOME`; Dotbot links its tracked files into your account.
  Some coding-agent files are copied instead. Read [coding agents](/docs/coding-agents.md)
  before changing those files.
- Back up existing configuration. Dotbot enables backup, force, and relink behavior; installation
  can replace files or links, install packages, configure Touch ID for sudo on macOS, and change
  your login shell to Homebrew Zsh.
- Review the [Brewfile](/home/.Brewfile) and [Mise configuration](/home/.config/mise/config.toml).
  Some desktop apps are macOS-only; see [platform limits](/docs/tooling.md#homebrew).
- Use your own interactive terminal. Installation may request sudo or Touch ID authentication.

## Install Git

If Git is unavailable on a fresh macOS installation, install the command-line tools and finish
any installer prompts before continuing:

```sh
xcode-select --install
```

On Debian:

```sh
sudo apt-get install -y git
```

## Clone and install

Run these 3 commands once for the initial setup:

```sh
git clone --recurse-submodules https://github.com/waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./scripts/install-dotfiles.sh
```

If GitHub SSH access is already configured, replace the clone command with:

```sh
git clone --recurse-submodules git@github.com:waldoibarra/dotfiles.git ~/.dotfiles
```

The installer runs [Dotbot](https://github.com/anishathalye/dotbot) with the repository's
configuration. It creates links and runs the package, Touch ID, and shell setup scripts.
See the [script reference](/scripts/README.md) for their responsibilities.

## Add machine-local settings

Create `~/.gitconfig.local` with your Git identity before committing. Read
[Git configuration](/docs/git-configuration.md#setting-up-gitconfiglocal) for the required
`[user]` block, optional signing, and per-directory identities.

Read [machine-local shell configuration](/docs/zsh-configuration.md#machine-local-configuration)
before adding session secrets or a custom welcome name. Keep these values outside the repository.

## Verify the setup

Open a new terminal so it loads the installed shell configuration. Check a representative link
and the task runner:

```sh
readlink ~/.gitconfig
cd ~/.dotfiles
just --list
```

The link should resolve to this checkout's `home/.gitconfig`. The recipe list should include
`sync`, `update-ca`, and the lint commands. This checks the link and task runner; it does not
prove every package or external integration is configured.

For subsequent updates, follow [Sync the workstation](/docs/tooling.md#sync-the-workstation).
Do not reclone the repository. Review the package-removal behavior before running a full sync.
