# Proposal

## Why

**Make `dots` deliver shared skills without tracking generated installation state.**
Waldo and Lluvia need the same declared skills available across Pi, Claude Code, and Cursor.
Routine upstream updates currently modify the tracked skills lockfile and generated OpenSpec skills.
The user accepts publication noise but prefers separating installation intent from local state.

## What Changes

- Track external skill names, sources, and client targets in a declarative manifest.
- Keep native lockfiles and generated OpenSpec skills local and untracked.
- Preserve automatic updates through the existing `dots` alias and `just sync` recipe.
- Document explicit enrollment of new shared skills before installation.
- Verify discovery across all three clients, including fresh Pi and Claude sessions through Herdr.

Exclude weekly maintenance skills, version pinning, unrelated updater cleanup, and automatic skill removal.
Do not change the orchestration reference or unrelated work.

## Approach and tradeoffs

### Decisions

| ID | Choice | Reason |
| --- | --- | --- |
| D1 | Track intent; retain local resolution state. | This is the user's selected option. |
| D2 | Continue automatic upstream updates. | Weekly pinned upgrades remain an alternative, not a new requirement. |
| D3 | Target Pi, Claude Code, and Cursor explicitly. | All three clients must discover shared skills. |
| D4 | Require explicit shared enrollment. | Personal experiments must not silently propagate between machines. |
| D5 | Preserve undeclared local skills. | Manifest removal does not authorize uninstalling personal installations. |
| D6 | Remove lockfile auto-commit and push. | Local resolution state no longer needs publication. |
| D7 | Test fixed-input idempotency. | New upstream releases legitimately change local installed state. |

### External skills

Add `home/.agents/skills-manifest.json` with a format version, client targets, and named source entries.
Seed it from the tracked lockfile's existing installation intent, without hashes or timestamps.
Load the manifest relative to the updater's resolved repository root, never from an installed copy.
No new Dotbot manifest link or caller working-directory assumption is required.
Validate names, duplicate entries, supported targets, and sources before mutations.
Reject collisions with repository-authored skills and OpenSpec-owned names.

Replace lockfile-driven installation with manifest-driven reconciliation in `scripts/update-coding-agents/`.
Check actual installed content and discovery links, not merely lockfile entries.
Repair missing delivery for any declared client without reinstalling already-correct content.
Use native CLI interfaces where supported; verify their actual semantics before choosing update calls.
Preserve the existing global update policy, including undeclared installed skills.
Undeclared skills remain local and never become manifest entries automatically.

Remove the Dotbot lockfile mapping.
Add a read-only ownership preflight before Dotbot executes its clean directives.
Invoke it from `scripts/install-dotfiles.sh` and again before standalone skill reconciliation.
Inspect lockfile and managed skill destinations with symlink-aware checks, including broken links.
Reject unknown targets before cleanup can erase evidence; leave their bytes and links untouched.
The guard must support bootstrap Python and preserve installer argument and dry-run behavior.
Migrate its known repository-owned symlink into a regular local lockfile before native CLI writes.
Preserve readable existing lock data; regenerate from declarations when the legacy target is missing.
Reject unknown symlink targets rather than overwriting them.
Keep existing regular lockfiles intact unless native reconciliation requires a real update.
Account for Dotbot cleanup removing broken legacy links during the first upgraded `dots` run.
Do not require a manual migration command on either machine.

Keep initial installation and agent provisioning as distinct supported stages.
`./scripts/install-dotfiles.sh` bootstraps tools and links without requiring generated skills.
After shell initialization, `dots` completes agent provisioning through the existing updater.
The documented `just update-ca` route must also work without a preceding full sync.
Update `docs/setup.md` to explain both routes and remove obsolete lockfile-publication warnings.

### OpenSpec

Stop tracking `.agents/skills/openspec-*/`; ignore only generated OpenSpec-owned output.
Keep authored `openspec/` configuration, schemas, specifications, and changes tracked.
Retain the current repository-local generation target and shared discovery source.
Move generated-skill link reconciliation after successful generation in the updater.
Remove premature static links from `install.conf.yaml` so fresh clones cannot fail before generation.
Preserve native preview gating and fail visibly on unsupported or invalid output.
Verify missing-file regeneration against the installed CLI, not mocks alone.

### Adding shared skills

