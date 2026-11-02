# Tasks

## 1. Approved work

- [x] 1.1 Deny native delegation, update guidance, and pass focused delivery tests and lint.
- [x] 1.2 Refresh installed settings and verify their denial matches tracked configuration.

## Evidence and handoff

The operator approved the scope and requested commit and push after verification.
The focused `test_claude_delegation_denial_survives_repeated_delivery` check passes.
It exercises two isolated deliveries.
Changed Markdown passes lint, including the installed orchestration reference through stdin.
`git diff --check` and strict OpenSpec validation pass.

The broader harness suite has three failures and four errors concerning removed Pi subagent support.
Running the unchanged test source from `HEAD` reproduced the same seven failures.
Two compiled-host tests were skipped because `PI_PACKAGE_DIR` was unset.
These unrelated failures remain outside this change.

Review was sequential self-review, not independent review.
The existing managed-copy function refreshed installed Claude settings without package upgrades.
Installed bytes match the tracked source; both delegation names are denied.
Fresh-session enforcement and instruction compliance remain unexercised.
Restart Claude before relying on the new configuration.
No inference probe ran because the verification guide retains an unresolved quota-recovery restriction.
