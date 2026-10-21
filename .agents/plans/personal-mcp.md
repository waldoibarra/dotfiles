# Personal MCP parity

## Current status

The personal Google Sheets MCP is retired at the user's request.
Its launcher, Dotbot mapping, dedicated tests, and setup guide are removed.
The installed launcher link and empty personal OAuth directories are removed.
No Sheets entry remains in the normal Claude, Pi, Cursor, or shared MCP configurations.
No personal token directory existed; no credential contents were read.
MCP and harness fixtures pass, with their opt-in checks skipped; repository lint passes.
Historical Sheets decisions and research below remain evidence, not instructions to reactivate it.
No Google authorization grant is revoked by local file removal.

## Outcome

Pi and Claude Code use one credential-free personal MCP source under `~/.agents/`.
Verify real public-documentation calls, not just configuration or process startup.
Work-only servers and project configurations are excluded.

Read this plan before continuing personal MCP setup or reviewing its verification evidence.
Read [the roadmap](/.agents/plans/ai-harness-roadmap.md) for the broader harness work.

## Decisions

| Id | Decision | Reason |
| --- | --- | --- |
| M1 | Superseded by M9: configure only the existing personal Context7 server. | Original scope excluded additional integrations. |
| M2 | Keep `home/.agents/mcp.json` as the canonical shared definition. | Both clients accept `mcpServers`; no second server definition or MCP extension is needed. |
| M3 | Link the source to `~/.agents/mcp.json` and Pi's native `mcp.json`. | Pi natively discovers its own path; links avoid copies. |
| M4 | Register missing canonical entries through `claude mcp add-json --scope user`. | Claude stores MCPs alongside private state in `~/.claude.json`; never replace or link that whole file. |
| M5 | Skip matching Claude entries; fail on conflicting definitions rather than overwriting them. | Preserve credentials, concurrent work, and unrelated user/project records. |
| M6 | Preserve pinned `@upstash/context7-mcp@2.2.5` and its existing stdio launch command. | Reuse the working configuration; no transport change, new account, or dependency upgrade is needed. |
| M7 | Use public library queries for live verification. | No private code, work data, or credentials should leave the machine during checks. |
| M8 | Document accepted decisions and handoff outcomes every session in existing scoped records. | Fresh sessions need durable context without duplicated logs or speculative automation. |
| M9 | Add personal Google Sheets access for Pi and Claude Code using the same MCP server. | The user requested spreadsheet improvements and charts from both agents. |
| M10 | Defer company Sheets configuration; keep personal and company access separate. | The user narrowed implementation to personal use. |
| M11 | Superseded by M15: use personal OAuth with `mcp-google-sheets==0.6.3`. | This implementation requires a user-owned OAuth client, rejected by the user. |
| M12 | Superseded by M17: use a personal launcher with a work-directory guard. | Native remote OAuth needs project scoping instead of a local process guard. |
| M13 | Superseded by M16: expose the local server's seven-tool allowlist. | Hosted Connect uses meta-tools; the selected app connection controls Google access. |
| M14 | Superseded by M16: pin `mcp==1.30.0` for the local server. | The remote endpoint removes this local runtime dependency. |
| M15 | Superseded by M22: require native `/mcp` browser sign-in without client JSON. | The user later accepted local open-source operation and its one-time OAuth setup. |
| M16 | Superseded by M19: configure Composio Connect for personal Sheets editing. | The user subsequently deferred Composio before implementation. |
| M17 | Deferred with M16: use a shared manifest in a dedicated personal project. | The replacement workflow stopped before any project configuration was created. |
| M18 | Leave Google consent and any account signup to the user through browser authentication. | Configuration approval does not authorize accepting paid terms or acting on Google data. |
| M19 | Defer Composio and identify the user's existing free MCP reference before proceeding. | The user explicitly redirected the task to an existing integration. |
| M20 | Superseded as recommendation by M21: trial Pipedream's free-signup MCP in this checkout. | The user subsequently required free, open-source software without metered connector usage. |
| M21 | Require a free, open-source Sheets MCP without hosted connector usage caps. | The user explicitly clarified this requirement; Google's API quotas still apply. |
| M22 | Restore the existing local Sheets server and remove the Pipedream project override. | The user accepted the local option and its one-time Google OAuth setup. |
| M23 | Add a personal-integration preflight and evidence-of-readiness rules to the shared harness. | The user authorized improvements after repeated provider changes and premature setup claims. |
| M24 | Commit this session's work separately from concurrent Lens changes. | The user explicitly requested commits while excluding pi-lens work. |

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

