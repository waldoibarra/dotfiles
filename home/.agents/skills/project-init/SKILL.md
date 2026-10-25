---
name: project-init
description: >-
  Initializes empty project directories for requirements and POCs without choosing an application stack.
  Includes mise, grouped just recipes, Markdown linting, and Git-message hooks.
  Use when asked to "start a new project" or "initialize this empty directory".
  Also use for "set up the bare minimum" when no application stack is requested.
compatibility: Requires Git, mise, just, Node.js for Markdown linting, and network access for missing tools.
---

# Initialize an empty project

**Outcome:** Establish a stack-free local baseline with minimal grounded documentation and working
lint hooks.
Use `scaffold-nextjs` or `scaffold-cli` when an application stack is explicitly requested.
This workflow does not create a remote, commit, publish, or deploy without a separate request.

## Check the destination

1. Inspect the directory, hidden files, and any enclosing Git repository.
2. Accept an existing empty `.git/`; ask before adapting a nonempty project.
3. Do not initialize a nested repository without approval.
4. Use the directory name as the title unless the user supplied one.
5. Ask only for missing decisions; no stack interview is needed.

## Establish the tool baseline

Confirm Git, mise, just, and Node are available before setup.
Report missing prerequisites instead of installing global tools without approval.
Reuse workstation runtimes; add no project runtime pins or package manifest solely for these
linters.

Read and copy the five templates below; paths resolve relative to this skill.
Preserve their tested versions unless a demonstrated compatibility issue requires an update.

| Template | Project destination |
| --- | --- |
| [Mise tools](assets/mise.toml) | `.mise.toml` |
| [Recipes](assets/justfile) | `justfile` |
| [Git hooks](assets/hk.pkl) | `hk.pkl` |
| [Commit rules](assets/committed.toml) | `committed.toml` |
| [Markdown rules](assets/markdownlint-cli2.yaml) | `.markdownlint-cli2.yaml` |

**Defaults:** Mise pins project tools; grouped just recipes expose setup through `just setup`.
Install repository-local hooks through mise and hk, retaining Markdown and conventional-commit
checks.
Preserve `raw/` exclusions; exclude source material when adding other linters or formatters.
Respect inherited EditorConfig settings and add an EditorConfig check when extending file checks.

Add `just run` only when an application exists, not as a placeholder.
Use Docker for prototype databases or emulatable infrastructure, rather than host-installed servers.
Do not add services to this baseline or containerize the application by default.

## Write only grounded project context

1. Create `README.md` with a title and `To be defined.` unless scope is already known.
2. Create `AGENTS.md` with a title and one or two sentences describing known scope and unresolved
    stack.
3. Add `GLOSSARY.md` with confirmed domain terms, linked from the overview and instructions.
4. If no terms are known, ask for the first concepts instead of inventing definitions or empty
    scaffolding.

Use `docs` conventions for known README content and `agents-md` for the instruction-file contract.
Do not add plans, decision tables, architecture documents, or command documentation at this stage.

## Initialize and verify locally

1. Reuse effective home EditorConfig and global Git ignores.
2. Initialize Git if needed, retaining the configured default branch.
3. Check `.env` and `.DS_Store` with `git check-ignore -v --no-index` after initialization.
4. Add only missing ignore patterns locally; never change global files during project setup.
5. Run `mise trust`, then `mise exec -- just setup`.
6. Run `mise exec -- just lint` and inspect `mise exec -- just --list`.
7. Exercise both installed hooks with valid and invalid disposable inputs.
8. Use a temporary Git index for staged fixtures; leave no test commits or fixtures behind.

Keep secrets untracked and verify project-specific secret paths before staging.
Git ignores do not protect already tracked files.
Stop when setup and hook checks pass; report missing prerequisites or failed checks precisely.

## Avoid known setup failures

- Direct recipe commands require the mise environment; use `mise exec -- just` when it is inactive.
- Home EditorConfig applies beneath home only; nearer `root = true` stops inheritance.
- `committed` exempts unbreakable tokens from wrapping limits; test length rejection with ordinary
  prose.
- `hk` does not support a `quote` template filter here; retain the tested quoted argument.

**Maintenance:** Read `evals/evals.json` when changing this skill; scenarios are not executed
behavioral results.
