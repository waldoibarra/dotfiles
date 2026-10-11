# Personal MCP parity

## Outcome

Pi and Claude Code use one credential-free personal MCP source under `~/.agents/`.
Verify real public-documentation calls, not just configuration or process startup.
Work-only servers and project configurations are excluded.

Read this plan before continuing personal MCP setup or reviewing its verification evidence.
Read [the roadmap](/.agents/plans/ai-harness-roadmap.md) for the broader harness work.

## Decisions

| Id | Decision | Reason |
| --- | --- | --- |
| M1 | Configure only the existing personal Context7 server. | The user-level registry contains Context7 only; no extra integrations are required. |
| M2 | Keep `home/.agents/mcp.json` as the canonical shared definition. | Both clients accept `mcpServers`; no second server definition or MCP extension is needed. |
| M3 | Link the source to `~/.agents/mcp.json` and Pi's native `mcp.json`. | Pi natively discovers its own path; links avoid copies. |
| M4 | Register missing canonical entries through `claude mcp add-json --scope user`. | Claude stores MCPs alongside private state in `~/.claude.json`; never replace or link that whole file. |
| M5 | Skip matching Claude entries; fail on conflicting definitions rather than overwriting them. | Preserve credentials, concurrent work, and unrelated user/project records. |
| M6 | Preserve pinned `@upstash/context7-mcp@2.2.5` and its existing stdio launch command. | Reuse the working configuration; no transport change, new account, or dependency upgrade is needed. |
| M7 | Use public library queries for live verification. | No private code, work data, or credentials should leave the machine during checks. |
| M8 | Document accepted decisions and handoff outcomes every session in existing scoped records. | Fresh sessions need durable context without duplicated logs or speculative automation. |

## Scope and implementation

1. Independently review the plan; add failing tests for links and safe native registration.
2. Add the shared manifest, Dotbot links, and a small Claude registration adapter in the existing updater.
3. Record the session improvement loop in shared global instructions.
4. Apply a temporary Dotbot config containing only the two MCP links.
   Run `python3 scripts/update-coding-agents/sync-personal-mcp.py` for registration only.
   Do not run the full updater, installer shell directives, or workstation upgrades.
5. Verify both clients and audit against this plan; update maintained docs and commit scoped changes.

No company-server migration, new MCP server, credentials, transport framework, or custom Pi MCP extension.
Subagent MCP access remains explicit and role-scoped; do not grant every child every server.

## Verification

- `python3 scripts/tests/test-personal-mcp.py`: missing/matching/conflicting/malformed/failure fixtures.
  Matching entries cause zero writes; malformed/conflicting input causes zero native calls.
  Isolated Dotbot `--only create link` checks shared and Pi paths resolve to identical tracked bytes.
- Preserve unrelated user/project records and ignore inherited alternate Claude configuration directories.
- Real `claude mcp get context7` and `pi mcp list --json` outside work projects.
- Real resolve-library-id and query-docs calls against public React documentation in each client.
- `python3 scripts/update-coding-agents/sync-personal-mcp.py`: matching installed entry is a no-op.
- `python3 scripts/tests/test-agent-harness.py` and `just lint` remain green.
- Native Claude concurrent-registration fixture uses a disposable home and preserves unrelated records.
  This establishes observed client behavior, not a lock guarantee against every competing writer.
- Capture private runtime output outside Git; publish only sanitized outcomes.

## Recovery

Remove only the managed Pi/shared links or revert their source configuration to disable Pi MCP.
A newly created Claude user entry can be removed by exact name after inspecting its scope.
The adapter never removes existing entries or imports project configuration.
Inspect conflicting user entries manually; do not force replacement during sync.

## Progress

- Pi 1.1.0 and Claude Code 2.1.296 inspected.
- Existing Context7 configuration is credential-free; no Pi MCP configuration exists yet.
- User reports the shared subagent setup works in a separate session; exact test steps were not recorded.
- Independent plan review completed on Astra; targeted application and executable tests clarified.
- The review's suggestion to defer the improvement loop was rejected: Waldo explicitly requested it.
  Record that policy in a separate atomic commit from MCP provisioning.
- Six regression tests added; five fail before implementation. The malformed-input test needs the adapter.
- Implementation delegated to Luna; main session reviewed configuration and corrected legacy SSE validation.
- Seven tests pass, including concurrent native Claude additions in a disposable home.
  Both additions and unrelated fixture records survived; tests never touched normal-home configuration.
- Existing four harness tests pass.
  Real registration ran twice: zero additions, one unchanged entry each time.
- Both links were applied through MCP-only Dotbot configuration; no full updater or `dots` ran.
- Pi and Claude both report Context7 connected. Pi exposes `resolve-library-id` and `query-docs`.
- Both clients resolved `/reactjs/react.dev` and returned useState documentation through MCP calls.
  Pi tool events and Claude tool-result blocks confirm success; neither test relied on model memory.
- Claude live calls used the shared manifest with strict MCP selection to exclude unrelated services.
  Its native user registration was checked separately with `claude mcp get context7`.
- A normal-profile Pi session completed a real Context7 lookup with all normal extensions loaded.
- Private health and tool-event logs remain under temporary paths, outside Git.
- Independent read-only audit on Astra returned **pass**.
- `just lint`, explicit global-instruction Markdown lint, and `git diff --check` pass.
- Both regression suites pass against the staged tree; its opt-in native case is skipped.
- The session learning policy is committed separately as `7fa72f0`.
- MCP configuration is installed and verified; this plan preserves the fresh-session handoff.
- No work-only MCP configuration, credentials, other-agent changes, or pending cleanup were included.

## Next session

1. Start a fresh Pi session and inspect `/mcp`; Context7 should be connected.
2. Read [personal MCP setup](/docs/coding-agents/mcp.md) before extending the personal server list.
3. Keep work-only MCP migration deferred; the roadmap's work-MCP decision remains open.
4. Record accepted decisions and handoff results in scoped records.
   Propose behavioral improvements before applying them.
