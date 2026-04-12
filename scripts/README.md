# Scripts

This directory contains scripts to:

- Idempotently install the dotfiles configuration ([install-dotfiles.sh](install-dotfiles.sh))
- Update coding agents ([update-coding-agents.sh](update-coding-agents.sh))

## Update Coding Agents

It will update the following:

- [AI Gentle Stack](https://github.com/Gentleman-Programming/gentle-ai)
- [Globally installed skills](https://skills.sh/)
- [Superpowers](https://github.com/obra/superpowers)

### Usage

```bash
just update-ca
```

## Development

When modifying the setup scripts, make sure to use ShellCheck to analyze for bugs.

```bash
just check
```
