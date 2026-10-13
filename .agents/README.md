# Agent workspace

Versioned plans, trial notes, spikes, and supporting evidence. These records preserve decisions
and experiments; maintained workstation documentation lives in `/docs/`.

## Maintenance

- Index evidence collections through their manifests rather than listing every artifact.
- Keep ideas and user-reported observations distinct from verified results. Historical plans are
  not authorization to execute them; read the latest notes before resuming work.
- Keep personal harness plans, routing, usage evidence, and cross-repository backlogs in this workspace.
  Public product repositories must not copy or link those records.
- Review additions for publication. Keep credentials, private recordings, model weights, and
  machine-local runtime files outside this directory. Record any evidence redactions in its manifest.

## Evidence storage

Keep the curated `spikes/pi-media-learning-and-live-voice-evidence/` collection in Git. At roughly
2 MB, its transcripts, metrics, and public-video frames are small enough to version alongside the
findings they support, preserving evidence across machines.

Keep raw audio/video, model weights, caches, and large generated batches outside Git; add targeted
ignore rules if these are stored locally in the workspace. Reconsider external artifact storage
if evidence accumulates frequently: repeated binary revisions grow repository history even when
old files are later removed. Size alone does not replace the publication review above.

## Index

| Read before… | Record |
| --- | --- |
| Continuing Markdown default-app setup or reviewing its verification | [Markdown application plan](/.agents/plans/markdown-default-app.md) |
| Continuing personal MCP parity, Sheets setup, and integration lessons | [Personal MCP plan](/.agents/plans/personal-mcp.md) |
| Continuing the shared-role migration and Pi delegation verification | [Shared roles plan](/.agents/plans/pi-shared-roles.md) |
| Changing agent rules, role agents, skill scope, or the improvement loop | [AI harness roadmap](/.agents/plans/ai-harness-roadmap.md) |
| Continuing Pi setup or reviewing the integration outcome | [Integration summary](/.agents/plans/pi-dotfiles-integration-summary.md) |
| Recording Pi trial feedback or exploring the transcript-handoff idea | [Trial notes](/.agents/plans/pi-live-codex-trial.notes.md) |
| Reusing the original Pi voice test scenarios; later notes supersede trial decisions | [Trial plan](/.agents/plans/pi-live-codex-trial.md) |
| Choosing browser access, studying authenticated media, or comparing Google sign-in options | [Browser and OAuth investigation](/.agents/spikes/browser-access-and-google-oauth.md) |
| Continuing media-learning, transcription, browser, or voice-option research | [Research spike](/.agents/spikes/pi-media-learning-and-live-voice.md) |
| Inspecting saved transcript, metric, or public-video frame evidence | [Evidence manifest](/.agents/spikes/pi-media-learning-and-live-voice-evidence/evidence-manifest.json) |
| Checking Lens rename, laptop provisioning, compatibility, or pending feedback | [Lens delivery and feedback plan](/.agents/plans/pi-lens-delivery.md#rename-and-provisioning-checkpoint) |
| Repeating Lens acceptance checks or distinguishing verified from active behavior | [Lens verification commands](/.agents/plans/pi-lens-verification.md#repeat-the-verified-checks) |
| Choosing compact Pi tool rendering or porting Lens | [Lens display spike](/.agents/spikes/pi-lens-tool-display.md) |
