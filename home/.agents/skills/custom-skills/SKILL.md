---
name: custom-skills
description: >-
  Maintains repository-owned custom skills, coordinating scope, authoring, verification, and local delivery.
  Use when asked to "maintain our custom skills" or "refactor our skill collection".
  Also use when turning a local workflow into a harness skill.
  General skill authoring belongs to agent-skills-creator; session improvement proposals belong to feedback-loop.
---

# Maintain repository-owned skills

**Outcome:** Deliver authorized skill changes that preserve their contracts and pass applicable
source and delivery checks.
This coordinator owns local integration, not another authoring method, external updates, or
automatic retrospectives.
Deployment and behavior remain separate evidence states.

## Establish scope and ownership

1. Resolve source ownership, repository instructions, affected readers, and the requested
    maintenance scope.
2. Edit owned sources, never installed external copies; audit-only requests produce findings without
    edits.
3. Identify the desired outcome, protected behavior, and concrete failure or preference motivating
    the change.
4. Reuse settled decisions; ask only about uncertainty changing behavior, risk, or scope.
5. Verify implementation and tests before treating a transcript or specification as authoritative.
6. Compare neighboring triggers and outputs before adding a skill.

Keep distinct jobs separate; prefer repairing an existing owner over adding a generic checklist.
Preserve safety, privacy, accessibility, and data-integrity requirements during simplification.
Record keep, improve, merge, or retire decisions in an existing permitted project plan.
Without comparative behavior evidence, label retention provisional and avoid speculative retirement.

## Load the owning guidance

Read `~/.agents/references/communication-rules.md` before reviewing or authoring skill prose and
output instructions.
Resolve dependencies through host discovery or their installed directories; report missing guidance
before dependent work.

| Task | Owner |
| --- | --- |
| Author, refactor, validate, or evaluate a skill | `agent-skills-creator`; load only the relevant mode and references |
| Check information architecture and preservation | `docs`; skill format and authoring still belong to `agent-skills-creator` |
| Resolve domain terminology | The repository glossary, with `domain-modeling` for unresolved meanings |
| Change bundled shell code | `shell-scripting` |
| Propose improvements from session evidence | `feedback-loop` |

Keep glossary definitions in their repository owner, not a new glossary inside every bundle.
Add grounded missing terms only during authorized repository maintenance.

Inspect optional `skill-creator` utilities before reuse; do not adopt a competing orchestration
loop.
Active model, concurrency, retry, and approval rules override imported workflow suggestions.

## Refactor around the job

- Compare intended triggers with neighboring near-misses before broadening a description.
- Preserve local decisions and observed gotchas; remove duplicated generic coaching, not domain
  requirements.
- Establish purpose and task-based reading routes before rearranging content.
- Give each concern one owner; split detail by loading condition, not line count or a directory
  template.
- Use deterministic code for fragile, repeated operations instead of regenerating their logic.
- Inspect script effects and dependencies before execution; repeatability does not establish
  correctness.
- Exercise authorized scripts in isolated fixtures, including failure and unchanged-input repeat
  runs.
- Address missing feedback access before adding instructions for failures the agent cannot observe.
- Name the check revealing the desired outcome; report unavailable tools or environments explicitly.

## Verify source, delivery, and behavior separately

1. Preserve or add representative scenarios before changing the behavior they specify.
    Include review-only boundaries, routing, near-misses, and relevant failure recovery.
    Authored scenarios are specifications, not executed evidence.
2. Run the existing authoring validator and repository checks against edited sources.
    Inspect the validator interface; distinguish format requirements from house conventions.
    Report unavailable checks rather than installing dependencies without approval.
3. Check authored prose, frontmatter, and output requirements against the shared communication
    rules.
    Skim headings and emphasis, then inspect coherence and retained meaning; lint alone is
    insufficient.
    Preserve quotations, required literals, safety text, and deliberately flawed fixtures under that
    reference's exceptions.
4. If delivery changes, exercise the real mechanism in a disposable target.
    Check bundled bytes, link targets, unchanged-input behavior, and unrelated-file preservation.
    Do not run a workstation updater merely to validate a skill.
5. Run behavioral comparisons only within explicitly approved models, tools, costs, and run limits.
    Use fresh contexts and identical task conditions for baseline and revised skills.
    Verify which source loaded; measure routing separately from task outcomes.
6. Update the catalogue and existing plan with results, unresolved limits, and rollback.
    Report source, installed, loaded, and exercised states separately.
    Rollback restores relevant sources and installed links; reload each host before checking
    discovery.

**Maintenance:** Read `evals/evals.json` only when changing this coordinator.
