# Plans and research

Versioned plans and research preserve decisions, experiments, and evidence.
They stay separate from shared harness configuration.
Read [architecture](/docs/architecture.md) before changing ownership.

- `openspec/changes/` holds new scoped changes; read [OpenSpec
  integration](/docs/ai-harness/openspec.md) before use.
- `docs/plans/` holds existing plans, roadmaps, trial notes, and their history.
- `docs/spikes/` holds investigations and their supporting evidence.
- `home/.agents/` holds shared harness configuration, not project plans or research.

Existing plan and research locations remain unchanged; they are not templates for new archives.
These records explain work; maintained operational guides describe current behavior.
Frozen history and evidence retain their original bytes, including historical paths.
For those records, map `.agents/plans/` to `docs/plans/` and `.agents/spikes/` to `docs/spikes/`.
The former `.agents/README.md` index is now this document.
Historical `docs/coding-agents/` paths now resolve under `docs/ai-harness/`.

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

## Private personal evidence

Keep private personal extracts outside this tracked workspace and outside shared harness
configuration.
Company material and mixed-source originals remain with their owning workspace.
Git ignore is not a scope boundary.

## Evidence storage

**Curated evidence:** Keep `docs/spikes/pi-media-learning-and-live-voice-evidence/` in Git.
The roughly 2 MB collection contains transcripts, metrics, and public-video frames supporting the
recorded findings.
Versioning preserves that evidence across machines.

**Large artifacts:** Keep raw audio/video, model weights, caches, and large generated batches
outside Git.
Add targeted ignores for local artifacts; reconsider external storage when evidence accumulates
frequently.
Binary revisions grow Git history even after files are removed.
Size alone does not replace the publication review above.

## Index

| Read before… | Record |
| --- | --- |
| Reviewing the harness-guide refactor and verification limits | [Documentation refactor](/openspec/changes/refactor-harness-guides/proposal.md) and [checks](/openspec/changes/refactor-harness-guides/tasks.md) |
| Comparing historical Pi voice results with current usage | [Voice trial evidence](/docs/ai-harness/pi/limitations.md#trial-environment) |
| Continuing Markdown default-app setup or reviewing its verification | [Markdown application plan](/docs/plans/markdown-default-app.md) |
| Evaluating evidence-aware meeting processing without duplicating retrieval or planning | [Meeting processing plan](/docs/plans/meeting-processing.md) |
| Continuing personal MCP parity or reviewing retired Sheets integration lessons | [Personal MCP plan](/docs/plans/personal-mcp.md) |
| Continuing the shared-role migration and Pi delegation verification | [Shared roles plan](/docs/plans/pi-shared-roles.md) |
| Refactoring shared instructions, memory lifecycle, and cross-repository documentation | [Harness information architecture](/docs/plans/harness-information-architecture.md) |
| Continuing reusable setup direction, Cursor trial planning, or current harness priorities | [AI harness roadmap](/docs/plans/ai-harness-roadmap.md) |
| Revisiting harness decisions, historical verification, or superseded proposals | [Harness roadmap archive](/docs/plans/history/ai-harness-roadmap-2026-10-13.md) |
| Continuing Pi setup or reviewing the integration outcome | [Integration summary](/docs/plans/pi-dotfiles-integration-summary.md) |
| Reviewing live-chat close errors, Pi trial feedback, or transcript handoffs | [Trial notes](/docs/plans/pi-live-codex-trial.notes.md) |
| Reusing the original Pi voice test scenarios; later notes supersede trial decisions | [Trial plan](/docs/plans/pi-live-codex-trial.md) |
| Choosing browser access, studying authenticated media, or comparing Google sign-in options | [Browser and OAuth investigation](/docs/spikes/browser-access-and-google-oauth.md) |
| Continuing media-learning, transcription, browser, or voice-option research | [Research spike](/docs/spikes/pi-media-learning-and-live-voice.md) |
| Inspecting saved transcript, metric, or public-video frame evidence | [Evidence manifest](/docs/spikes/pi-media-learning-and-live-voice-evidence/evidence-manifest.json) |
| Continuing current Lens follow-through or checking remaining gates | [Lens delivery current status](/docs/plans/pi-lens-delivery.md) |
| Repeating current Lens local checks or acceptance evidence | [Lens verification current record](/docs/plans/pi-lens-verification.md#repeat-the-verified-checks) |
| Inspecting historical Lens decisions and old status records | [Lens delivery archive](/docs/plans/history/pi-lens-delivery-2026-10-13.md) |
| Inspecting historical Lens command output and verification notes | [Lens verification archive](/docs/plans/history/pi-lens-verification-2026-10-13.md) |
| Choosing compact Pi tool rendering or porting Lens | [Lens display spike](/docs/spikes/pi-lens-tool-display.md) |
