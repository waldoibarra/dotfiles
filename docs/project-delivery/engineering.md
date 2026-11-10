# Test uncertain workflows, then build only approved scope

For phase decisions and deliverables, see the [project-delivery overview](README.md) and [lifecycle](lifecycle.md).

**Core:** Choose one owner for each product rule and link related tickets,
tests, and agent prompts. Product scope lives in an approved scope or PRD; tests
encode observable cases. Tickets track execution; release evidence records
actual verification. Never paste duplicate requirements into every artifact.

**Filled scope example, proposed:** Problem: staff cannot confidently reconcile
stock transfers. Outcome: managers identify mismatches before closing transfers.
Scope: dispatch, partial receipt, and discrepancy visibility. Exclusions:
payments, fiscal documents, and purchase orders. Acceptance references: the
approved transfer workflow's short-receipt and permission-denial examples. The
approved scope owns these facts; tickets and tests link rather than restate
them.

## Select a useful artifact

- **Core:** Record a workflow and acceptance examples for consequential user
  actions. Example: Receiving fewer units than dispatched records a discrepancy
  without silently closing the transfer.
- **Conditional:** Add a PRD when several stakeholders need one evolving
  product contract. Skip for a single bounded journey; consequence: approved scope
  and acceptance cases carry intent.
- **Conditional:** Add research when decisions depend on external facts or
  uncertain user behavior. User observation is research; record methods and
  findings. Skip a separate report when observations already answer the
  question; consequence: evidence remains limited to observed cases.
- **Conditional:** Record an architecture decision when reversal is costly and
  alternatives matter. Skip ordinary implementation choices; consequence:
  rationale stays in the scoped plan.
- **Conditional:** Add specialist review for payment, security, or regulatory
  exposure. Skip outside those domains; consequence: no specialist assurance can
  be claimed.

## Prototype with explicit limits

**Core when prototyping:** Agree question, audience, fixtures, observation,
budget, and stop rule first.
Use the [disposable-work route](/docs/ai-harness/session-workflow.md#prototype).
Production hardening and durable implementation require separate approval.
Use synthetic people, transactions, sales, and inventory.
Do not copy private or client data into prompts or demonstrations. Example: A
synthetic prepared-food sale consumes fictional ingredient quantities and
displays a shortage. Ask observers to predict the resulting stock record. Record
successes, misunderstandings, timings when useful, and confounders. Recommend
discard, rerun, or separate durable scope. See [phase gates](lifecycle.md).

**Conditional:** Test competing interaction concepts when users disagree about a
control. Skip when one pattern already passes observation; consequence: fewer
alternatives explored. **Conditional:** Test offline behavior when a
disconnected sale is possible. Skip when the workflow cannot operate offline;
consequence: offline selling remains unsupported, not implicitly guaranteed.

## AI-assisted delivery

**Core when using AI:** Give each agent one bounded task, context links,
exclusions, and an executable check. Human owner approves scope, external
disclosure, expenditures, privileged actions, and release. Configure tool
permissions and spending limits where available; prompts alone cannot enforce
hard boundaries. Redact sensitive inputs and verify provider retention rules
before sharing private or client material.

**Core:** Inspect diffs and tests independently of agent summaries. Run relevant
checks and compare negative cases, authorization boundaries, and data
migrations. Verify that tests fail for a deliberately wrong behavior before
trusting newly generated regression coverage. Record changed files, test output,
model/tool provenance when relevant, unresolved risks, and actual reviewer
signoff. No model result counts as project-owner or client acceptance.

**Conditional:** Use multiple agents for separable research or implementation
tasks. Skip when coordination exceeds expected benefit; consequence: less
parallelism, clearer ownership. **Conditional:** Compare AI-assisted and manual
execution on representative work when claiming productivity gains. Skip if no
productivity claim; consequence: never advertise measured speedups. Track time,
correction effort, defects, and token or service costs.

Treat generated instructions as advisory; place nonnegotiable checks in
enforceable gates. NIST's SSDF supports integrating secure practices into any
lifecycle, not replacing review with a label.
[Dated research](/docs/spikes/ai-assisted-client-delivery.md) details evidence and
counterevidence.
