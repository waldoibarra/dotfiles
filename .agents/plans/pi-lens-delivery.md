<!-- markdownlint-disable MD013 -->
# Lens delivery current status

**Current authority:** This is the authoritative Lens coordination record.
Historical statuses are not current authorization.
Read [verification](/.agents/plans/pi-lens-verification.md) before claiming acceptance or repeating checks.
Read [remaining work](#remaining-work) before reopening an unfinished target.
Read [delivery history](/.agents/plans/history/pi-lens-delivery-2026-10-13.md) before investigating earlier decisions.
The archive preserves all decisions D1–D138, including original superseded markings.

## Current status

| Component | Published / configured | Installed / exercised |
| --- | --- | --- |
| Pi Lens | `latest` → `0.2.0`, commit `237e3c561ba68e3e77c3f18d7613c3e45756e0ae` | Normal profile; Pi 1.2.0 discovery, views, and reload passed both terminal modes |
| Claude Lens | Archived 2026-10-23 at `2c9ead4`; last release `0.1.2` (`1420f37`) | Removed from tracked settings; Claude Code now covers its features natively |
| Installed Pi | Mise `latest`, currently `1.2.0` | Unchanged by Lens delivery |
| Development Pi | Local compiled `1.1.0` | Patched host remains separate from installed Pi |
| Development launch | Local host, Lens, subagents, installed voice | Persists by default; accepts `--continue` and explicit `--no-session` |

User accepted the current presentation for now and requested more testing during ordinary use.
Pi's stock host lacks patched input-origin and clipboard metadata; unknown input labels stay neutral.
No release adds host patches, completed send-now parity, or microphone authentication guarantees.
Normal-profile upgrades used targeted native commands, not `dots` or a host/package-wide update.

## Approved harness follow-through

User approved all five improvements, normal-profile upgrades, and pushing dotfiles including `28c15d6`.

| ID | Decided rule | Current implementation |
| --- | --- | --- |
| D132 | Bind workflows to one repository and verify Git root before inspection | Native `cwd` example and tested correct/wrong-root guard in delegation guide |
| D133 | Define real-producer, runtime, failure-path, and pre-edit acceptance before edits | Acceptance matrix in personal workflow guide |
| D134 | Reuse native persistence and safe CLI passthrough | Recipe-scoped positional arguments; default persistence, continue, and ephemeral cases tested |
| D135 | Keep current status short and archive history intact | Current pages plus indexed, byte-preserved archives |
| D136 | Right-size workers under existing shared routing policy | Task-risk guidance and bounded acceptance packets; no new global model defaults |
| D137 | Upgrade normal Lens profiles with targeted native commands | Complete; versions and enabled state read back |
| D139 | Deploy both Lens packages from movable GitHub `latest` tags | User explicitly replaces version pins; supersedes archived D105–D106 deployment policy |
| D140 | Defer automated-input folding on stock Pi | Current implementation requires host attribution; replacing the runner is not a verified solution |
| D138 | Push approved dotfiles work, including `28c15d6` | Complete; remote main read back at `2ae8b67` before this record-only follow-up |

Global instructions, roles, skills, provider selection, and runner settings remain unchanged.
Documentation is an operating procedure, not runtime enforcement of worker behavior.
The persistence fixture tests the explicitly selected compiled SDK; launcher argument checks use fake Node.
No fresh live worker-behavior probe or provider conversation was used to validate these guide changes.
Implementation commits: launcher `b8126fb`, workflow `f01cd86`, compact records `2ae8b67`; all pushed and read back.

## Remaining work

| Item | State / next gate |
| --- | --- |
| Routine visual review | Continue in ordinary sessions; report concrete regressions before widening this accepted slice |
| Runner workflow teardown | Test-only draft remains unaccepted; failed-settlement cleanup still needs separately approved repair |
| Ctrl+Enter send-now | Isolated checkpoint exists, unmerged; capture retention and typed queue usage remain blockers |
| Ctrl+S stash/pop | Not implemented; occupied-stash behavior remains undecided; swap was recommended |
| Earlier duplicate-image feedback | Exact target was never resolved; obtain a concrete reproduction before changing attachment presentation |
| Host patch distribution | Not included in Lens releases; normal Pi lacks patched attribution and clipboard support |
| Claude Lens collapse click | Closed 2026-10-23 without a fix: Claude Lens is archived, and Claude Code's native collapse/expand replaces it |

Approval for the five harness improvements does not authorize unfinished runner or host lifecycle implementation.
Read [feedback history](/.agents/plans/history/pi-lens-delivery-2026-10-13.md#current-feedback-implementation)
before reopening those targets.

## Direct-launch diagnostic

Waldo reports unfolded subagent wake messages labeled `Input` when launching ordinary `pi`.
Read-back confirmed Mise Pi `1.2.0` and linked settings.
Installed Lens `v0.2.0` matched the recorded commit.
The installed runner sends this wake through `sendUserMessage`; Lens folds only inputs attributed as `extension`.
Stock Pi lacks that attribution, matching the screenshot and the documented host limitation.
This is not evidence of a missing Lens installation. No runtime or configuration changes were made.
Deferred at the user's request. Existing folding requires the local Pi patch or equivalent upstream host support.
A producer integration may avoid custom Pi; feasibility is unverified. No runner replacement is required by current evidence.
Next gate, only when reopened: choose an approach and exercise the real wake in ordinary Pi.

## Latest-tag deployment

Both tracked sources now select `latest`; GitHub tags still resolve to the release commits listed above.
Pi's targeted install completed. Claude's copied settings and marketplace now select `latest`.
Claude marketplace refresh and plugin update completed; plugin version remains `0.1.2`.
No GitHub tags were moved, no custom host was installed, and no runner was replaced.
The harness suite passed: 11 tests, one compiled-host check skipped without `PI_PACKAGE_DIR`.
Fresh interactive loading remains unverified. Restart sessions to load refreshed packages.
This configuration change was self-reviewed, not independently reviewed.

## Verification and recovery

Run from the repository root:

```sh
PI_PACKAGE_DIR="$HOME/projects/personal/pi/packages/coding-agent" \
  python3 scripts/tests/test-agent-harness.py
just --dry-run pi-lens-dev 2>&1 | shellcheck --shell=sh -
just lint
```

The package root must already contain its compiled SDK. The tests do not install or rebuild it.
Without `PI_PACKAGE_DIR`, basic harness tests run and the compiled-host persistence check explicitly skips.
Read [verification commands](/.agents/plans/pi-lens-verification.md#repeat-the-verified-checks)
before repeating installed-product or archive checks.

For development, use `just pi-lens-dev --continue` from the same working directory.
Native session storage is shared with ordinary Pi; continue selects that directory's latest saved session.
Use `--session` for a particular saved session. Earlier `--no-session` conversations remain ephemeral.
Use `/lens raw` for rendering recovery; select an earlier immutable version for rollback without moving release tags.

## Pi 1.2.0 installation delivery

This compatibility anchor preserves existing links.
Read [installation history](/.agents/plans/history/pi-lens-delivery-2026-10-13.md#pi-120-installation-delivery)
for the earlier 0.1.1 delivery; the table above owns current installed state.
