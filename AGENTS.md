# Dotfiles

Personal workstation configuration for Apple Silicon macOS and partial Debian support.
`home/` mirrors `$HOME`; Dotbot links most files, while the updater copies Claude settings and
renders client assets.

## Commands

Run from the repository root:

- `just --list`: list recipes.
- `just lint`: run all static checks.
- `just lint-sh`, `just lint-md`, `just lint-yaml`, `just lint-ec`: check one area.
- `python3 scripts/tests/test-agent-harness.py`: check isolated harness delivery; compiled-host
  checks need `PI_PACKAGE_DIR`.
- `python3 scripts/tests/test-cursor-rule.py`: check isolated Cursor rendering.

No application build or test recipe exists. Smoke-run changed behavior in an isolated environment.
Shared skill Markdown may be Git-ignored; validate edited files through stdin as documented in
[tooling](/docs/tooling.md).

## Guardrails

- Keep setup declarative; automate repeatable steps and document unavoidable manual actions.
- Scripts MUST be idempotent: unchanged inputs and desired state must not cause repeated mutations.
- Read [idempotency checks](/scripts/README.md#idempotency) before adding or changing scripts.
- Edit tracked sources under `home/`, not installed copies; symlink edits affect this repository.
- Read [agent ownership](/docs/coding-agents/README.md#file-ownership) before changing copied or
  generated configuration.
- Keep credentials, identities, signing keys and machine-local overrides outside the repository.
  Use `$HOME`, supported `~` expansion or native path handling, never absolute personal home paths.
- **Run `dots` only when a change must reach `$HOME` or targets the sync path, and announce it
  first.** Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running it.
  Never run `just brew` alone as validation; it can remove packages.

## Navigate before changing

Read [the glossary](/GLOSSARY.md) before domain edits and [architecture](/docs/architecture.md)
before changing ownership boundaries.
Read only relevant sections; old plans and transcripts do not override current guidance or grant
approval.

| Area | Guide |
| --- | --- |
| Documentation structure, stale guidance, or decision retention | [Documentation workflow](/docs/documentation.md) |
| Installation and local overrides | [Setup](/docs/setup.md) |
| Packages, recipes, lint, and hooks | [Tooling](/docs/tooling.md) |
| Agent prompts, settings, integrations, and skills | [Coding agents](/docs/coding-agents/README.md) |
| Installer and updater scripts | [Scripts](/scripts/README.md) |

| Area | Guide |
| --- | --- |
| Zsh startup | [Zsh configuration](/docs/zsh-configuration.md) |
| Git defaults, identity, and signing | [Git configuration](/docs/git-configuration.md) |
| Design tooling | [Agent UI design tools](/docs/agent-ui-design-tools.md) |
| Plans, trial notes, spikes, and research evidence | [Workspace index](/.agents/README.md) |

Update the workspace index whenever adding, moving, or removing records or evidence collections.
Keep frozen snapshots and original sources intact; mark historical guidance without rewriting its
evidence.
