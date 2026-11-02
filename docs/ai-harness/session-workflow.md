# Work through an agent session

**Choose the outcome and authority; let the agent select the relevant procedures.**
Custom skills make recurring work consistent without requiring you to invoke a checklist every
session.
Planning depth scales with the task; implementation still requires approval unless you explicitly
waive planning.

Read the [skill catalogue](skills.md#repo-managed-skills) when choosing a specialist
workflow.
Read [harness verification](harness-verification.md) when testing instruction delivery or loading,
rather than ordinary task outcomes.
Installed readers resolve links against this file's real source in dotfiles, not their current
repository.

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
It checks intent, audience, and required reader context before answering or drafting.
A medium such as Slack does not identify the readers or establish their knowledge.
Read [intent
clarification](/home/.agents/references/communication-rules.md#clarify-intent-and-audience)
for conversation guidance.
Read [ambition](/home/.agents/references/ambition.md) when exploring better outcomes or materially
different approaches.
The [prompting guide](/docs/prompting.md) instead covers model prompts authored for apps and
services.
You do not need to prescribe every tool call or repeat rules already owned by the harness.

## Choose the work route

**Classify the request before invoking OpenSpec.** Read-only advice and review need no change
artifacts.

| Route | Outcome | Planning record |
| --- | --- | --- |
| Prototype | Disposable artifact or experience answering a bounded question | A concise agreement in conversation |
| Durable change | Maintained behavior, configuration, or documentation | The project's approved change plan |

### Prototype

Use [`prototype-selection`](/home/.agents/skills/prototype-selection/SKILL.md) before choosing an
approach.
It owns tradeoff comparisons, inventive alternatives, capability checks, and routing to execution
skills.
Carry settled choices forward; selection is not a repeated approval ceremony.
Agree on the question, boundaries, observation method, and stop condition before building.
Keep the experiment disposable and clearly identified.

**Throwaway exception:** Do not add or require test suites, linters, coverage targets, or
production hardening.
This exception applies to disposable artifacts, not maintained harness changes or production code.
If a project's mandatory checks conflict, use an approved isolated experiment location rather than
disabling its safeguards.
Observe the output sufficiently to answer the question; measurements or evaluations may themselves
be the experiment.
Protect credentials, private data, spending, and participants regardless of the artifact's lifespan.
Do not initialize OpenSpec or create its artifacts for prototype requests.
This exclusion also applies inside repositories already using OpenSpec.

Evaluate the result against the question; optionally retain useful learnings with their owning
project.
No ADR, report, production migration, or prototype commit is required merely because an experiment
ran.
External skill instructions cannot authorize production edits, commits, or publication.
Promotion requires a separate approved durable change; prototype success alone grants no
implementation authority.

### Durable change

Use the project's existing planning convention; do not initialize OpenSpec without authorization.
Dotfiles selects the [session-workflow schema](/openspec/schemas/session-workflow/schema.yaml) for
new changes.
Its behavioral acceptance remains separate from schema selection.

| Artifact | Responsibility |
| --- | --- |
| `proposal.md` | Outcome, approach, alternatives, boundaries, acceptance, and approval state |
| `specs/**/spec.md` | Observable behavior changes, when present |
| `tasks.md` | Implementation, verification evidence, blockers, and handoff state |

Use native `skip_specs: true` only when observable behavior does not change.
Keep technical reasoning in the proposal initially; separate supporting detail only when complexity
warrants it.
No design document, ADR, interview transcript, review manifest, summary, or retrospective is
mandatory.
Existing ADR gates still apply when a durable decision genuinely needs a record.

This guide owns session routing; shared instructions own approval and specialist skills own their
procedures.
The schema implements the artifact contract without replacing these owners.

## Let the task select the skills

**Refinement and approval precede implementation; specialist skills depend on the task.**
For durable changes, start with `grill-with-docs`, compare alternatives, and review the plan before
authorizing implementation.
For prototypes, use the bounded conversational agreement above instead of the durable-change plan
format.
Use natural-language requests by default; name a skill when you want an explicit workflow.

Use the [skill catalogue](skills.md#repo-managed-skills) to find the procedure for the task.
It owns installation and invocation details; individual skills own their procedures.

| Task | Skill | Boundary |
| --- | --- | --- |
| Refine a durable change before implementation | `grill-with-docs`, which calls `grilling` and `domain-modeling` | Confirm decisions first; glossary and ADR work stays under task authority. |
| Choose and bound a disposable prototype | `prototype-selection`, then the external `prototype` | The [prototype route](#prototype) owns disposable-work boundaries. |
| Maintain Markdown within the task | `docs`; `ghostwriter` for prose | [Documentation maintenance](/docs/documentation.md) owns ownership and checks. |

Pi reads `grill-with-docs` dependencies from their installed skill files; its tracked
`APPEND_SYSTEM.md` handles the unavailable `Skill` tool.
Skill names do not grant authority, install dependencies, or guarantee automatic selection.
Roles assign bounded worker responsibilities; tools perform actions under the applicable approval
boundaries.

## Resolve decisions that change the work

The [global contract](/home/.agents/AGENTS.md#make-decisions-actionable) states the decision rules.
Their reasoning: one recommended option saves the reader a survey.
Alternatives appear only when they change the decision.
Reconciling the latest request with the active plan carries settled
decisions forward and batches missing approvals. When unresolved ambiguity changes the answer,
state the interpretation and ask one focused question. A question about an action is never
authorization for it.

The [shared instructions](/home/.agents/AGENTS.md#make-decisions-actionable) own the planning gate.
It applies to configuration and documentation changes too; feedback requests another draft, not
implementation.
For a small task, explicitly waive planning if you want direct execution.
Read [OpenSpec integration](openspec.md) before starting or resuming an OpenSpec change.

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

## Evolve the workflow from evidence

Use `feedback-loop` to compare intended and observed outcomes before proposing workflow changes.
Evolutionary architecture means improving demonstrated friction while preserving authority,
ownership, and observable checks.
Feedback alone does not authorize schema edits.

When approved workflow or skill changes affect artifact responsibilities, update this guide and the
schema together.
Keep procedure rules with their canonical owners and remove superseded guidance within scope.
Test prototype routing, approval boundaries, native artifact operations, and cross-harness
discovery.
Static tests cannot prove that every future agent will follow the rules.

A schema name selects mutable files, not a frozen revision of their content.
Check active changes before updating shared schema semantics.
Use a new schema name for incompatible artifact changes instead of silently breaking existing work.
Keep the built-in `spec-driven` schema available as a fallback.

## Close with an explicit next action

Request Git delivery when ready; distinguish committing from pushing.
Confirm the target and scope for publication or external messages.
A general completion request does not authorize either.

```text
Commit the verified changes for this task. Do not push.
Report remaining blockers and the next action.
```

Use `feedback-loop` when closing or examining repeated friction; it proposes supported changes
without applying them.
A review can legitimately produce no improvement proposal.
Compare observed outcomes and correction effort against the original problem after an approved
change.
Without follow-up evidence, improvement remains unverified even when installation and static checks
pass.
Approved follow-up work uses its owning workflow; closure itself does not authorize policy changes
or new records.
Keep durable outcomes and next steps with their repository or vault owner, following local
recording rules.

**For the next session:** Carry current decisions, verified outcomes, unresolved issues, and next
actions.
Link relevant context rather than copying the entire transcript.
The agent should retrieve relevant context and recheck claims that affect the new task.
