# Learning and session improvement

**Two skills: `socratic-teaching` teaches; `feedback-loop` compares intent with outcome.**
Both are repo-managed; read [skills](skills.md#repo-managed-skills) for installation.

- Use `socratic-teaching` for guided learning.
- Use `feedback-loop` to compare intended and observed outcomes, including follow-up evidence after
  approved changes.
- They share neither learner records nor project curricula.
- Projects can require the teaching skill in their own instructions and keep local content
  separately.

| Task | Pi | Claude Code |
| --- | --- | --- |
| Start guided learning | `/skill:socratic-teaching` | `/socratic-teaching` |
| Review session improvements | `/skill:feedback-loop` | `/feedback-loop` |

- Natural-language requests can also select these skills through their descriptions.
- A closure question requests review, not permission to edit or publish.
- `feedback-loop` assesses evidence first, then loads its placement reference only for
  warranted proposals.

**Touched docs:** `feedback-loop` uses `docs` for read-only review of session-edited Markdown.
It skips unrelated Git changes and read-only sources; any proposed corrections still require
execution authority.

**Voice feedback:** `feedback-loop` reads Ghostwriter and relevant profiles when the
session supplies writing feedback.
It proposes evidence-backed profile changes, checking whose voice and which co-users are affected.
Explicit preferences can justify proposals without repeated corrections; profile changes still
require approval.

**Follow-up:** The skill assesses correction effort, repeated context, review burden, and decision
clarity from available evidence.
It diagnoses intent and audience mismatches through the canonical communication rules.
Without comparable evidence, report improvement as unverified; static checks and installation do not
prove reduced human effort.
No monitoring, observation logs, automatic learning, or model experiments follow from invoking the
skill.

**Approved edits:** Use the owning specialist workflow and repository delivery rules.

`ghostwriter` owns prose; it replaces the former `docs-writing` name.

No shutdown hook runs `socratic-teaching` or `feedback-loop`; neither reconstructs
inaccessible
conversation history.

Read [Claude skill loading](https://code.claude.com/docs/en/features-overview)
before changing Claude invocation or discovery expectations.

## Loading is not behavior

Treat fresh-session loading and observed communication quality as separate checks.
Rewritten instructions guarantee neither; `feedback-loop` compares intent with observed outcomes
and proposes evidenced changes with scope, benefit, verification, and rollback.
