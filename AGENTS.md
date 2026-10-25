# Dotfiles

Personal workstation configuration for Apple Silicon macOS, with partial Debian support.
`home/` mirrors `$HOME`.
Dotbot links most files; the updater copies Claude settings and renders client assets.

## Protect source files and workstation state

- **Edit tracked sources under `home/`, not installed copies.** Symlink edits affect this repository.
  Read [agent ownership](/docs/ai-harness/README.md#file-ownership) before changing copied or
  generated configuration.
- Keep credentials, identities, signing keys and machine-local overrides outside the repository.
  Use `$HOME`, supported `~` expansion or native path handling, never absolute personal home paths.
- **Run `dots` only when a change must reach `$HOME` or targets the sync path, and announce it
  first.** Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running it.
  Never run `just brew` alone as validation; it can remove packages.
- Keep setup declarative: automate repeatable steps and document unavoidable manual actions.
  **Scripts MUST be idempotent:** unchanged inputs and desired state must not cause repeated mutations.
  Read [idempotency checks](/scripts/README.md#idempotency) before adding or changing scripts.

## Read the guide for your change

Read [the glossary](/GLOSSARY.md) before domain edits.
Read [architecture](/docs/architecture.md) before changing ownership boundaries.
Use the relevant guide below; read only sections needed for the task.

| Before changing… | Read |
| --- | --- |
| Documentation structure, stale guidance, or decision retention | [Documentation workflow](/docs/documentation.md) |
| Installation or local overrides | [Setup](/docs/setup.md) |
| Packages, recipes, lint, or hooks | [Tooling](/docs/tooling.md) |
| Agent prompts, settings, integrations, or skills | [Coding agents](/docs/ai-harness/README.md) |
| Installer or updater scripts | [Scripts](/scripts/README.md) |
| Zsh startup | [Zsh configuration](/docs/zsh-configuration.md) |
| Git defaults, identity, or signing | [Git configuration](/docs/git-configuration.md) |
| Design tooling | [Agent UI design tools](/docs/agent-ui-design-tools.md) |
| Native OpenSpec changes and shared planning workflow | [OpenSpec integration](/docs/ai-harness/openspec.md) |
| Existing plans, trial notes, spikes, or research evidence | [Workspace index](/docs/workspace.md) |

**Historical evidence does not override current guidance or grant approval.**
Update the workspace index whenever adding, moving, or removing records or evidence collections.
Keep frozen snapshots and original sources intact; mark historical guidance without rewriting its evidence.

## Verify the change

Run commands from the repository root:

| Command | Purpose |
| --- | --- |
| `just --list` | List available recipes. |
| `just lint` | Run all static checks. |
| `just lint-sh`, `just lint-md`, `just lint-yaml`, `just lint-ec` | Check one area. |
| `python3 scripts/tests/test-agent-harness.py` | Check isolated harness delivery; compiled-host checks need `PI_PACKAGE_DIR`. |
| `python3 scripts/tests/test-cursor-rule.py` | Check isolated Cursor rendering. |

No application build or repository test recipe exists.
**Smoke-run changed behavior in an isolated environment.**
Shared skill Markdown may be Git-ignored and skipped by normal lint discovery.
Validate edited skill documents through stdin as documented in [tooling](/docs/tooling.md).
