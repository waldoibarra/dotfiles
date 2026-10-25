# Documentation conventions

Use this reference for entrypoints, shared language, filenames, links, and retention.
The `docs` entrypoint owns the workflow; its structure reference owns information architecture and
page-purpose guidance.

**House conventions take precedence over generic templates and external recommendations across
maintained documentation.**
AI-assisted drafts are permitted within authorized scope.
Verify their claims, commands, boundaries, and links before acceptance.

## Contents

- [Lead with the reader's need](#lead-with-the-readers-need)
- [README.md](#readmemd-earn-the-readers-interest)
- [AGENTS.md](#agentsmd-define-the-working-contract)
- [Share language](#share-language)
- [Installed formats](#reuse-installed-artifact-formats)
- [Links and names](#link-and-name-consistently)
- [Preservation](#preserve-what-matters)

## Lead with the reader's need

**Each page serves a reader's question.** Lead with its answer, then the evidence or action needed.
Keep terminology consistent with the project's glossary and claims consistent with inspected
sources.

## README.md: earn the reader's interest

**The repository README is a human-facing entrypoint. Start with why, then what; link to how.**
Use a marketing mindset: help readers recognize the problem, value, and fit. Avoid unsupported
claims.

1. **Why:** Open with the problem and benefit in one or two plain-language sentences.
2. **What:** Explain what the project provides, who benefits, and meaningful scope or limitations.
3. **How:** Link to canonical setup, usage, contribution, and maintenance guides when those concerns
    exist.

- Make the opening understandable on a quick scan; avoid unexplained jargon and feature inventories.
- Use screenshots, logos, or diagrams when they clarify value or explain the project.
- Keep installation steps and runnable quick starts in linked guides; avoid duplicating their
  commands here.
- Make the next action obvious through descriptive links, including prerequisites where relevant.
- Link contribution and license information when applicable; do not invent sections merely to fill a
  template.
- Prefer a concise landing page over a comprehensive manual or an arbitrary section list.
- Add a contents list when navigation needs it. First check whether detail belongs in linked
  documentation.

## AGENTS.md: define the working contract

**AGENTS.md owns operational instructions for agents; README.md owns the human introduction.**
Use `agents-md` for authoring, auditing, and loading checks; these house conventions govern content
choices.

- State repository-specific commands, prerequisites, verification expectations, hidden constraints,
  and actionable gotchas.
- Verify commands against maintained scripts or configuration; distinguish inspected commands from
  safely exercised commands.
- Make required actions, approval boundaries, and prohibited actions explicit where they affect real
  work.
- Keep universal repository rules at the root; place narrower instructions with their owning scope.
- Link specialized procedures and explanations with reading triggers instead of copying them into
  the root.
- Preserve critical safety boundaries inline; check client loading before relying on scoped
  instructions.
- Prefer direct, task-relevant instructions over a rigid persona or generic claims of expertise.
- Let formatters and linters own enforceable style; document exceptions and necessary commands, not
  duplicated style manuals.
- Include paths when they reveal non-obvious ownership or guide action; omit exhaustive directory
  trees.
- Keep every rule necessary and concise; no universal line limit replaces scope, safety, and loading
  checks.
- Do not repeat the README pitch, shared policy, or discoverable facts without operational value.

Treat external performance claims as unverified unless their evidence supports the specific claim.
Neither authorship nor line count proves instruction quality; check loading and observed behavior
separately.

## Share language

**Contract:** Each maintained repository or vault has a root `GLOSSARY.md` for its domain terms.
Read it before choosing terminology; use `GLOSSARY-MAP.md` when multiple established contexts
require separate glossaries.
Define existing concepts precisely; do not invent product commitments or pad the glossary with
generic dictionary terms.
Keep implementation details and procedures outside definitions; use `domain-modeling` for glossary
work.
Read `~/.agents/skills/domain-modeling/GLOSSARY-FORMAT.md` before editing; preserve local meaning when
adopting its structure.
Capture newly settled, reusable terms during authorized sessions; clarify conflicting meanings
before recording them.
Read-only requests and local approval rules still govern writes; propose updates when authority is
absent.
No glossary entry is required when a session establishes no new domain language.
If absent during authorized maintenance, add grounded definitions and link them from the overview
and instructions.
For read-only or narrower work, report the missing glossary without expanding write authority.

## Reuse installed artifact formats

Use the owning installed skill's template or format before designing another artifact structure.
For glossary and ADR formats, use `domain-modeling` from [Matt Pocock's
skills](https://github.com/mattpocock/skills).
An available ADR template does not bypass the ADR gates or authorize creating a record.
Other artifacts use their applicable specialist's format; house conventions and local contracts
retain precedence.
Link the canonical format instead of copying its instructions into multiple documents.
Report missing templates before dependent work; do not modify external installed skills or update
them implicitly.

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
Exclude repository-root `raw/` from linters and automatic formatters when maintaining project
tooling.
Use native exclusions; Git ignores alone do not establish linter coverage.
Verify exclusions with invalid source fixtures and confirm equivalent maintained files still fail
checks.

Read `~/.agents/references/memory.md` before changing decision status, retention, or ADR guidance.
Read `~/.agents/references/communication-rules.md` before writing.
Safety warnings and source quotations retain their wording.
