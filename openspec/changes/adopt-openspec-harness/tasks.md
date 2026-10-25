# Tasks

## 1. Native setup and delivery

- [x] 1.1 Install the Mise-managed CLI and confirm its actual version.
- [x] 1.2 Generate core skills using native initialization with skills-only preferences.
- [x] 1.3 Link both clients and native configuration; pass isolated delivery and repeat-run checks.
- [x] 1.4 Verify native update no-ops and error propagation with isolated synchronization tests.

## 2. Approval and collaboration guidance

- [x] 2.1 Document refinement, plan approval, and OpenSpec artifact rules in shared instructions.
- [x] 2.2 Document lead-owned cross-harness coordination and Herdr's verified control surfaces.
- [x] 2.3 Clarify vault verification and confirm edited notes through lint and retrieved Sync content.
- [x] 2.4 Validate authored artifacts, instruction links, and generated-source preservation.

## 3. Runtime acceptance

- [x] 3.1 Run the authorized workstation sync and record completed steps and blockers.
- [ ] 3.2 Verify fresh-session skill loading and a same-harness delegation against the approved change.
- [ ] 3.3 Verify a cross-harness handoff without copying conversation history or overlapping writes.
- [ ] 3.4 Verify Lluvia's machine separately after its own synchronization and client reload.

## Verification checkpoint

OpenSpec structural validation and repository lint pass.
Harness tests pass with two optional host checks skipped.
Synchronization tests cover eight preview/update cases.
Independent review found a missing expected-skill assertion; the fix and both suites pass.
The reviewer resumed from native change artifacts without prior chat.
This does not establish fresh-session global discovery or a cross-harness implementation handoff.

The first `dots` attempt stopped before synchronization because local and remote commits diverged.
The user approved reconciliation; all 142 preserved paths matched their backup after restoration.
Rebasing changed local `15f1c16` to `7062f42` above remote `b9b570d`.
The second `dots` run completed successfully and published `7062f42` plus skill-lock update `35b52b8`.
OpenSpec 1.15.0 and six valid skill links per client were verified afterward.
Native usage exposed machine telemetry data in the linked configuration.
Portable preferences now disable telemetry.
Git delivery and Lluvia's installation remain separate from these local verification results.

## Workflow follow-up

- Keep the change active until remaining acceptance is verified.
- Refactor historical documentation in the separately requested next session.
- Archive through the native CLI only after completion and the applicable review boundary.
