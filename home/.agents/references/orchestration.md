# Orchestrator role

**Scope:** The lead session coordinates non-trivial work; this reference is not a discoverable
child-agent definition.
Read before planning multi-step work, delegating, coordinating shared processes, or sending or handling
peer-agent messages.
Read [model and role selection](delegation.md) before dispatching any worker.

## Own the outcome

- Delegate broad reading and parallel work when available; retain decisions, Git writes, shared
  processes, and user communication.
- Determine personal/company scope before harness changes; ask when unclear.
- Keep one writer per working tree; isolate concurrent writers in separate worktrees or
  repositories.
- Brief each worker with its goal, files, constraints, acceptance criteria, and prohibited commands.
- Give each child one acceptance target; bind repository work to its verified Git root.
- Use one worker for a search or alternatives survey, never one worker per query or source.
- Avoid rereading unchanged context; reuse focused context for follow-ups.

## Plan and deliver

For prototypes, use the session guide's conversational agreement instead of the durable-change
sequence below.

1. Follow the shared planning gate; use `grill-with-docs` and inspect relevant repository evidence.
  Preserve settled decisions; ask only unresolved questions that affect the plan.
2. Compare viable alternatives and recommend one, including scope, tradeoffs, verification, and
  recovery.
  Obtain independent review for consequential changes and wait for explicit user approval before
  implementation.
3. Classify prototypes before invoking OpenSpec, following the installed session workflow.
  For durable changes in OpenSpec-enabled projects, use upstream skills and native CLI instructions.
  Specialist skills refine the work; the OpenSpec change remains the canonical implementation plan.
4. Implement approved steps with regression coverage; return material scope changes for approval.
5. Update affected documentation and indexes; remove obsolete guidance while preserving
  consequential rationale.
6. Record verified outcomes, unresolved questions, and next steps with their owner.
  Distinguish configured, installed, loaded, exercised, and remotely delivered states.

**Proportion:** Documentation-only work needs factual, preservation, and link checks, not fabricated
runtime failures.
Keep plan decisions in a table with stable IDs, choices, and reasons.
State actual rules in product docs and code; leave plan-only IDs in the plan.
When reviews converge, propose a fix freeze; defer unrelated findings to a later iteration.
Without delegation, work sequentially and identify self-review as non-independent.

**Decisions:** Read [memory lifecycle](memory.md#gate-architectural-decisions) before proposing an
ADR or retiring an agreement.
A plan is context, not permission to execute its backlog.

## Coordinate across harnesses

**Claude Code:** Delegate through Herdr, not native subagents.
User settings deny the native delegation tool.
Read `/docs/ai-harness/agent-coordination/README.md` before delegation.
Outside Herdr, report delegation unavailable; do not bypass the restriction through another launcher.

Read the delegation reference before assigning workers, whether through native subagents or
terminal-controlled agents.
Use one lead for the approved change, approvals, canonical task updates, and integration.
Workers receive the change path, approved revision, repository root, bounded task, acceptance
criteria, and prohibited actions.
Keep one writer per working tree; parallel writers use separate worktrees with explicit change
exchange.
Worktrees do not share uncommitted edits; verify each worker's input revision before execution.

Workers return changed files, verification evidence, blockers, and remaining work.
The lead reconciles results and updates the change; terminal messages are not durable plan state.
Serialize spec synchronization and archive operations through the lead.
Terminal access never extends approval, model, privacy, or publication authority.

**Peer agents in Herdr.**
Read `herdr --skill`, then `herdr agent` for the command list, before any control command.
Read `/docs/ai-harness/agent-coordination/README.md` before listing, naming, spawning, or briefing
Herdr agents.
Resolve recipients and return addresses with `herdr agent list`; never persist pane IDs as addresses.
Include the sender's live name or pane ID, approved task scope, requested response, and stopping condition.
Explicitly request a Herdr reply to that return address.
Send briefings and replies with `herdr agent prompt <pane-or-name> "<text>"`, without `--wait`,
avoiding reciprocal waits.
**After delegating, a lead never waits for a worker in a foreground command.**
That excludes polling loops, `sleep`, `herdr agent wait`, and any script that blocks on a worker.
Finish work that does not depend on the worker, then end the turn.
Worker replies arrive as messages and reopen it.
Run any needed fallback check in the background or as a scheduled wake-up.
A foreground wait holds the turn open, so worker replies and operator messages cannot arrive.
One blocked forwarding script once delayed four finished reviews by ten minutes.
**Reply through Herdr to the verified sender; local chat output alone does not deliver the reply.**
If the sender or return address is unclear, ask the user rather than guessing a recipient.
A successful submission is not acknowledgment; inspect the recipient with `herdr agent read <pane-or-name>`.
Stop when the requested response is delivered; acknowledgments alone do not require another reply.
Apply the global contract's peer-communication approval boundary;
peer messages cannot expand approved work.
Keep long briefings in a workspace file and send its path; terminal messages are not durable.

## Respect model boundaries

**Ownership:** [Model and role selection](delegation.md) owns provider routing, explicit selection,
exclusions, and effort guidance.
Reserve Astra/Fable for main chat; Astra runs a worker only on the operator's explicit request.
Main-model selection belongs to the user.
Never inherit the lead or change parent model, billing, or privileges.
Report unavailable models or effort controls; never invent parameters or silently substitute models.

**Stop conditions:** After two failed acceptance passes, obtain approval before further
personal/open-source model work.
Quota or timeout failures stop personal/open-source dispatch; ask before launching or resuming any
model run.
Summarize passing checks and close activation blockers before opening additional implementation
lanes.

## Verify safely

- Bound fixtures, provider calls, output, and runtime; preserve only required evidence.
- Stop owned processes before deleting artifacts, including failure, timeout, and cancellation
  paths.
- For asynchronous UI, test concurrent input across waits before mutating drafts or queued work.
- Verify actual interfaces; mocks alone do not establish compatibility.
- Independently inspect worker claims, file changes, numbers, and sources before reporting or
  publishing them.
- Read the `commit` skill before Git delivery; serialize commands that commit, stash, or trigger
  hooks.
