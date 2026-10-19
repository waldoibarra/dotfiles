# Browser access, media study, and Google sign-in

## Recommendation for review

**Trial Microsoft Playwright MCP with its official browser extension first.**
Use one personal Chrome profile, manual website login, and explicit connection approval.
The same server package can run under Pi and Claude Code's native stdio support.
Actual browser compatibility and Google Sheets editing still need a user-approved pilot.

**Keep Chrome DevTools MCP as the second choice for browser debugging and performance work.**
Its automatic connection is convenient, but exposes every open window in the selected profile.
Playwright's documented tab selection and per-client tab groups better fit private courses and two
agents.
This is a source-based recommendation, not a measured performance comparison.

**Browser session reuse is not native `/mcp` OAuth.**
It avoids creating a Google Cloud OAuth app because you sign into the website normally.
A universal, free, open-source Sheets API connector with managed OAuth remains unverified.
Do not present browser automation as that missing API connector.

Read the [existing media spike](/.agents/spikes/pi-media-learning-and-live-voice.md)
before reusing its transcription experiments or voice conclusions.
Read the [personal MCP plan](/.agents/plans/personal-mcp.md) before changing the installed Sheets
setup.

## Status and boundaries

- Research checked on **2026-10-12**; recommendations await review.
- Scope: browser access, course/media study, Sheets authentication, and relevant [TODO
  items](/todo.md).
- Current local Sheets configuration was not changed; its Google authentication remains blocked.
- No MCP installation, browser extension installation, profile change, sign-in, or account
  connection occurred.
- No private course, saved-video collection, Google file, meeting, or work configuration was
  accessed.
- No separately billed browser/media service, browser automation, model download, or media
  acquisition was used.
- Public documentation, package manifests, and downloaded package source were inspected.
- Review is self-review; the earlier subagent usage limit prevented another independent review.
- Research-document Markdown lint, local link checks, and `git diff --check` pass.
- Research-time working-tree lint reported five unrelated line-length errors in `ai-harness-roadmap.md`.
  That file was not changed by this investigation.

Evidence labels:

- **Observed:** local metadata or public-file contents inspected during this investigation.
- **Documented:** a first-party source describes the capability; it was not exercised here.
- **Proposed:** a workflow or trial requiring approval.
- **Unknown:** evidence does not establish the behavior or availability.

## Decisions and recommendations

| Id | Status | Decision | Reason |
| --- | --- | --- | --- |
| B1 | Accepted scope | Investigate and document; do not install. | The user will review the recommendation later. |
| B2 | Requirement | Prefer local, free/open-source operation without a metered connector allowance. | Preserve the user's stated constraints. |
| B3 | Requirement | Keep personal and work access separate. | Existing personal setup must not reuse work identities. |
| B4 | Recommended | Trial Playwright MCP with its official extension. | Explicit tab selection, existing logins, and documented client tab groups. |
| B5 | Recommended fallback | Use Chrome DevTools MCP for DevTools-specific needs. | Strong network, console, performance, and memory diagnostics. |
| B6 | Proposed refinement | Prefer MCP for this authenticated-browser pilot over the earlier CLI baseline. | The user requested a shared MCP and low-friction browser access. No speed winner was established. |
| B7 | Retained | Keep media acquisition, transcription, vision, and knowledge evaluation separate. | A browser does not provide complete video understanding. |
| B8 | Deferred | Do not reopen Composio or other hosted-provider installation. | Composio was explicitly deferred; OAuth convenience does not override that decision. |
| B9 | Verification gate | Require a real, authorized Sheets edit before claiming spreadsheet support. | Browser control alone does not prove reliable interaction with Sheets. |

## Browser shortlist

| Candidate | Verified provenance and cost model | Access approach | Fit and limits |
| --- | --- | --- | --- |
| **Playwright MCP + extension** | Microsoft; Apache-2.0; local package without a hosted call allowance | Attach to selected tabs using existing website logins | Recommended pilot for courses, saved items, and Sheets UI editing. No verified end-to-end trial yet. |
| **Chrome DevTools MCP** | Google Chrome DevTools project; Apache-2.0; local package | Dedicated browser or permission-based attachment to existing Chrome | Best debugging alternative. Automatic attachment exposes all windows in the selected profile. |
| **Playwright CLI + skills** | Existing spike's portable direction | Agent invokes browser commands through its shell | Retain for repeatable scripting. It is not the user's requested MCP interface. |
| **Browser Use** | Open-source agent/CLI plus separately hosted products | Local browser, browser harness, or cloud browser | Adds another agent/runtime path; unnecessary for this first pilot. Cloud and model usage are separate costs. |
| **Claude in Chrome / Claude-hosted connectors** | Anthropic product integrations | Claude account and browser/product integration | Useful within Claude, but no verified equivalent integration was established for Pi. |

