# Tasks

## 1. Manifest and migration

- [x] 1.1 Add the manifest and validation, preserving existing shared skill names and sources.
  Verify all three targets and reject invalid entries before mutations.
  Load the manifest repository-relatively, testing absent installed copies and unrelated working directories.
- [x] 1.2 Replace lockfile-driven installation and remove its automatic Git delivery.
  Add read-only ownership checks before Dotbot cleanup and before standalone reconciliation.
  Test fresh homes, regular lockfiles, legacy links, missing targets, and unknown-link conflicts.
  Verify unknown broken links survive rejected installer runs and installer dry-runs remain non-mutating.
- [x] 1.3 Reconcile missing content and client delivery without rewriting already-correct installations.
  Gate native call selection on isolated unchanged-input evidence, including source conflicts.
  Stop for plan revision if native behavior cannot satisfy fixed-input idempotency.
- [x] 1.4 Add `scripts/tests/test-skill-sync.py` with repeated-run and partial-failure fixtures.
  Check bytes, timestamps, modes, links, local-only preservation, and absence of Git publication.

## 2. OpenSpec generation and delivery

- [x] 2.1 Untrack generated skills and remove premature generated-skill links from Dotbot.
  Retain authored OpenSpec content and add targeted generated-output ignores.
- [x] 2.2 Generate before reconciling discovery links for Pi, Claude Code, and Cursor.
  Verify missing-file bootstrap with the native CLI and preserve native no-op preview behavior.
- [x] 2.3 Extend `scripts/tests/test-openspec-sync.py` for bootstrap, conflicts, failure, and retry.
  Assert repeated fixed-input runs preserve skill bytes, timestamps, modes, and links.

## 3. Dots integration and agent guidance

- [x] 3.1 Exercise the real `dots` alias and recipe chain in isolated workstation fixtures.
  Stub unrelated package, vault, authentication, and publication effects, not skill reconciliation.
  Verify existing-user migration and fresh installation under different home and checkout paths.
  Exercise installer-only bootstrap, subsequent `dots`, and standalone `just update-ca` separately.
- [x] 3.2 Test a published manifest addition across two isolated machine checkouts.
  Verify all declared clients discover it after their normal sync path.
- [x] 3.3 Update `docs/agent-skills.md` with enrollment, installation, verification, and sharing instructions.
  Add focused agent navigation and reconcile obsolete publication guidance in affected current guides.
  Update `docs/setup.md` to distinguish initial installation from agent provisioning.
- [x] 3.4 Run focused Python checks, `just lint`, and `git diff --check`.
  Run `openspec validate separate-skill-intent-from-state --strict --no-interactive`.
  Run `openspec schema validate session-workflow`.
  Record unrelated failures without expanding implementation scope.

## 4. Client acceptance

- [x] 4.1 After announcing deployment, exercise the approved real `dots` path on the available workstation.
  Inspect tracked state before and after; distinguish unrelated sync mutations from skill reconciliation.
- [x] 4.2 Use fresh Pi and Claude Code sessions through Herdr for read-only discovery checks.
  Explicitly select eligible models and verify skill names, source paths, and harmless invocation.
  Close only owned test sessions; stop and report quota, authentication, or permission blockers.
- [ ] 4.3 Verify Cursor's native skill discovery and record any unavailable interactive check.
  Do not substitute filesystem existence for evidence that Cursor loaded the skills.
- [x] 4.4 Record per-machine and per-client evidence and remaining activation requirements.
  Do not mark Lluvia's workstation verified without exercising it there.

## Evidence and handoff

Implementation approved by the user's explicit instruction to proceed.
The existing `dots` alias invokes the repository's `just sync` with an explicit working directory.
Fresh Pi and Claude Code acceptance sessions were launched through Herdr and closed after verification.
Independent review found pre-clean ownership and manifest-loading gaps in the original draft.
The revised plan adds pre-clean validation, repository-relative loading, and two-stage bootstrap tests.
Native fixed-input idempotency passed isolated checks and a repeated live skill reconciliation.
Initial change and schema validation passed; validation is repeated after review revisions.

Delegated implementation and one repair pass completed; two independent reviews assessed the diff.
The lead reran 17 skill-sync tests and three OpenSpec tests successfully.
Read-only workstation preflight accepted all 73 declared skill entrypoints.
Workstation deployment and sampled Pi/Claude skill invocation are verified below.
Cursor loading and Lluvia's workstation remain unverified.

The second review identified a dangling generated-document symlink hazard.
A bounded lead fixture confirmed partial repair writes through that link before reporting failure.
Only disposable fixture files were affected; the workstation was not changed.
The user approved a focused repair after the second review.
The delegated repair now rejects generated-document symlinks before every generation path.
The lead reran 17 skill-sync, four OpenSpec, 15 harness, and eight bootstrap tests.
All passed except two skipped compiled-host checks; the OpenSpec test exercises native partial repair.
Eight generated-state paths were untracked while preserving their working copies.

## Deployment evidence

The actual `dots` alias completed with exit zero in a dedicated Herdr pane.
The native local lockfile became a regular file, leaving its former tracked working copy intact.
All three client directories contain 73 external, 11 repository-owned, and six generated skills.
A repeated live skill/OpenSpec reconciliation compared 1,325 entries and changed none.
The comparison included file bytes, modes, modification times, and symlink targets.
Git HEAD remained unchanged; no commit or push occurred.
The existing full sync also upgraded hk and reconciled packages, vault configuration, and integrations.

Fresh Pi used `openai-codex/gpt-6-sol` with read-only tools and low effort.
Its startup catalog listed shared skills, including all three sampled ownership categories.
Fresh Claude Code resolved the explicit `haiku` selection to `claude-haiku-5-5` with low effort.
Both reported discovery of `animation-vocabulary`, `docs`, and `openspec-propose`.
Both loaded and exercised `animation-vocabulary`, correctly identifying the popover effect as `Pop in`.
Claude's native Skill-tool result independently confirmed successful loading.
The authored and generated samples were discovered, not behaviorally exercised.
Only owned acceptance panes were closed.

Cursor 3.27.22 is installed; its documented global directories contain all shared skills.
The standalone agent CLI was missing.
Running `cursor agent --help` unexpectedly triggered the launcher's automatic installation.
That command timed out; no further installation or model run was attempted.
A partial `~/.local/share/cursor-agent` directory remains; no executable was verified.
Cursor discovery requires a fresh native UI check or separately approved CLI setup.
No existing Cursor worker was controlled or changed.
Lluvia's machine requires publication, its next `dots` run, and fresh-client verification.

Final focused suite: 44 tests, 42 passing and two compiled-host checks skipped.
`just lint`, native change/schema validation, and whitespace checks passed.

## Deferred feedback

The lead initially prepared direct implementation before the user's delegation correction.
Implementation and repairs were then delegated; the lead retained review, Git integration, and deployment.
Review delegation selection separately with the user; no orchestration policy changed in this task.

Publication and archiving require separate authorization.
