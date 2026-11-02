# Proposal

## Why

Claude delegation should use our Herdr coordination guide instead of native subagents.
Firstmate remains future work.

## What Changes

Deny `Agent` and its legacy `Task` name in tracked Claude user settings.
Route Claude delegation through existing coordination instructions and document the restriction.
Preserve checklist tools, other clients, hooks, model defaults, and permissions unrelated to delegation.

## Approach and tradeoffs

| Decision | Choice | Reason |
| --- | --- | --- |
| D1 | Native permission denial | Enforces the restriction without another hook |
| D2 | Deny both tool names | Covers current naming and older clients |
| D3 | Existing managed-copy delivery | Keeps `dots` authoritative without another installer |

Instruction-only prohibition is weaker than tool denial.
Blocking only built-in agent types would leave custom native subagents available.
This restriction also blocks custom subagents; Herdr workers remain available.
Outside Herdr, report delegation unavailable instead of bypassing the restriction.
Rollback removes these deny entries and routing guidance, then refreshes installed settings.

## Capabilities

- New `claude-delegation-policy`: user-level native delegation denial and Herdr routing.

## Impact

Owners: `home/.claude/settings.json`, shared orchestration guidance, and harness configuration documentation.
Regression checks belong in `scripts/tests/test-agent-harness.py`.
The existing managed-copy function delivers settings without running package upgrades.
No Firstmate installation, additional delegation bans, or changes to other clients are included.

## Verification

Check isolated settings delivery twice and preserve unrelated settings and checklist availability.
Run focused harness tests, Markdown checks, and diff validation.
Refresh installed settings through the existing delivery function and compare them with tracked bytes.
Report fresh-session enforcement separately from static and installation checks.

## Approval

The operator approved global subagent denial after reviewing the scoped implementation plan.
The preceding request authorized committing and pushing the completed change.
`Task` denotes the former delegation tool name, not task checklist tools.
