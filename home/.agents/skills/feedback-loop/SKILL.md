---
name: feedback-loop
description: >-
  Compares intended and observed outcomes and proposes scoped improvements without applying them.
  Use when closing a session, reviewing repeated corrections, or asking whether an approved improvement helped.
---

# Close the feedback loop without changing policy

**Outcome:** Return an evidence-backed assessment and only warranted, scoped improvement proposals.
Repeated friction, explicit preferences, and follow-up evidence can justify review; closure never
authorizes execution.

- **IS:** comparing intent with outcomes, diagnosing mismatches, and assessing approved changes from
  available evidence.
- **IS NOT:** implementation, monitoring, automatic learning, or a required interview before every
  reply.

Use `agents-md` for instruction edits, `custom-skills` for owned skills, and `ghostwriter` for
prose.

This skill never edits, commits, publishes, installs, syncs, or mines private history.

## Select relevant evidence

1. Inspect accessible conversation, requested files, and repository artifacts only.
2. Report unavailable history; never mine logs to reconstruct it.
3. Identify repeated friction, its owner, and the repository's existing improvement rules.
4. Separate reusable rules, project knowledge, harness mechanics, and individual preferences.
5. Check whether missing tools, runnable fixtures, or feedback access caused the failure.
6. Prefer repairing missing feedback over adding instructions the agent still cannot verify.
7. Reject unsupported one-off incidents, already-covered concerns, and changes better handled
    manually.

Explicit writing preferences use the profile criteria below; they need not recur before
consideration.
Add no observation logs or automation.

## Compare intent with observed outcomes

Read `~/.agents/references/communication-rules.md` for the canonical intent and audience checks.
Use the accepted request and accessible evidence, not a reconstructed or invented baseline.

- Identify the intended outcome, actual result, and any remaining uncertainty.
- Diagnose mismatched goals, constraints, assumptions, targets, audiences, author voices, or reader
  context.
- Distinguish missing access or feedback from missing guidance and misunderstood intent.
- Assess correction effort, repeated context, review burden, and whether the user could make the
  consequential decision.
- Use qualitative observations unless measurements exist; do not invent time savings or scores.
- Check whether clarification questions resolved consequential uncertainty or merely repeated
  settled context.

Prefer fixing the owning context, tool, or procedure over adding another global rule.
Useful feedback can support removing instructions or retaining the current workflow unchanged.

## Follow the relevant review route

| Evidence | Read or action |
| --- | --- |
| A warranted improvement needs an owner | Read [placement](references/placement.md) before drafting the proposal |
| This session created or edited Markdown | Use [docs](../docs/SKILL.md) for read-only content and reader-route checks |
| Writing feedback or corrected drafts | Read `ghostwriter` and the relevant active profile |
| No supported gap | Return no proposal; do not manufacture one |

The placement reference owns scope, audience, local-loop precedence, and permitted retention.
Report unavailable guidance rather than inventing its contents.

**Documentation:** Inspect session-edited files and only the references needed to verify their
context, claims, or links.
Exclude documents merely read, unrelated Git changes, and repository-wide audits.
Skip this route when no documentation was edited.
Do not apply rewrites or create directories during review.

**Voice profiles:** Resolve the active profile root through Ghostwriter; inspect only profiles
relevant to the evidence.
Confirm whose voice is represented and who receives changes through shared storage or installation.
Distinguish observed habits from explicit preferences; silence and uncorrected output establish
neither.
Propose the smallest supported change, or none when the preference is already covered.
Keep personal preferences out of shared communication rules and exclude company details or private
source material.
Use Ghostwriter's existing profile and correction procedures, not another schema or learning log.
Its Learn mode does not bypass this skill's proposal-only boundary.

## Prepare the approval packet

Include only what the reader needs to decide:

- Observed evidence and the smallest durable change.
- Scope, harness, audience, exact target paths, and affected readers.
- Expected benefit, verification criteria, and rollback.
- Commit and push destinations, when requested.
- Exact approval boundaries.

Keep sensitive evidence private; publish only sanitized reusable guidance.
Silence is not approval, and approval covers only the presented items.
Profile proposals identify the target, audience, evidence, verification, and rollback before routing
implementation to `ghostwriter`.

## Route execution after approval

This skill does not execute changes; the approved target selects its owning workflow.

| Target | Workflow |
| --- | --- |
| Agent instructions | `agents-md` |
| Repository-owned custom skills | `custom-skills`, with `agent-skills-creator` for authoring |
| Other skill definitions | `agent-skills-creator` in their owning repository |
| Documentation or other prose | `ghostwriter`, under applicable documentation conventions |

Execution verifies each approved repository, preserves unrelated work, and follows local delivery
rules.
Report partial failures and configured, installed, loaded, exercised, committed, and pushed states
separately.
Source edits do not establish fresh-session loading or behavioral improvement.

## Assess an approved change afterward

Compare available follow-up evidence against the original problem and its acceptance criteria.
Distinguish source edits, installation, loading, observed behavior, and user effort.
Recommend keeping, revising, or reverting the change; this skill applies none of those actions.
Without a comparable baseline or exercised outcome, report improvement as unverified and name the
missing check.
New model experiments, monitoring, or access require separate authorization.
Keep permitted outcomes with the existing owner; do not create a parallel learning log.

**Maintenance:** Read `evals/evals.json` when changing this skill; scenarios are specifications, not
executed behavioral evidence.