Sources: [Playwright MCP][playwright], [extension][extension], [Chrome MCP][chrome],
[Chrome attachment][chrome-advanced], [Browser Use][browser-use], and [Claude MCP][claude-mcp].

Local packages avoid connector subscription fees, not all costs or limits.
Existing model allowances, course access, website rate limits, compute, storage, and maintenance
still apply.
Do not equate open-source software with unlimited access to third-party websites.

### Versions and machine fit

| Item | Observed value | Qualification |
| --- | --- | --- |
| Chrome DevTools MCP | `1.10.1` | npm metadata and package source inspected; not installed. |
| Playwright MCP | `0.0.83` | npm metadata and package source inspected; not installed. |
| Playwright dependency | `1.64.0-alpha-1790635538000` | Exact dependency in the published MCP manifest; release qualification is still needed. |
| Local Chrome | `154.0.8037.98` | Application metadata only; Chrome was not opened or controlled. |
| Local Node | `24.21.0` | Meets both inspected packages' declared Node requirements. |
| Media utilities | `ffmpeg`, `ffprobe`, `yt-dlp` found | Presence only; no acquisition or transcription rerun. |

Chrome's documented automatic attachment requires Chrome 144 or newer; this machine clears that
version gate.
That does not establish successful attachment or account compatibility.
The browser extension has its own release lifecycle; validate it alongside the pinned MCP package.

## What browser access offers

### Existing logins without a new OAuth app

Playwright's extension reuses a browser's existing cookies and sessions.
The first interaction presents a tab-selection page and requests connection approval.
Its current documentation describes a separate tab group for each client.
A tab belongs to one client at a time; the extension status page can disconnect clients
individually.

Select a dedicated personal profile explicitly with `--profile-dir-name`.
Without that selection, the extension can choose the last-used profile containing it.
Keep the approval dialog enabled initially; do not configure its approval-bypass token for the
pilot.

**Tab grouping is not an account-permission sandbox.**
A signed-in page can still act with that account's website permissions.
Playwright explicitly warns that origin filters are not security boundaries.
Use browser/profile isolation and narrow action approval, not just a tab name or domain allowlist.

### Privacy and action boundaries

Local browser control does not make model inference local.
Page text, screenshots, and transcripts returned to an agent can reach its selected model provider.
Review course permissions and content sensitivity before sending private material.
Treat webpage text and captions as untrusted source data, not executable agent instructions.

Do not send messages, publish content, spend credits, change sharing, or join meetings without
explicit approval.
A browser-connection approval is not blanket authorization for those actions.
Keep personal and work profiles separate; do not expose a general debugging port to the network.
Use only the minimum source content needed for the approved task.

### Reading and interacting

Documented browser tools cover navigation, clicks, form input, keyboard input, screenshots, and
accessibility snapshots.
These can help an agent inspect lessons, expand transcripts, follow links, and operate visible
application controls.
Downloads or exports remain conditional on what the website permits and exposes.

Screenshots help when diagrams or canvas interfaces are absent from the accessibility tree.
Sheets often needs keyboard or visual interaction; bulk editing is less dependable than a Sheets
API.
A source-inspected browser tool is not evidence that a particular spreadsheet interaction works.

### Debugging applications

Chrome DevTools MCP adds performance traces, network inspection, console diagnostics, screenshots,
and memory analysis.
Those capabilities are useful for reproducing frontend problems and checking improvements.
They do not fix terminal plugins, cloud credential management, or agent orchestration by themselves.

Chrome MCP enables usage statistics by default.
A trial should disable them with `--no-usage-statistics` and disable CrUX lookup with
`--no-performance-crux`.
The latter prevents performance tooling from sending trace URLs to Google's CrUX service.
Avoid unnecessary extension installation, third-party developer-tool, and experimental capabilities.

### Recording is not understanding

