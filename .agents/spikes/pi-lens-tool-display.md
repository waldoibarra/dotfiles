# Lens-style tool display in Pi

## Current package recheck

Read this comparison before installing a substitute for the current Lens work.
Published Pi remains 1.1.0.
Registry metadata and these package artifacts were rechecked without installation.

| Candidate | Verified mismatch |
| --- | --- |
| `pi-compact-tools@0.15.0` | Claude style groups exploratory tools; commands and edits retain separate rows. This differs from Lens mixed-run folds. |
| `@prjct.app/pi-clipboard@0.1.10` | Identifies clipboard images by temporary filename patterns; previews drafts and deletes previewed files at shutdown. |
| `@pi-archimedes/image-paste@2.10.4` | Matches visible marker text, transforms submitted input into image blocks, and resets its queue on session start. |
| `pi-wait@0.1.5` | `/wait now` still uses follow-up delivery while busy; it cannot transfer current work into the background. |

No inspected candidate exactly satisfies the relevant preservation, identity, and delivery requirements.
No package was installed or executed. This is a bounded comparison, not an exhaustive ecosystem claim.

Sources: published package READMEs; image-paste `src/index.ts` marker matching/input transformation;
pi-wait `index.ts` delivery branch.
The clipboard preview package explicitly documents its filename heuristic.
Read [Pi Compact Tools](https://github.com/nedleeds/pi-compact-tools)
before considering its alternate styles.
Read [Pi Clipboard](https://github.com/prjct-app/pi-clipboard) before evaluating draft-only previews.
Read [Archimedes image-paste](https://github.com/danielcherubini/pi-archimedes)
before considering its input transformation.
Read [Pi Wait](https://github.com/brettinternet/pi-extensions/tree/main/extensions/wait)
before scheduling delayed prompts.

Native Pi all-message steering already addresses the queued-message batch boundary.
No additional package is needed.
Host activation, exact clipboard identity, and immediate send-now remain separate concerns.

## Historical recommendation

The user subsequently chose a standalone Pi Lens sibling. The original recommendation below is superseded.
Read `.agents/plan.md` in the local `pi-lens` checkout before continuing implementation.
The local Pi Lens checkout owns the cross-repository completion list and verification results.
Public GitHub source is authorized. Package publication awaits local validation.
Dotfiles declares no Pi Lens package yet.

The original recommendation was to trial **`pi-compact-tools@0.14.2` in Claude style**, with silent
mode disabled, before building anything.

It already groups reads and searches, preserves visible failures, and supports expansion.
Custom work remains justified for Lens's mixed-tool folds and failure-preserving clean view.

**Spike status:** source-backed research; no installation, configuration changes, or interactive test
occurred during this spike. Later implementation and local trials are tracked in the sibling repository.

## Scope and evidence

- Inspected Lens at commit `ca16172`; its working tree was clean.
- Inspected Pi `1.1.0` documentation, renderer declarations, example, and default expansion binding.
- Searched npm and GitHub; downloaded four published packages into a temporary inspection directory.
- Reviewed documentation and selected implementations; this was not a comprehensive security audit.
- No model calls, package lifecycle scripts, or third-party extension execution were needed.
- No independent sub-agent review was available through this session's tools.

Read [Lens's implementation](https://github.com/waldoibarra/claude-code-lens/blob/ca16172/hooks/register.tsx)
before porting its behavior.
Read [Pi's extension contracts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md)
before implementation; the locally installed `1.1.0` documentation supplied the version-specific evidence.

## What Lens does

Lens changes presentation, not tool execution, stored conversation content, or model context.

| Feature | Observed implementation |
| --- | --- |
| Normal view | Counts each consecutive tool run, showing five steps before an expandable remainder |
| Clean view | Shows the run's step count and latest failure; details expand on demand |
| Raw view | Delegates rendering to Claude Code |
| Run boundaries | Assistant prose separates runs; mixed tool kinds can share a fold |
| Labels | Human-readable actions, result facts, and categorized errors |
| Expansion | Commands, output, and edit diffs appear in place |
| Additional chrome | Message timestamps, model labels, answered questions, current activity, and delegated-agent models |
| State limits | Last 600 steps; detailed output for 150; 400 message stamps |
| Resume limit | Earlier unrecorded steps fall back to individual rows |

The pure formatting helpers in `hooks/lens.ts` are reusable candidates.
The Claude-specific hooks, atoms, and JSX rendering require replacement.

## Existing packages

Versions below are the published artifacts inspected, not unversioned compatibility promises.

| Package | Relevant behavior | Limitation |
| --- | --- | --- |
| [`pi-compact-tools@0.14.2`](https://github.com/nedleeds/pi-compact-tools) | Compact, Claude, and Codex styles; exploratory grouping; expansion; custom tools | Grouping uses internal UI adapters; silent mode hides errors and warnings |
| [`pi-compact-transcript@0.11.1`](https://github.com/avhagedorn/pi-compact-transcript) | One-line previews; repeated-tool coalescing; visible failures; end-of-run counts | Prototype patches; commentary restyling; no exact Lens normal/clean/raw modes |
| [`@pi-kaush/pi-tool-call-markers@0.3.17`](https://github.com/kaushikgopal/pi-kaush/tree/main/extensions/pi-tool-call-markers) | Compact mixed-tool rows; grouping; question blocks; subagent presentation | Prototype adapters; bundled thinking changes; prose-only toggle hides tools entirely |
| [`@nicknisi/pi-compact-tools@0.1.1`](https://github.com/nicknisi/pi-extensions/tree/main/packages/compact-tools) | Two-line cards; native expansion; error preview | No run-count folding; private component wrapping |

### Why the first candidate wins

Its source uses `registerToolRenderer` when available, without replacing tool execution or declarations.
Its manifest supports Pi `>=0.85.1`; its documentation describes Pi `1.1.0` behavior and CI coverage.
Those compatibility claims remain upstream claims until an interactive trial succeeds here.

Read `extensions/compact-tools.ts` before evaluating renderer routing.
Read `extensions/compact-tools-grouping.ts` before relying on grouped failure visibility.
Read `extensions/compact-tools-silent.ts` before enabling silent mode.

The silent implementation returns no tool rows, including failures.
It also suppresses intermediate assistant turns, extension notices, and host warnings and errors.
That differs materially from Lens clean mode, which retains failure information.

Some alternatives claim Pi lacks public global tool rendering. That is outdated for Pi `1.1.0`.
Transcript grouping still lacks an equivalent documented public integration point.

## What Pi supports

The installed declarations expose:

- `pi.registerToolRenderer()` handles built-in, extension, and unknown tools.
- `renderCall`, `renderResult`, and `renderShell: "self"` for compact row presentation.
- Render context containing `toolCallId`, arguments, expansion, errors, duration, padding, and invalidation.
- `next()` for renderer composition without re-registering tools.
- `ctx.ui.setToolsExpanded()`; native `Ctrl+O` toggles tool expansion.
- Fullscreen mouse input; regular terminal mode needs keyboard interaction.
- Session-branch access for reconstructing state after resume or navigation.

**Display compaction is not context compaction.** Model-visible results should remain unchanged.
The existing `compaction` settings solve a different problem.

The `built-in-tool-renderer.ts` example re-registers tools and contains an outdated shortcut comment.
Prefer the newer renderer resolver and installed keybinding declarations over copying that example literally.

### Custom extension feasibility

| Desired behavior | Approach | Confidence |
| --- | --- | --- |
| One compact row per tool | Public renderer resolver; self-managed shell | Supported API |
| Plain labels and persistent failure previews | Port pure formatters; inspect renderer error state | Supported API |
| Expanded original details | Delegate to saved downstream renderers; supply fallback when absent | Supported API; needs testing |
| Activity label | UI working-message/status APIs | Feasible; needs integration testing |
| All adjacent tool kinds folded together | Cross-row bookkeeping and transcript-layout integration | Prototype demonstrated by packages; private integration risk |
| Labels beneath native user/assistant messages | Native message-component adapter | No equivalent documented public hook found |
| Exact clean/normal/raw redraw | Shared display state plus invalidation and grouping integration | Feasible, but not a trivial renderer-only port |

A public-API-only first version should compact individual tools and always retain failures.
Treat mixed-run aggregation and message decorations as a separate, higher-maintenance scope.
Never shrink tool results through `tool_result` or `context` merely to change the screen.

## Proposed trial

This is a recommendation, not an executed setup change.

1. Launch a disposable profile with only the pinned package and synthetic session data.
2. Compare Compact and Claude styles; leave silent mode off.
3. Exercise two reads, a successful command, a failed command, an edit, and a custom tool.
4. Check individual fullscreen clicks and global `Ctrl+O` expansion.
5. Verify streaming, cancellation, narrow widths, resizing, reload, resume, and theme changes.
6. Compare model-visible tool declarations and results against the baseline.
7. Repeat with `pi-live-codex`; check shortcut, widget, and renderer interactions.

A one-invocation package trial is supported:

```sh
pi -e npm:pi-compact-tools@0.14.2
```

That avoids adding a package declaration, but package commands can still persist their own configuration.
Use an isolated profile for the trial; `/compact-tools claude` saves style preferences.

**Acceptance:** readable replies, compact calls, visible failures, recoverable details, and unchanged
execution semantics.

## Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| D1 | Evaluate display-only changes | Matches Lens and the requested reduction in visual noise |
| D2 | Superseded: trial the existing package first | User later selected a custom sibling |
| D3 | Keep silent mode off | It hides failures and host warnings |
| D4 | Prefer public renderer APIs for custom work | Avoids replacing tools and reduces host-version coupling |
| D5 | Superseded: defer exact transcript-wide parity | User later requested closest supported sibling parity |
| D6 | Historical: leave the workstation unchanged during research | The spike did not authorize installation |
| D7 | Build standalone Pi Lens, with Pi prioritized | User selected a reusable sibling and Pi as the main agent |
| D8 | Commit verified work; publish packages after local validation | Source-only GitHub push is separately authorized |

## Unknowns at the original research checkpoint

- Actual rendering and performance in Waldo's terminal and current session shape.
- Coexistence with `pi-live-codex` and future delegation packages.
- Whether exploratory grouping is sufficient, or Lens-style mixed-run counts are essential.
- Whether upstream would accept a failure-preserving clean mode, avoiding a separate maintained package.
