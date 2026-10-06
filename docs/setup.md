# Set up a workstation

Read this before installing. This is a personal **Apple Silicon macOS** setup, with partial Debian
support. Review the configuration before applying it to another account.

## Before you start

- Back up existing dotfiles. [Dotbot configuration](/install.conf.yaml) enables backups and forced
  replacement; installation replaces configuration, installs packages and changes the login shell.
- Review the [Brewfile](/home/.Brewfile), [Mise tools](/home/.config/mise/config.toml),
  [SSH hosts](/home/.ssh/config) and [AWS profiles](/home/.aws/config). The login shell selects the
  `waldo` AWS profile. Credentials are not supplied.
- macOS uses Homebrew at `/opt/homebrew`; Intel Macs are not handled. Debian uses
  `/home/linuxbrew/.linuxbrew` and `apt-get`. The Brewfile includes macOS casks without Linux guards;
  this is not an unattended cross-platform installer.
- Use an interactive terminal for sudo, Touch ID and login-shell prompts.

If Git is missing, install it first. On macOS, finish the command-line tools installer:

```sh
xcode-select --install
```

On Debian:

```sh
sudo apt-get install -y git
```

## Install the dotfiles

```sh
git clone --recurse-submodules https://github.com/waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./scripts/install-dotfiles.sh
```

Dotbot updates submodules, links configuration, enables Touch ID for sudo on macOS, installs
Homebrew packages and Mise tools, then selects Homebrew Zsh. See the
[script reference](/scripts/README.md) for exact responsibilities.

This command does **not** run the coding-agent updater or install this repository's Git hooks.
The three [copy-managed agent files](/docs/coding-agents.md) are populated by the updater, not Dotbot.

## Add local settings

Create `~/.gitconfig.local` with your identity before committing; follow
[Git configuration](/docs/git-configuration.md#setting-up-gitconfiglocal) for signing and
per-directory overrides.

Use `~/.zprofile.local` for session environment overrides and `~/.zlogin.local` for the welcome
name. Read [local shell configuration](/docs/zsh-configuration.md#machine-local-configuration)
first. Keep credentials and these local files outside the repository.

## Finish agent setup

Open a new terminal, then read [coding agents](/docs/coding-agents.md) before running:

```sh
cd ~/.dotfiles
just update-ca
just hooks
```

**`just update-ca` can commit and push skill-lockfile changes**, including other unpushed commits
on the branch. Run it only when publication is intended and your Git identity and remote access
are ready. Supply your personal `~/AGENTS.md` if you use OMP's configured append link.

## Verify

```sh
readlink ~/.gitconfig
just --list
```

The link should resolve to this checkout's `home/.gitconfig`; the recipe list includes `sync`,
`update-ca` and lint commands. This checks the link and task runner, not every integration.

For later updates, use [Sync the workstation](/docs/tooling.md#sync-the-workstation).
