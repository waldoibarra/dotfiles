---
name: skill-maintenance
description: >-
  Coordinates repository-owned custom skill creation, refactoring, and retirement with local
  ownership and delivery checks. Use when asked to "maintain our custom skills", "refactor our
  skill collection", or "turn this local workflow into a harness skill".
---

# Skill maintenance

- **IS:** coordinating repository-owned custom skills, their boundaries, and local integration.
- **IS NOT:** another generic authoring method, external package updater, or automatic
  retrospective.
- Use `agent-skills-creator` for generic authoring; use `session-improvement` for closure-time
  proposals.

**Done:** Authorized source changes preserve contracts and pass applicable checks.
Deployment and behavior remain separate evidence states.

## Establish the contract

1. Resolve source ownership, repository instructions, affected users, and the requested maintenance
    scope.
    - Edit owned sources, not installed external copies.
    - Audit mode reports findings without edits.
2. Identify the desired outcome, protected behavior, and concrete failure or preference motivating
    the change.
    - Reuse supplied decisions; ask only about uncertainties that change behavior, risk, or scope.
    - Inspect implementation and tests before treating a transcript or specification as
      authoritative.
3. Compare neighboring triggers and outputs before adding a skill.
    - Keep separate jobs separate; prefer a targeted owner change over another universal checklist.
    - Retain safety, privacy, accessibility, and data-integrity requirements during simplification.
    - Record keep, improve, merge, or retire decisions in the repository's existing permitted plan.
    - Without comparative behavior evidence, label retention provisional and avoid speculative
      retirement.

## Reuse specialist procedures

Resolve dependencies through host discovery or their installed skill directory.
Read dependencies before using their guidance; report missing dependencies before dependent work.

- Read `agent-skills-creator` for authoring, refactoring, validation, and relevant evaluation
  guidance.
  - It owns those procedures; this coordinator owns local scope, integration, and completion
    evidence.
  - Load only references relevant to the selected mode.
- Use `domain-modeling` only when terms or domain relationships need resolution.
  - Reuse existing vocabulary; do not create a glossary merely because a skill is being edited.
- Read `shell-scripting` when changing bundled shell code.
- Inspect optional `skill-creator` utilities and their interfaces before use.
  - Do not adopt its whole orchestration loop alongside the existing authoring owner.
  - Active model, concurrency, retry, and approval rules override imported workflow suggestions.

## Refactor for the job

Apply the authoring procedure to the smallest scope that preserves the contract:

- Compare should-trigger requests with neighboring near-misses before broadening descriptions.
- Preserve local decisions and observed gotchas; remove duplicated generic coaching, not domain
  requirements.
- Split detail by loading condition, not an arbitrary line target.
- Reuse deterministic code for fragile, repeatable operations instead of regenerating their logic.
  - Inspect script effects and dependencies before execution; repeatable code can still be
    incorrect.
  - Verify authorized scripts in isolated fixtures, including applicable failure and repeat-run
    paths.
- Repair missing feedback access before adding instructions for failures the agent cannot observe.
  - Name the executable check or interaction that reveals the desired outcome.
  - Report unavailable tools or environments rather than claiming a prose review exercised them.

## Verify and deliver

1. Preserve or add representative scenarios before changing the behavior they specify.
    - Include review-only boundaries, intended routing, near-misses, and relevant failure recovery.
    - Authored scenarios are specifications, not executed evaluation evidence.
2. Run the existing authoring validator and repository checks against edited sources.
    - Inspect the validator's interface; distinguish format failures from upstream house
      conventions.
    - Report unavailable checks rather than installing dependencies without approval.
3. If delivery changed, exercise the real delivery mechanism in a disposable target.
    - Check bundled files, link destinations, and unchanged-input repeat runs.
    - Do not run a workstation updater merely to validate a skill.
4. Run behavioral comparisons only within explicitly approved models, tools, costs, and run limits.
    - Use fresh contexts and identical task conditions for baseline and revised skills.
    - Verify which source loaded; measure routing separately from task outcomes.
5. Update the owning catalogue and existing plan with results, unresolved limits, and rollback.
    - Report source, installed, loaded, and exercised states separately.
    - Rollback includes new installation links when present, not only reverting source files.

**Maintenance only:** Read `evals/evals.json` when changing this coordinator.
