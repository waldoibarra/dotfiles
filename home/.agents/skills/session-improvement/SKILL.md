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
3. Check existing owners before proposing anything, starting with the repository's own
  self-improvement setup (see Local Setups).
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
- placement: scope, harness, and audience from Placement Axes, with the resulting target
  paths or repositories;
- expected benefit;
- validation plan;
- rollback plan;
- proposed commit and push destinations, if any;
- the exact approval boundary, paths, and repositories.

Silence, session closure, or skill invocation is not consent. Approval covers only presented items,
not future discoveries. Commit or push only explicitly approved paths and repositories. Work
permissions still apply; personal applicability never overrides a work repository's rules.

## Placement Axes

Classify every proposal on three axes before naming a target path. State the classification in
the packet; when the session does not settle an axis, state the assumption instead of guessing.

- **Scope: personal or work.** A person's personal configuration (dotfiles) is shared with the
  people who use those same dotfiles and travels across every workplace. Each workplace has its
  own shared harness, and its members do not use one another's dotfiles. Strip workplace names,
  tools, repositories, and people from the rule: if it still prevents the friction, it is personal
  scope; if not, it belongs to that workplace's shared harness. Work evidence and work-only
  mechanics never enter personal configuration; personal preferences enter a work harness only
  with that team's approval.
- **Harness: neutral or specific.** Prefer the harness-neutral location every agent reads
  (shared instructions, portable skills). Use a harness-native location only when the
  mechanism exists in that harness alone (hooks, settings, model routing). Keep credentials and
  runtime state harness-native regardless of scope.
- **Audience: private, dotfiles co-users, or workplace team.** Name who else will load the change.
  A change that only suits the current user stays in private memory or local settings. A change
  for dotfiles co-users or a team is a shared rule: write it for them, generic and without naming
  individuals, and the packet says they are affected.

## Local Setups

A repository or environment may run its own self-improvement loop: a closure prompt, a plan
with a decisions table, a ledger, a retrospective doc, or rules on what may be recorded and
what is pre-approved. Read its instruction files (`AGENTS.md`, `CLAUDE.md`, and the workflow or
maintenance docs they link) before drafting, and identify its closure trigger, its permitted
home for proposals, its record rules, its pre-approved change classes, and its verification and
delivery policy. Where the local setup is silent, the shared harness rules apply.

Then keep the two apart:

- **Inside that repository, the local loop wins.** This skill supplies the method; the local
  setup decides what may be saved, where, and how it ships. Changes it pre-approves go through
  its own route, not through a packet. Changes it forbids or reserves for scoped approval stay
  in the packet. With no permitted home for proposals, unanswered items live in the reply only.
- **Outside it, the local loop is evidence, not policy.** A local rule, prohibition, closure
  phrase, or outcome never moves into the shared harness (global instructions, portable skills,
  dotfiles) because it worked there. It moves only when the friction is shown to repeat across
  repositories and the user approves that specific change. A repository that adapts a global
  skill owns its adapter; a change to the global skill needs the cross-repository justification.

## Placement Rules

- Shared reusable rules may belong in global instructions or a portable skill.
- Project knowledge belongs in that project's docs, plans, or skills.
- Harness mechanics belong in the owning harness documentation or plan.
- Individual preferences stay separate from reusable policy unless the user approves sharing them.
- Retain unanswered proposals only in an existing permitted project plan, not a new global log;
  with no permitted plan, retain nothing.
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
- Do not create records this skill does not need; a repository's rules on what may be recorded
  override this skill's defaults inside that repository.
- Do not sweep dirty repositories or force-push while applying an approved improvement.
- A local closure prompt invokes the method, not consent; the local rules on records and
  approval still apply.
- A session spent inside a repository with a strong local loop makes its rules feel global.
  Before proposing a shared-harness change, name the second repository where the same friction
  occurred; if there is none, the proposal targets the local setup or nothing.
- A rule learned at work that reads as generic still carries work context: a tool, a repo layout,
  a team norm. Rewrite it without those before calling it personal scope; if the rewrite is empty,
  it was work scope.

Maintenance only: `evals/evals.json` contains routing scenarios, not executed behavioral results.
