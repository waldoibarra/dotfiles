# Tasks

## 1. Native schema and portable delivery

- [x] 1.1 Create the native schema and templates; confirm schema validation succeeds.
- [x] 1.2 Verify artifact ordering, specification skipping, task progress, and archive behavior in
  disposable projects.
- [x] 1.3 Verify default selection and existing-change compatibility through native CLI fixtures.
- [x] 1.4 Verify schema and guide links through isolated, repeat-run Dotbot delivery.

## 2. Routing and documentation

- [x] 2.1 Document prototype exclusion and separate production approval in shared routing and the
  session guide.
- [x] 2.2 Link workflow and schema ownership, preserving current intent and feedback-loop guidance.
- [x] 2.3 Document Pi, Claude Code, and Cursor use of the maintained shared skill sources.
- [x] 2.4 Verify touched links, prose, glossary consistency, and repository lint.

## 3. Installation and review

- [x] 3.1 Install the two approved links and refresh Cursor's generated rule without unrelated
  workstation changes.
- [x] 3.2 Independently review the schema and routing against the approved plan.
- [x] 3.3 Check prototype and feedback routing in a bounded fresh-context review.
- [ ] 3.4 Verify real Cursor discovery and cross-harness execution before claiming three-harness
  runtime readiness.

## Verification evidence

Five native CLI fixtures pass, including specification skipping, archiving, progress, and
default-change compatibility.
All fifteen harness tests pass with the installed Pi 1.4.0 host checks enabled.
All six Cursor-rendering tests, repository lint, native validation, and touched-link checks pass.
Scoped Dotbot delivery preserves link timestamps on repeated runs.

Independent review identified a prototype planning conflict and stale design wording.
Both were corrected.
The default-change fixture now exercises an actual configuration transition.
The reviewer selected the expected routes for prototypes, proposal feedback, and approved
production work.
That exercise classified requests without executing them; it does not prove end-to-end behavior.

Cursor 3.27.12 is installed, but its agent CLI is unavailable.
UI discovery, cross-harness execution, and Lluvia's installation remain unverified.
Verification used disposable fixtures and scoped link updates, not a full workstation update.
The user subsequently authorized Git delivery and the AI harness documentation rename.

## Workflow follow-up

- Keep the broader historical-document refactor deferred.
- Keep Lluvia's machine verification separate from local delivery checks.
- Archive through native tooling after the remaining acceptance checks and review are complete.