Both projects document browser screencast/video capabilities.
Chrome's screencast tools are experimental and require FFmpeg.
Neither inspected browser-tool reference establishes a complete audio-transcription pipeline.
Audio capture, microphone routing, and semantic understanding were not tested.

Do not promise that playing a lesson delivers its complete sound and visuals to the coding model.
Recordings and screenshots can also capture unrelated personal content; capture only explicitly
approved material.

## Fit against todo.md

| Existing item | Browser contribution | What remains separate |
| --- | --- | --- |
| Research browser access for models | Directly addressed by this comparison and proposed pilot | Real Pi/Claude connection and isolation tests. |
| Make models study courses; start with “Clief notes” | Read lesson structure, text, permitted transcripts, and visible slides | Clarify that phrase and the first source; acquire media lawfully, transcribe, align, and verify notes. |
| Check Higgsfield and video-creation alternatives | Compare current features, inspect interfaces, and later operate approved workflows | Generation credits, creative models, output rights, and quality evaluation. |
| Create a test influencer profile/content | Research formats and prepare drafts; later navigate approved publishing interfaces | Account creation, spending, and each publication require separate approval. Monetization is not guaranteed. |
| Assist on a group call when asked | Navigate meeting controls or inspect available captions after approval | Joining consent, permitted audio capture, speaker context, live reasoning, and controlled speech output. |
| Consider Hermes installation | No prerequisite relationship | Existing Pi and Claude can use these browser tools without another agent platform. |
| Improve dotfiles from another repository | Inspect public documentation or rendered interfaces | Source inspection remains better handled by existing code tools. |

Mise rate limits, AWS profiles/credentials, the screen bar, pinned messages, and Lens rendering are
not browser-MCP fixes.
No TODO item is marked implemented by this research.

## Course, video, and saved-media workflow

