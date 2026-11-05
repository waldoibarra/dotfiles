# Proposal

## Why

Provision Cursor Agent CLI and Herdr integration through tracked dotfiles instead of manual
installation.

## What Changes

Declare Cursor CLI through Mise and reconcile its native Herdr hook during coding-agent updates.
Add isolated regression tests and operational documentation.
Install only the approved CLI and hook locally; preserve unrelated working changes.

## Approach and tradeoffs

| ID | Decision | Reason |
| --- | --- | --- |
| D1 | Use Mise `cursor-agent = "latest"` | Matches existing CLI ownership and supports macOS and Linux. |
| D2 | Reuse Herdr's native installer | Avoids maintaining generated hooks or tracking machine-local settings. |
| D3 | Keep authentication manual | Credentials and account consent remain local. |

Homebrew's `cursor-cli` cask also supplies the required executable, but creates another CLI
package owner.
The Mise registry downloads Cursor's official archive through its HTTP backend.
Rollback removes the declaration and calls `herdr integration uninstall cursor`; credentials
remain untouched.

## Capabilities

- `cursor-herdr`: declarative CLI provisioning and repeat-safe native hook reconciliation.

## Impact

Touch the global Mise declaration, coding-agent updater, isolated tests, integrations guide,
and workspace index.
Generated Cursor hooks remain local, including when `CURSOR_CONFIG_DIR` overrides their directory.
Do not run full workstation sync, change other integrations, or push commits.

## Verification

Check missing prerequisites, first installation, outdated hooks, repeat runs, and retry after
failure in isolated fixtures.
Run repository lint and the existing harness and Cursor suites.
Verify the installed CLI version and native integration status locally.
Authentication and an authenticated Herdr session remain manual follow-up unless already available.

## Approval

The user approved the presented scope and targeted local installation: "Go, commit when done."
This artifact records that agreement without changing its scope.
