# Set up a workstation

**Scope:** This setup targets Apple Silicon macOS, with partial Debian support.
Review the configuration before installing it for another account.

## Before you start

- Back up existing dotfiles. [Dotbot configuration](/install.conf.yaml) enables backups and forced
  replacement; installation replaces configuration, installs packages and changes the login shell.
- Review the [Brewfile](/home/.Brewfile), [Mise tools](/home/.config/mise/config.toml),
  [SSH hosts](/home/.ssh/config), and [AWS profiles](/home/.aws/config). Credentials are not supplied.
- macOS uses Homebrew at `/opt/homebrew`; Intel Macs are not handled.
  Debian uses `/home/linuxbrew/.linuxbrew` and `apt-get`.
  The Brewfile includes macOS casks without Linux guards;
this is not an unattended cross-platform installer.
- Export `LIFE_PROFILE` in `~/.zprofile.local` to select your directory under `~/life/people/`.
- Use an interactive terminal for sudo, Touch ID and login-shell prompts.

Git is required to clone the repository.
[Dotbot's launcher](/dotbot/bin/dotbot) requires Python 3.7+ to run; our wrapper checks `python3`.
Homebrew, Mise, and `just` are not prerequisites for initial installation.

**Clean-machine verification pending:** Neither clean macOS nor clean Debian installation has been exercised.
Fixture tests simulate prerequisites; successful `dots` runs used an already-provisioned workstation.
Python availability after platform setup remains unverified; a separate installation may be necessary.

If Git is missing, install it first. On macOS, finish the command-line tools installer:

```sh
xcode-select --install
```

On Debian:

```sh
sudo apt-get install -y git python3
```

Verify both prerequisites before continuing:

```sh
git --version
python3 --version
```

If macOS still lacks Python, install [Python 3](https://www.python.org/downloads/macos/)
and reopen the terminal.
The installer checks both prerequisites before changing submodules or invoking Dotbot.

## Install the dotfiles

```sh
git clone --recurse-submodules https://github.com/waldoibarra/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./scripts/install-dotfiles.sh
```

Dotbot updates submodules, links configuration, and enables Touch ID for sudo on macOS.
It then bootstraps packages sequentially:

1. Install Homebrew if absent and expose it on the installer's `PATH`.
2. Install missing Brewfile packages, including Mise, without requesting upgrades of existing declarations.
3. Trust the Mise configuration and install missing tools, including `just` and managed Python.
4. Configure the Markdown handler and select Homebrew Zsh.

Homebrew can still upgrade dependencies required by newly installed packages.
The wrapper exposes Homebrew's supported prefix to later Dotbot commands,
including the login-shell configuration.
See the [script reference](/scripts/README.md) for exact responsibilities.

Initial installation does not use the parallel coordinator or require `just`.
Later `dots` runs defer Mise tools to that coordinator and use Brew's no-upgrade bootstrap check.

This command does **not** run the coding-agent updater or install this repository's Git hooks.
The updater populates
[copy-managed Claude settings](ai-harness/README.md#copy-managed-files), not Dotbot.
Dotbot links Claude's global instructions directly to the shared source; no import adapter runs.
The updater renders
[Cursor's global instructions](ai-harness/README.md#cursor-global-instructions) as a regular file.

## Add local settings

Create `~/.gitconfig.local` with your identity before committing; follow
[Git configuration](/docs/git-configuration.md#setting-up-gitconfiglocal) for signing and
per-directory overrides.

Use `~/.zprofile.local` for session environment overrides and `~/.zlogin.local` for the welcome
name. Read [local shell configuration](/docs/zsh-configuration.md#machine-local-configuration)
first. Keep credentials and these local files outside the repository.

## Finish agent setup

Open a new terminal, then read [coding agents](ai-harness/README.md) before running:

```sh
cd ~/.dotfiles
just update-ca
just hooks
```

**`just update-ca` can commit and push skill-lockfile changes**, including other unpushed commits
on the branch. Run it only when publication is intended and your Git identity and remote access
are ready.

Mise installs Pi, Dotbot links its preferences and shared instructions, and `just update-ca`
installs `pi-live-codex`. Pi discovers `~/.agents/skills` without another copy. A fresh
workstation still needs its own subscription login and microphone permission. Credentials are
never supplied by the repository.

Start `pi`, use `/login openai-codex` to authorize your subscription, and check `/model` before
starting voice. Select device-code or browser login in Pi's prompt.
Then use `/live spruce` (or `/live`) and grant macOS microphone permission if requested.
This setup does not configure an API-key fallback.
Read [Pi and live voice](ai-harness/pi/README.md) for model defaults, controls, and limitations.
Restart an already-running Pi session after provisioning so it loads the new configuration.

## Shared life map

Waldo and Lluvia use a shared Obsidian vault at `~/life/`.
It holds goals, domain links, ideas, and agent coordination.
The vault is private and separate from this public-facing dotfiles repository.

Set `export LIFE_PROFILE="waldo"` or `export LIFE_PROFILE="lluvia"` in your untracked
`~/.zprofile.local`. Open a new login terminal so `dots` inherits the selected profile.
Read [local shell configuration](zsh-configuration.md#machine-local-configuration) before changing
profile selection. Agent updates warn if the vault exists but `LIFE_PROFILE` is empty or unset.

Agent updates link `~/.agents/personal-context.md` and `~/.agents/agent-identity.md`
into the selected profile.
Pi and Claude Code read these alongside `~/life/README.md`.
Cursor receives those reading instructions through its rendered global rule. Read
[personal profile routing](agent-instructions.md#personal-profile-routing) before provisioning links
or removing an old `~/AGENTS.md` selector.
Agent note edits are Markdown-only, with approved exceptions for declared plugins, lint
configuration, and the ruler.
Read [Obsidian setup](obsidian.md) before provisioning human formatting or agent checks on either
computer.

Both collaborators need active Obsidian Sync subscriptions. Obsidian's end-to-end encryption applies
to remote vault data; local files are not encrypted by Obsidian. Keep work and NDA-restricted
material outside the shared vault.

## Verify

```sh
readlink ~/.gitconfig
just --list
```

The link should resolve to this checkout's `home/.gitconfig`; the recipe list includes `sync`,
`update-ca` and lint commands. This checks the link and task runner, not every integration.

For later updates, use [Sync the workstation](/docs/tooling.md#sync-the-workstation).