The [earlier spike](/.agents/spikes/pi-media-learning-and-live-voice.md#proposed-workflow)
already separates acquisition, local transcription, visual evidence, synthesis, and skill
evaluation.
Keep that architecture; add browser access only where it solves authenticated navigation or source
discovery.

| Source | Proposed browser role | Limitation or stop condition |
| --- | --- | --- |
| Purchased course, including the previously discussed Skool case | Open authorized lessons; identify text, transcript, slides, and permitted download controls | Course-page login does not authorize every embedded player or guarantee a downloadable file. |
| Public YouTube video | Read source metadata and available transcript; identify relevant timestamps | Captions may be missing or incorrect; they are not ground truth. |
| Saved social videos / private playlists | Navigate the user's selected collection and create a reviewable source-link inventory | No universal bulk-export path is established; test each platform separately. |
| Prerecorded webinar | Prefer organizer-provided transcript and recording; inspect synchronized visuals | Permission to attend does not automatically permit recording, redistribution, or external processing. |
| Live webinar or group call | Read available captions or approved recordings as separate inputs | Browser control alone does not provide a real-time listening and speaking assistant. |
| Local media supplied by the user | Browser not required for ingestion | Use the existing media pipeline directly. |

Proposed first lesson workflow:

1. The user selects one authorized lesson and signs in manually, including any two-factor challenge.
2. The browser records its title, URL, lesson position, and available source types.
3. Prefer provided transcripts and permitted exports before considering local audio transcription.
4. If authorized media is available, reuse the existing local ASR and timestamped-frame approach.
5. Preserve raw transcripts separately from corrections, notes, and interpretations.
6. Produce concise notes with timestamps, source links, uncertain passages, and exercises.
7. Check important technical claims against the original audio, frames, or course materials.
8. Propose a reusable skill only after evaluating its benefit on unseen tasks.

The earlier Qwen3-ASR preference came from one English excerpt, not a full-course benchmark.
Browser access does not validate that model on new courses, languages, accents, or long recordings.
Do not retrain, promote instructions, or alter global behavior merely because a course recommends
it.

Keep cookies, browser storage, signed URLs, screenshots, recordings, and paid-course material
outside this public repository.
Do not bypass authentication, CAPTCHA, DRM, or access controls. Let the user complete challenges.
If authorized media cannot be obtained, stop at a sourced outline or request a permitted
transcript/file.

## Simple Google OAuth: what is actually available

The desired experience is: add a connector, approve Google access in a browser, then use it.
That experience depends on who owns the registered Google OAuth application, not merely on using
MCP.

| Route | Sign-in experience | Why it does or does not fit |
| --- | --- | --- |
| **Browser MCP** | Normal Google website login plus browser-connection approval | Best low-friction local pilot; no Google Cloud app. It is UI automation, not Sheets API OAuth. |
| **Claude-hosted Google connectors** | Google authorization managed through the Claude account | Matches the observed Claude experience. No supported Pi import path was established. |
| **Official Google Sheets remote MCP** | Google OAuth plus configured client credentials | Real first-party option, but currently documented as Developer Preview with Cloud setup. It retains the present setup burden. |
| **Google's open-source Workspace extension** | Documented Gemini CLI Google sign-in | Its current Sheets tool list contains reads, not spreadsheet editing. Pi compatibility was not tested. |
| **Local mcp-google-sheets** | User-owned Desktop OAuth app, then browser consent | Free/open-source and API-based editing; currently blocked by the reported Google onboarding friction. |
| **Community Google Drive MCP** | Its quick start also requires a Desktop OAuth client JSON | Broader Workspace editing does not remove the same setup requirement. |
| **Hosted managed-OAuth services** | Provider-owned app and browser consent | Convenient, but introduce service terms, a processor, and potentially usage caps. Composio remains deferred. |

### Correction: Google does document an official Sheets MCP

The earlier catalogue-only check was incomplete.
Google's current [Sheets MCP guide][google-sheets] documents
`https://sheetsmcp.googleapis.com/mcp/v1`, including cell updates and structural batch operations.

Its documented prerequisites include Developer Preview membership, a Cloud project, enabled APIs,
and OAuth consent/client configuration.
The Claude setup explicitly asks for an OAuth client ID and secret.
The guide does not establish an immediate no-setup, first-party connection for this Pi account.
Do not substitute this endpoint and claim the onboarding problem is solved.

### Why the Claude connector cannot simply be copied

[Claude Code's documentation][claude-mcp] explains connector delivery from the signed-in Claude account.
This is distinct from a local `.mcp.json` registration.
Some Anthropic-hosted connectors accept only the callback registered by claude.ai.
A screenshot or connector name therefore does not establish a portable endpoint and OAuth client for
Pi.

[Anthropic's documentation][claude-workspace] describes separate Docs, Sheets, and Slides connectors.
Its live editing pane is documented for Claude web/Desktop, not proven here for Pi or Claude Code.
Google Drive itself handles file discovery and related file operations.
Do not assume the Drive connector's presence alone proves cell-editing capability.
Do not extract or reuse Claude's private session tokens to manufacture Pi access.

**Conclusion:** no investigated option is verified to combine every requirement unchanged:
local/free/open-source, no connector cap, API-level Sheets editing, no user OAuth app, and native Pi
`/mcp` sign-in.
Browser session reuse satisfies the immediate interaction goal through a different authentication
route.

## Proposed pilot for approval

### Initial configuration direction

Use one `personal-browser` stdio server with pinned `@playwright/mcp@0.0.83`.
Proposed arguments are `--extension`, `--profile-dir-name <PERSONAL_PROFILE_DIRECTORY>`, and
`--no-webmcp`.
The package source confirms these options exist; this is not an applied configuration.
Read the profile directory name from `chrome://version` in the selected personal profile.
Never guess it or default to whichever profile was used last.

Keep connection approval enabled. Do not export cookies, configure the bypass token, or enable
unrestricted file access.
Do not automatically grant clipboard, microphone, camera, or screen-recording permissions.
Add optional visual interaction only if the Sheets pilot needs it and its permissions are
understood.

Scope the future registration to personal sessions rather than all workspaces.
Use the same portable definition for both agents if the pilot passes; do not install a second
browser engine.
Avoid simultaneous writes to the same site/tab even with per-client tab groups.

### Acceptance checks

| Stage | Test | Pass condition |
| --- | --- | --- |
| Browser attachment | Approve one personal test tab in Pi | Correct profile/tab is controlled; unrelated/work tabs are not selected. |
| Public navigation | Open a harmless public page and inspect text/screenshot | Tool results identify the actual page; no claimed page content comes from model memory. |
| Sheets edit | Read a named cell, authorize a unique test value, then read it back | Correct spreadsheet, correct cell, successful write and visible confirmation. |
| Recovery | Disconnect, restart, and reconnect | Approval and identity remain clear; no silent profile switch or repeated write. |
| Second client | Attach Claude Code to a different test tab | Separate client groups behave as documented; no cross-tab confusion. |
| One course | Inspect one selected lesson and permitted transcript/media route | Acquisition boundaries are recorded; notes cite actual evidence. |
| One saved-video platform | Inventory a small, explicitly selected collection | Links are accurate; nothing is liked, saved, shared, or deleted incidentally. |
| Permission challenge | Encounter a login/2FA or unexpected consequential action | Agent stops for the user rather than bypassing or approving it. |

Run these stages sequentially. Stop if isolation, authentication, or read-back verification fails.
A screenshot proving connection is not a passed editing or learning pipeline.

Rollback: disconnect the extension, remove only the trial MCP registration, and restart the affected
agent.
Do not delete browser profiles, account data, or cookies as automatic cleanup.
If the browser path fails, document the concrete failure before choosing another connector.

## Questions for morning review

1. Approve the Playwright-extension pilot, or prefer Chrome DevTools despite its broader attachment
   scope?
2. Which personal Chrome profile should the pilot use?
3. Which disposable spreadsheet and first course/lesson should be tested?
4. Does “Clief notes” mean brief course summaries or a particular source?
5. Which saved-video platform should be evaluated first, and what export/processing rights apply?

The simple Google API OAuth requirement remains open; this browser pilot does not silently replace
it.

These questions gate implementation, not completion of this investigation.

## Sources and reproducibility

Read the linked primary sources before implementation; package behavior and product terms can
change.

- [Playwright MCP README and CLI options][playwright]. Published package: `@playwright/mcp@0.0.83`.
- [Playwright extension][extension]: profile selection, connection approval, client tab groups, and
  token bypass.
- [Chrome MCP][chrome], [configuration][chrome-config], [tools][chrome-tools], and
  [attachment][chrome-advanced].
  Published package: `chrome-devtools-mcp@1.10.1`.
- [Browser Use product boundaries][browser-use]: local library/CLI versus cloud browser and agent
  services.
- [Google Sheets remote MCP setup][google-sheets]: first-party endpoint and actual onboarding
  prerequisites.
- [Google Workspace extension tool list][google-workspace]: current Sheets read operations.
- [Community Google Drive MCP][community-drive]: its own client-JSON requirement.
- [Claude MCP authentication and connector delivery][claude-mcp].
- [Claude Google Workspace connectors][claude-workspace]: account-managed Google access and
  editing-product limits.
- [Earlier media
  experiments](/.agents/spikes/pi-media-learning-and-live-voice.md#local-experiments-and-measured-results).

Downloaded npm tarballs were inspected without executing package code:

| Package | SHA-256 |
| --- | --- |
| `chrome-devtools-mcp@1.10.1` | `012cbcf6e832d4f6709dad0c21d7bef17089e94adee9cf33179d15ea0a9adf2b` |
| `@playwright/mcp@0.0.83` | `f0014a13361b1ee2d8607a4e187868ab9a6e8ac637dbcd66e4af43f738d0c8cb` |

The Playwright core dependency's packaged CLI confirms extension/profile options and `--no-webmcp`.
Chrome's packaged source confirms automatic attachment, telemetry controls, and experimental
screencast tools.
Current extension documentation is not proof that an uninspected installed extension has matching
behavior.
No browser performance, course-extraction success rate, or authenticated Google operation was
measured.

[playwright]: https://github.com/microsoft/playwright-mcp
[extension]: https://github.com/microsoft/playwright/tree/main/packages/extension#readme
[chrome]: https://github.com/ChromeDevTools/chrome-devtools-mcp
[chrome-config]: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md
[chrome-tools]: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/tool-reference.md
[chrome-advanced]: https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/advanced-usage.md
[browser-use]: https://github.com/browser-use/browser-use
[google-sheets]: https://developers.google.com/workspace/sheets/api/guides/configure-mcp-server
[google-workspace]: https://github.com/gemini-cli-extensions/workspace/blob/main/docs/index.md
[community-drive]: https://github.com/piotr-agier/google-drive-mcp
[claude-mcp]: https://code.claude.com/docs/en/mcp#use-mcp-servers-from-claude-ai
[claude-workspace]: https://support.claude.com/en/articles/10166901-using-the-google-drive-integration
