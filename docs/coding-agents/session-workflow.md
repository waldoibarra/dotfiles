# Work through an agent session

**Choose the outcome and authority; let the agent select the relevant procedures.**
Custom skills make recurring work consistent without requiring you to invoke a checklist every
session.
These checkpoints scale with the task; a small correction needs no elaborate planning ceremony.

Read the [skill catalogue](/docs/agent-skills.md#repo-managed-skills) when choosing a specialist
workflow.
Read [harness verification](harness-verification.md) when testing instruction delivery or loading,
rather than ordinary task outcomes.

## Start with a bounded request

Tell the agent what success means, which repository owns the work, and any important constraints.
Distinguish advice, review, and implementation; reviewing something does not automatically authorize
editing it.
Name protected behavior, excluded files, or sensitive evidence when they affect the task.

For example:

```text
Review this settings flow without editing files.
Focus on keyboard behavior and narrow layouts.
Report confirmed defects separately from unverified concerns.
```

The agent should inspect relevant instructions and evidence before choosing a procedure.
You do not need to prescribe every tool call or repeat rules already owned by the harness.

## Let the task select the skills

**Skills are task-specific procedures, not a mandatory sequence.**
A session may need one skill, several cooperating skills, or none beyond ordinary assistance.
Use natural-language requests by default; name a skill when you want an explicit workflow.

| Need | Custom skill |
| --- | --- |
| Learn a concept or orient yourself | `socratic-teaching` |
| Initialize an empty, stack-free project | `project-init` |
| Maintain documentation | `docs` |
| Work on shell scripts | `shell-scripting` |
| Coordinate interface behavior and layout | `web-interface` |
| Work on platform behavior or layout alone | `web-standards` or `css-layout` |
| Prepare a verified commit or authorized push | `commit` |
| Review recurring friction and propose improvements | `session-review` |
| Maintain repository-owned skill bundles | `custom-skills` |
| Record an assigned personal manual task | `shared-todo` |

The [catalogue](/docs/agent-skills.md) owns installation and invocation details; individual skills
own their procedures.
Skill names do not grant authority, install dependencies, or guarantee automatic selection.
Roles assign bounded worker responsibilities; tools perform actions under the applicable approval
boundaries.

## Resolve decisions that change the work

The agent should surface ambiguity affecting behavior, risk, ownership, or scope.
Confirm consequential decisions before dependent implementation, while allowing independent work to
continue.
Settled decisions should not require repeated approval.

For example:

```text
Implement the approved plan in this repository.
Preserve the public API and update affected documentation.
Run the available checks, but do not commit or publish yet.
```

Delegate only within approved scope and applicable harness instructions.
Agree worker boundaries and any model-experiment limits before dependent work.
A skill recommendation does not authorize changing shared policy, contacting others, or accessing
another workspace.

## Review the evidence before delivery

Ask what changed, what was checked, and what remains uncertain.
Inspect the outcome rather than accepting a successful command as proof of every requirement.

- Tests and lint cover their specific contracts, not all possible behavior.
- Installed or discovered instructions do not establish model compliance.
- Missing browser, service, or authentication access must remain an explicit verification limit.
- Review should distinguish applied changes from proposed changes and current behavior from future
  work.

Use the [verification guide](harness-verification.md) for harness changes and repository-owned
checks for product changes.
Avoid importing harness-specific acceptance probes into every ordinary task.

## Close with an explicit next action

Request Git delivery when ready; distinguish committing from pushing.
Confirm the target and scope for publication or external messages.
A general completion request does not authorize either.

```text
Commit the verified changes for this task. Do not push.
Report remaining blockers and the next action.
```

Use `session-review` when closing or examining repeated friction; it proposes supported changes
without applying them.
A review can legitimately produce no improvement proposal.
Approved follow-up work uses its owning workflow; closure itself does not authorize policy changes
or new records.
Keep durable outcomes and next steps with their repository or vault owner, following local
recording rules.

**For the next session:** Carry current decisions, verified outcomes, unresolved issues, and next
actions.
Link relevant context rather than copying the entire transcript.
The agent should retrieve relevant context and recheck claims that affect the new task.
