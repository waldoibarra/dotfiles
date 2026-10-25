---
name: session-improvement
description: >-
  Proposes minimal session-improvement changes from accessible evidence without applying them.
  Use when handing off, closing a session, or reviewing repeated corrections, failed checks, or
  manual friction.
  For instruction edits use agents-md; for custom skill maintenance use skill-maintenance;
  for prose use ghostwriter.
---

# Session improvement

- **IS:** deciding whether recurring friction warrants a proposal, then preparing its approval
  packet.
- **IS NOT:** editing, committing, publishing, installing, syncing, or mining private history.

Finish with one scoped proposal per pattern, or no proposal when none is warranted.

Skill invocation and session closure grant no write authority.

## Assess the evidence

1. Inspect accessible conversation, requested files, and repository artifacts only. Report
  unavailable history; never mine logs.
2. Identify repeated friction, its current owner, and the repository's existing improvement rules.
3. Separate reusable rules, project knowledge, harness mechanics, and individual preferences.
    - Check whether missing tools, runnable fixtures, or feedback access caused the repeated
      failure.
    - Prefer repairing that environment over adding instructions the agent still cannot verify.
4. Reject one-off, already-covered, or better-handled-manually proposals. Add no observation logs or
  automation.
5. Before drafting a warranted proposal, read [placement](references/placement.md) for scope,
  audience, local-loop precedence, and permitted retention.

## Review touched documentation

- Identify Markdown documentation created or edited during this session; skip this review when none
  was touched.
- Exclude documents merely read, unrelated Git changes, and repository-wide audits.
- Read [docs-maintenance](../docs-maintenance/SKILL.md) for documentation review criteria; report if
  unavailable rather than inventing its guidance.
- Use its read-only review mode; this skill's proposal-only boundary still applies.
- Inspect only touched documents and references needed to verify their context, claims, or links.
- Propose supported improvements to the big picture, concern boundaries, information preservation,
  and factual accuracy.
- Apply the same evidence and placement gates; return no documentation proposal when none is
  warranted.
- Name affected paths, necessary link updates, verification, and rollback; do not apply rewrites or
  create directories.

## Draft the approval packet

Include only what the reader needs to decide:

- Observed evidence and the smallest durable change.
- Scope, harness, audience, and exact target paths or repositories.
- Expected benefit, verification criteria, and rollback.
- Commit and push destinations, if requested.
- Exact approval boundaries and affected readers.

Keep sensitive evidence private; publish only sanitized reusable guidance.

Silence is not approval, and approval covers presented items only.

## Route approved work

Use the owning specialist workflow after scoped approval; this skill does not execute changes.

| Target | Workflow |
| --- | --- |
| Agent instructions | `agents-md` |
| Repository-owned custom skills | `skill-maintenance`, using `agent-skills-creator` for authoring |
| Other skill definitions | `agent-skills-creator` in their owning repository |
| Documentation or other prose | `ghostwriter` |

- The execution workflow verifies each approved repository, preserves unrelated work, and follows
  local delivery rules.
- It reports partial failures and configured, installed, loaded, exercised, committed, and pushed
  states separately.
- A changed source file proves no fresh-session loading or behavioral improvement.
- Compare verified results with the original problem; retain the change or propose scoped rollback.

## Maintenance

Read `evals/evals.json` when changing this skill; scenarios are specifications, not executed
behavioral evidence.
