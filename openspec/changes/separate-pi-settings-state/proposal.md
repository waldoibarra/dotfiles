# Proposal

## Why

Pi writes changelog state through a tracked settings symlink after upgrades.
Separate portable defaults from writable state so routine updates do not require commits.

## What Changes

Replace the settings symlink with a local JSON file, merged before package reconciliation.
Keep other Pi files linked and preserve unrelated local settings.
Document future settings edits through the existing Pi configuration reading route.

## Approach and tradeoffs

| Decision | Choice | Reason |
| --- | --- | --- |
| D1 | Tracked top-level keys replace matching local values | Nested deletions and package removals propagate without duplicate declarations. |
| D2 | Unspecified top-level keys remain local | Preserve runtime state and local preferences without enumerating Pi internals. |
| D3 | Atomic replacement under Pi's settings lock | Avoid writing through the old symlink or colliding with native settings writes. |
| D4 | Keep procedures in the Pi configuration guide | Existing entrypoints provide progressive disclosure without expanding global instructions. |

Removing an entire tracked key relinquishes ownership; explicitly remove its local value when
resetting to upstream defaults.
A full copy would erase runtime state; Git ignore flags would conceal intentional preference
changes.
Rollback requires saving local settings before restoring the old link and delivery configuration.
No packages, authentication, shared policy, or unrelated client behavior changes.

## Capabilities

### New Capabilities

- `pi-settings-delivery`: merge tracked defaults into local writable settings without repository
  churn.

### Modified Capabilities

None.

## Impact

Changes affect Dotbot settings delivery, the coding-agent updater, isolated tests, and maintained
Pi guides.
The targeted sync command also supports settings-only delivery without package upgrades.
Existing source content remains unchanged during link migration, preserving the current changelog
marker locally.

## Verification

Test fresh setup, migration, local-state preservation, managed replacements, repeat-run metadata,
malformed input, locks, and failure recovery.
Run repository lint, focused settings tests, and the existing harness suite.
Inspect documentation routes from repository instructions to the canonical editing procedure.
Do not claim fresh-agent compliance from static navigation checks.

## Approval

The user approved the recommended separation and requested documented fresh-session editing
guidance: “Go do it.”
Implementation includes targeted local migration, not a full workstation sync or Git publication.
