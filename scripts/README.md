# Scripts

This directory contains scripts to:

- Idempotently install the dotfiles configuration ([install-dotfiles.sh](install-dotfiles.sh))
- Set Homebrew zsh as the default shell ([set-default-shell.sh](set-default-shell.sh))
- Update coding agents ([update-coding-agents.sh](update-coding-agents.sh))

## Set Default Shell

Sets Homebrew's zsh as the default shell. Idempotent — skips each step if already done.
May prompt for a password to write to `/etc/shells` and to run `chsh`.

Runs as part of `just setup`.

## Update Coding Agents

It will update the following:

- [Globally installed skills](https://skills.sh/)

### Usage

```bash
just update-ca
```

## Development

When modifying the setup scripts, make sure to use ShellCheck to analyze for bugs.

```bash
just lint-sh
```
