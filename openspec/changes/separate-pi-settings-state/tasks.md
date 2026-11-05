# Tasks

## 1. Approved work

- [x] 1.1 Implement settings delivery and integration; pass isolated migration, preservation,
  failure, and idempotency tests.
- [x] 1.2 Update canonical Pi guidance and existing routes; verify links, commands, and repository
  lint.
- [x] 1.3 Migrate local settings without package updates; verify state preservation and unchanged
  tracked defaults after local writes.

## Evidence and limits

Approval and boundaries are recorded in [the proposal](proposal.md).
Fresh-session model compliance remains separate from static documentation-route verification.

- Eleven isolated tests pass, including Dotbot settings-step execution and repeat-run metadata checks.
- `just lint` passes; concurrent Cursor/Herdr work remains outside this change.
- All 107 local links and anchors across the instruction-to-Pi documentation route resolve.
- Native OpenSpec strict validation and `git diff --check` pass.
- Local settings are a regular file retaining `lastChangelogVersion: 1.5.0`.
- Repeated local sync preserves source bytes, installed bytes, and modification time.
- Simulated Pi bookkeeping writes leave tracked defaults unchanged in isolated tests.
- The existing harness suite retains three failures, four errors, and two skips before and afterward.
  Failures concern removed subagent configuration, packages, links, development wiring, and the
  missing delegation guide.
- No full workstation sync, package upgrades, authentication, or provider calls ran.
  Fresh-agent behavior remains untested.

Review was self-review, not independent review.
Follow up separately on stale harness tests; this change does not restore removed subagent support.
