<!-- markdownlint-disable MD013 -->
# Lens and personal harness delivery

This cross-repository plan belongs to dotfiles. Do not copy or link it from public product repositories.
The retained record keeps its original formatting; historical statuses are superseded by the current checkpoint.

## Pi 1.2.0 installation delivery

The user authorized removing the version guard safely, testing normal installation, and publishing the verified fix.
The target is `dots` followed by opening Pi on the other laptop, without a development checkout.

| ID | Decision | Reason |
| --- | --- | --- |
| D100 | Replace the exact-version rejection with verified structural fallback | User requests Pi 1.2.0 support without retaining the hard guard |
| D101 | Publish Pi Lens `v0.1.1` after compatibility acceptance | User approved the immutable follow-up release and shared pin update |
| D102 | Test isolated installation before targeted normal-profile installation | Preserve unrelated packages, credentials, and a reversible release pin |
| D103 | Push shared dotfiles delivery after verification | User requires the other laptop to receive the configuration through `dots` |
| D104 | Superseded: automatically follow latest published Lens versions | User subsequently preferred explicit pin bumps when updating the Lens repositories |
| D105 | Keep Pi binary on `latest`, but both Lens deployments on version tags | User distinguished host updates from accepted Lens release upgrades |
| D106 | Maintain `latest` only as a movable published-release alias | User requested its release process be documented; no release branch is needed |
| D107 | Release Claude Lens `v0.1.1` with renamed marketplace metadata | An immutable pin must include the approved marketplace rename |
| D108 | Apply three targeted shared-rule refinements | User explicitly requested harness improvements from observed session friction |

Observed starting state:

- Installed `pi --version` returns `1.2.0`.
- Normal-profile Lens is already installed at `v0.1.0`, commit `9528bc9`; only generated package-lock data is untracked.
- A real Pi 1.2.0 terminal fixture reproduces the guard rejection and fails Lens presentation assertions.
- This intentional baseline failure is TDD evidence, not a failed acceptance pass.
- Existing patched Pi 1.1.0 host and isolated send-now worktree remain untouched.

Implemented and independently audited. Pi release `v0.1.1` is commit `fbb2f72`; Claude release is `35ecd19`.
Both releases and their `latest` aliases are published; aliases point exactly to the corresponding versioned release commits.
No release branch was created. Versioned tags remain immutable.

Lead verification passed:

- Pi: 180 tests, full type/lint checks, and direct terminal fixtures on both Pi 1.1.0 and 1.2.0.
- Pi 1.2.0: batch fixtures in both modes; fullscreen image fixture; model-visible baseline equivalence.
- Installed discovery: both terminal modes using a local candidate, a released Git package, and the normal profile.
- Fresh Git reconciliation: native `pi update --extensions --no-approve` installed the missing published package.
- Claude: 29 tests, full checks, isolated native marketplace/plugin install with `source.ref: v0.1.1`.
- Dotfiles: eight provisioning tests and full lint. Shared instructions also passed direct Markdown lint.
- Tagged-commit CI passed for both repositories, including the Pi 1.2.0 runtime job.

Normal Pi Lens is installed at `fbb2f72` and auto-loads on Pi 1.2.0; view changes and reload passed without model requests.
Only Lens was updated in the normal profile; voice and subagents package declarations remain unchanged.
The native smoke updated tracked `lastChangelogVersion` to `1.2.0`; formatting was normalized afterward.
Claude's normal profile was not migrated; shared settings disable its old plugin identity when copied by `dots`.

The shared deployment uses Pi Lens `@v0.1.1` and Claude marketplace `source.ref: v0.1.1`.
The Pi binary remains on Mise `latest`; future host compatibility is not guaranteed by these results.
Release procedures live in each product's contributor/development guide; dotfiles owns pin-update and sync instructions.
Rollback restores the previous version pins; Pi Lens `v0.1.0` intentionally uses native rendering on Pi 1.2.0.
No clipboard-origin host support, completed send-now parity, or user visual acceptance is claimed.

The deployment payload is ready to push. After it reaches `origin/main`, the other laptop can run `dots` and open Pi.
This push includes previously committed EditorConfig, global-ignore, and start-project-skill changes, inspected read-only.
Shared-rule refinements and their evidence are recorded in the harness roadmap; no fresh model-behavior probes were run.

## Rename and provisioning checkpoint

The user approved the `claude-lens` rename, Lens provisioning through `dots`, and documentation updates.
Product rename commits are pushed: Claude `9aea61d`, Pi sibling references `a3a10de`.
Dotfiles provisioning is committed locally only; its branch also contains unrelated unpushed user commits.
Push authorization must account for that complete branch before laptop `dots` can fetch these changes.

| ID | Decision | Reason |
| --- | --- | --- |
| D95 | Rename Claude repository, local directory, and marketplace to `claude-lens` | User confirms sole ownership and accepts the rename |
| D96 | Keep plugin identity `lens` and command `/lens` | Repository/marketplace naming does not require state-namespace migration |
| D97 | Keep Mise's Pi selector at `latest` | User explicitly rejected pinning the binary |
| D98 | Declare released Pi Lens Git package through existing updater | Native Git-package reconciliation already handles missing installations |
| D99 | Request approval before expanding Lens compatibility to Pi 1.2.0 | Registry contradicts the user's 1.1.0 assumption; current guard rejects other versions |

Completed source changes:

- GitHub repository renamed to `waldoibarra/claude-lens`; local checkout is `~/projects/personal/claude-lens`.
- Marketplace/package metadata and Git remote use the new name; published `v0.1.0` tags are unchanged.
- Dotfiles selects `lens@claude-lens` without retaining a second enabled marketplace identity.
- Pi settings declare `git:github.com/waldoibarra/pi-lens@v0.1.0` with empty skill/prompt filters.
- Existing `install_pi_packages` implementation is unchanged; no additional installer loop was needed.
- Docs describe native old-marketplace migration and distinguish provisioning from compatibility and active installation.

Verification: independent combined audit passed; lead confirms seven isolated provisioning tests, Pi 179 tests, and Claude 29 tests.
Full dotfiles lint passed after correcting two line-length errors introduced during lead documentation cleanup.
The provisioning fixture verifies settings and native command invocation, not real package installation.
Current normal-profile installation, fresh published-package install, and physical terminal acceptance remain unverified.
No `dots` or package installation ran. Editing linked Pi settings changes the declaration, not installed package state.
Unrelated `docs/agent-skills.md` and `home/.agents/skills/start-project/` changes remain outside this work.

**Compatibility blocker:** `npm view @earendil-works/pi-coding-agent version` returned `1.2.0`.
Lens `v0.1.0` accepts `1.1.0` only and retains native rendering elsewhere.
The user has been asked to approve adding and verifying `1.2.0` support while retaining `latest`.
Do not claim the laptop gets active Lens rendering after sync until that blocker is resolved.

## Published-release planning

The user explicitly authorized replacing Claude's `v1.0.0` tag and publishing `v0.1.0` in both Lens repositories.
Both tags and GitHub Releases are now published. Shared-dotfiles provisioning and normal-profile changes remain separate.

| ID | Decision | Reason |
| --- | --- | --- |
| D90 | Target Pi Lens `0.1.0` as a published Pi package | User wants versioned distribution rather than a local checkout |
| D91 | Recommend native Git-tag distribution for Pi Lens | Existing Pi manifest supports it; no new registry ownership or npm authentication required |
| D92 | Superseded by D93: resolve Claude numbering before editing manifests | Existing `v1.0.0` required an explicit downgrade decision |
| D93 | Delete Claude `v1.0.0` tag and publish `v0.1.0` in both repositories | User explicitly reaffirmed the requested version and tag reset |
| D94 | Preserve the old GitHub release record pending deletion approval | User authorized tag deletion; separate record deletion was asked explicitly |

Verified release facts:

- Pi Lens already declares `pi.extensions: ["./src/index.ts"]`; no compilation is required.
- Its package version is already `0.1.0`; `private: true` prevents accidental npm publication, not Git distribution.
- The npm name `pi-lens` belongs to `apmantza/pi-lens`, currently `4.4.3`.
- The scoped name `@waldoibarra/pi-lens` returned registry 404; publish permissions remain unverified.
- Claude Lens's manifest is now `0.1.0`; `v1.0.0` tags were deleted locally and remotely.
- GitHub automatically changed the old `v1.0.0` release record to draft after tag deletion.
- Both new `v0.1.0` releases are published and marked Latest; their tagged commits passed CI.
- Claude Lens distributes through its native plugin marketplace, not Pi's package manager.

Release sequence (steps 1–5 complete; provisioning remains pending):

1. Apply the user-approved version reset to `0.1.0` in Claude; retain Pi's existing `0.1.0`.
2. Freeze verified presentation commits; exclude blocked runner and send-now checkpoints.
3. Update generic manifests, changelogs/release notes, compatibility, installation docs, and sibling links.
4. Run Pi full checks and terminal fixtures, Claude `just check`, and inspect distribution payloads.
5. Publish immutable Git tags and GitHub Releases after explicit execution approval; never move published tags.
6. With provisioning approval, declare `git:github.com/waldoibarra/pi-lens@v0.1.0` in dotfiles and pin compatible Pi `1.1.0`.
7. Verify Git-package reconciliation and Claude marketplace installation in disposable profiles without provider calls.
8. Push verified dotfiles delivery changes; laptop runs `dots`, then starts fresh Pi and Claude processes.

Published tags: Pi Lens `9528bc9`; Claude Lens `874be93`. Both package/plugin versions are `0.1.0`.
Lead checks passed: Pi 179 tests, direct terminal modes, package payload; Claude 29 tests and all checks.
Git-tag publication is the selected first release route. npm remains optional and would require a scoped package name.
No release package was installed in either normal profile. Git-package clean-profile installation remains unexercised for these tags.
Existing Claude `1.0.0` installations need version verification; automatic downgrade to `0.1.0` is unverified.
Publishing Lens alone does not deliver host-backed clipboard previews or composer attribution.
Those features require a separately verified patched-host distribution; the blocked send-now branch must not be used.
Manual acceptance remains user-owned; a published artifact or passing fixture does not check those boxes.
Recovery uses `/lens raw` or disabling the package; revert dotfiles pins rather than moving published tags.

## Laptop delivery handoff

The user requested committing all remaining work, then continuing improvements in another session.
All product source changes are now committed locally; incomplete work remains separate from deployment.

