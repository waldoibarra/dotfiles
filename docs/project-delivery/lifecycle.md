# Decide what deserves delivery

For route selection and applicability, start at the [project-delivery overview](README.md).

Use only the phases needed for the project's question and risk.
Move through qualification, optional discovery, route selection, bounded experiment,
implementation, and acceptance when applicable. Each gate may end with **stop**, **revise**,
**defer**, or **continue**. Commercial terms belong in [commercial
decisions](commercial.md); production gates belong in
[operations](operations.md).

## 1. First contact and qualification

**Value:** Avoid building an unsuitable solution. **Inputs:** Project goal,
current process, urgency, authority, and rough constraints. **Accountable:**
Delivery owner qualifies; project owner validates priorities and access.

- **Core:** Ask who suffers, what happens today, and what failure costs.
  Example: A manager spends hours reconciling stock adjustments across
  locations.
- **Core:** Establish decision authority, available users, and access constraints.
  Record the problem, uncertainty, proposed next step, and exclusions proportionately.
  For client work, assess sponsor authority and paid-discovery fit in an opportunity note.
- **Conditional:** Inspect existing tools when the client uses a vendor. Skip
  without a vendor or access; consequence: comparisons remain provisional until
  access exists.
- **Exit:** Investigate meaningful unknowns before committing to implementation.
  Offer paid discovery only when client terms and access support it.
  For known, low-risk work, skip discovery with documented evidence and project-owner approval.
  Consequence: undiscovered risks remain outside any estimate; stop if material uncertainty persists.

## 2. Discovery when needed

**Value:** Resolve the most costly unknown before recommending implementation.
**Inputs:** Recorded question and agreed discovery scope; client work may require a paid agreement.
**Accountable:** Delivery owner leads research; project owner supplies access and approves decisions.

- **Core:** Observe representative users and map one end-to-end workflow,
  exceptions, and existing records. Example: Map receiving, transfer, sale,
  waste, and count for one ingredient.
- **Core:** Define baseline, proposed outcome metric, measurement owner, and
  measurement period. Example: Compare sampled transfer discrepancies before and
  after a trial; no target is assumed.
- **Core:** Record constraints, alternatives, unknowns, and a stop
  recommendation. Deliver a short discovery brief and recommendation, not a
  speculative full PRD.
- **Conditional:** Review fiscal, payment, privacy, accessibility, or
  employment obligations when the workflow touches them. Skip irrelevant
  domains; consequence: unreviewed regulated scope cannot be promised.
- **Conditional:** Audit device, network, and vendor capabilities when adoption
  depends on them. Skip if irrelevant; consequence: hardware-dependent promises
  remain blocked.
- **Exit:** Deliver the discovery brief and route decision.
  Project owner chooses stop, configure, integrate, buy, prototype, or build.
  For client work, discovery payment does not authorize construction.

## 3. Choose the smallest credible route

**Value:** Spend only where the expected benefit exceeds switching, operating,
and risk costs. **Inputs:** Discovery brief or documented low-risk evidence,
relevant vendor findings, constraints, and estimated ownership costs.
**Accountable:** Delivery owner compares; project owner selects.

- **Keep or configure:** Existing tools cover critical journeys. Check
  licensing, workflow fit, training, and exports.
- **Buy:** A supported product covers critical journeys. Check ownership cost,
  lock-in, support, offline behavior, and data access.
- **Integrate:** Systems work separately but handoffs fail. Check interface
  rights, reconciliation, recovery, and vendor change risk.
- **Build:** Essential needs remain unmet. Check maintenance burden, timing,
  security, and operational capacity.

**Core:** Compare routes using the same sample journey, expected cost range,
reversibility, and evidence gaps. Example: Test whether configured inventory
transfers eliminate double entry before proposing a custom transfer service.
**Conditional:** Commission a spike when one integration risk blocks a decision.
Skip when documentation and demonstrations suffice; consequence: avoidable
experiment cost remains unspent. **Exit:** Deliver a comparison note naming the
chosen route and tradeoffs. Project owner approves next steps or stops; material unknowns
remain explicit. Client funding needs separate approval.

## 4. Bounded experiment

**Value:** Test a risky assumption without committing to production. **Inputs:**
One question, demonstration audience, synthetic fixtures, limit, and stop
condition. **Accountable:** Delivery owner designs; project owner observes and decides.

- **Core when prototyping:** Declare what the demonstration can and cannot
  prove. Example: Simulate selling one prepared item and reducing ingredient
  quantities.
- **Core when prototyping:** Agree observation method and a decision threshold
  as a proposal before testing. Capture observed steps, confusion, errors, and
  unresolved risks.
- **Conditional:** Use a disposable interface when users need to judge
  interaction. Skip when a paper journey or vendor configuration answers the
  question; consequence: less UI fidelity.
- **Exit:** Deliver an observation note and discard, repeat, or
  production-scope recommendation. A convincing demo never authorizes
  deployment.

## 5. Plan, deliver, and validate approved durable scope

This phase applies to durable implementation, not disposable prototypes.
For prototypes, use the bounded agreement and observations in [phase 4](#4-bounded-experiment).
Do not require production test infrastructure for disposable work.
**Value:** Deliver a narrow usable outcome with traceable acceptance.
**Inputs:** Approved scope, acceptance examples, and an owner; client work also needs agreed terms.
**Accountable:** Delivery owner plans and verifies; project owner approves the plan and product decisions.

- **Core before building:** Approve a proportionate delivery plan covering
  workflow, data invariants, permissions, security, and acceptance. Check
  integration, hardware, offline, deployment, and recovery risks when
  applicable. Deliver a reviewed plan with responsible owners and verification.
  Example: Specify that a short receipt never silently closes a transfer. The
  project owner approves product behavior; the delivery owner confirms technical
  feasibility. Stop if unresolved risks prevent safe implementation.
- **Core:** Break work into reviewable journeys with expected results and
  exceptions. Example: A transfer remains pending until receipt confirms the
  received quantity.
- **Core:** Review demonstrated behavior against acceptance examples, defects,
  and measured outcomes. Keep change requests separate from defects against
  agreed scope.
- **Conditional:** Maintain a PRD for multiple stakeholders or unstable
  requirements. Skip for a narrow, agreed journey; consequence: use a concise
  approved scope instead.
- **Exit:** Deliver a validated increment and test evidence before readiness.
  Critical acceptance examples must pass; otherwise fix, re-scope, or pause.

## 6. Production, acceptance, and service

**Value:** Keep operations recoverable after launch. **Inputs:** Verified
release evidence and named operational ownership; client work also needs support and payment terms.
**Accountable:** Delivery owner prepares handover; named operator assumes agreed duties.
Skip this phase for disposable prototypes; deployment requires separate production approval.

- **Core:** Exercise rollout, reversal, training, handover, and acceptance
  using [release and support procedures](operations.md). Example: Restore a
  backup before one-site launch. Rehearse failed stock migration when replacing
  existing records.
- **Conditional:** Stage multiple locations when failure can disrupt multiple
  teams. Skip for isolated low-risk use; consequence: broader simultaneous
  exposure requires explicit approval.
- **Exit:** Deliver release evidence, recorded acceptance, and an ownership handover.
  For client work, obtain signed acceptance and invoice only under agreed terms.
  Retain support ownership only when agreed; close through maintenance, replacement, or offboarding.