Make `docs/agent-skills.md` the canonical enrollment procedure for future sessions.
Add a focused reading trigger in the repository's `AGENTS.md`.
Link that procedure through existing shared skill-maintenance navigation where needed.
Agents obtain approval, record the source and skill name, then exercise installation for all three clients.
Sharing additions requires publishing the manifest through an explicitly authorized commit and push.
The other machine installs the published declaration on its next `dots` run.
Local-only experiments require neither enrollment nor changes to the shared manifest.

### Alternatives and recovery

Auto-committing generated files is acceptable debt, but retains unnecessary tracked state.
Pinned weekly upgrades provide stronger reproducibility but introduce an additional maintenance workflow.
Neither alternative is required for the selected automatic-update policy.
Machines can temporarily resolve different upstream versions between syncs.
This plan does not promise bit-for-bit installations across different update times.

Rollback restores the previous tracked files, mappings, updater, and documentation from Git.
Preserve local lockfiles before restoring links; restore links only when their tracked targets exist.
No automatic uninstall or deletion of unrelated local skills belongs to rollback.

## Capabilities

### New capabilities

- `shared-skill-reconciliation`: declarative enrollment, local state, migration,
  and cross-client delivery through `dots`.

Existing `harness-change-workflow` remains in an unarchived change, not the main specification tree.
This capability adds ownership and reconciliation requirements without rewriting that separate change.

## Impact

Affected implementation owners:

- `scripts/update-coding-agents/entrypoint.sh` and skill reconciliation helpers.
- `scripts/update-coding-agents/sync-openspec.py` and its isolated tests.
- `scripts/install-dotfiles.sh`, `install.conf.yaml`, and the pre-clean ownership guard.
- `.gitignore` and tracked skill state slated for migration.
- `docs/agent-skills.md`, relevant harness guides, `docs/tooling.md`, and `scripts/README.md`.
- Repository agent navigation and focused regression tests under `scripts/tests/`.

Keep `home/.zshrc`'s alias and `justfile`'s public sync entrypoint compatible.
The current alias already invokes the repository's `just sync` from the correct working directory.
Do not claim every existing `dots` integration becomes idempotent through this scoped change.

## Verification

- Exercise fresh and existing homes with different usernames and checkout paths.
- Exercise the actual alias-to-recipe chain with unrelated workstation mutations stubbed.
- Gate native update-call selection on unchanged-input evidence from isolated real CLI runs.
- Run real native skill and OpenSpec commands inside isolated homes and disposable checkouts.
- Test installer-only bootstrap, subsequent `dots`, and standalone `just update-ca` separately.
- Test unknown broken links before Dotbot cleanup, not just before the later updater.
- Test manifest loading without an installed manifest and from an unrelated working directory.
- Compare contents, timestamps, modes, and symlink targets across repeated fixed-input runs.
- Test missing client links, missing lockfiles, broken legacy links, conflicts, and interrupted updates.
- Confirm retries converge without duplicate backups, installs, or manifest entries.
- Confirm skill synchronization leaves tracked files unchanged and performs no Git publication.
- Confirm manifest additions appear on a second isolated machine through the same `dots` path.
- Run `python3 scripts/tests/test-agent-harness.py` and `python3 scripts/tests/test-openspec-sync.py`.
- Add `python3 scripts/tests/test-skill-sync.py` for migration, enrollment, and idempotency coverage.
- Run `just lint` and `git diff --check`; report unrelated failures without broad cleanup.
- Run `openspec validate separate-skill-intent-from-state --strict --no-interactive`.
- Run `openspec schema validate session-workflow`.

After implementation, use fresh dedicated Pi and Claude Code sessions through Herdr.
Select eligible models explicitly; do not reuse unrelated user sessions or reserved main-chat models.
Check discovered names and source paths, then exercise a harmless read-only skill invocation.
Check Cursor's native discovery surface separately; filesystem links alone do not prove loading.
Record installed, discovered, loaded, and exercised evidence separately for each client.
Lluvia's machine remains unverified until exercised there.
Isolated fixtures establish portability, not remote deployment.
Announce any real `dots` invocation before running it; fixtures are not workstation deployment.

## Approval

The user selected option 3, explicit enrollment, and all three client targets.
Herdr-based Pi and Claude Code checks are authorized within this task's verification scope.
The user explicitly approved implementation after the review revisions.
Approved scope includes isolated verification and announced workstation deployment through `dots`.
Commit, push, and archive operations still require separate approval.
