---
name: docs-maintenance
description: >-
  Maintains accurate, information-preserving Markdown documentation within the active task.
  Use when creating, editing, rewriting, or reviewing READMEs, guides, or other Markdown
  documentation.
  Proposes concern-based splits before restructuring. For AGENTS.md use agents-md; for SKILL.md use
  agent-skills-creator.
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
2. Name the documents created, edited, or explicitly reviewed for this task.
3. Inspect only those documents and sources needed to verify their claims, context, or links.
4. Exclude unrelated dirty files; a Git diff alone does not establish task ownership.

- Reading or summarizing Markdown does not authorize rewriting it.
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
- Preserve every unique item from the inventory, either in place or at an approved linked
  destination.
- Correct stale claims explicitly; retain necessary historical context rather than silently erasing
  earlier agreements.
- Combine repeated facts only when no distinct condition or meaning is lost.
- Keep unchanged text when no useful improvement is supported.
- Use `ghostwriter` for prose when available; otherwise follow the repository's writing conventions.

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

**Maintenance:** Read `evals/evals.json` when changing this skill; authored scenarios are not
executed behavioral evidence.
