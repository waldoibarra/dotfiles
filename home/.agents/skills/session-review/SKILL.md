---
name: session-review
description: >-
  Reviews session evidence and proposes focused workflow or voice-profile improvements without applying them.
  Use when handing off, closing a session, or examining repeated corrections, failed checks, or manual friction.
  For instruction edits use agents-md; for custom skill maintenance use custom-skills; for prose use ghostwriter.
---

# Review a session without changing policy

**Outcome:** Return one scoped proposal per supported pattern, or no proposal when none is
warranted.
Recurring friction and explicit writing preferences can justify review; closure does not authorize
execution.

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
Compare verified results with the original problem; retain the change or propose scoped rollback.

**Maintenance:** Read `evals/evals.json` when changing this skill; scenarios are specifications, not
executed behavioral evidence.