| ID | Decision | Reason |
| --- | --- | --- |
| D87 | Commit unfinished work as explicit checkpoints, without activation | User explicitly requested every remaining change be committed |
| D88 | Keep send-now on its own named branch | Preserve incomplete work without merging unsafe behavior into the verified host |
| D89 | Explain laptop provisioning before changing its delivery configuration | User asked what `dots` needs; publication and normal-profile changes were previously excluded |

| Repository | Latest local commit | Delivery state |
| --- | --- | --- |
| Pi Lens | `86b0858` | Clean; verified metadata-only Details; remote still `262add2` |
| Claude Lens | `6e8b6ca` | Clean; question disclosure changes remain local |
| pi-subagents | `a366357` | Clean checkpoint; workflow fixture cleanup remains blocked |
| Pi primary checkout | `97400e2` | Clean; verified origin, clipboard, and diagnostic source patches |
| Pi isolated send-now worktree | `dfdd6ad`, branch `wip/send-now-checkpoint` | Committed but unaccepted; not merged; dependency symlinks excluded |

The send-now worktree remains `/tmp/pi-send-now-worktree.zHjd4W`; its named branch preserves commits if that directory expires.
Untracked `node_modules` and `packages/ai/node_modules` are machine-local symlinks, not missing source commits.
Neither blocked checkpoint is approved for installation. Manual acceptance boxes remain unchecked.

### What laptop `dots` currently lacks

- `home/.pi/agent/settings.json` declares voice and subagents, but no Pi Lens package.
- Mise selects latest Pi; Lens currently guards exactly version `1.1.0`.
- Pi Lens remote `main` remains `262add2`; the three newer local commits are not reachable there yet.
- The updater already reconciles configured Git packages through `pi update --extensions`.
- Clipboard previews and composer attribution require the verified patched host, not stock Pi alone.

Recommended first delivery: verified Lens presentation with stock Pi `1.1.0`; omit unfinished send-now and workflow checkpoints.
This requires approval to push verified Lens source, declare its immutable Git revision, pin the host, and push dotfiles.
Stock-host delivery lacks host-backed clipboard tokens/previews and proven composer attribution; inputs remain neutral.
Matching this trial's clipboard behavior instead needs a separately distributed verified patched-host artifact.
No such portable host artifact or installer is claimed ready. Never distribute the send-now checkpoint as that host.
Run isolated provisioning checks before publishing delivery changes; do not run `dots` locally for this handoff.
After approved sources are reachable, the laptop runs `dots`, authenticates separately, and opens a fresh Pi process.

Read the feedback queue and verification record before resuming repairs. Remaining approvals are not implied by checkpoint commits.

## Current feedback implementation

This checkpoint supersedes the paused handoff below. The user authorized implementation and local commits, not installation or publication.

| ID | Decision | Reason |
| --- | --- | --- |
| D78 | Resume bounded workers and commit inspected existing changes | User requested continued implementation and preservation of uncommitted work |
| D79 | Keep image Details metadata-only | User rejects repeated message content before path, MIME, and size |
| D80 | Clarify which image presentations should merge before changing them | Screenshot contains inline token, attachment preview, and legitimate read disclosure |
| D81 | Track subsequent harness feedback in this existing plan | User requested coordinated implementation across Lens and dotfiles |
| D82 | User confirmation alone completes manual acceptance | Automated tests cannot establish the user's visual acceptance |
| D83 | Announce test readiness, exact steps, and reload or restart requirements | User requests actionable testing notices throughout delivery |
| D84 | Continue Ctrl+Enter send-now and add Ctrl+S draft stash/pop parity | User explicitly requests both Claude-style Pi controls |
| D85 | Implement send-now first for idle and safely interruptible assistant streaming | Isolate ordering and recovery before adding tool background ownership |
| D86 | Refuse unsupported send-now states without consuming queue or draft | Partial delivery must not masquerade as completed Claude parity |

Current feedback queue:

| Feedback | Owner | State / acceptance |
| --- | --- | --- |
| Pasted image appears folded twice | Pi Lens | Awaiting clarification: inline token versus preview, or preview versus tool read |
| Image Details repeats the message before metadata | Pi Lens | Committed `86b0858`; independent audit and automated checks pass; user acceptance pending |
| Live subagent purpose/current-step summaries | pi-subagents | Checkpoint `a366357`; failure-path cleanup blocks acceptance; bounded repair approval requested |
| Ctrl+Enter sends queued messages and draft now | Pi host | Checkpoint `dfdd6ad`; clipboard retention and private-queue fallback block acceptance; repair approval required |
| Ctrl+S stashes/pops the message draft | Pi host | Plan reviewed; awaiting replace-versus-swap choice for an occupied stash |
| Actionable testing and reload notices | Delivery | Announce readiness only after verification; distinguish extension reload from host restart |
| Preserve existing uncommitted changes | All checkouts | All source committed; machine-local dependency symlinks intentionally excluded |

### Send-now repair checkpoint

The first implementation failed independent acceptance despite its passing focused tests and full host check.
Confirmed blockers: delayed editor clearing loses new drafts; asynchronous auth permits tool-start races.
Queue reservations also lack rollback after removal, and an empty composer prevents queued-only delivery.
The bounded GPT-5.5 high repair fixed queued-only delivery, safe-state rechecks, rollback, and duplicate in-flight submissions.
Its second independent acceptance pass failed two remaining gates:

- Accepted-prefix clearing drops newer retained clipboard images without spans.
- Send-now retains private-queue mutation despite the native typed reservation API.

Lead verified both findings in source. Stop further repair dispatch until the user approves another bounded pass.
The isolated draft is committed as `dfdd6ad` but remains unmerged; no activation or complete Claude parity is claimed.

### Workflow-summary repair checkpoint

Two independent audits reported no blockers, but lead inspection found unresolved fixture cleanup.
The first implementation omitted rootless task summaries and removed artifacts immediately after launch.
The repair adds rootless task snippets and waits on the successful path.
Its `finally` still removes artifacts when an earlier assertion fails or terminal-state waiting times out.
`installSingleExecutionHooks` also removes temporary directories without stopping those workflows.
No provider failure or quota failure occurred; this is the second failed acceptance pass for this target.
Asked permission for one bounded cleanup repair. No further worker dispatch for this target until approval.
The code is not installed; manual acceptance remains unchecked.

### Test readiness

**Image Details:** source-ready at `pi-lens@86b0858`; the active extension checkout remains unconfirmed.
After the parent turn finishes, run `/reload` if the session loads `~/projects/personal/pi-lens/src/index.ts`.
Open a pasted image, then `Details`; expect path, MIME type, and captured size without repeated message text.
Report the result before checking its acceptance box. `/lens raw` remains recovery.

All previously launched workers have finished. Image Details can be tested after the parent turn ends.

**Ctrl+Enter and Ctrl+S:** not ready for manual testing. Host source changes need compilation and a new isolated process.
Neither key can be activated by extension `/reload` alone. No normal-profile changes are authorized.

