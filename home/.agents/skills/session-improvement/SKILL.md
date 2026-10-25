---
name: session-improvement
description: >-
  Proposes minimal session-improvement changes from accessible evidence without applying them.
  Use when handing off, closing a session, or reviewing repeated corrections, failed checks, or
  manual friction. Includes evidence-backed voice-profile suggestions.
  For instruction edits use agents-md; for custom skill maintenance use skill-maintenance;
  for prose use ghostwriter.
---

# Session improvement

- **IS:** assessing recurring friction or explicit writing preferences, then preparing warranted
  approval packets.
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
4. Reject unsupported one-off incidents, already-covered concerns, and changes better handled manually.
    Explicit writing preferences use the profile-review criteria below.
    Add no observation logs or automation.
5. Before drafting a warranted proposal, read [placement](references/placement.md) for scope,
  audience, local-loop precedence, and permitted retention.

## Review touched documentation

- Identify Markdown documentation created or edited during this session; skip this review when none
  was touched.
- Exclude documents merely read, unrelated Git changes, and repository-wide audits.
- Read [docs](../docs/SKILL.md) and follow its applicable content and reader-route checks without editing.
  Report unavailable guidance instead of inventing it.
- Inspect only session-edited documents and references needed to verify their context, claims, or links.
- Return a scoped proposal only for evidenced gaps; the approval packet below owns its required contents.
- Do not apply rewrites, create directories, or treat closure as authorization.

## Review voice-profile feedback

When the session contains writing feedback, read `ghostwriter` and the relevant profile before
proposing improvements.
Explicit user preferences can justify a proposal without repeated mistakes.
Otherwise, use recurring corrections or edited drafts; silence and uncorrected output do not
establish preferences.

- Resolve the active profile root through Ghostwriter's instructions; inspect only profiles
  relevant to the evidence.
- Confirm whose voice the profile represents and who receives changes through its storage or
  installation.
- Propose the smallest profile change, keeping observed habits separate from explicit preferences.
- Keep personal preferences out of shared communication rules; exclude company details and
  private source material.
- Use Ghostwriter's profile and correction procedures instead of inventing another schema or
  learning log.
- Return no proposal when evidence is absent or the preference is already covered.

Profile changes remain proposals, including corrections that Ghostwriter would otherwise retain
in its Learn mode.
Name the target, audience, evidence, verification, and rollback; approval routes implementation
through `ghostwriter`.

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
