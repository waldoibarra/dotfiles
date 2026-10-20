# Agent workspace

Versioned plans, trial notes, spikes, and supporting evidence. These records preserve decisions
and experiments; maintained workstation documentation lives in `/docs/`.

## Maintenance

- Index evidence collections through their manifests rather than listing every artifact.
- Keep ideas and user-reported observations distinct from verified results. Historical plans are
  not authorization to execute them; read the latest notes before resuming work.
- Keep personal harness plans, routing, usage evidence, and cross-repository backlogs in this
  workspace.
  Public product repositories must not copy or link those records.
- Review additions for publication. Keep credentials, private recordings, model weights, and
  machine-local runtime files outside this directory. Record any evidence redactions in its
  manifest.

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
| Evaluating evidence-aware meeting processing without duplicating retrieval or planning | [Meeting processing plan](/.agents/plans/meeting-processing.md) |
| Continuing personal MCP parity, Sheets setup, and integration lessons | [Personal MCP plan](/.agents/plans/personal-mcp.md) |
| Continuing the shared-role migration and Pi delegation verification | [Shared roles plan](/.agents/plans/pi-shared-roles.md) |
| Choosing current harness priorities or checking pending decisions | [AI harness roadmap](/.agents/plans/ai-harness-roadmap.md) |
| Revisiting harness decisions, historical verification, or superseded proposals | [Harness roadmap archive](/.agents/plans/history/ai-harness-roadmap-2026-10-13.md) |
| Continuing Pi setup or reviewing the integration outcome | [Integration summary](/.agents/plans/pi-dotfiles-integration-summary.md) |
| Reviewing live-chat close errors, Pi trial feedback, or transcript handoffs | [Trial notes](/.agents/plans/pi-live-codex-trial.notes.md) |
| Reusing the original Pi voice test scenarios; later notes supersede trial decisions | [Trial plan](/.agents/plans/pi-live-codex-trial.md) |
| Choosing browser access, studying authenticated media, or comparing Google sign-in options | [Browser and OAuth investigation](/.agents/spikes/browser-access-and-google-oauth.md) |
| Continuing media-learning, transcription, browser, or voice-option research | [Research spike](/.agents/spikes/pi-media-learning-and-live-voice.md) |
| Inspecting saved transcript, metric, or public-video frame evidence | [Evidence manifest](/.agents/spikes/pi-media-learning-and-live-voice-evidence/evidence-manifest.json) |
| Continuing current Lens follow-through or checking remaining gates | [Lens delivery current status](/.agents/plans/pi-lens-delivery.md) |
| Repeating current Lens local checks or acceptance evidence | [Lens verification current record](/.agents/plans/pi-lens-verification.md#repeat-the-verified-checks) |
| Inspecting historical Lens decisions and old status records | [Lens delivery archive](/.agents/plans/history/pi-lens-delivery-2026-10-13.md) |
| Inspecting historical Lens command output and verification notes | [Lens verification archive](/.agents/plans/history/pi-lens-verification-2026-10-13.md) |
| Choosing compact Pi tool rendering or porting Lens | [Lens display spike](/.agents/spikes/pi-lens-tool-display.md) |
