# Learnings

Temporary file. Will be used to draft the final AGENTS.md.

## Meta

- Always research and apply best practices before implementing anything — don't default to the
  first working solution.
- Before writing the final AGENTS.md, research best practices for AGENTS.md files specifically:
  what agents need, what format works best, what sections are essential.

## Shell Scripts

- New shell scripts must be added to `just lint-sh` immediately — don't leave them unlinted.
- Use `set -euo pipefail` for safety. Use `local -r` for read-only locals.
- When a script is idempotent, make each sub-step independently idempotent with a guard check,
  and print a clear message for both the skip and the run case.
- `$(brew --prefix)/bin/zsh` is the correct way to reference the Homebrew zsh — works on both
  Apple Silicon (`/opt/homebrew`) and Intel (`/usr/local`) Macs.
- Use `grep -qx` to match a whole line exactly in `/etc/shells` — `-qF` doesn't anchor the match.
- Always update `scripts/README.md` when adding a new script.
- Duplicate `### Usage` headings across sections in the same markdown file will fail MD024.
  Either rename headings or remove the redundant one and reference the right recipe inline.

## Linters and Tools

- Each linter needs its own `just lint-*` recipe — don't use hk builtins directly.
- Add the linter's config file to the hk step glob so the step re-runs when config changes.
- Always exclude `dotbot/` from every linter — it's a submodule we don't own.
- Tool choices: prefer self-contained binaries (Go, Rust) over tools that require a runtime
  dependency when both options are equivalent. Avoids accidental coupling.
- After adding a linter, always run `just check-hooks` before committing to verify it passes
  against all files in the repo.
- `ec` (editorconfig-checker) catches violations across all files — run it early to surface
  issues like tabs in git config files, missing final newlines, and long lines.
- Git config files (`.gitconfig`, `.gitmodules`) use tabs by design — add `.editorconfig`
  overrides rather than fighting the format.
- When a file legitimately can't conform to a rule (URLs, shell commands in YAML), add an
  `.editorconfig` override scoped to that file rather than disabling the rule globally.

## hk

- hk's `exclude` filters which files trigger a step and are passed as `{{files}}`, but if the
  `just` recipe does its own file discovery (e.g. `markdownlint-cli2 "**/*.md"`), hk's exclusion
  has no effect — the tool finds files itself. Submodule exclusions must also live in the tool's
  own config file.
- Commit subjects must be ≤50 chars. Use the body to explain why, the footer for metadata.
- When a linter runs via a `just` recipe rather than receiving `{{files}}` from hk, the glob in
  the hk step is only used to decide _whether_ to trigger the step — not to scope what the tool
  lints.

## AGENTS.md Best Practices (Research-backed)

- Auto-generated AGENTS.md files reduce task success rates — always write it by hand.
- Codebase overviews don't help agents navigate faster — skip directory trees and file listings.
- Code style guidelines don't belong here — linters and formatters handle that deterministically.
- Task-specific instructions that only apply sometimes dilute focus — keep it universal.
- Tools mentioned in AGENTS.md get used 160x more often — explicitly name mise, just, hk, etc.
- Keep it under 300 lines; aim for under 100. Every line goes into every session.
- Use progressive disclosure: keep AGENTS.md short, point to other files for task-specific detail.
- Prefer pointers (`file:line`) over embedded code snippets that go stale.
- The HOW is what matters most: build, test, verify commands and non-obvious tooling choices.

## AGENTS.md Best Practices (OpenCode)

- `AGENTS.md` should be a concise entry point, not a document that duplicates existing docs.
- Use the `instructions` field in `opencode.json` to automatically include other files
  (e.g. `README.md`, `scripts/README.md`) — this is the recommended approach.
- Alternatively, use lazy-loading instructions in `AGENTS.md`: tell the agent to read specific
  files on demand when relevant to the task, not preemptively.
- Most of what an agent needs is already documented in this repo: `README.md`,
  `scripts/README.md`, `justfile`, `hk.pkl`, `mise.toml`. AGENTS.md should orient and route,
  not repeat.
