# Documentation conventions

Read before naming, organizing, or editing maintained documentation.

## Explain before detailing

- Give each document one concern and audience. Keep facts with their owner; link instead of
  duplicating.
- Match the code, explain what and why first, then reveal detail as needed.
- Keep root READMEs human-facing: purpose, then links for setup, use, and maintenance. Add visuals
  when useful.
- Split by concern, never convenience; keep task instructions separate from history and reference
  facts.
- Describe links with reading triggers: `Read <doc> before <action>.`

## Share language

**Contract:** Each maintained repository or vault has a root `GLOSSARY.md` for its domain terms.
Read it before choosing terminology; use `GLOSSARY-MAP.md` when multiple established contexts
require separate glossaries.
Define existing concepts precisely; do not invent product commitments or pad the glossary with
generic dictionary terms.
Keep implementation details and procedures outside definitions; use `domain-modeling` for unresolved
meanings.
If absent during authorized maintenance, add grounded definitions and link them from the overview
and instructions.
For read-only or narrower work, report the missing glossary without expanding write authority.

## Link and name consistently

- Prefer repository-root Markdown links; use portable relative links inside installable bundles.
- Use relative links in vaults; follow destination rules when linking across documents.
- Commit screenshots only when documentation needs them; reviewer aids belong in PRs.
- Name files lowercase kebab-case, with docs under `docs/`.
- Keep uppercase root conventions: `README.md`, `AGENTS.md`, `CHANGELOG.md`, `LICENSE`,
  `GLOSSARY.md`, `GLOSSARY-MAP.md`, and `STRUCTURE.md`.
- Preserve required names such as `SKILL.md`, `Dockerfile`, and `justfile`.
- Preserve language conventions such as Python `snake_case`, React `PascalCase`, dotfiles, and
  lockfiles.
- Keep existing justified local filenames until an authorized migration repairs all incoming links.

## Preserve what matters

**Current content:** Correct or retire stale operational guidance within the authorized task.
**Historical content:** Preserve consequential rationale with explicit status and successor links
outside default reading paths.
**Protected content:** Leave frozen snapshots, original sources, generated output, and vendored
material to their owning process.

Read `~/.agents/references/memory.md` before changing decision status, retention, or ADR guidance.
Read `~/.agents/references/communication.md` before writing; safety warnings and source quotations
retain their wording.
