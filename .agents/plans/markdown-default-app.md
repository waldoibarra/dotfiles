# Markdown default application

## Outcome

Open local Markdown documents with Cursor through macOS's user-wide file association.
Keep the desired association in dotfiles, not a copy of the LaunchServices database.

## Decisions

| Id | Decision | Reason |
| --- | --- | --- |
| F1 | **Retained via F9:** use Homebrew `duti` on macOS. | A consent prompt was pending; failure of duti was not established. |
| F2 | **Retained via F9:** store one mapping in `home/.config/duti/markdown.duti`. | One canonical bundle ID and no generalized association framework. |
| F3 | Link the mapping and apply it after OS package installation. | Homebrew owns both Cursor and duti. |
| F4 | Resolve the configured app through LaunchServices before applying. | Skip unavailable apps without hardcoding application installation paths. |
| F5 | Apply only the targeted package, link, and script in this session. | Full sync could upgrade, prune, or publish unrelated concurrent work. |
| F6 | **Retained via F9:** give the Dotbot command a Homebrew PATH prefix. | Package-install subprocess PATH changes do not reach later Dotbot commands. |
| F7 | **Superseded by F9:** native asynchronous Swift setter investigated. | Proposed after a premature duti-failure diagnosis; not shipped. |
| F8 | **Superseded by F9:** native JSON mapping proposed. | Not implemented; consent evidence removed the reason for changing mechanisms. |
| F9 | Retain duti; check before setting, verify afterward, and never automatically retry. | Waldo saw multiple macOS consent prompts and approved them; setter success alone is not effective-state evidence. |

The user approved implementation after being told this changes all Markdown files, not just Pi.
The pre-change `duti -x md` query reported Antigravity (`com.google.antigravity`).
Cursor's installed bundle ID is `com.todesktop.230313mzl4w4u92`.

## Implementation and checks

1. Add macOS-only duti, a single-row mapping, and a guarded Bash script with ShellCheck coverage.
2. Read the mapping's bundle ID; resolve the app through JXA without launching it.
3. Skip non-macOS or an unavailable app. Fail on missing config/duti and on query/application errors.
4. Check the handler first. If already selected, make no request; otherwise request once and verify.
   If not yet active, report pending/unsatisfied state and require responding to any macOS prompt.
5. Test guards, no-op repeats, pending consent, and error propagation with fake commands.
   Exercise the selected installer command with a restricted PATH to verify bootstrap wiring.
6. Document operation/recovery and commit only this session's changes.

Read [tooling](/docs/tooling.md) before running workstation commands.
Read [scripts](/scripts/README.md) before changing installer wiring.

## Progress and handoff

- Installed `duti` 1.5.4_1 using targeted Homebrew installation without auto-update or cleanup.
- Native app lookup returned true for Cursor and false for a nonexistent bundle, without launching either.
- Independent plan review flagged bootstrap PATH and ShellCheck coverage; both were addressed.
- Seven regression tests added; six fail before implementation.
- Duti returned success before the OS handler changed; repeated setter requests caused repeated prompts.
- Waldo supplied a screenshot of the macOS consent dialog and reported choosing Cursor on every prompt.
  The dialog covers both `.md` and `.markdown`; no screenshot is committed.
- A native Swift setter was explored outside Git, but individual setter effects cannot be separated.
  The earlier claim that duti failed was premature; retain the simpler duti configuration.
- Read-only queries now report Cursor for `.md` and `.markdown`; `.txt` remains unchanged.
- Before/after checks prevent repeated requests and false success while approval is pending.
- Ten isolated regression tests pass; pending approval issues exactly one request and fails visibly.
- Both default Bash and system Bash return the no-change result when Cursor is already selected.
- Independent audit found one issue: failed handler reads could trigger requests or imply pending consent.
  Read failures now propagate without that fallback; dedicated precheck/postcheck regressions pass.
- Repository lint and the existing harness/MCP regression suites pass.
- The selected Dotbot step also succeeds with restricted PATH and reports no change requested.
- Retired-harness cleanup: `e755550`. Historical-guide reference repair: `fbe948a`.
- Markdown configuration is installed; concurrent `pi-lens` changes remain excluded.
- Manual link-click verification remains a user check; CLI queries cannot prove terminal-specific behavior.
