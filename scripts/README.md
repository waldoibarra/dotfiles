# Scripts

This directory contains scripts to:

- Idempotently install the dotfiles configuration ([install-dotfiles.sh](install-dotfiles.sh))
- Install Homebrew (and its packages), Mise (and its tools), Git hooks, and sets Zsh (from Brew) as
  default Shell ([install-os-packages.sh](install-os-packages.sh))
- Update coding agents ([update-coding-agents.sh](update-coding-agents.sh))

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
