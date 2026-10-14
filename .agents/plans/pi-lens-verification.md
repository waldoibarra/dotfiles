<!-- markdownlint-disable MD013 -->
# Lens verification current record

Read [current delivery status](/.agents/plans/pi-lens-delivery.md) before changing scope.
Read [verification history](/.agents/plans/history/pi-lens-verification-2026-10-13.md) before reusing earlier results.
Archived results retain their original context; they do not override this checkpoint.

## Released and installed

| Product | Release commit | Verified state |
| --- | --- | --- |
| Pi Lens 0.2.0 | `237e3c561ba68e3e77c3f18d7613c3e45756e0ae` | Published; normal-profile checkout read back; discovery/views/reload passed on Pi 1.2.0 |
| Claude Lens 0.1.2 | `1420f37cf82cb1290707fdcf652a22c9435f91f2` | Published; normal plugin list reports enabled; marketplace ref is v0.1.2 |

- Pi: 192 tests, full checks, direct/batch terminal fixtures in both modes, and model-visible baseline equivalence passed.
- Pi 1.2.0 image fixture passed fullscreen; regular image mouse interaction remains explicitly unverified.
- Compiled development host provenance fixture passed both modes; development host reports 1.1.0.
- Claude: 29 engine tests, validation, typecheck, lint, and release CI passed on Claude Code 2.1.296.
- Fresh isolated installs passed for both published versions before normal-profile upgrades.
- Normal Pi discovery/views/reload passed both modes after its targeted upgrade; no prompt reached a provider.
- Old Claude identity remains disabled; unrelated marketplaces remain registered.
- No host upgrade, credential copy, `dots`, or live microphone session ran.

## Harness follow-through

Independent audit passed the worker implementation; lead inspection corrected additional gaps before acceptance.
Corrections scoped positional arguments to one recipe, selected the intended compiled SDK explicitly,
added fixture cleanup, completed native-cwd dispatch guidance, and fixed current-state/link inaccuracies.

| Target | Evidence / limit |
| --- | --- |
| Default persistence and CLI passthrough | Fake-Node recipe tests verify exact argv, spaces, shell metacharacters, cwd, and missing-file guards |
| Compiled-host persistence/resume | Selected host's `SessionManager` writes and reopens a synthetic session; memory mode selects no file |
| Fixture isolation | Temporary session directory removed in `finally`; no provider or subprocess session starts |
| Repository guard | Documented shell guard exercised in correct and wrong disposable Git roots |
| Acceptance and routing guidance | Source-reviewed matrix and bounded task packet; no fresh model-behavior enforcement claim |
| Historical preservation | Byte comparisons against prior Git records; delivery additionally retains approved follow-through |

Lead checks: 11 harness tests passed with the local compiled package selected.
The source-only default run skips the optional compiled-host check instead of requiring a workstation checkout.
Lead full lint, diff checks, changed-document links/anchors, and dry-run ShellCheck passed.
The actual updated development recipe loaded all three extensions and exposed voice flags through `--help` offline.
This proves launch/registration, not a live microphone connection or provider session.
The initial independent audit preceded the lead's corrections; those focused corrections received lead self-review.
No new product release is required for these harness changes.

## Repeat the verified checks

From dotfiles:

```sh
PI_PACKAGE_DIR="$HOME/projects/personal/pi/packages/coding-agent" \
  python3 scripts/tests/test-agent-harness.py
PI_PACKAGE_DIR="$HOME/projects/personal/pi/packages/coding-agent" \
  node scripts/tests/check-pi-session-persistence.mjs
just --dry-run pi-lens-dev 2>&1 | shellcheck --shell=sh -
just lint
```

To recheck normal-profile Pi discovery without a provider request:

```sh
cd "$HOME/projects/personal/pi-lens"
python3 tests/installed-smoke.py --profile "$HOME/.pi/agent" --expected-version 1.2.0
```

Native Claude `plugin list --json` establishes installation/enabled state, not physical TUI rendering.
Read [development launch](/docs/tooling.md#develop-lens-locally) before testing resume or live voice.
Existing ephemeral processes are not retroactively persisted by changing the launcher.

## Archive integrity

| Archive | SHA-256 |
| --- | --- |
| `history/pi-lens-delivery-2026-10-13.md` | `12f1a82421927bdcf5bb15217d2ac8ff3893d7679b30aa40e7a2121bbc5483c0` |
| `history/pi-lens-verification-2026-10-13.md` | `2b7943c8e2094773aa62a15b49d95ef07216354ed3c5025288cada4c7c0375aa` |

Delivery history preserves all 138 distinct IDs D1–D138 and their original superseded markings.
Lead compared prior committed delivery bytes after excluding the added approval section; they match exactly.
Verification history is byte-identical to its prior committed record.
Old links may point into these archives; never interpret a historical 'current' heading as today's status.
