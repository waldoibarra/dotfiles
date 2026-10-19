# Orchestration detail

Read before planning non-trivial work or delegating.

Global authority, model exclusions, quota stops, and retry limits remain binding.

## Plan and deliver

- Plan, independently review, implement test-first, audit against the plan, verify behavior, then
  update documentation.
- Define observable acceptance before implementation. Documentation-only work needs factual and link
  checks, not fabricated runtime failures.
- Keep plan decisions in a table: stable IDs, decision, reason. `docs-maintenance` owns superseding
  rows.
- State decided rules in documentation, comments, tests, PRs, and tickets; omit plan-only IDs and
  session codes.
- When reviews converge, propose a fix freeze; defer later findings to the next iteration.
- Write ADRs or RFCs only when requested or required by the project's process.

## Dispatch workers

- Choose role, model, and supported effort independently. Shared roles stay provider- and
  effort-neutral.
- Brief each worker with its goal, files, constraints, acceptance criteria, and prohibited commands.
- Run at most four workers on one task at once.
- Use one worker for a search or alternatives survey, never one worker per query or source.
- Bind each worker to its intended repository; verify the Git root before source inspection.
- Report unavailable models or effort controls. Use supported or actual/default effort; never invent
  API parameters.
- Do not silently substitute models.
- Without delegation, work sequentially; identify self-review as non-independent.

## Select by scope

Determine scope from project and user context, never client, provider, or payment.

**Company sessions:** use the strongest eligible worker for planning, review, and audit.

- Use a mid-tier worker for implementation and the smallest for lookups, unless adaptation is
  approved.

**Personal/open-source sessions:** select the least expensive capable non-lead worker within the
authorized provider.

- Consider context, tools, risk, observed reliability, latency, and usage; briefly record the
  rationale.
- Pi workers use available OpenAI models; Claude workers use Anthropic models.
- Give each child one acceptance target.
- Avoid rereading unchanged context; reuse retained context only for focused follow-ups.
- Summarize passing checks. Close activation blockers before opening additional implementation
  lanes.

## Verify safely

- Bound fixture runtime, provider calls, and output; preserve required evidence.
- Stop owned processes before deleting artifacts on success, failure, timeout, and cancellation.
- For async UI, test concurrent input across awaits before mutating drafts or queued work.
- Verify actual interfaces; mocks alone do not establish compatibility.
