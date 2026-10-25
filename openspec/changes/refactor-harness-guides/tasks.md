# Tasks

## 1. Approved work

- [x] 1.1 Refactor entrypoints and ownership references; verify preservation and reading routes.
- [x] 1.2 Review focused guides; verify distinctions between guidance, history, and unknowns.
- [x] 1.3 Repair related links and indexes; verify local destinations and anchors.
- [x] 1.4 Run documentation and schema checks; record evidence and remaining limits.

## Evidence and handoff

The working tree was clean before this change.
Runtime configuration and frozen records remain outside the edit scope.
Publication to the existing `origin/main` branch is authorized after verification.

### Preservation review

All twelve original guides were reviewed; three focused reference pages were added.
Ownership, Cursor rendering, and Claude copy behavior now live in `configuration.md`.
Ghostwriter routing and privacy boundaries now live in `ghostwriter.md`.
Behavioral scenarios remain in `verification-cases.md`, separate from verification procedures.
Pi trial versions remain in `pi/limitations.md`; original records and frozen history were not rewritten.
Retired migration commentary and duplicated skill/model advice were removed from operational guides.
The obsolete smoke-prompt reference to a Learning instruction now names maintainability.
Work-parity wording now respects the existing requirement for separately authorized company changes.
Known incoming links were repaired; referenced README anchors still route readers to their owners.

### Observed checks

| Check | Result |
| --- | --- |
| `just lint-md` | Passed across 129 discovered Markdown files |
| `just lint-ec` | Passed |
| `just lint-yaml` | Passed |
| `git diff --check` | Passed |
| Local path and anchor check | 240 links resolved across 22 changed or scoped documents |
| Prose rule | Only the preserved publication warning exceeds 17 words; safety-text exemption applies |
| `test-openspec-schema.py` | 5 tests passed |
| `test-cursor-rule.py` | 6 tests passed |
| `test-personal-mcp.py` | 6 tests passed; optional native-Claude test skipped |
| `test-agent-harness.py` | 13 tests passed; 2 compiled-host checks skipped |
| `test-openspec-sync.py` | 1 test passed |
| Native change validation | Passed with documentation-only specification skipping |

Configuration claims were checked against tracked settings, links, scripts, and Pi 1.4.0 documentation.
The review was a self-review, not an independent review.
No workstation sync, model inference, OAuth, microphone exercise, or company-workspace access ran.
Compiled-host checks were skipped because `PI_PACKAGE_DIR` was not set for the suite.
Existing runtime observations remain historical; this refactor does not reverify live service access.

### Handoff

Implementation is complete; no configuration changes or additional policy proposals are needed.
Commit and push the reviewed documentation change to the authorized destination.
Native archival remains separate from this refactor.
