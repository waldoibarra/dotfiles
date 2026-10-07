# Dotfiles

Personal workstation configuration for Apple Silicon macOS and partial Debian support.
`home/` mirrors `$HOME`. [Dotbot](/install.conf.yaml) links most files; the agent updater copies
three configs and generates machine-local assets.

## Commands

Run from the repository root:

- `just --list`: list recipes.
- `just lint`: run all checks. For one area: `just lint-sh`, `just lint-md`, `just lint-yaml` or
  `just lint-ec`.
- No application build or test recipe exists. Smoke-run changed behavior in an isolated environment.

## Guardrails

- Edit tracked sources under `home/`, not installed copies. Symlink edits affect this repository;
  copied agent files are overwritten on sync. Read the agent guide before changing either.
- Keep credentials, identities, signing keys and machine-local overrides outside the repository.
  Use `$HOME`, supported `~` expansion or native path handling, never absolute personal home paths.
- **Run `dots` only when a change must reach `$HOME` or targets the sync path, and announce it
  first.** Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running it.
  Never run `just brew` alone as validation; it can remove packages.

## Read before changing

| Area | Guide |
| --- | --- |
| Installation or local overrides | [Setup](/docs/setup.md) |
| Packages, recipes, lint or hooks | [Tooling](/docs/tooling.md) |
| Agent prompts, settings, integrations or skills | [Coding agents](/docs/coding-agents/README.md) |
| Zsh startup files | [Zsh configuration](/docs/zsh-configuration.md) |
| Git defaults, identity or signing | [Git configuration](/docs/git-configuration.md) |
| Installer or updater scripts | [Scripts](/scripts/README.md) |
| Design tooling | [Agent UI design tools](/docs/agent-ui-design-tools.md) |