Read [Claude's interactive controls](https://code.claude.com/docs/en/interactive-mode) before changing queue or stash semantics.
Verified reference: stash restores cursor, pasted content, and shell mode; send-now uses queued order, then draft.
An occupied stash with another nonempty draft needs verified semantics, not an invented overwrite policy.
Asked user to choose replace or swap; recommended swap to preserve both drafts. No default was applied.
Stash implementation must reuse native snapshots, remain composer-scoped, preserve selector shortcuts, and refuse lossy custom editors.
Clear stash on session replacement; retain the same session's native snapshot through extension reload.
Send-now's first bounded slice must refuse unsupported states intact; this does not complete Claude parity.
The earlier reviewer suggestion to deliver steering before follow-ups is rejected; global submission order remains required.

### User acceptance checklist

Automated results belong in the verification record. Only explicit user confirmation checks these boxes.

- [ ] Duplicate pasted-image presentation behaves as requested; exact target awaits clarification.
- [ ] Image Details shows attachment metadata without repeating the message.
- [ ] Thinking history has the requested inset and preserves viewport anchoring.
- [ ] Claude question disclosures preserve native answer controls and details.
- [ ] Subagent warnings stay outside the composer and preserve the draft.
- [ ] Composer messages show `You`; verified automated inputs fold correctly.
- [ ] Clipboard previews, metadata, reload, and resumed history render correctly.
- [ ] Live subagent purpose and observed current action are useful and accurate.
- [ ] Ctrl+Enter send-now matches accepted Claude behavior, including draft and queue handling.
- [ ] Ctrl+S draft stash/pop matches verified Claude behavior without losing text or attachments.

Testing notices must identify the changed checkout, active-runtime requirements, steps, and expected result.
Use `/reload` for changed extension source only when this session actually loads that source.
Host keyboard/queue changes require a rebuilt host and a separate process; `/reload` cannot activate them.
Do not install or replace the normal profile to make a test ready.

Routing: GPT-5.5 medium for clipboard, workflow summaries, and stash review.
GPT-5.5 high handles send-now review/implementation because queue ordering and recovery cross host lifecycle boundaries.
No Astra/Fable workers. Provider/model changes, quota recovery, and extra repair rounds remain approval-gated.
Existing Pi thinking/provenance and Claude question changes passed fresh checks and were committed locally.
Runner diagnostics and warning fixtures also passed fresh checks and were committed locally.
No installs, publication, normal-profile replacement, or credential copying are authorized.

## Current parity delivery

This checkpoint supersedes older stop instructions and completion tables below.
The user authorized plan audit and implementation across both Lens repositories.

| ID | Decision | Reason |
| --- | --- | --- |
| D65 | Do not rewrite published history | User declined history cleanup; historical exposure remains |
| D66 | Record Pi Lens as active, separately from host patches | User confirmed this session loads Lens; patched-host activation is unverified |
| D67 | Resume bounded eligible-worker dispatch | User authorized implementation in this fresh session |
| D68 | Target closest supported behavior in both harnesses | Preserve native capabilities without inventing unsupported parity |
| D69 | Deliver reviewed presentation slices before host activation | Existing Lens activation permits isolated UI improvements without replacing Pi |
| D70 | Give every Claude question transcript row a disclosure; leave its dialog native | Generated API separates question controls from transcript rows |
| D71 | Build patched Pi offline and verify in disposable profiles | User approved isolated activation to accelerate manual visual review |
| D72 | Show subagent task summaries and observed current steps | User screenshot shows generic delegation labels and opaque active rows |
| D73 | Reproduce warning placement against the actual loaded runner | User still sees extension-policy warnings inside the composer |
| D74 | Prioritize proven composer labels and collapsed automated inputs | User still sees neutral Input labels; source success is not activation |
| D75 | Stop worker dispatch after the second failed warning acceptance pass | Repaired fixture still asserts prompt submission as completion and checks a different warning |
| D76 | Allow one bounded GPT-5.5 high warning repair | User explicitly approved the checkpoint request; no Astra/Fable workers |
| D77 | Pause implementation and preserve the fresh-session handoff | User requested docs for continuing testing and implementation later |

### Audited state

- Pi Lens `262add2` and Claude Lens `a3e074f` have clean starting worktrees.
- Pi host source includes origin, clipboard, and native diagnostic patches; source worktree is clean.
- Input attribution and clipboard previews are implemented and source-verified, not pending implementation.
- Installed host activation and physical clipboard acceptance remain unverified in this session.
- Claude native detail delegation is implemented; physical rendering remains unaccepted.
- Send-now retains an isolated, unmerged draft; no completed behavior is claimed.
- History rewriting is excluded. Package releases, pushes, and managed-profile replacement remain separate approvals.

### Execution and acceptance

| Order | Acceptance target | Files / verification | State |
| --- | --- | --- | --- |
| 1 | Expanded Pi thinking has a two-column inset without breaking wrapping or peek | `pi-lens/src/progress.ts`, progress and expansion-scroll tests, behavior docs | Implemented; independent audit's mouse-test gap resolved; 177 tests pass; direct/batch terminal modes pass |
| 2 | Claude question disclosures preserve native details and match supported Pi controls | `claude-code-lens/hooks/register.tsx`, render tests, views and README; `just check` | Implemented; independent audit passes; lead confirms 29 tests and all checks pass |
| 3 | Both repositories pass their full checks; native fallback and model-facing content remain intact | Pi `bun run check` with source normalizer and voice; direct/batch terminal smoke; Claude `just check` | Passed; physical terminal acceptance remains separate |
| 4 | Verify host-dependent features through the compiled default loader | Offline build and isolated activation first; no normal-profile replacement | Compiled diagnostics, input attribution, and async TASKS warning fixtures pass; user trial remains pending |
| 5 | Finish host queue/send-now separately, then distribution | Retain draft without merging; re-audit before implementation | Pending host work |

Pi inset acceptance includes ordinary bullets, whole-document native fallback, narrow widths, mouse offsets, and raw bypass.
Claude waiting, answered, skipped, and failed transcript rows use chevrons and expose original native rows when opened.
The separate `AskUserQuestion` dialog receives no Lens hook; question controls remain native and available.
Do not force Claude thinking or viewport behavior through APIs that do not expose those controls.
Read each repository's behavior docs before editing. Update public docs only for its generic behavior.
Use explicit eligible non-lead workers under the fresh-session routing and approval boundaries below.
Stop on quota or timeout failure; after two failed acceptance passes, checkpoint and ask before further model work.
No physical terminal, microphone, or user visual acceptance is implied by automated fixtures.
Recovery remains `/lens raw` or unloading Lens; revert only owned changes.

### Fresh-session handoff

The user requested documentation for continuing in a fresh session. No additional implementation was authorized by that request.
Read [verification results and commands](/.agents/plans/pi-lens-verification.md#repeat-the-verified-checks) before retesting.

#### Checkouts and uncommitted work

Repositories are under `$HOME/projects/personal/`; coordination records remain in `$HOME/.dotfiles/.agents/`.

| Repository | HEAD | Current worktree |
| --- | --- | --- |
| `pi` | `97400e2` | Clean source; offline build completed; compiled CLI is `packages/coding-agent/dist/bundle/cli.js` |
| `pi-lens` | `262add2` | Thinking inset, mouse regression, compiled provenance fixture, and behavior/testing docs |
| `claude-code-lens` | `a3e074f` | Question chevrons and native details, render tests, README and views |
| `pi-subagents` | `b67d202` | Async launch-warning emission, compiled diagnostics, TASKS terminal/integration tests, testing docs |
| Dotfiles | `056e8ae` | Delivery plan, verification record, and workspace index |

Inspect each diff before editing. Preserve these uncommitted changes; no commits or pushes were made this session.
The isolated send-now draft remains at `/tmp/pi-send-now-worktree.zHjd4W`; it is unmerged and unaccepted.
Do not stage its `node_modules` symlinks. Temporary worktrees and evidence may disappear across sessions.

#### Verified versus active

- Pi inset and Claude question disclosures passed their recorded checks; both bounded presentation scopes are ready for a fix freeze.
- Patched Pi built offline successfully: 77 bundle files, 8.7 MiB; source remains clean.
- Compiled-host provenance proves composer `You`, extension folds, raw/global recovery, and cold resume in both terminal modes.
- Compiled default-loader diagnostics and repaired async TASKS warning tests pass; exact test results live in the verification record.
- The final warning repair received lead review against earlier independent findings, not another independent final audit.
- Installed runner JavaScript still has the older direct-console warning path; earlier installation claims are superseded.
- User confirmed Lens active, but the loaded extension path was not conclusively established.
- User ran `/reload`; recent persisted input still lacked origin bindings. Reload cannot replace the Pi host binary.
- A patched-host process and updated runner source are required for the verified host-dependent behavior.
- No normal-profile replacement, authenticated manual trial, physical clipboard acceptance, release, or `dots` occurred.

#### Next work, in order

1. Obtain authorization for the next bounded worker lane; the approved warning repair is complete.
2. Implement live subagent purpose/current-step summaries from existing task and progress metadata.
3. Prepare a disposable visual-review launch using the compiled host, local Lens, and updated runner source.
4. Confirm physical rendering, composer protection, new composer labels, automated-input folds, and native dialog behavior.
5. Re-audit the isolated send-now draft before continuing host queue work; then address distribution separately.

For status work, inspect `pi-subagents/src/runs/foreground/subagent-executor.ts` and `src/tui/render.ts`.
The compact workflow renderer uses `job.description`, but its root producer does not populate it.
Do not blindly use `derivedObjective`: it can contain generated workflow code rather than a useful task summary.
Async chain descriptions already exist; TASKS uses a different generated-workflow path.
Reuse normalized child task snippets and observed tool/path metadata; never invent progress or add summarization calls.
Live summaries and the manual-review launcher are not implemented.

Choose trial authentication deliberately: credential-free demonstration or explicit reuse of existing authentication.
Do not copy credentials, replace the normal profile, or switch the user's main model without authorization.
Older unbound messages must remain neutral; do not infer origin from their wording.

#### Routing and recovery

All session workers used explicit `openai-codex/gpt-5.5`, medium except the approved high-effort warning repair.
Astra/Fable remain main-chat-only. Renew authorization after quota/timeouts or two failed acceptance passes.
The warning repair needed two rejected attempts before explicit approval; do not repeat unlimited review loops.
Use installed local test executables, not `npx` auto-installation. One earlier worker attempted that prohibited path.
Keep one writer per checkout; the main session owns builds, installation, Git operations, and communication.
Normal-profile changes and publishing remain separate approvals. History cleanup was declined.
Recovery is `/lens raw` or leaving the disposable trial; the installed host has not been replaced.

Pending routing proposal: use GPT-5.5 high for native TUI fixture repairs after one medium-effort acceptance failure.
Evidence: two medium-effort warning attempts failed acceptance; the approved high-effort repair passed lead checks.
Scope: personal native-TUI fixture repairs only. Benefit: fewer rejected implementation rounds.
Verify against the next approved repair's acceptance count; rollback to task-specific medium routing if ineffective.
This proposal needs approval; no global instructions or routing defaults were changed.

## Ownership correction and implementation plan

| Work | Code/configuration owner | Coordination owner |
| --- | --- | --- |
| Thinking indentation, folds, activity ordering, spacing, and peek behavior | `pi-lens` | This plan |
| Equivalent Claude presentation and public sibling links | `claude-code-lens` | This plan |
| Input-origin bindings and clipboard capture/persistence | Pi core | This plan |
| Native queue timing and immediate send-now execution | Pi core | This plan |
| Native loader/event diagnostic callbacks | Pi core | This plan |
| Subagent warnings, child diagnostic adapters, and runner compatibility | `pi-subagents` | This plan |
| Main/worker routing, quota controls, terminal preferences, and shortcuts | Dotfiles | This plan and the AI harness roadmap |
| Local builds, activation, accepted package pins, and `dots` delivery | Dotfiles | This plan |
| Personal usage evidence, cross-repository backlog, and package comparisons | Dotfiles `.agents/` | This plan |
| Generic public behavior and supported host contracts | Each product's `docs/` | Product repository |

| ID | Decision | Reason |
| --- | --- | --- |
| D63 | Keep personal harness records in dotfiles, not Pi Lens | User corrected an unintended public disclosure |
| D64 | Public product repositories contain no operator-specific plans or backlinks | Prevent recurrence without duplicating the backlog |

Implementation order:

1. Preserve this plan and verification evidence in dotfiles; update their index and local references.
2. Remove the misplaced public records and personal installation details from Pi Lens.
3. Retain generic host compatibility requirements; remove operator-specific checkout and patch references.
4. Check documentation links, formatting, and publication boundaries; commit and push the scoped Pi Lens cleanup.
5. Leave published history and repository visibility unchanged; history cleanup was declined.
6. Resume UX work through its owning repository and an eligible worker after the quota/activation gates are resolved.

Ownership migration checks passed: preserved records, updated local index/references, product-only public docs, and ignored agent records.
The focused Pi Lens documentation test and both repositories' documentation checks passed.
This cleanup was self-reviewed without additional model dispatch.
The current source cleanup does not remove old commits, caches, or existing clones.
No dotfiles push, history rewrite, package release, or billing change is authorized by this migration.

## Historical ownership handoff (superseded)

This earlier handoff is historical; the current fresh-session handoff above supersedes its statuses and stop instructions.
The user then requested task-list ownership changes only, followed by an implementation stop.

- Dotfiles owns this plan and `pi-lens-verification.md`; both are indexed in `.agents/README.md`.
- Ownership migration is committed locally as `1ac7057`; dotfiles was not pushed.
- Public Pi Lens cleanup is committed and pushed as `262add2`; application behavior was unchanged.
- Old published commits still contain the misplaced records. The user subsequently declined history cleanup.
- Thinking indentation is not implemented. The attempted Luna dispatch failed schema validation before any worker launched.
- No further worker launch or application implementation may occur in this session.

Before resuming, check the owning repositories and use the current pending-work table below.
The isolated send-now draft remains at `/tmp/pi-send-now-worktree.zHjd4W`; it is unmerged and unaccepted.
Do not stage its dependency symlinks or treat characterization tests as a completed send-now feature.
Host offline-build approval, default-loader validation, quota recovery, and local UX acceptance remain separate gates.
Astra/Fable remain main-chat-only; the user may choose a weaker main model for the new session.

## Outcome

Ship a standalone Pi package matching Claude Code Lens's normal, clean, and raw views.
Waldo's Pi 1.1.0 workstation is the first supported environment.

This file is authoritative. Read it before continuing implementation.
Read [verification results](/.agents/plans/pi-lens-verification.md) before claiming acceptance.
The checkpoint below supersedes historical routing and status statements elsewhere in this plan.
Earlier Astra child assignments are historical, not permission to repeat them.

## Current pending work and activation checkpoint

| Priority | Work                         | Verified state / remaining gate                                                                                                       |
| -------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1        | Usage discipline             | Shared policy reserves Astra/Fable for main chat; Pi strict worker allowlist rejects Astra before inference.                          |
| 1        | Main model choice            | User-owned per session; weaker main models are allowed. No automatic parent-model change.                                             |
| 1        | Activate host fixes          | Installed Pi remains stock 1.1.0. Offline-build approval and default-loader validation remain outstanding.                            |
| 2        | Indent expanded thinking     | Newly requested two-column left inset under the heading; preserve bullets, wrapping, raw output, and peek anchoring. Not implemented. |
| 2        | Human versus automated input | Source is implemented and audited. New composer input becomes You; extension input folds. Host activation is missing.                 |
| 2        | Pasted-image tokens          | Host and Lens source are implemented and audited. Built-host activation and physical clipboard acceptance remain missing.             |
| 2        | Queued notes after tools     | Native steeringMode is now all. Fresh offline SDK confirms it; reload applies it to the running host.                                 |
| 3        | Queue clarity                | Draft work exists in the isolated send-now worktree; not independently accepted or merged.                                            |
| 3        | Immediate send-now           | Not implemented. Native bash handoff, recovery, shortcuts, command/chord/subagent parity remain unfinished.                           |
| 3        | Native diagnostics           | Source and real source-SDK/TUI checks passed. Compiled default-loader activation is still unverified.                                 |
| 4        | Claude parity                | Local commit a3e074f passed audit and 26 tests. Physical rendering remains a manual gate; no release.                                 |
| 4        | Portable dots provisioning   | Await locally accepted immutable sources and explicit deployment; no fabricated package version or local-only path pin.               |
| 4        | Package release              | Blocked until user validation. Only Pi Lens GitHub source push is authorized.                                                         |

No model workers may resume after the quota failure without operator approval.
The padding change belongs to one small non-lead worker; no Astra/Fable implementation or review child.
Configuration edits were checked without inference; self-review is not independent review.

### Accepted corrections

| ID  | Decision                                                               | Reason                                                                        |
| --- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| D56 | Astra/Fable are main-chat-only, never workers or auxiliary probes      | User correction after quota exhaustion; supersedes earlier worker assignments |
| D57 | The user chooses the main model, including weaker research models      | Session needs determine the main model                                        |
| D58 | Use explicit, least-expensive capable worker selection by role         | Prevent lead inheritance and unnecessary premium-model work                   |
| D59 | Bound repair rounds; stop dispatch after quota or timeout failures     | Avoid unattended retry and review loops                                       |
| D60 | Use native all-message steering before considering another package     | Pi already accepts steering after the current tool batch                      |
| D61 | Add a two-column inset to expanded thinking history                    | User screenshot shows bullets aligned with the disclosure header              |
| D62 | Keep You for proven composer input and fold identified extension input | No fabricated human attribution or text-based classification                  |

### Queue behavior and package decision

Claude sends queued messages when the running tool calls finish, within the same turn.
Slash and shell commands generally wait until that turn ends; immediate commands are exceptions.
Pi Enter already uses steering; Alt+Enter uses follow-up delivery after current work.
Its previous one-at-a-time default could delay later notes behind other queued entries.
The tracked native steeringMode is now all; no package is needed for that change.

The boundary is an outer tool batch, not an arbitrary operation inside a running Codemode script.
Neither native steering nor this setting injects a message into an already-streaming model response.
Immediate send-now is a separate feature; do not advertise an abort/dequeue shortcut as equivalent.
Read [Claude's queue reference](https://code.claude.com/docs/en/interactive-mode#when-claude-code-sends-what-you-queued)
before changing those semantics.

A bounded package recheck rejected four candidates against mandatory requirements:
pi-compact-tools 0.15.0, pi-clipboard 0.1.10, Archimedes image-paste 2.10.4, and pi-wait 0.1.5.
The dotfiles Lens display spike owns the detailed source comparison. Nothing was installed.

### Usage audit snapshot

Canonical assistant usage entries were deduplicated by session file and entry ID.
Artifact transcript copies and cumulative resume metadata were not summed.
Previous no-session CLI children are absent, so this is not a complete account-wide total.

| Scope                      | Model   | Responses | Uncached input |  Output | Reasoning subset | Cache reads |
| -------------------------- | ------- | --------: | -------------: | ------: | ---------------: | ----------: |
| Current child sessions     | GPT-5.5 |       702 |      2,099,268 | 217,848 |           78,816 |  64,320,256 |
| Current child sessions     | Astra   |       839 |      3,865,375 | 334,580 |          105,939 |  88,578,304 |
| Current main session       | Astra   |       243 |      1,532,188 | 264,360 |          204,334 |  70,845,056 |
| Previous Lens main session | Astra   |       521 |      3,910,527 | 447,715 |          303,039 | 124,512,640 |

Reasoning is included in output, not additional to it. These are token records, not provider quota charges.
Recorded dispatch metadata contains 44 runs, including resumes: 33 Astra and 11 GPT-5.5.
Astra handled 13 implementation, 17 audit, and 3 planning dispatches.
The main sessions also consumed substantial reasoning and repeatedly processed large contexts.
The orchestration mistake was premium worker use plus oversized scopes and repeated review/rework—not just tool output.
No exact subscription quota conversion, reset time, or actual monetary charge is established.

## Behavior contract

Use `claude-code-lens` commit `ca16172` as the reference, especially `docs/views.md` and `hooks/register.tsx`.

- Normal groups consecutive mixed-tool steps, shows counts, five steps, and an expandable remainder.
- Clean shows each run's count and latest failure; clicking reveals step names.
- Raw delegates to native Pi rendering without decorations.
- Assistant prose and user messages separate runs; questions render independently.
- Steps expose commands, output, errors, and diffs on click; native expansion remains available.
- User, assistant, and run footers show timestamps and the actual model when known.
- A Lens-owned status describes current activity; questions and subagents use their available metadata.
- The native spinner remains untouched because its shared setter cannot safely restore another extension's message.
- Tool execution, arguments, results, prompts, and stored messages remain unchanged.
- `pi-live-codex-delegation` messages collapse to one line and expand to their original contents.
- The live-voice editor, visualizer, status, microphone, keyboard handling, and controls remain untouched.
- Reload preserves the selected view and expanded choices; new sessions start normal.
- Previously unobserved steps use Lens's single-row resume fallback, without invented timing.
- Fullscreen clicks open folds and details; native expansion exposes every original tool in either TUI mode.
- Unsupported private component shapes fall back to native rendering, never hidden failures.

Pi has no universal question or subagent schema. Support Claude-style question records and
`pi-subagents@0.77.0` result metadata through named, tested adapters; otherwise retain native details.
Background completion and slash-command errors have no universal native event schema.
Expose unsupported cases honestly rather than guessing text origins or fabricating metadata.
Pi's bash tool has no description field; use Lens's existing fallback, “Ran a shell command”.

## Approach and slices

1. Establish package, pinned host development dependencies, strict TypeScript, and test commands.
2. Port pure Lens formatting with parity tests first; adapt Pi names and results at one boundary.
3. Gate feasibility using the real extension loader and credential-free terminal fixture, then test
   a display-only transcript projection against real Pi component instances.
4. Implement normal/clean folds, click routing, native expansion, labels, and raw recovery.
5. Wire lifecycle, `/lens`, working status, resume, and session replacement.
6. Audit unchanged model-facing state, teardown, errors, unknown tools, images, and narrow terminals.
7. Run deterministic terminal smoke tests without model calls, then validate workstation package loading.
8. Write Diátaxis documentation and dotfiles-specific trial instructions; report exact readiness limits.

Keep modules limited to formatting, Pi normalization, presentation, host adapter, and extension wiring.
Reuse pure formatting without extracting a shared package or introducing a plugin framework.
Use an instance-scoped transcript adapter instead of process-wide patches wherever host access permits.
The public renderer API alone cannot provide mixed-run grouping and native message footers.

## Decisions

| ID  | Decision                                           | Reason                                                       | Authority               |
| --- | -------------------------------------------------- | ------------------------------------------------------------ | ----------------------- |
| D1  | Standalone sibling repository                      | Reusable outside dotfiles                                    | User                    |
| D2  | Behavior parity before improvements                | Avoid redesigning the requested first version                | User                    |
| D3  | TDD for each behavior                              | Prove regressions before adding implementation               | User                    |
| D4  | Pin Pi 1.1.0 for first support                     | Matches the primary user's installed host                    | Repository evidence     |
| D5  | No shared cross-repo runtime dependency            | Keep installation independent; avoid premature abstraction   | Implementation decision |
| D6  | Guard private transcript integration               | Exact grouping and message footers require host internals    | Spike evidence          |
| D7  | No publication or default-profile installation yet | Local testing does not require shared writes                 | Scope boundary          |
| D8  | No output/context rewriting                        | Lens is presentation-only                                    | Existing Lens contract  |
| D9  | Fold live-voice delegation messages only           | User supplied screenshots of verbose transcript messages     | User                    |
| D10 | Never patch the editor or intercept voice keys     | Protect the live-voice visualizer and controls               | User                    |
| D11 | Use a Lens-owned activity status                   | Pi's global working-message setter has no ownership contract | Audit correction        |

## Accepted trial refinements

| ID  | Decision                                                          | Reason                                        | Authority           |
| --- | ----------------------------------------------------------------- | --------------------------------------------- | ------------------- |
| D12 | Mark expandable steps with closed/open chevrons                   | Make available detail visible before clicking | User trial feedback |
| D13 | Humanize recognized model IDs without changing stored identifiers | Prefer labels such as GPT 6 Astra             | User trial feedback |

These changes retain the accepted views, native fallback, and voice-UI boundaries.

## Expand every collapsed step

Current task: make all Lens-collapsed steps individually expandable, including reads and historical calls.
Native expanded components replace copied, bounded detail previews. No tool executes again.
The guarantee is no additional Lens truncation; upstream tool truncation and native renderer limits still apply.

| ID  | Decision                                                        | Reason                                                                        | Authority               |
| --- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------- |
| D14 | Every collapsed tool step opens its original expanded row       | Reads, old calls, running tools, and custom renderers must remain inspectable | User                    |
| D15 | Remove Lens detail caps and copied payloads                     | Native rows already own the complete retained result                          | User requirement        |
| D16 | Use the public global-expansion flag for native bypass          | Individual expansion must not unfold sibling steps                            | Independent plan review |
| D17 | Global collapse clears individual tool and voice opens          | Collapse must not immediately reopen prior details                            | Review recommendation   |
| D18 | Synchronize native collapse and restore choices on rebuilt rows | Preserve click behavior, raw transitions, and reload                          | Independent plan review |

The original bounded-preview acceptance criteria below are superseded by these decisions.
Keep run folds, error summaries, readable model names, and the live-voice editor unchanged.
Questions retain their friendly summary and expose the original arguments/results when opened.
The transcript adapter must delegate its original renderer when the projection returns the original child array.

Implementation order:

1. Add failing native-equivalence tests for reads, historical/custom tools, large outputs, and mouse controls.
2. Implement a shared native disclosure wrapper and explicit global/raw transition reconciliation.
3. Remove obsolete copied preview fields/helpers; keep summary facts only.
4. Reconcile historical/voice disclosure keys against the active branch, separately from bounded metadata.
5. Run independent audit, all tests, voice compatibility, both TUI modes, then update user documentation.

Required regressions: output beyond 20,000 characters/2,000 lines; commands beyond 4,000 characters;
diffs beyond 200 lines; rows older than 150 and 600 calls; custom buttons/images; streamed updates;
header/body collapse; global toggles; raw clicks; reload; branch navigation; unchanged model-visible context.

## Action summaries instead of internal labels

The resumed-session screenshot shows an unhelpful `Codemode` step and several verbose reasoning headings.
Summarize observed nested actions from Pi's `details.calls`; do not infer tasks from arbitrary script text.
A batch reading files should name those files or give action counts, not say `Took 1 other step`.
The user's follow-up requests the latest thinking heading with expandable history.
Keep assistant prose and failures visible; implement the requested progress layout.
All original script, nested-call, reasoning, and result details remain available through expansion.

| ID  | Decision                                                      | Reason                                                             | Authority       |
| --- | ------------------------------------------------------------- | ------------------------------------------------------------------ | --------------- |
| D19 | Summarize executed nested actions, not the orchestration tool | `Codemode` is implementation detail, not useful progress           | User screenshot |
| D20 | Superseded: generic folded reasoning label                    | User prefers useful live progress rather than hiding every heading | User correction |
| D21 | Latest progress heading with expandable history               | Keep current activity visible without accumulating noise           | User follow-up  |

Action summaries follow the independent expansion worker's owned presentation changes.
Progress layout uses inline disclosure (`rule/inline-before-modal`),
keeps user-opened history stable (`rule/preserve-mental-model`), and retains specific progress copy
(`rule/loading-state-specific`) from the product-design rule registry.

## Hover feedback and latest progress

The existing headers handle clicks but do not render pointer-hover feedback.
Use the theme's selected background on clickable headers without changing their geometry or error colors.
Hover must clear when the pointer leaves, on view changes, and during scrolling/selection.
Observe terminal mouse sequences without consuming input; do not replace the editor or capture pointer gestures.
Hover refreshes must not reset transcript text selection.

Progress uses one latest heading per user request, with all earlier thinking available on expansion.
Reuse native thinking components where possible, preserving prose, errors, truncation warnings, and raw rendering.
An opened history stays open while new headings arrive. No model calls generate these summaries.

| ID  | Decision                                                | Reason                                                | Authority             |
| --- | ------------------------------------------------------- | ----------------------------------------------------- | --------------------- |
| D22 | Theme-based hover highlight for every Lens click target | Make interactive steps visibly discoverable           | User                  |
| D23 | Non-consuming mouse observation; selection-safe repaint | Preserve native selection and live-voice input        | Safety constraint     |
| D24 | Superseded by D30: one progress disclosure per request  | Later activity was hidden above newer assistant prose | Earlier user feedback |

Verification: header enter/leave, full-width hover, errors retaining red text, no action on motion,
selection/capture/voice unaffected, hover surviving redraw, mode/reset cleanup, chronological progress expansion,
streaming updates, multiple assistant rows, visible prose/failures, raw equality, and both terminal modes.

## Thinking-list clarity and stable expansion

User feedback requests explicit thinking labels, a tight bulleted history, role-specific model colors,
and expansion that leaves the viewport in place. Normal run totals are labels, not disclosure controls.

| ID  | Decision                                                                | Reason                                                       | Authority |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------------------ | --------- |
| D25 | Label active reasoning Thinking… and completed history Thinking updates | Make the progress row's purpose explicit                     | User      |
| D26 | Render one bullet per thinking update without blank separators          | Make expanded history scannable while retaining its detail   | User      |
| D27 | Warm reply-model labels; muted grey tool-run labels                     | Match the role distinction in the supplied Claude screenshot | User      |
| D28 | Disable follow-end at the current viewport offset when details expand   | Keep the reader in place; new detail extends below           | User      |
| D29 | Normal run totals are non-interactive and never hover-highlight         | Only actual disclosure controls advertise interaction        | User      |

Thinking activity is inferred only from streaming thinking content, not merely a still-streaming reply.
Before thinking content arrives, Pi's native working indicator remains responsible for activity feedback.
Thinking-history formatting may use display-only per-update native Markdown components; stored messages remain unchanged.
Preserve prose, errors, fenced code, detailed paragraphs, raw rendering, and Markdown transformer behavior.

Viewport pinning uses Pi 1.1's guarded primary ScrollView and its public scrollTo(disableFollow) option.
It runs before the next layout pass, without changing editor focus or intercepting navigation keys.
Regular-mode terminal scrollback remains terminal-owned. Raw mode retains native behavior.

Verification: active/completed labels; tight bullets and retained detailed text/code; readable small widths;
reply-versus-tool color assertions; inert normal totals with working more/fewer controls;
real fullscreen expansion while following bottom and while scrolled up, including tool, voice and thinking rows;
manual scrolling afterward; and unchanged voice UI/model context.

## Verification

- Pure tests: labels, 15 error classes, run counts, five-step limit, clean failures, question answers, models.
- Host tests: real tool components, mixed calls, assistant boundaries, click coordinates, raw equality.
- Lifecycle tests: reload, fresh sessions, repeated prompts, branching, disposal, unsupported host shapes.
- Safety tests: deep-frozen messages/results; unknown tools; cancellation; images recoverable natively.
- Width tests: narrow/wide terminals, ANSI styling, Unicode paths, long command output.
- Voice tests: exact delegation custom type; full expansion; raw equality; unchanged editor and sibling widgets.
- Load installed `pi-live-codex` beside Lens in an isolated profile, without opening audio or connecting voice.
- Package checks: typecheck, tests, formatting, Markdown, publish payload, and clean dependency installation.
- Terminal smoke: synthetic fixture, no API credentials, fullscreen and regular modes, view switching.
- Workstation: isolated profile and workspace with explicit compatibility extensions; never activate voice.
- No dotfiles writes, settings/package commands, default-profile installation, or `dots` execution.

### Parity acceptance matrix

| Behavior                                            | Source                        | Executable evidence                                |
| --------------------------------------------------- | ----------------------------- | -------------------------------------------------- |
| Labels, facts, 15 errors, bounded output            | `hooks/lens.ts`               | `tests/domain.test.ts`                             |
| Normal five steps; clean latest failure; mixed runs | `drawFold`                    | `tests/presentation.test.ts`                       |
| Click step, more/fewer, question; native expansion  | `drawFold`, question renderer | `tests/adapter.test.ts`, `tests/terminal-smoke.py` |
| Status, model, time, duplicate prompts              | `stampLabel`, render hooks    | `tests/presentation.test.ts`                       |
| `/lens` status, invalid args, global redraw         | command handler               | `tests/extension.test.ts`                          |
| Raw equals native Pi with identical extensions      | raw guards                    | component equality and terminal smoke              |
| Reload choices; fresh/reset; unseen resume rows     | atoms and fallback render     | lifecycle tests                                    |
| Active label; no custom working label in raw        | spinner hook                  | extension tests                                    |
| Command box, diff, output caps                      | `drawFold`, `outputOf`        | presentation tests                                 |
| Subagent model, question states                     | agent/question helpers        | normalization fixtures                             |

Private integration must restore native rendering after partial failure and remain inert outside TUI.
Keep UI state in an in-process session-keyed slot solely for reload, never in model-facing messages.
Use native expansion state rather than intercepting a hardcoded Ctrl+O shortcut.
Use Pi wording for errors and preserve non-Claude model identifiers rather than calling them Claude.

### Independent review

The plan reviewer identified interaction, historical-state, and loader-test gaps; this revision addresses them.
Remaining platform gaps must be reported before claiming full parity: arbitrary slash-command output and
unrecognized background-agent notification schemas have no universal Pi contract.

Review the plan independently before implementation. Audit the result against this contract afterward.
Do not call a source inspection or component test a human terminal acceptance test.

## Documentation

Use Ghostwriter's plain fallback; no private voice profile is installed.
README explains value and a local-checkout trial without claiming a published registry package.
Separate tutorial, how-to, reference, and explanation pages under `docs/`.
Keep contributor commands in `AGENTS.md` and a contribution how-to.
Document private API coupling and any remaining parity gaps explicitly.

## Packaging constraint

The npm registry already contains an unrelated `pi-lens@4.4.3` from `apmantza/pi-lens`.
The repository name remains `pi-lens`; `private: true` prevents accidental publication under that package name.
A scoped publication name and remote creation remain separate decisions after local acceptance.

## Current feedback and sibling delivery plan

This section governs remaining work and supersedes conflicting original trial exclusions.
Both Lens implementations share one visual and behavioral target wherever host capabilities permit.
Every supported refinement must be evaluated in both repositories, not treated as a Pi-only redesign.
A Pi-first delivery unblocks the current trial; the paired Claude review remains required before parity acceptance.
The user now requests implementation of every remaining local work item through delegated execution.
Exact send-now behavior, local upstream patches, and laptop-first image presentation are approved.
Installing patched host builds, publication, and new global behavioral instructions remain separate approval gates.

### Feedback decisions

| ID  | Decision                                                                              | Reason                                                                               | Status / authority                                               |
| --- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| D30 | Start a new activity segment after visible assistant prose                            | New work must remain visible below the latest reply                                  | User; supersedes D24                                             |
| D31 | Remove bold styling from compact thinking labels                                      | Compact history needs less visual emphasis                                           | User                                                             |
| D32 | Remove spacing owned solely by hidden rows                                            | Folding must reclaim vertical space without flattening native content                | User                                                             |
| D33 | Unknown authorship stays neutral and visible                                          | User role and text equality do not prove human authorship                            | Confirmed provenance audit                                       |
| D34 | Verified automation gets a distinct expandable presentation                           | Separate generated input from human messages without losing content                  | User; identity binding is a feasibility gate                     |
| D35 | Keep native batch ownership; distinguish actions from batches                         | Three nested actions can belong to one expandable Codemode call                      | Recommendation; do not fabricate independent native child rows   |
| D36 | Fix raw warning output at its producer                                                | Global console interception and weaker child isolation are inappropriate workarounds | Source evidence; upstream delivery choice remains open           |
| D37 | Keep queue mutation outside Lens                                                      | Lens changes presentation, not execution or composer controls                        | Existing contract                                                |
| D38 | Use versioned Git distribution for Pi Lens                                            | The unscoped npm name belongs to another project                                     | Proposed release route; publish only with explicit authorization |
| D39 | Document unavoidable host-specific parity limits                                      | Claude declares neither Pi-style thinking replacement nor exact viewport anchoring   | Independent API audit; report exceptions before release          |
| D40 | Maintain a shared visual and behavioral target across both Lens implementations       | The user explicitly reaffirmed closest possible sibling parity                       | User; applies to every delivery slice                            |
| D41 | Match Claude send-now exactly, including conditional interruption and draft inclusion | User explicitly resolved the conflict in favor of exact parity                       | User; supersedes earlier no-interruption request                 |

### Recovery and resumed implementation

The resumed session recovered the original conversation and late child artifacts before continuing.
Pi is the primary coding agent; Claude Code remains the closest supported behavior reference.
The user approved implementation of the recovered backlog in the personal AI harness.
The user separately approved creating and pushing public GitHub source at <https://github.com/waldoibarra/pi-lens>.
The remote now exists. Package publication and releases remain blocked until local user validation.

| ID  | Decision                                                                      | Reason                                                              | Authority                                                  |
| --- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------- |
| D42 | Prioritize Pi while preserving paired Claude behavior                         | Pi is the user's primary coding agent                               | User, resumed session                                      |
| D43 | Repair completed drafts before adding dependent features                      | Late independent audits found unresolved defects                    | Recovered audit evidence                                   |
| D44 | Deliver host identity before clipboard tokens and send-now                    | Attribution and attachment handling require exact message ownership | Independent host review                                    |
| D45 | Keep installation and publication separate from source verification           | Existing approval gates protect the running harness                 | Existing boundary; activation decision pending             |
| D46 | Commit verified changes atomically with explicit paths                        | Preserve concurrent agents' unrelated work                          | User, resumed session                                      |
| D47 | Block publication until user validates locally                                | User requires local acceptance before release                       | User, resumed session                                      |
| D48 | Handoff only when every unresolved owner explicitly supports it               | Mixed or nested execution cannot safely assume background ownership | Lead; conservative Pi policy, not verified Claude behavior |
| D49 | Preserve ordinary queue scheduling; send-now selects in submission order      | Avoid changing Enter or SDK timing while adding immediate delivery  | Lead; implementation boundary                              |
| D50 | Settle owned background work before session invalidation; no restart survival | Prevent orphan results or cross-session delivery                    | Lead; conservative Pi policy                               |
| D51 | Add configurable Ctrl+Enter before a separate chord implementation            | Existing keybinding arrays are alternatives, not chord sequences    | Source review and lead                                     |

Recovered state supersedes stale pending-implementation labels below:

- Image-first rendering exists; audit corrections and full image lifecycle verification remain pending.
- The image loader fixture exists; fullscreen passed historically, regular image interaction remains unverified.
- Composer-safe warning routing exists; async and static-metadata warning escapes remain unresolved.
- Claude native delegation exists; standalone result visibility, questions, footer order, and status require fixes.
- Host identity received independent review with corrections; host implementation has not started.
- Harness lessons are recorded in the dotfiles roadmap; no additional global policy is needed.
- No earlier implementation workers were observed running during recovery.
- Historical Pi full-check log records 125 passing tests; this is not fresh acceptance of the remaining defects.

Current execution: one writer per repository, followed by independent audits and lead verification.
Use native delegation; the previous session's CLI-child workaround is no longer needed.
Do not overwrite unrelated dirty dotfiles changes or claim patched builds are active before installation.

Active resumed lanes:

- GPT-5.5 high: Pi Lens image audit repairs, warning-routing repairs, Claude native-detail repairs, and Pi identity implementation.
- Astra high: independent implementation briefs for send-now/queue diagnostics and clipboard/attribution integration.
- The lead owns integration, fresh verification, atomic commits, and approval-gated activation.
- User requires local validation before package publication. Source-only GitHub push is now explicitly authorized.
- Pi Lens has a verified public GitHub remote; initial commit and source push follow source verification.
- Both READMEs use actual public sibling URLs. No release tags, registry publication, or release claims.
- Dotfiles already contains unrelated MCP and policy edits; never stage whole dirty files without ownership review.

### Latest visual feedback: current activity at the transcript tail

The new screenshot shows completed thinking above newer work and excessive space before the composer.
Current source anchors grouped thinking at its first segment; normal folds can hide running steps after the fifth.
This feedback reopens activity and spacing acceptance despite earlier passing tests.

| ID  | Decision                                                     | Reason                                                        | Authority                                             |
| --- | ------------------------------------------------------------ | ------------------------------------------------------------- | ----------------------------------------------------- |
| D52 | Keep current observed activity after the latest visible work | Old anchors make active work appear stalled                   | User screenshot; supersedes first-anchor presentation |
| D53 | Fold summaries expose the current observed action            | Running work must remain visible beyond the five-step preview | User                                                  |
| D54 | Remove presentation-owned gaps between messages              | Dense transcript improves progress visibility                 | User; preserve meaningful content whitespace          |

Implementation boundary: Pi Lens display projection first; evaluate equivalent Claude behavior through supported hooks.
Both READMEs link their public GitHub sibling. Pi Lens remains source-only and unreleased.
Use specific observed thinking/tool labels, never guessed plans, invented progress percentages, or elapsed-time promises.
Preserve prose order and full history; current progress must not rewrite or reorder model-visible messages.
Keep one authoritative live indicator rather than duplicate moving controls.
User-opened details and scrolled history stay stable; do not force follow-bottom or steal editor/voice focus.
The user explicitly requires peek expansion: keep the clicked header and content above at their screen positions.
Expansion pushes content below downward. Collapse preserves the anchor where native scroll bounds permit.
Apply this to tool details, thinking history, images, Details, clean folds, and more/fewer controls.
Keep more/fewer at one fixed position after the preview; insert additional rows below its toggle.
Keep historical thinking disclosures stable; later cycles after visible tools start chronological segments.
This supersedes the older rule that all tool cycles must append into one earlier history disclosure.
Use one noninteractive current-activity summary at the transcript tail, separate from historical disclosure controls.
Assert screen coordinates and upper-content snapshots before scrolling to newly revealed details.
Completed/failed/interrupted work must stop advertising active thinking.
Unknown native shapes retain native rendering.

Verification: reproduce reply → tools → thinking → tools, over-five-step running folds, async notices, narrow widths,
normal/clean/raw, streaming to settled, open-history stability, actual terminal snapshots, and no accumulated message gaps.
Separate real inter-message spacers from unused viewport height; do not remove space by changing terminal height.
Preserve code fences, paragraphs, native result contents, images, selection, links, and model-context equivalence.

Product basis: specific loading feedback, inline disclosure, and preserving the reader's context.
Rules: `rule/loading-state-specific`, `rule/inline-before-modal`, `rule/preserve-mental-model`.

Fresh lead verification before this feedback: 130 tests and direct/batch both-mode voice-co-loaded smoke passed.
The image-specific fullscreen fixture failed waiting for `fixture-image-details-ok`; it remains an integration blocker.
The image audit traced this to metadata correctly expanding below the pinned viewport, not a failed click.
Assert stable header position before scrolling to inspect metadata; retain voice co-loading.

Latest automation feedback: collapse verified generated updates by default, with concise summaries and complete expansion.
Keep human messages visible as You. Do not classify authorship from the screenshot's text or filename patterns.
Requests requiring human approval remain prominent; do not hide required decisions inside routine completion folds.
The host identity slice is committed as e988874. Lens now consumes its exact native-row bindings.
The consumer passed independent audit, 149 tests, and both source-host terminal modes with cold resume.
Published Pi 1.1.0 lacks those bindings; legacy inputs remain neutral until a patched host supplies provenance.

The user reconfirmed composer-warning removal as urgent. Producer routing is committed in pi-subagents as `00e2bed`.
The lead verified 19 warning/runtime tests, 41 executor tests, typecheck, and diff checks after audit corrections.
Real-loader warning/composer checks now pass against source and installed local builds in both modes.
The lead installed the warning-only local build without network access, lifecycle scripts, or settings changes.
Rollback artifacts remain under the native profile's private `local-trials` directory.
The running process still retains the old runner until restart; no active workers were interrupted.

Repeated incomplete UI and identity repairs justify routing their final corrections to Astra high.
Claude Lens passed final independent audit and 26 tests; source commit `a3e074f` remains local.
The applicable Claude scope is ready for a fix freeze and local visual validation.

### Completion checklist

This is the authoritative cross-repository execution checklist. Do not stop at an isolated polish milestone.
Mark implemented, independently reviewed, locally verified, activated, and published states separately.

| Work item                                                | Owning repository                       | Current state                                                                          | Completion gate                                                                           |
| -------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Thinking typography, activity placement, compact spacing | Pi Lens                                 | Implemented; final independent audit passes; 138 tests and terminal gates pass         | Current work stays visible; remove presentation-owned gaps                                |
| Inert totals, singleton layout, chevrons, model labels   | Claude Lens                             | Implemented; reviewed; 25 tests passed                                                 | Preserve paired behavior                                                                  |
| Laptop inline-image protocol                             | Dotfiles                                | Committed `0f7c160`; five fresh provisioning tests and full lint pass                  | User screenshot confirms laptop rendering; Moshi deferred                                 |
| Image-first disclosure with technical details secondary  | Pi Lens                                 | Implemented; final independent audit and image-fullscreen terminal check pass          | Fix Details integration and pass independent audit                                        |
| Clipboard image tokens and attachment identity           | Pi host, then Lens                      | Source verified; activation and physical clipboard checks pending                      | `[Image 1]` maps losslessly to original input; no arbitrary path inference                |
| Distinct automated-input presentation                    | Pi host, then Lens                      | Host e988874 and Lens consumer audited; 149 Lens tests and both source-host modes pass | Exact origin/message/row identity survives queues and history                             |
| Composer-safe subagent diagnostics                       | pi-subagents; Pi diagnostics separately | Committed and installed locally; source and installed native-terminal checks pass      | UI warnings remain visible without terminal writes; native diagnostics follow             |
| Queue visibility and exact send-now                      | Pi host                                 | Source plan exists; implementation pending                                             | Typed queue, eligible background handoff, conditional interruption, draft, recovery, keys |
| Native details and remaining sibling parity              | Claude Lens                             | Committed a3e074f; 26 tests and final independent audit pass                           | Native details, footer ownership, and real host acceptance                                |
| Sibling links and release/install preparation            | Both Lens repositories                  | Pending                                                                                | Consistent docs/manifests and reproducible isolated installs                              |
| Managed workstation provisioning                         | Dotfiles                                | Pending release artifact                                                               | Pinned reachable artifact; preserve other agents' changes                                 |
| Harness-roadmap session lessons                          | Dotfiles                                | Recorded; retain existing global policy                                                | Commit Lens-owned records without other agents' changes                                   |

Lead-owned decisions for remaining implementation:

- Image bodies prioritize the native image; expose original technical output through a secondary Details disclosure.
- Only host-verified clipboard-pasted images receive tokens; ordinary image files retain their actual paths.
- Number pasted images within their originating human message; stable attachment IDs preserve labels across reload and branches.
- Never mint image tokens from filename prefixes, extensions, read results, or visible-row order.
- Host attachment metadata must survive reload/resume without modifying model-facing content.
- Genuine composer messages must display `You`; the temporary `Input` fallback is not the finished UX.
- Automated messages need distinct source attribution. Unknown historical origin must not be invented.
- Route diagnostics through explicit callback selection; a void callback must never fall through to console via `??`.
- Keep headless/detached logs; nested in-process children inherit the UI diagnostic sink.
- Prefer an explicit background receipt plus linked eventual completion; never duplicate tool results or orphan work.
- Never claim complete send-now parity until mixed tool batches, cancellation, queue order, and draft handling pass.
- Derive remaining technical ownership choices from source and tests; ask only for genuinely unresolved user behavior.
- User reviews after integrated implementation; do not repeatedly require manual acceptance of unfinished slices.

### Delivery order and ownership

One implementation writer per worktree at a time. Read-only research may run concurrently.
Independent host work may use isolated, frozen-base worktrees; the lead alone integrates their commits.
This supersedes serial-per-repository scheduling for the independent diagnostics and send-now slices.
The lead owns decisions, integration, git operations, publication, and workstation synchronization.

| ID  | Decision                                                     | Reason                                                                               | Authority                         |
| --- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------ | --------------------------------- |
| D55 | Isolate send-now development from the ordinary host checkout | Preserve verified identity/clipboard work during independent diagnostics integration | Lead; existing worktree mechanism |

1. **Visible activity and compact spacing — Pi Lens, first delivery.**
   - Files: `src/progress.ts`, `src/presentation.ts`, `src/state.ts`, and progress/state/presentation/terminal tests.
   - Replace timestamp-only segment keys and update reconciliation for independent segments within one assistant component.
   - Verify independent toggles, streaming stability, same-process reload preservation, and branch pruning.
   - Replace obsolete per-request ordering assertions in `tests/progress.test.ts`.
   - Write failing tests for reasoning, reply prose, then new reasoning and tools.
   - Segment thinking at visible prose boundaries; do not move older activity beneath newer replies.
   - Handle reasoning and prose within one native assistant component in chronological order.
   - Existing tool grouping checks prose; reproduce its reported failure before changing that boundary.
   - Reproduce the screenshot's expanded thinking bullets with an ANSI-style assertion before changing typography.
   - Remove bold from compact history labels, not the already-muted disclosure header; preserve body Markdown and code.
   - Measure spacing from hidden assistant components, content containers, and transcript-level spacers.
   - Remove only verified presentation-owned empty space; preserve paragraph/code whitespace and unknown native rows.
   - Gate: new activity appears below the latest prose; empty hidden rows leave no accumulated gaps.
   - Paired Claude acceptance: equivalent activity placement, compact spacing, and typography wherever its render API permits.
   - Record unsupported thinking replacement explicitly; do not invent a hook or silently accept avoidable visual divergence.
   - Verify normal, clean, raw, streaming, narrow widths, cached redraws, Mermaid, and viewport stability.

2. **Truthful attribution — Pi Lens, independently shippable safety fix.**
   - Files: `src/state.ts`, `src/presentation.ts`, lifecycle wiring only if proven necessary.
   - First remove unconditional `You` and update tests; unknown input remains visible and neutral.
   - Separately prove message-to-origin and message-to-component identity before adding automated-input folds.
   - Public `input.source` alone cannot join transformed, handled, queued, or historical messages reliably.
   - No content-prefix classifiers, last-source latch, pending FIFO, or timestamp-based authorship guesses.
   - If no reliable integration contract exists, report partial delivery rather than claim solved automation attribution.
   - Gate: identical human/extension text, handled/rejected input, queue reordering, reload, resume, branches, eviction.
   - Preserve frozen message fixtures, native expansion, voice controls, and model-visible context.

3. **Action counts and sibling parity — compare before changing counts.**
   - Pi: `src/pi-data.ts`, `src/domain.ts`, `src/presentation.ts`, normalization and rendering tests.
   - Claude: `hooks/lens.ts`, `hooks/register.tsx`, corresponding tests and generated host declarations.
   - Inventory counting units: native calls, nested observed actions, visible rows, and more/fewer counts.
   - Keep the native batch disclosure; clarify totals if action counts imply independently expandable rows.
   - Shared comparison fixtures cover typography, spacing, chevrons, counts, model/time labels, and expanded native detail.
   - Claude implementation: native detail at each original render site; mixed known/unknown groups retain every member.
   - Remove copied-detail caps only after native delegation is verified against the actual host renderer.
   - Match inert normal totals, singleton display, readable models, and control-only hover where supported.
   - Preserve Claude's positive-origin allowlist; fix ambiguous text-based stamp fallback separately.
   - Explicit exceptions: thinking replacement, exact viewport anchoring, unidentified voice integrations, native expansion limits.
   - Gate: live, historical, failed, running, custom, nested, and partially observed calls retain inspectable details.
   - Test grouped and standalone results, waiting/skipped questions, mixed-known groups, and previous size/age thresholds.
   - Require raw/Ctrl+O recovery and actual Claude host rendering; mocked ENGINE nodes cannot prove native detail completeness.

4. **Warning output — upstream producer, not Lens.**
   - Confirmed source: installed `pi-subagents/src/runs/foreground/execution.js` emits launch warnings with `console.warn`.
   - The screenshot's warning is generated in `src/runs/shared/child-tool-plan.js` for explicit empty extension lists.
   - Retain intentional child isolation; do not remove `defaultExtensions: []` merely to suppress the warning.
   - Inspect supported notification/logging paths; prepare a bounded upstream fix in a separate checkout if authorized.
   - Release-blocking gate: no subagent log renders inside the composer, including the repeated empty-extension warning.
   - Warning remains visible through supported UI; editor draft remains byte-for-byte unchanged, with no terminal corruption.
   - Reproduce in an actual TUI with nonempty draft, repeated launches, completion, failures, resize, and both screen modes.
   - This defect is independently shippable and must not wait for provenance research or full sibling parity.
   - Cover foreground/background and headless logging; dotfiles changes only the verified deployment artifact afterward.
   - No installed-package edits, process-wide console patches, unapproved fork publication, or guessed release versions.
   - Verified producer approach: run-scoped diagnostic callback from execution to the UI-owning executor's `ctx.ui.notify`.
   - Preserve transcript/headless logs and propagate diagnostics into nested in-process children.
   - Pi resource-loader and event-bus diagnostics also write directly; full native-child coverage needs per-instance host sinks.
   - User approved local upstream patch preparation. Installation and publication remain separately approval-gated.

5. **Send queued messages now — research and decision gate.**
   - New user feedback requires explicit visual distinction between working, input received/queued, and input delivered.
   - Replace opaque queue terminology with clear delivery timing in the host's pending-message display.
   - Keep activity visible near the composer; completed tool rows must not imply the agent has finished thinking.
   - Preserve queue contents, draft, and native controls; never visually claim delivery before actual consumption.
   - Screenshot evidence shows reload rejected during active work; end the parent turn before inviting a reload.
   - The lead must distinguish interim progress messages from final handoff; do not continue tools after a reload handoff.
   - Pi 1.1.0 documents Enter submission, Alt+Enter follow-up, and Alt+Up dequeue-to-editor.
   - Tracked `home/.pi/agent/keybindings.json` does not override these actions.
   - Claude documents `chat:sendNow`: Ctrl+Enter or Ctrl+X Ctrl+S, including queued messages and draft.
   - Current Claude backgrounds eligible running work; otherwise it interrupts. An abort-only port is not exact parity.
   - Verified: Pi 1.1.0 native bash lacks foreground-to-background handoff; abort kills its process tree.
   - Subagents have a narrower accepted-receipt detachment path; this does not supply generic host handoff.
   - Source: <https://code.claude.com/docs/en/interactive-mode> and <https://code.claude.com/docs/en/keybindings>.
   - Verified: Pi 1.1.0 has no named send-now action; a keybinding-only change cannot implement it.
   - In ordinary streaming only, Escape restores queued text and requests abort; Enter can resubmit reviewed text afterward.
   - Compaction and retry install different Escape handlers; this is not a generally safe send-now workaround.
   - This workaround merges steering before follow-ups and is unsafe for preserving queued attachments.
   - `_queueSteer` retains image blocks, but `clearQueue()` returns only text and clears underlying agent queues.
   - Recommended implementation owner: Pi host; dotfiles binds the eventual supported action, never Lens.
   - Preserve typed queue records and attachments rather than building on lossy dequeue-to-editor behavior.
   - Distinguish steering at the next boundary from immediate interruption; never advertise a dequeue remap as send-now.
   - Existing public extension APIs do not suffice; prefer a native host action with dotfiles binding after delivery.
   - Host prerequisites: identity-based typed queue, global submission order, command barriers, and background lifecycle ownership.
   - Include duplicate-safe acknowledgements, transformed-input preservation, and exactly-once eventual tool results.
   - Claude's portable Ctrl+X Ctrl+S fallback also needs chord dispatch; Pi currently uses single-key matching.
   - Evaluate already-queued messages first; leave the current draft untouched during research and feasibility tests.
   - Accepted: match Claude exactly, including queued messages followed by the current draft.
   - Background eligible work; interrupt only when Claude would, including its shell-mode and queued-command exceptions.
   - The earlier unconditional no-interruption requirement is superseded by the user's explicit clarification.
   - Feasibility remains unverified in Pi; never ship an abort-only shortcut claiming exact parity.
   - Test idle/streaming/tool-running/compacting/retrying states, duplicate inputs, attachments, delivery order, and failures.
   - Verify keyboard protocol support and conflicts with voice/editor controls; no automatic retries or duplicate submission.
   - Recovery must preserve unsent queue items and draft; cancellation cannot promise rollback of completed tool effects.

### Pasted-image presentation

User requests readable `[Image 1]` tokens with previews collapsed by default.
Expanding should reveal the rendered image where supported, with the original path still accessible.

- Pi 1.1.0 clipboard handling currently inserts temporary paths; native user rows retain only text.
- The current session reports `TERM_PROGRAM=herdr`, with no image-protocol override.
- Pi's automatic detection disables image protocols for Herdr; this is not proof Herdr lacks image support.
- Verified laptop: Ghostty 1.3.1 auto-launches Herdr client/server 0.9.3 through tracked Ghostty configuration.
- Exact Herdr 0.9.3 documentation confirms standard Kitty graphics support, including local Ghostty clients.
- Dotfiles now sets native `terminal.images: "kitty"`; `/reload` reapplies it without installing a patched host.
- A native SDK check reproduced the old fallback, verified Kitty image output, and verified rollback to automatic detection.
- Five isolated dotfiles provisioning checks pass. Physical image appearance still requires the user's laptop trial.
- This profile-wide preference targets the laptop stack; Moshi and other terminal paths are deferred.
- Separate host attachment identity/editor tokens from Lens transcript folding and terminal rendering capability.
- Reuse native paste-token and image components where their contracts support this behavior.
- Do not reinterpret arbitrary path-looking prose as an attachment or load arbitrary files while rendering.
- Preserve actual submitted content, model context, raw output, voice controls, and access to original paths.
- Verify inline support before enabling a protocol; never mask Herdr as another terminal.
- Cover multiple images, missing files, repeated paths, resume, narrow widths, expansion, and native image cleanup.
- GPT-5.5 medium reviewed native integration points and the laptop override; the override passed independent plan review.
- Readable image tokens and collapsed user-message previews remain unfinished; they require host-owned attachment identity.

### Distribution and documentation — after behavioral acceptance

- Add reciprocal sibling links and host-specific behavior matrices to both repositories.
- Update Pi's `docs/reference/views.md`, `docs/explanation/display-only.md`, and installation guide.
- Behavior documentation ships with each implementation slice, not deferred until final distribution.
- Update Claude's views, architecture/development docs, and release metadata after verifying its release commands.
- Separately authorize and deliver the Claude release before clean-profile verification of that exact published version.
- Publish an immutable Pi Git tag only after authorization and passing release checks.
- Then declare the reachable Git package in dotfiles; preserve filtered existing package declarations.
- Dotfiles targets: `home/.pi/agent/settings.json`, `scripts/tests/test-agent-harness.py`, Pi installation/configuration docs.
- Existing updater likely needs no functional change; verify missing pinned Git installation in an isolated profile.
- Verify Claude marketplace installation on a clean profile rather than assume startup reconciliation.
- Run `dots` only when deployment is authorized and necessary; announce it and protect unrelated dirty files.

### Orchestration and verification

- Queue research: `code-auditor`, `openai-codex/gpt-5.5`, medium effort; bounded source tracing suits this model.
- Independent plan review: `plan-reviewer`, `openai-codex/gpt-6-astra`, high effort; cross-host trust and ordering need deeper review.
- Pi UX implementation: GPT-5.5 high, sole Pi writer; native segmentation and reconciliation justify extra reasoning.
- Claude polish implementation: GPT-5.5 medium, sole Claude writer; bounded labels and control behavior need less exploration.
- Host controls research: Astra high, read-only; exact queue parity and in-process logging require careful capability tracing.
- Final audit: Astra high, read-only, after writer completion; then lead runs integrated verification.
- Native subagent tool is unavailable in this session; explicit isolated Pi CLI children provide delegation.
- No child may publish, commit, install, run `dots`, modify credentials, or start shared services.

Pi gates: focused failing tests first, then `bun run check` and credential-free terminal fixtures.
Run terminal fixtures in both TUI modes, with the installed voice extension without opening audio.
Compare model-visible context before/after each presentation slice; report exact test counts only after execution.
Claude gates: `just help` and its recipes were inspected; run `just check`, then verify native rendering in its host.
Dotfiles gates: `python3 scripts/tests/test-agent-harness.py`, scoped lint, and isolated fresh-profile provisioning.
Native terminal acceptance must cover actual screenshots' ordering and spacing, not only mocked renderer nodes.

After independent audit convergence, propose a fix freeze before release; later findings enter the next-iteration list.
Recovery: `/lens raw` or unload Lens; revert owned source changes only, never unrelated workstation modifications.
Unresolved: patched-host activation, default-loader diagnostics, exact send-now feasibility, and publication authorization.
Reliable Pi origin identity is implemented and source-verified; stock Pi lacks its required bindings.

### Planning evidence and handoff

Queue research completed through GPT-5.5 medium; key behavior was independently checked against installed source.
`interactive-mode.js:2416–2419,3663–3671,3885–3901` establishes abort, follow-up, and text restoration behavior.
`agent-session.js:1733–1756,1882–1889` establishes structured queue ingestion and lossy clear/restore behavior.
Paths above resolve under the pinned Pi package's `dist/modes/interactive/` and `dist/core/` directories.
Claude shortcut evidence comes from its official documentation, not a local terminal reproduction.
The native batch screenshot shows three nested calls inside one Codemode disclosure; no actions were discarded.
No implementation, shortcut change, installation, publication, or workstation sync occurred during planning.
The 113-test result predates these reports and does not establish their fixes.
Independent Astra review returned ready with fixes. Verified findings were incorporated: segment identities/reconciliation,
Escape-state exceptions, actual native-detail acceptance, per-slice docs, and exact Claude release ordering.
The reviewer initially preferred queued-only evaluation; the user subsequently authorized exact Claude parity, including the draft.
No implementation tests ran during planning. Subsequent execution delivered the first Pi UX and Claude polish slices.
Pi lead verification passed 117 tests and both voice-co-loaded terminal fixture variants with baseline equivalence.
Independent review found structured-prefix and expanded-label retention defects; a bounded writer is correcting them.
Claude lead verification passed `just check` with 25 tests; audit corrections were reproduced and fixed.
Preservation fixes and the neutral-attribution slice now pass lead verification: 122 tests and both terminal fixture variants.
Final integration also corrected unintended per-tool thinking boundaries; tool cycles retain one fold until visible prose separates them.
Independent follow-up inspection verified preservation fixes and neutral attribution; a terminal-ordering verification gap was corrected.
The final snapshot review confirmed the gap closed; the lead removed a redundant assertion and reran every Pi gate.
Fix freeze is proposed for the completed Pi UX and Claude polish slices; no completed automation-origin contract is claimed.
Next independent slices: Claude native-detail feasibility, reciprocal links, release preparation, and isolated dotfiles provisioning.
Producer warning routing and exact send-now are upstream-owned; the user approved local patch preparation.
Checkouts target Pi v1.1.0 and pi-subagents v0.77.0; installed packages remain unchanged.
The initial bounded jobs finished. The latest implementation wave now has explicit repository owners:

| Lane                            | Role/model/effort            | Scope                                                                        | Result artifact                                      |
| ------------------------------- | ---------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------- |
| Image-first Pi UI               | Implementer / GPT-5.5 / high | Original image components, secondary Details; retain non-pasted paths        | `/tmp/lens-image-first-implementation.txt`           |
| Composer-safe warnings          | Implementer / GPT-5.5 / high | Run-scoped UI diagnostic sinks; preserve isolation and headless logs         | `/tmp/lens-warning-implementation.txt`               |
| Host origin/attachment contract | Plan reviewer / Astra / high | Clipboard-only tokens, composer attribution, persistence, queue dependencies | `/tmp/lens-host-origin-attachment-plan.txt`          |
| Claude native details           | Implementer / GPT-5.5 / high | Per-site native delegation, mixed history, no copied-detail caps             | `/tmp/lens-claude-native-details-implementation.txt` |

High effort is justified by native rendering, nested execution, and identity preservation.
Astra owns the cross-layer contract review; bounded implementation uses GPT-5.5.
Dependencies were hydrated with lifecycle scripts disabled in local upstream checkouts only.
No patched host was installed, no model routing changed, and no publication occurred.
Read each result and inspect actual changes before changing a lane to verified.

## Recovery and exclusions

Stop the trial process to unload Lens; `/lens raw` restores native presentation during a session.
The current feedback section authorizes paired Claude Lens work; publication and managed-profile deployment remain approval-gated.
Do not add unrelated styling, configuration systems, telemetry, model calls, or context compression.
