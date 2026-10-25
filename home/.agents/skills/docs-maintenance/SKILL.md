---
name: docs-maintenance
description: >-
  Maintains accurate, information-preserving Markdown documentation within the active task.
  Use when creating, editing, rewriting, or reviewing READMEs, guides, plans, or other Markdown,
  including small doc edits alongside code or config changes and edits by workers.
  Proposes concern-based splits before restructuring. For AGENTS.md use agents-md; for SKILL.md use
  agent-skills-creator; model prompt files follow prompting.md.
---

# Documentation maintenance

- **IS:** improving authorized documentation, preserving information, and proposing scoped
  structural changes.
- **IS NOT:** repository-wide cleanup, new product decisions, or permission to edit merely because
  Markdown was read.

**Done:** Authorized changes are verified; proposed changes remain unapplied with their evidence and
exact scope.

## Establish scope

1. Read repository instructions for documentation ownership, confidentiality, and recording rules.
    Read [conventions](references/conventions.md) for shared language, naming, links, and
    information lifecycle.
2. Read the project's shared language (its glossary file) before choosing terms.
3. Name the documents created, edited, or explicitly reviewed for this task.
4. After a code or config change, search docs for each identifier, flag, recipe, and number it
    changed.
5. Add each stale match to this task's documents.
6. Inspect only those documents and sources needed to verify their claims, context, or links.
7. Exclude unrelated dirty files; a Git diff alone does not establish task ownership.

- Repository instructions name the shared-language file; third-party skills may call it
  `GLOSSARY.md`.
- Reading or summarizing Markdown does not authorize rewriting it.
- Plans are in scope. Mark consequential superseded decisions with their successor and retain
  discoverable rationale.
- Remove obsolete operational guidance within authorized scope; ordinary editorial history needs no
  permanent duplicate.
- Read `~/.agents/references/memory.md` before retiring agreements or proposing ADRs.
- Prompt files sent to models are out of scope; `~/.agents/references/prompting.md` owns their
  rules.
- For `AGENTS.md` and `SKILL.md`, use `agents-md` and `agent-skills-creator` respectively.
- Preserve generated, vendored, and frozen historical files; use their owning process instead.
- If scope or ownership is unclear, ask before expanding it.

## Understand before editing

- Establish the purpose, reader, main components, boundaries, and relationships relevant to these
  documents.
- Explain the big picture before changing headings or proposing directories.
- Inventory unique facts, numbers, units, links, examples, decisions, qualifications, and safety
  conditions.
- Check claims against current implementation and the latest accessible agreements.
- Label agreed but unimplemented behavior as planned; distinguish it from current code and observed
  deployment.
- Preserve superseded decisions as history when needed; do not present them as current instructions.
- Report unavailable evidence and unresolved conflicts; never invent a resolution or claim
  unperformed verification.

## Improve within authority

- During authorized editing, fix organization, duplication, clarity, and verified inaccuracies
  without another cosmetic approval round.
- Preserve unique current facts, qualifications, safety conditions, and consequential rationale in
  place or at their approved owner.
- Account for retired material explicitly; do not preserve obsolete instructions as current
  guidance.
- Correct stale claims explicitly; retain necessary historical context without making every old
  instruction permanent.
- Check comments beside changed code for stale intent; preserve still-relevant constraints and
  explain uncertainty.
- Combine repeated facts only when no distinct condition or meaning is lost.
- Keep unchanged text when no useful improvement is supported.
- Use `ghostwriter` for prose when available; otherwise follow the repository's writing conventions.
- A doc adding an agent rule needs `Read <doc> before <action>.` in the instructions file, via
  `agents-md`.

```text
Never shorten safety content, including destructive-action confirmations, to fit a word budget.
```

**Structure:** Read [concern-based structure](references/structure.md) before proposing splits,
moves, new directories, or substantial rewrites.

- Propose structural changes, deletion, and substantial rewrites before applying them unless that
  exact scope is already approved.
- Name additional files needed for link or index repairs; request approval if outside the authorized
  task.
- A structural proposal never expands into an unsolicited repository-wide audit.

## Verify and hand off

- Compare the final document against the inventory; account for each unique item and every corrected
  claim.
- Resolve changed links and anchors; verify commands safely against their owning implementation or
  documented checks.
- Never execute destructive or shared-system commands merely to validate documentation.
- Check applicable word limits, lead-ins, and Markdown structure in both documentation and proposal
  output.
- Measure numeric writing limits before handoff; visual inspection alone does not verify them.
- Run applicable repository checks; distinguish static checks, exercised behavior, and unverified
  assumptions.
- Report improvements, unapplied proposals, and remaining uncertainty without claiming automatic
  reliability across all sessions.
- Follow local rules for retaining outcomes; do not create logs or global memories for this
  workflow.

## Gotchas

Stale docs survived code commits; scope step 4 searches for exactly these misses:

- A doc kept claiming a limit was unenforced after code enforced it.
- A new recipe shipped without an entry in the tooling reference.

**Maintenance:** Read `evals/evals.json` when changing this skill; authored scenarios are not
executed behavioral evidence.
