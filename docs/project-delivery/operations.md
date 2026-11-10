# Release safely, transfer control, and leave a usable exit

For phase timing, start at the [project-delivery overview](README.md) or [lifecycle](lifecycle.md).

Production is a separate approved decision. A demo, passing unit tests, or
stakeholder enthusiasm does not establish readiness. **Accountable:** Delivery owner
produces evidence; project owner authorizes rollout; named operator owns daily
operation. For client work, the project owner is the authorized sponsor.
One person may perform several duties, but responsibilities remain explicit.

## Readiness and rollout

**Core before production:** Confirm project-owned accounts, access roles,
network assumptions, and support contact. Check devices and printer behavior
when hardware is involved. Example: Record which checkout terminal and printer
each location actually uses.
**Conditional:** Rehearse migration, record counts, reconciliation, and
previous-path retention when replacing or moving existing records. Skip without
migration or replacement; consequence: no legacy reconciliation or fallback
claim applies. **Core when retaining data:** Restore a backup on a recoverable
copy. Test reversal of the release using an agreed recovery path. **Core:** Test
representative sale, refund, stock adjustment, permission denial, and
reconciliation exceptions where included. Collect release version, checks, test
output, known limitations, and decision signoff.

**Conditional:** Test offline checkout, collisions, and synchronization only
when offline selling is supported. Skip without offline support; consequence: no
disconnected sale is promised. **Core:** Rehearse the outage fallback and train
staff to recover safely. Example: Record transactions through the agreed manual
process until connectivity returns. **Conditional:** Pilot one site before wider
rollout when locations share financial or stock records. Skip when isolated
testing and reversal sufficiently contain risk; consequence: broader
first-release exposure needs project-owner acceptance. **Conditional:** Add a
parallel-run window for replacing a live financial system. Skip when no
replacement occurs; consequence: there is no side-by-side reconciliation.

Check failed transactions, stuck transfers, sync backlog, backup failures, and
access anomalies where applicable. Define who watches each signal and what
response starts. Train real operators with one successful journey and one
failure recovery. Example: A cashier records a discrepancy; the manager knows
how to investigate without editing history.

## Acceptance, collection, and handover

**Core:** Demonstrate agreed acceptance scenarios, log remaining defects, and
request recorded acceptance from the project owner. For client work, obtain written
acceptance from the authorized sponsor. Record accepted limitations and the next owner;
invoice only against contractually agreed milestones.
For client work, [commercial terms](commercial.md) own review windows and payment triggers.
**Core:** Hand over account ownership, access inventory, runbook,
backup restoration steps, vendor contacts, and escalation contact. Transfer
secrets through an approved channel, never documentation or an AI prompt.
Confirm the operator can repeat a recovery step unaided.

**Conditional:** Offer enhanced response coverage if the client needs
after-hours operation and funds staffing. Skip otherwise; consequence: support
follows agreed business hours and service limits.

## Maintain, respond, and exit

**Core during agreed support:** Define intake channel, severity, coverage hours,
first response, investigation owner, and update cadence. Example: A failed
payment recording triggers incident triage; do not retry blindly without
checking settlement. Preserve evidence, contain impact, communicate verified
facts, restore service, reconcile records, and review recurrence. Separate
warranty defects from enhancements and third-party incidents. Measure incident
duration, recurring errors, and usage against agreed outcomes. Schedule upgrades
and access reviews only when ongoing maintenance is contracted.

**Core at exit:** Export project data in an agreed format and demonstrate
readability. Transfer account control and revoke delivery-team access.
For client work, agree final invoices, outstanding risks, retention, deletion evidence,
and transition assistance under contract. **Conditional:** Run a rehearsal with a replacement
supplier when migrations or lock-in make transfer risky. Skip for simple
exports; consequence: the client validates the handoff independently.

**Handover example:** Client operator can restore a test backup and reconcile
three synthetic sales. Project owner accepts known limitations. Delivery owner records the
support start and coverage boundaries when support is agreed. These are illustrations, not observed
client results.
