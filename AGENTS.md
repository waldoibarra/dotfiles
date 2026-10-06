# Dotfiles

Personal workstation configuration for Apple Silicon macOS and partial Debian support.
`home/` mirrors `$HOME`. [Dotbot](/install.conf.yaml) links most files; the agent updater copies
four configs and generates machine-local assets.

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
- **Do not use `just sync`, `just brew` or `just update-ca` as validation.** Sync and Brew can remove
  packages; sync and the agent updater can commit and push, including other unpushed commits.
  Obtain publication authorization before invoking either publishing workflow.
- Use a PTY and wait for user authentication when running an authorized workflow that needs it.

## Read before changing

| Area | Guide |
| --- | --- |
| Installation or local overrides | [Setup](/docs/setup.md) |
| Packages, recipes, lint or hooks | [Tooling](/docs/tooling.md) |
| Agent prompts, settings, integrations or skills | [Coding agents](/docs/coding-agents.md) |
| Zsh startup files | [Zsh configuration](/docs/zsh-configuration.md) |
| Git defaults, identity or signing | [Git configuration](/docs/git-configuration.md) |
| Installer or updater scripts | [Scripts](/scripts/README.md) |
| Design tooling | [Agent UI design tools](/docs/agent-ui-design-tools.md) |
