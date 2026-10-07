# Agent workspace

Versioned plans, trial notes, spikes, and supporting evidence. These records preserve decisions
and experiments; maintained workstation documentation lives in `/docs/`.

## Maintenance

- Index evidence collections through their manifests rather than listing every artifact.
- Keep ideas and user-reported observations distinct from verified results. Historical plans are
  not authorization to execute them; read the latest notes before resuming work.
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
| Continuing Pi setup or reviewing the integration outcome | [Integration summary](/.agents/plans/pi-dotfiles-integration-summary.md) |
| Recording Pi trial feedback or exploring the transcript-handoff idea | [Trial notes](/.agents/plans/pi-live-codex-trial.notes.md) |
| Reusing the original Pi voice test scenarios; later notes supersede trial decisions | [Trial plan](/.agents/plans/pi-live-codex-trial.md) |
| Continuing media-learning, transcription, browser, or voice-option research | [Research spike](/.agents/spikes/pi-media-learning-and-live-voice.md) |
| Inspecting saved transcript, metric, or public-video frame evidence | [Evidence manifest](/.agents/spikes/pi-media-learning-and-live-voice-evidence/evidence-manifest.json) |
