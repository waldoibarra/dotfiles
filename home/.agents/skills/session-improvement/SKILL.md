---
name: session-improvement
description: >-
  Proposes minimal session-improvement changes from accessible conversation evidence without
  applying them. Use when handing off, closing a session, seeing repeated corrections, failed
  checks, manual friction, or being asked "what should we improve from this session?" For
  AGENTS.md use agents-md; for SKILL.md use agent-skills-creator; for docs use docs-writing
  or ghostwriter.
---

# Session Improvement

- **IS:** deciding whether an evidence-backed improvement proposal is warranted, then drafting
  the approval packet.
- **IS NOT:** directly editing instructions, committing, pushing, mining logs, or replacing
  specialized skills without scoped approval and the owning workflow.

Use this skill near closure, after repeated corrections, or on direct invocation.
A valid result can be "no improvement is warranted."

## Workflow

1. Inspect only the accessible current conversation, requested files, and repo artifacts.
  If earlier history is unavailable, say so; do not mine raw logs or private history.
2. Separate evidence into reusable rules, project knowledge, harness mechanics, and individual
  preferences. Never mix identity details, family details, work secrets, or project-private facts
  into reusable global rules.
3. Check existing owners before proposing anything.
  Route approved edits to `agents-md`, `agent-skills-creator`, `docs-writing`, `ghostwriter`,
  or another specialized skill.
4. Propose only the smallest durable change that would prevent the repeated friction.
  If the issue is one-off, already covered, or better handled manually, propose no change.
5. Return an approval packet. After scoped approval, route execution through the owning specialist
  workflow, verify the exact acceptance criteria and deployment state, and report results
  separately. Compare the result with the observed problem; retain it or propose the scoped rollback.
  Inspect each approved repository separately, preserving unrelated work and respecting branch policies.
  Commit and push only when those operations and destinations are authorized.
  Report partial failures explicitly.
  Do not edit, commit, push, sync, or install from this skill alone.

## Approval Packet

Include:

- evidence observed in the accessible session;
- the smallest proposed change;
- target paths or repositories;
- expected benefit;
- validation plan;
- rollback plan;
- proposed commit and push destinations, if any;
- the exact approval boundary, paths, and repositories.

Silence, session closure, or skill invocation is not consent. Approval covers only presented items,
not future discoveries. Commit or push only explicitly approved paths and repositories. Work
permissions still apply; personal applicability never overrides a work repository's rules.

## Placement Rules

- Shared reusable rules may belong in global instructions or a portable skill.
- Project knowledge belongs in that project's docs, plans, or skills.
- Harness mechanics belong in the owning harness documentation or plan.
- Individual preferences stay separate from reusable policy unless the user approves sharing them.
- Retain unanswered proposals only in an existing permitted project plan, not a new global log.
- Separation of concerns: give each document or skill one responsibility and a clear owner.
- DRY: edit the canonical source and link consumers; do not copy rules between repositories.
- YAGNI: reuse existing mechanisms; add a skill, folder, or automation only for a demonstrated need.
- Respect each repository's domain layout; do not impose one project's folder structure globally.

## Report States

When relevant, report **configured**, **installed**, **loaded**, **exercised**, **committed**, and
**pushed** separately. A file existing in this repository proves only configuration source state.
A fresh host session or host-specific context inspection is needed before claiming loaded behavior.

## Gotchas

- Do not diagnose an error from a user report unless the task includes investigation evidence.
- Do not create hooks, daemons, schemas, dependencies, settings, or updater paths for observation.
- Do not teach, coach, or track the user globally; project-specific no-learner-record rules win.
- Do not sweep dirty repositories or force-push while applying an approved improvement.

Maintenance only: `evals/evals.json` contains routing scenarios, not executed behavioral results.