- Pattern: AGENTS.md = project overview + key conventions + pointers to where detail lives.

## Repository

- `home/` mirrors `$HOME`. Every config file lives here and is symlinked by Dotbot.
- Never edit files directly in `$HOME` — always edit the source in `home/` and run `just sync`.
- `install.conf.yaml` is the OS bootstrap manifest (Dotbot). Its job is to configure the OS,
  not manage packages.
- `just sync` = full sync: Dotbot + Brew + Mise + coding agents. Safe to re-run anytime.
- Brew manages GUI apps and system-level packages. Mise manages developer tools and CLIs.
  Never add to Brew what Mise can manage.
- Global tools live in `home/.config/mise/config.toml`. Project-level tools live in `mise.toml`
  at the repo root.
- Shell scripts all live under `scripts/` and must have `.sh` extensions. ShellCheck config lives
  at `scripts/.shellcheckrc`.
- All shell scripts must pass `just lint-sh` (shellcheck) before committing. hk enforces this
  automatically on pre-commit.

## Code Style

- Shell: bash, two-space indent, shellcheck-clean, formatted with shfmt.
- YAML/TOML/JSON: two-space indent, LF, UTF-8, no trailing whitespace.
- Commit messages: imperative mood, present tense, no period, concise
  (e.g. `Add shellcheck pre-commit hook with hk`).
- No commented-out code. No dead files. Git history is the backup — revert if needed.
- No stale notes or unresolved TODOs in docs.

## Git Hygiene

- Atomic commits. One concern per commit.
- Always check `git diff` and `git status` before committing to ensure the right files are staged
  and changes align with the current concern.
- Understand changes fully before committing — don't just stage and commit blindly.
- Amend is acceptable when the commit hasn't been pushed and the fix belongs to the same concern.
- Always test before committing.

## Zsh Configuration

- `.zshenv` is read for every process including scripts — keep it minimal, no side effects.
- `.zprofile` is for login-session setup (PATH, tool initializations, session-wide env vars).
- `.zshrc` is for interactive shell experience only (plugins, themes, aliases, completions).
- `.zlogin` is for login-only tasks that run after everything else is set up (e.g. welcome message).
- Scope machine-local overrides to the file that needs them — not `.zshenv`. A `~/.zlogin.local`
  sourced by `.zlogin` is the right pattern when only `.zlogin` needs the value.
- File-level comments that just describe the file's purpose belong in docs, not in the file itself.

## Markdown / Docs

- In GitHub-flavored Markdown, links starting with `/` are relative to the repository root —
  use them instead of `../` when linking to files from within a `docs/` subdirectory.
- Rename a doc file to match its `# Title` heading for consistency.

## Working with the User

- Ask one clarifying question at a time — don't front-load multiple questions.
- Propose a plan and confirm before implementing non-trivial changes.
- When the user pushes back, investigate first before defending a position — they are often right.
- Don't over-engineer. If something adds complexity without clear benefit, the user will reject it.
- The user values clean separations of concern: bootstrap vs maintenance, global vs local,
  manual vs automated.
- The user thinks in atomic commits and will catch if changes from different concerns are mixed.
- The user expects docs to stay accurate. If a change affects documented behaviour, update the
  docs in the same commit.
- The user will catch dead code, stale references, and misleading wording. Proactively remove them.
- When the user says "do you agree?", give an honest answer with reasoning — don't just validate.
- Anticipate follow-up: after implementing something, consider what the user is likely to notice
  or ask next and address it proactively.
- The user prefers explicit, descriptive naming (e.g. `install-local-tools`, `install-git-hooks`)
  over short but ambiguous names.
- The user will ask "why?" if an argument doesn't hold up to scrutiny. Make sure reasoning is
  sound before stating it.
- Don't jump into implementation before discussing tradeoffs on non-trivial decisions — the user
  will call it out.
- When unsure about a claim, look it up before defending it — the user is often right and will
  push back until you verify.
