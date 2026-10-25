---
name: docs
description: >-
  Maintains accurate Markdown documentation with concern-based organization and layered reading paths.
  Use when creating, editing, rewriting, or reviewing READMEs, guides, plans, or documentation structure.
  Includes small doc edits alongside code changes and edits by workers.
  For AGENTS.md use agents-md; for SKILL.md use agent-skills-creator.
  Model prompts follow prompting.md.
---

# Maintain documentation

**Required:** Before drafting or reviewing, read and follow
`~/.agents/references/communication-rules.md`.
Apply it to authored prose, comments, examples, and review findings; preserve its literal and safety
exceptions.
Report unavailable guidance before dependent work rather than inventing its contents.

- **IS:** improving authorized documentation, preserving information, and organizing it around
  reader needs.
- **IS NOT:** repository-wide cleanup, new product decisions, or permission to edit merely because
  Markdown was read.

**Done:** Authorized edits preserve verified information and pass applicable content, navigation,
and repository checks.
Unapproved structural changes remain scoped proposals; unavailable evidence remains explicit.

## Choose a reading route

This entrypoint owns the maintenance procedure and its approval boundaries.
Use the references for their distinct concerns; they are not mandatory sequential chapters.

| Before… | Read |
| --- | --- |
| Looking up artifact conventions after reading the required communication rules | [Conventions](references/conventions.md): entrypoints, shared language, filenames, and retention |
| Choosing or reviewing a guide's organization and page purposes | [Information architecture](references/structure.md): concerns, Diátaxis, progressive disclosure, and navigation checks |
| Retiring agreements or proposing ADRs | `~/.agents/references/memory.md` for lifecycle and decision gates |
| Editing model prompt files | `~/.agents/references/prompting.md` instead of this workflow |

Small factual corrections need not become structural reviews.
Use `agents-md` for instruction files and `agent-skills-creator` for skill definitions.
Use `ghostwriter` for prose; house conventions govern organization when generic writing advice
conflicts.
If prose tooling is unavailable, follow repository conventions and report the limitation.

## Establish scope and owners

1. Read repository instructions for documentation ownership, confidentiality, and recording rules.
2. Name documents created, edited, or explicitly reviewed; exclude unrelated changes and other
    contributors' work.
3. Read the project's glossary before choosing terms; local instructions may name a different
    shared-language file.
4. After code or configuration changes, search docs for changed identifiers, flags, defaults,
    recipes, and constraints.
5. Include verified stale references in scope; inspect only sources needed to establish their
    current meaning.

## Understand before editing

- Establish purpose, reader, components, boundaries, and relationships from inspected evidence.
- Identify the system's big picture before proposing headings or directories.
- Choose each page's primary reader need through the structure reference; orient without delaying
  its task.
- Inventory unique facts, numbers, units, links, examples, decisions, qualifications, and safety
  conditions.
- Check claims against implementation and current agreements; distinguish implemented behavior from
  accepted future work.
- Report inaccessible evidence and unresolved conflicts; never invent current behavior or performed
  verification.

## Improve within authority

**Editing:** Fix organization, duplication, clarity, and verified inaccuracies within approved scope
without another cosmetic approval round.
Keep unchanged text when no useful improvement is supported.
Combine repeated facts only when no distinct condition or meaning is lost.

**Structure:** Apply the linked information architecture guidance during ordinary guide work, not
only directory migrations.
Reuse existing entrypoints and concern directories; keep cohesive pages intact when headings and
links suffice.
Avoid empty scaffolding and repository-wide taxonomies for one touched guide.

Before splits, moves, deletions, or substantial rewrites:

1. Name affected sources, destinations, reading routes, and necessary incoming-link or index
    repairs.
2. Map each unique fact, example, decision, qualification, and safety condition to its retained
    owner.
3. Explain reader benefits, verification, tradeoffs, and rollback; resolve uncertain ownership
    before selecting destinations.
4. Reuse approval covering the exact scope; otherwise wait before restructuring or editing
    additional files.

A structural proposal never authorizes an unsolicited repository-wide audit or cross-repository
migration.
Local documentation contracts retain precedence.

**Preservation:** Keep unique current information at its existing or approved owner.
Correct obsolete operational claims; preserve consequential rationale with explicit status and
successor links.
Plans are in scope, but ordinary editorial history needs no permanent duplicate.
Leave generated, vendored, and frozen sources to their owning process.
Keep plans and evidence in their permitted workspace, separate from maintained operational guidance.

**Comments:** Check comments beside changed code for stale intent and hidden constraints.
Verify unfamiliar rationale before removing it; documentation work does not authorize unrelated code
cleanup.

**Instructions:** A new agent requirement needs a reading trigger in its instruction file, through
`agents-md`.
Use `Read <doc> before <action>.` rather than copying the procedure into instructions.

```text
Never shorten safety content, including destructive-action confirmations, to fit a word budget.
```

## Verify and hand off

1. Compare the result with the information inventory; account for each retained, corrected, or
    retired item.
2. For structural work, check reader routes using the structure reference, including canonical
    ownership and cross-concern navigation.
3. Resolve changed links and anchors; verify commands against maintained implementations or safe
    execution evidence.
4. Run repository checks and measure authored sentences against the shared communication rules.
    Check headings and emphasis first, then read the full text for coherence, qualifications, and
    completeness.
    Preserve required literals and safety wording; formatting alone does not establish communication
    quality.
5. Report applied changes, remaining proposals, failed checks, and uncertainties without claiming
    universal reliability.

Never execute destructive or shared-system commands merely to validate documentation.
Distinguish static checks, instruction loading, exercised behavior, and unverified assumptions.
Follow local recording rules; this workflow does not create session logs or global memories.

## Gotchas

Stale docs survived code changes because the review missed a limit's enforcement and a new recipe.
Search changed behavior and command names, not just the document named in the request.

## Maintain this bundle

Read `evals/evals.json` when changing this skill; scenarios are specifications, not executed
behavioral evidence.
Use `agent-skills-creator` for skill authoring and the owning repository's delivery checks.
Keep the workflow here, information architecture in `references/structure.md`, and lookup
conventions in `references/conventions.md`.
Fixtures are evaluation inputs, not current guidance or prose to polish.
No tutorial is required merely to complete a Diátaxis set.
The communication requirement is an instruction-followed gate, not an automatic linter or guarantee
of model compliance.
