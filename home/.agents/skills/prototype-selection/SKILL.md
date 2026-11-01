---
name: prototype-selection
description: >-
  Selects a throwaway prototype or POC by goal, evidence, and tradeoffs, including ambitious hybrid formats.
  Use when asked to "prototype this", "build a POC", or compare ways to test an idea before production.
---

# Select a prototype that answers the question

- **IS:** selecting and bounding a disposable experiment, then routing approved execution to the
  relevant specialist.
- **IS NOT:** implementing the whole product or replacing Matt Pocock's code-focused `prototype`
  skill.

**Done:** The user has a supported recommendation, meaningful alternatives, evidence limits, and
an executable experiment agreement.
Selection-only requests stop there; approved build requests continue through execution and
observation within that agreement.
Do not turn example ideas or a request for reusable guidance into authorization to build.

## Read only what the decision needs

| Before… | Read |
| --- | --- |
| Comparing formats, mixed media, or tool prerequisites | [Options and capabilities](references/options.md) |
| Choosing game mechanics, engagement incentives, or immersive experiences | [Gamification evidence](references/gamification.md) |
| Exploring a materially different or ambitious approach | `~/.agents/references/ambition.md` |

## Establish the experiment

Extract settled answers from context; ask only questions that change selection or execution.
Identify the decision, audience, main uncertainty, constraints, and observation that would change
the decision.
Distinguish personal exploration, communication, usability, demand, technical feasibility, and
business viability.
A technical POC cannot establish demand merely because it works.
Name what must genuinely work, what may be simulated, and when the experiment stops.
Keep this agreement in conversation; follow the shared session workflow rather than creating
OpenSpec artifacts.

## Recommend and compare

Recommend one best-fit approach and offer one or two credible alternatives with explicit tradeoffs.
Include an inventive or ambitious option when it could materially improve the outcome or learning.
Compare evidence quality, realism, audience access, total effort, cost, risk, and iteration speed
as relevant.
Account for setup, recruitment, operation, and cleanup, not just generation or coding time.
Neither cheapest nor most elaborate wins automatically.
Explain why the recommendation fits this experiment and what each candidate cannot establish.
Consider combined formats; an app can embed 3D, generated video, images, audio, and AI interactions.

Identify required capabilities and their verified states before promising readiness.
MCP is an optional access mechanism, not a prerequisite for every external tool.
Propose missing setup separately; preserve existing installation, spending, sharing, and privacy
approvals.
Obtain approval for the experiment agreement before building; carry existing approval forward
without repeated selection.

## Hand off disposable execution

The shared session workflow owns throwaway boundaries and production-promotion approval.
For logic or UI questions, read `~/.agents/skills/prototype/SKILL.md` for branch-specific
construction guidance.
Use its logic or UI branch within the approved experiment boundaries.
Do not execute its capture rule without separate approval for production integration and Git delivery.
Our session workflow takes precedence over upstream instructions requiring commits, issue updates,
or production changes.
For other formats, use the matching specialist or direct file/API tools within the approved scope.
Report a missing execution dependency before dependent work; do not invent its procedure.

Tell the executor the question, chosen approach, simulated parts, observation, resource limits,
and stopping condition.
Do not add test suites, linting setup, coverage targets, or production hardening to disposable work.
Inspect enough output to answer the question; a benchmark or model evaluation may itself be the
experiment.
Use temporary data and mock dependencies unless realism in those areas is being tested.
Keep credentials, private information, participants, and external systems protected despite the
artifact's disposable status.

## Conclude with learning

Report observations, interpretation, limitations, and the resulting decision separately.
An impressive output, model agreement, or passing smoke check does not prove demand or general
reliability.
Retain useful findings in the owning project when permitted; do not manufacture learner progress
or mandatory records.
Preserve runnable evidence when useful and authorized; prototype success does not authorize
committing or production changes.

## Sources and boundaries

[Matt Pocock's prototype skill](https://www.aihero.dev/skills-prototype) owns narrow code
experiments.
This skill adds selection across formats rather than copying or modifying the external
implementation skill.
[Strategyzer's Test
Card](https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card)
informs hypothesis, observation, measurement, and stopping criteria.
[Marty Cagan's discovery risks](https://www.svpg.com/four-big-risks/)
help distinguish value, usability, feasibility, and viability evidence.

**Maintenance:** Read `evals/evals.json` when changing routing or behavior.
These are scenario specifications, not evidence of executed model comparisons.