## Google Sheets extension: preparation

Personal Google Sheets setup is authorized; company configuration remains untouched.
The user selected personal OAuth and then confirmed Sheets-only scope.
The earlier service-account recommendation is superseded by that explicit selection.

Verified preparation:

- `mcp-google-sheets` 0.6.3 supports raw Sheets batch updates, including chart requests.
- Its OAuth flow requests full Sheets and Drive scopes; service-account access depends on file sharing.
- Missing or invalid service-account paths can fall back to OAuth or Application Default Credentials.
- An independent plan review recommends explicit credentials and fail-closed authentication before registration.
- The downloaded wheel matches PyPI's SHA256; its server source matches inspected upstream `main`.
- Preparation created no Sheets credentials, Google resources, or client registrations.

Read [upstream authentication documentation](https://github.com/xing5/mcp-google-sheets#-authentication--environment-variables-detailed)
before choosing authentication. Never copy its broad Project Editor recommendation.
Read [the server source](https://github.com/xing5/mcp-google-sheets/blob/main/src/mcp_google_sheets/server.py)
before implementing credential isolation; a configured folder is not an access boundary.

Implementation plan:

1. Independently review this OAuth plan before implementation.
2. Add the Python launcher `home/.local/bin/google-sheets-personal-mcp`; link it individually.
   Reject resolved startup directories under `~/projects/work` before reading credentials.
   Include symlinks in the guard. This is not a sandbox; changing directories retains connected tools.
3. Require Desktop OAuth client JSON at `~/.config/mcp-google-sheets/personal/client.json`.
   Store tokens at `~/.local/state/mcp-google-sheets/personal/token.json` with private permissions.
   Reject absent or malformed OAuth client configuration before launch; never print credentials.
4. Overwrite inherited `CREDENTIALS_CONFIG` and `SERVICE_ACCOUNT_PATH` with empty values.
   Set explicit OAuth paths and `GOOGLE_APPLICATION_CREDENTIALS=/dev/null`; ADC must fail closed.
   Clear inherited folder selection; fix the tool allowlist through command-line arguments.
5. Launch the pinned server over stdio with Python 3.12 and `--with mcp==1.30.0`.
   Allow only `get_sheet_data`, `get_sheet_formulas`, `list_sheets`, `update_cells`, `batch_update`,
   `create_spreadsheet`, and `copy_sheet`. Raw batch updates include destructive spreadsheet operations.
6. Add `google-sheets-personal` to the shared manifest; preserve Context7 and the registration adapter.
   Add tests first: missing/malformed OAuth, hostile inherited credentials, work-directory rejection,
   symlink rejection, exact launch command/environment, private state permissions, and Dotbot linkage.
7. Run isolated fixtures, package tool-discovery checks, and an independent implementation audit.
   Apply only the new Dotbot link and targeted Claude registration; never run a full workstation sync.
8. Document Desktop OAuth setup, full Sheets/Drive scopes, and testing-mode token expiration,
   one-client-at-a-time first login, startup guard limits, rollback, and incomplete live verification.
   Keep sign-in user-driven; do not create Google resources or inspect existing private credentials.
9. Verify both clients against a disposable personal spreadsheet after credentials become available.
   Chart creation needs write access; no real spreadsheet changes are authorized by configuration alone.

### Implementation verification

- Independent OAuth plan review passed on Astra before implementation.
- Luna implemented the bounded launcher, manifest entry, link, fixtures, and documentation.
- Main-session review caught unsupported environment names and a tool-filter flag in the first draft.
  Corrected fixtures failed twice before fixing the launcher to match the upstream contract.
- Package import failed with unconstrained MCP 2.x; the compatible SDK pin fixes that failure.
- Seven Sheets checks pass with `MCP_SHEETS_PACKAGE_CHECK=1`, including actual package inspection.
  Tool discovery exposes exactly seven allowed tools; ADC fails with the null-file override.
  Package checks do not start OAuth or call Google APIs.
- Existing MCP fixtures pass with one opt-in native test skipped; four harness fixtures pass.
- Isolated native Pi and Claude CLI checks preserve the work startup directory.
  Both reject the personal launcher under the temporary work root, without Google access.
- Live personal authentication, Google reads, and chart writes remain unverified.
  No private OAuth file has been inspected; user consent is still required.
- Independent implementation audit passed on Astra; no confirmed or plausible blockers remained.
- Main proposed a fix freeze; later enhancements belong to the next iteration.
- Applied only the launcher link through targeted Dotbot configuration; existing MCP links were preserved.
- Claude registration added one server and preserved Context7; the second adapter run made no changes.
- Installed executable, Pi shared link, and Claude user registration match the tracked configuration.
- Final checks pass: 17 tests, one opt-in native test skipped, `just lint`, and `git diff --check`.
- No full updater, workstation sync, company configuration change, or Google resource write occurred.
- Simultaneous token refresh remains unverified; upstream token writes are unsynchronized.

### Native sign-in replacement: pending provider approval

The user rejected manual OAuth JSON provisioning after installation. Do not continue that setup.
The local launcher and registrations remain installed until a replacement is selected and applied.

Independent research recommends Composio Connect at `https://connect.composio.dev/mcp`.
Main-session verification confirmed public OAuth discovery, dynamic registration, and PKCE metadata.
The Sheets catalog documents managed OAuth plus explicit chart creation and update tools.
Pipedream supports native browser sign-in, but its chart support remains unverified.

Official Google options were also checked:

- The earlier hosted-catalog check missed Google's official Sheets MCP preview guide.
  Read [the corrected investigation](/.agents/spikes/browser-access-and-google-oauth.md#correction-google-does-document-an-official-sheets-mcp)
  before revisiting first-party options; the documented preview still requires OAuth client setup.
- Its open-source Workspace extension registers only Sheets text, range, and metadata reads.
  It does not currently expose chart creation or spreadsheet editing tools.
- The Google Workspace CLI requires a Cloud project for OAuth and disclaims official product support.
- Composio remains the recommendation for native Sheets charts and managed sign-in across both clients.
  Use local Python for deeper statistical analysis; a separate analysis MCP is not required.

Read [Google's hosted catalog](https://docs.cloud.google.com/mcp/supported-products)
before revisiting official remote-server coverage.
Read [Workspace tool documentation](https://github.com/gemini-cli-extensions/workspace/blob/main/docs/index.md)
before assuming the official extension supports Sheets writes.

Read [Composio Connect](https://docs.composio.dev/docs/composio-connect) before configuring the endpoint.
Read [Sheets tools](https://docs.composio.dev/toolkits/googlesheets) before retrieving chart schemas.

Provider approval remains pending:

- Composio would handle Google authorization and process accessed spreadsheet data.
- The endpoint exposes general app-discovery and remote-execution tools, not a Sheets-only allowlist.
- Client login, exact consent scopes, retention, and Connect-specific pricing remain unverified.
- Native HTTP registration does not preserve the local launcher's work-directory startup guard.
  Resolve personal-session isolation before applying a replacement; do not silently remove that boundary.
- No Composio registration, authentication, account connection, or spreadsheet operation has occurred.

### Pricing and local-charting assessment

The user requested pricing, broader project uses, and cheaper alternatives; local charting is acceptable.
This is research authorization, not approval to purchase, connect another provider, or change the setup.

Verified published [Composio pricing](https://composio.dev/pricing):

- Hobby is $0, requires no card, and pauses at its limits.
- Managed OAuth apps receive up to 20,000 calls and 10,000 trigger events monthly within the free allowance.
- Pro is $29 monthly, including $29 usage credit; managed-call overage is $0.0005 per call.
- Own-app/API-key/MCP usage has 100,000 free calls; do not promise this for managed Google OAuth.
- Sandbox, proxy, Instant Tools, and other add-ons may introduce separate costs.
- How these platform allowances map to personal Connect remains unconfirmed in public documentation.

Published [retention](https://docs.composio.dev/docs/security/data-retention) includes tool payloads
for up to one year. [Managed-app ZDR](https://docs.composio.dev/docs/security/zero-data-retention)
is Enterprise-only; paying for Pro alone does not remove that concern.

Recommendation, not yet approved: use local Python and Plotly for analysis and interactive HTML charts.
Both agents can run the same scripts without an additional MCP or charting subscription.
Start from private CSV/XLSX exports; add a connector if live refresh justifies its cost and access.
Local processing avoids a connector processor, but model-visible data still reaches the model provider.
Local charts do not automatically become native Google Sheets charts or update the source spreadsheet.

Read [Plotly HTML export](https://plotly.com/python/interactive-html-export/)
before implementing offline interactive reports.
Pipedream advertises free MCP signup; consumer quotas remain unverified. Developer pricing is separate.
Google's Workspace extension is another potential read-only source; cross-client login remains untested.

Broader value: draft-first planning, GitHub workflows, and customer OAuth in SaaS prototypes.
SDK sessions, tenant authorization, tool policies, and webhooks are separate from personal Connect.
Do not treat trade-journal analysis as validated market-data or brokerage execution infrastructure.

### Deferred replacement plan: Sheets editing only

This plan was stopped before implementation after the user explicitly deferred Composio.
All three workflow steps returned without edits; no remote server was installed.
The requested reference connector remains unidentified; ask rather than substitute another provider.
Charting, company integration, and other app connections remain out of scope.

1. Independently review this replacement plan, then add failing project-scope fixtures.
2. Add `home/.agents/google-sheets.mcp.json` containing only `google-sheets-personal`:
   `type: http`, `url: https://connect.composio.dev/mcp`; no credentials, headers, or paid settings.
3. Dotbot links that source to both files inside `~/projects/personal/google-sheets`:
   `.mcp.json` for Claude Code and `.pi/mcp.json` for Pi. Global Context7 remains unchanged.
4. Remove the superseded global Sheets manifest entry, launcher, launcher link declaration,
   launcher-only tests, and launcher assertions. Preserve generic registration/link regression coverage.
5. Test both project paths resolve to one canonical file; no global manifest contains Sheets.
   Retain registration preservation, conflict handling, and harness tests. Run lint and diff checks.
6. Independently audit the source changes before applying only those two links through Dotbot.
   Refuse conflicting destinations. Do not run the full installer or updater.
7. Main inspects and removes only the old `google-sheets-personal` Claude user registration.
   Main removes only the verified old launcher symlink; never delete OAuth files or other private state.
8. Document starting either client from the personal workspace, trusting project configuration,
   using `/mcp` for authentication, then authorizing only Google Sheets when requested.
   Composio signup and Google consent remain user-driven; neither agent should enable paid services.
9. Verify configuration and OAuth discovery without registering OAuth clients or signing in.
   Authenticated tool availability and spreadsheet editing remain pending user login.

Limits to disclose: Composio is a hosted processor; Connect exposes general meta-tools.
Only Sheets should be connected for this workflow. There is no server-side Sheets-only guarantee here.
Published free-platform limits do not establish exact personal Connect quotas; never promise paid capacity.
Projects outside the personal workspace do not load this project manifest.
Reusing an already-running personal session in another directory is not an isolation boundary.

### Pi-only immediate trial

- The user prioritized testing Pi immediately; the supplied screenshot identified a Claude-hosted connector.
- Added `.pi/mcp.json` with a project override for `google-sheets-personal` at Pipedream's native endpoint.
- No paid account, OAuth registration, sign-in, or Google data operation was performed.
- Native Pi connection in an isolated profile reports `needs-auth`, confirming the OAuth entry point.
- Normal-profile Pi ignores this checkout's project MCP until the user grants project trust.
- The user must restart Pi here, accept trust, then use `/mcp` to sign in and connect only Sheets.
- Work and Claude configuration remain untouched. Composio and charting remain deferred.
- Exact free consumer quotas and authenticated editing remain unverified.
- This small configuration-only change was self-reviewed; no independent review was claimed.

### Free, open-source requirement clarified

The user now requires free, open-source software without metered connector usage.
Recommend the local MIT-licensed `mcp-google-sheets`, not Pipedream or Composio.
No paid connector or monthly tool-call allowance is involved; Google's API quotas still apply.
The documented personal OAuth path requires a one-time Google Cloud Desktop OAuth client setup.
Browser consent follows that setup; it is not native remote `/mcp` authentication.
This clarification did not change installed configuration or authorize Google resource creation.

### Authorized local restoration and harness improvement

The user accepted the local server and requested implementation, documentation, and harness improvements.
No further provider selection is needed. Personal OAuth consent remains a user action.

Implementation and verification:

1. Independently review this scope, then add a failing regression for conflicting project overrides.
2. Remove only `.pi/mcp.json`, the Pipedream override created during this session.
   Preserve the canonical global manifest, local executable link, SDK pin, and isolated credential paths.
3. Make missing-client errors name the expected path without displaying credential contents.
   Retain fake-launcher checks and the actual upstream package contract test.
4. Move the current local setup instructions into `docs/coding-agents/google-sheets.md`.
   Link the guide from the MCP overview and coding-agent index; remove obsolete trial instructions.
   State MIT licensing, no subscription, Google quotas, OAuth setup, scopes, and verification limits.
   Keep charts, hosted providers, work configuration, and new authentication frameworks out of scope.
5. Add a short personal/open-source integration rule under the existing shared Harness design section.
   Establish hosting, license, costs/quotas, authentication effort, operations, and client scope first.
   Check existing/first-party options, distinguish hosted account connectors from portable servers,
   and recommend one compatible option instead of installing successive mismatched alternatives.
   Ask only about unresolved constraints; existing answers carry forward.
   Verify actual interfaces; distinguish configuration, authentication, and successful operations.
6. Extend `docs/coding-agents/personal-workflow.md` with synthetic acceptance cases for those failures.
   Keep policy canonical in the shared instruction file. Do not encode a universal free-provider preference.
   The new behavior is personal/open-source scoped; no company policy adaptation is authorized.
7. Run the explicit checks below, followed by independent diff audit.
   Do not run normal-profile MCP connection checks, even if credentials appear absent.
   Check only OAuth file existence; never inspect real credential contents in the conversation.
8. Main verifies existing links and registration without full workstation sync or unrelated client changes.
   Prepare only the private personal credential directory if absent; do not create cloud resources.
9. Update outcome notes, preserving superseded decisions. No commit or push is requested.

Exact verification contract:

- Red: the project-override regression fails while the Pipedream override exists.
  The missing-client error regression fails until it includes the expected client path.
- Green: `python3 scripts/tests/test-personal-google-sheets.py`,
  `python3 scripts/tests/test-personal-mcp.py`, and `python3 scripts/tests/test-agent-harness.py` pass.
- `MCP_SHEETS_PACKAGE_CHECK=1 python3 scripts/tests/test-personal-google-sheets.py` passes
  with real upstream tool discovery and ADC rejection; it never starts OAuth or calls Google.
- `just lint`, `markdownlint-cli2 - < home/.agents/AGENTS.md`, and `git diff --check` pass.
- Main checks installed links and the named Claude registration as configuration only.
  Do not run normal-profile `pi mcp list` or `claude mcp get`, which connect servers.
- Main runs `pi mcp list --json` only with disposable `HOME` and `PI_CODING_AGENT_DIR`.
  Its temporary manifest contains only the actual local launcher, with an absolute command path.
  No credentials exist in that disposable home; run from its directory, not a real project.
  Expect the launcher transport and a missing-client error, no remote endpoint or browser flow.
  This proves native resolution and failure behavior, not authenticated spreadsheet access.
- Synthetic behavioral cases are documented and reviewed, not executed as fresh-session smoke tests.
  Report that limitation explicitly; do not infer behavior changes from instruction-file edits.

Harness evidence and acceptance:

- Provider churn followed missing upfront cost, hosting, and authentication constraints.
  The new preflight must preserve already supplied answers and require only unresolved decisions.
- Fake fixtures mirrored incorrect upstream names; the actual package check caught SDK incompatibility.
  Compatibility claims must include real-interface evidence rather than fake-only tests.
- Connection states were repeatedly mistaken for usable access during handoff.
  A `needs-auth` result must be reported as awaiting login, never working spreadsheet editing.
- Read-only access does not satisfy editing requirements.
  Hosted account connectors need provenance checks.
- Rollback: revert only the new shared instruction paragraph and its smoke cases; restart the agents.
  No hooks, new roles, recurring logs, automatic learning, or model/billing changes are needed.

### Restoration outcome

- Independent plan review found verification ambiguity; isolated checks resolved it.
- Astra was selected because earlier drafts required upstream-contract corrections.
- The implementer hit the provider usage limit before changing files; the final audit did not run.
- After the user requested continuation, main completed the work and self-reviewed it.
  Final review is not independent review; no provider, privileges, or billing route was changed.
- Both new regressions failed before fixes: project override shadowing and missing credential-path guidance.
- Removed the Pipedream project override and retained the local server, SDK pin, and credential isolation.
- Added the dedicated Sheets guide and linked it from the MCP overview and coding-agent index.
- Added seven lines to shared instructions, restricted to personal/open-source integrations.
  The file grew from 134 to 141 lines; the missing integration criteria are covered.
- Added cases for constraints, editing capability, connector provenance, and verification states.
  These cases were reviewed, not executed in fresh agent sessions.
- Final suites pass: eight Sheets checks, six registration/link checks, and four harness checks.
  The opt-in native concurrent-registration test remains skipped.
- The actual package contract check confirms seven allowed tools and fail-closed ADC behavior.
- `just lint`, explicit global-instruction Markdown lint, and `git diff --check` pass.
- Native Pi in a disposable profile resolves the actual local launcher and rejects missing credentials.
  No real OAuth flow or Google API call was made during verification.
- Installed links, executable, Claude registration, and instruction wiring match their sources.
- Prepared the private OAuth directory; `client.json` is absent. No credential contents were read.
- No workstation sync, company configuration change, commit, push, or writing-style profile was created.

### Browser investigation follow-up

The user requested research on browser MCPs, course/media study, TODO coverage, and simpler Google sign-in.
Read [Browser access and Google sign-in](/.agents/spikes/browser-access-and-google-oauth.md)
before approving a pilot. It recommends Playwright MCP's extension, with Chrome DevTools as a fallback.
Browser session reuse is explicitly distinguished from native remote OAuth.
No integration, authentication, or work configuration changed during that research.

### OAuth onboarding blocker

The user reports required app links and verification prompts, and rejects the setup effort.
The exact console state remains unknown; general testing exemptions do not resolve that observed blocker.
Do not continue insisting that the fields are optional or imply the integration is authenticated.

Alternatives under discussion, not approved:

- Recommended: the same local MCP with a service account and explicitly shared spreadsheets.
  It avoids the OAuth consent-screen flow but still requires a service-account JSON key.
  Do not grant project-wide Editor access for ordinary spreadsheet editing.
- Browser MCP: use a signed-in browser to edit Sheets through its UI instead of the Google API.
  This avoids Cloud OAuth setup, but introduces broader browser access and UI reliability limits.

No authentication mode or configuration has changed in response to the alternatives question.

### Commit handoff

- Sheets setup committed as `8138b97`; harness guidance committed separately as `cbe299c`.
- Browser research and this decision record form a separate documentation change.
- The staged Sheets snapshot passed offline tests and full lint without including Lens changes.
- Lens files and the Lens-only workspace-index row remain outside this session's commits.
- No push, browser installation, or Google authentication was requested or performed during committing.

## Next session

Continue only active personal MCP verification. Sheets reactivation requires a new explicit request.
Historical setup paths and commands above refer to removed artifacts.
