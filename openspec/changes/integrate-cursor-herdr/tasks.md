# Tasks

## 1. Approved work

- [x] 1.1 Declare Cursor in Mise and reconcile native hooks; isolated prerequisite and
  idempotency tests pass.
- [ ] 1.2 Document ownership, authentication, verification, and rollback; repository lint and
  existing suites pass.
- [x] 1.3 Install only Cursor CLI and its native hook; verify version and integration status.

## Evidence and handoff

Five isolated Cursor integration tests and six existing Cursor rule tests pass.
Native Herdr installation in a temporary home preserved an unrelated hook.
Repeating the updater preserved file bytes, modification times, and permissions.
Repository lint and strict OpenSpec validation pass.

Installed Cursor CLI `2026.10.22-27dcf5f` through Mise.
Installed Herdr's Cursor integration v2; a second reconciliation performed no installation.
`cursor-agent status` reports `Not logged in`.
Authenticated lifecycle and session restoration remain unverified; run `cursor-agent login` next.

The existing harness suite reports three failures, four errors, and two skipped compiled-host checks.
Six failures also reproduce against an isolated HEAD snapshot before this change.
The remaining Dotbot check references removed subagent configuration, outside this change's scope.
The snapshot had additional fixture limitations from untracked shared files.
Task 1.2 remains incomplete because its full-suite acceptance is not satisfied.
No unrelated fixes or push are authorized.
