# Prototype options and capabilities

**Choose by the uncertainty, not by a fixed ladder from cheap artifacts to elaborate apps.**
Return to [prototype selection](../SKILL.md) for the decision procedure.
The capabilities below are prerequisites to verify, not claims about an operator's installed
environment.

## Compare candidate formats

| Format | Choose when testing… | Main limitation | Minimum capabilities |
| --- | --- | --- | --- |
| Chat or reusable prompt | Reasoning, wording, conversation, or whether an app is needed | No independent usage or demand evidence | Chat, relevant input modalities, appropriate source access |
| Markdown, PDF, slides | An offer, report, explanation, or information structure | Limited interaction evidence | File writing and preview; renderer/exporter for PDF or slides |
| Diagram or storyboard | Relationships, architecture, workflow, or service journey | Can hide timing and behavioral failures | Diagram data or SVG generation and rendered inspection |
| Paper or clickable mockup | Navigation, terminology, comprehension, and task sequence | Backend behavior remains simulated | Paper or linked screens; participant observation |
| Spreadsheet or notebook | Calculations, pricing, economics, or transformations | Results depend on input assumptions | Calculation runtime, representative data, table/chart inspection |
| CLI or technical spike | Algorithm, integration, performance, or device feasibility | Usually weak customer-experience evidence | Runtime, isolated inputs, logs, sandbox access when needed |
| Interactive simulation | State transitions, scheduling, constraints, or scenario consequences | Validates the model, not its assumptions | Interactive runtime, visible state, reproducible inputs |
| Single-file web prototype | A focused interaction with easy sharing | Browser and local-file restrictions | HTML generation, browser inspection; server only when required |
| Hosted web app or landing page | Remote use, onboarding, end-to-end behavior, or an offer | Adds operations, privacy, and distribution work | Runtime, browser checks, approved hosting, secrets, scoped measurement |
| Mobile or desktop app | Sensors, notifications, offline use, background work, or OS integration | Build, permissions, and distribution overhead | Target SDK, emulator/device, inspection; signing when required |
| 3D or physical mockup | Spatial understanding, manipulation, scale, fit, or embodiment | Visual realism alone cannot establish physical performance | Authoring/rendering tools; physical testing for physical claims |
| Generated image, video, audio | Aesthetic direction, tone, narrative, or a proposed experience | Convincing media cannot establish functionality | Approved generation access, assets, playback, spending limits |
| AI behavior evaluation | Output quality, latency, cost, and failure modes | One good answer proves little | Model access, representative cases, criteria, protected keys, usage records |
| Concierge or Wizard-of-Oz | Service usefulness before automation | Manual success cannot establish scalable automation | Intake/delivery channels, human operator, consent, outcome observation |
| Offer or fake-door experiment | A specific expression of interest or commitment | Not proof of satisfaction or retention | Approved audience access, honest availability disclosure, scoped measurement |
| Immersive hybrid app | Game-like interaction combining 3D, AI, and generated media | Novelty and production expense can obscure user benefit | Relevant app and media capabilities; interaction, accessibility, and performance inspection |

AI, game mechanics, and generated media can combine with any suitable delivery format.
A static media sample may precede an immersive app when only its premise needs testing.
A functioning app can be the best first experiment when realistic interaction is the central
uncertainty.
[Gamification evidence](gamification.md) distinguishes engagement mechanisms from evidence of
commercial success.

## Verify capabilities, not connector names

Distinguish configured, installed, loaded, authenticated, and exercised states.
Verify only prerequisites relevant to the chosen experiment; do not install the entire menu.
A CLI, direct API, or compatible file can suffice without an MCP server.
Keep secrets outside client-side artifacts, source control, and research reports.
Use synthetic or sanitized inputs when private data is unnecessary.

| Named option | Minimum route | What still needs checking |
| --- | --- | --- |
| Excalidraw | Compatible scene data and import/export workflow | Schema compatibility, rendered result, editing needs; MCP optional |
| Higgsfield | Official SDK/API; `HF_KEY` or `HF_API_KEY` with `HF_API_SECRET` | Account credits, exact modality endpoint, asset rights, polling and result retrieval |
| OpenRouter | API key and server-side HTTP/SDK calls | Approved models/providers, spending limits, privacy settings, real request compatibility |

These examples describe documented interfaces, not installed integrations or guaranteed account
access.
An agent's chat subscription does not automatically provide API access to its generated application.
Model/provider changes can affect privacy, latency, cost, and reproducibility; record the
configuration used.

## Source pointers

- [Excalidraw export
  utilities](https://github.com/excalidraw/excalidraw/tree/master/packages/utils): scene data and
  rendered exports.
- [Higgsfield official Python client](https://github.com/higgsfield-ai/higgsfield-client):
  credentials, submission, polling, and results.
- [OpenRouter quickstart](https://openrouter.ai/docs/quickstart): direct API and SDK access,
  separately from MCP.
- [OpenRouter limits](https://openrouter.ai/docs/api_reference/limits): key usage and spending
  information.
- [GOV.UK prototyping guidance](https://www.gov.uk/service-manual/design/making-prototypes):
  choose suitable realism and separate prototypes from production.
- [Karpathy's MenuGen experience](https://karpathy.bearblog.dev/vibe-coding-menugen/): operational
  costs beyond initial code generation.

Recheck live documentation before implementation; names, endpoints, and availability can change.
