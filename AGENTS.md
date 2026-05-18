# AI Instructions for dotfiles

## Architecture Overview

Personal dotfiles for macOS (primary) and Debian Linux (partial).

The [`home/`](home/) directory mirrors `$HOME` and every config file is
symlinked there by Dotbot.

## Conventions

### Do

- Ask one clarifying question at a time — don't front-load multiple questions.
- When unsure about a claim, look it up before defending it.
- Propose a plan and confirm before implementing non-trivial changes.
- Investigate first before defending a position.
- **Atomic commits.** One concern per commit.
- If a change affects documented behaviour, update the docs in the same commit.
- When the user says "do you agree?", give an honest answer with reasoning — don't just validate.
- Prefer explicit, descriptive naming over short but ambiguous names.

### Don't

- **Never edit files directly in `$HOME`.** Always edit the source under `home/` and run
  `just sync` to apply.
- Don't over-engineer. If something adds complexity without clear benefit, the user will reject it.
- Don't jump into implementation before discussing tradeoffs on non-trivial decisions.

## Reference docs

- [`docs/tooling.md`](/docs/tooling.md) — just, hk, committed, Homebrew, mise.
- [`docs/zsh-configuration.md`](/docs/zsh-configuration.md) — zsh startup files and `.local` overrides.
- [`scripts/README.md`](/scripts/README.md) — what each script does and when it runs.
