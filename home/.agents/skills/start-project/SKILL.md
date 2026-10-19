---
name: start-project
description: >-
  Sets up empty project directories for requirements and POCs using mise, grouped just recipes,
  Markdown linting, and Git-message hooks. Use when asked to "start a new project",
  "initialize this empty directory", or "set up the bare minimum" without choosing an application stack.
compatibility: Requires Git, mise, just, Node.js for Markdown linting, and network access for missing tools.
---

# Start Project

- **IS:** a stack-free local baseline for an empty directory, including working lint hooks.
- **IS NOT:** application scaffolding; use `scaffold-nextjs` or `scaffold-cli` when explicitly requested.

## Setup defaults

- Use mise for project tools, with versions pinned in `.mise.toml`.
- Reuse workstation runtimes for this stack-free baseline.
- Use grouped just recipes; `just setup` owns setup.
- Add `just run` when an application exists, not a placeholder.
- Install repository-local Git hooks through mise and hk.
- Retain Markdown and conventional-commit checks from the templates.
- Respect inherited EditorConfig settings.
- Add an EditorConfig check when extending the baseline's file checks.
- Keep secrets untracked; verify project-specific secret paths are ignored before staging.
- Never rely on ignores for already tracked files.
- Use Docker, not host-installed servers, for prototype databases or emulatable infrastructure.
- Do not add services to the stack-free baseline or containerize the application by default.

## Workflow

1. Inspect the destination, including hidden files and any enclosing Git repository.
    - An existing empty `.git/` is fine; otherwise ask before adapting a nonempty directory.
    - Do not initialize a nested repository without approval.
2. Use the directory name for the title unless the user supplied a project name.
    - Ask only for missing decisions; no stack interview is needed.
3. Confirm Git, mise, just, and Node are available.
    - Reuse workstation runtimes; add no project runtime pins or package manifest for these linters.
    - Report missing prerequisites instead of installing global tools without approval.
4. Read and copy the five [templates](#templates) into the project root.
    - Preserve the tested versions; update only for a demonstrated compatibility problem.
5. Create `README.md` with a title and `To be defined.` unless scope is already known.
    - Create `AGENTS.md` with a title and one or two sentences stating known scope and unresolved
      stack.
    - Do not add plans, decision tables, architecture docs, or command documentation at this stage.
6. Reuse effective home EditorConfig and global Git ignores.
    - After Git initialization, check `.env` and `.DS_Store` with `git check-ignore -v --no-index`.
    - Add only missing ignore patterns locally; do not change global files during project setup.
7. Initialize Git if needed, retaining the configured default branch.
    - Run `mise trust`, then `mise exec -- just setup`.
8. Run `mise exec -- just lint` and inspect `mise exec -- just --list`.
    - Exercise both installed Git hooks with valid and invalid disposable inputs.
    - Use a temporary Git index for staged fixtures; leave no test commits or fixtures behind.

- Stop when local setup and hook checks pass.
- Report missing prerequisites or failed checks precisely.
- Commit, create remotes, publish, or deploy only when the user requests those actions.

## Templates

Read these files before copying them; paths resolve relative to this skill.

| Template | Project destination |
| --- | --- |
| [Mise tools](assets/mise.toml) | `.mise.toml` |
| [Recipes](assets/justfile) | `justfile` |
| [Git hooks](assets/hk.pkl) | `hk.pkl` |
| [Commit rules](assets/committed.toml) | `committed.toml` |
| [Markdown rules](assets/markdownlint-cli2.yaml) | `.markdownlint-cli2.yaml` |

## Gotchas

- Direct recipe commands require the mise environment; use `mise exec -- just` when it is not activated.
- Home EditorConfig applies beneath home only; a nearer `root = true` stops inheritance.
- Git ignores do not protect already tracked files.
- `committed` exempts unbreakable tokens from wrapping limits; test length rejection with ordinary prose.
- `hk` does not support a `quote` template filter in this baseline; retain the tested quoted argument.

**Maintenance only:** `evals/evals.json` contains authored scenarios, not executed behavioral results.
