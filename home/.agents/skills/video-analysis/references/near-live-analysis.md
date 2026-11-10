# Analyze completed segments while capture continues

**Near-live analysis trades processing delay for reviewable, bounded evidence.**
This is an agent-operated workflow, not an installed streaming service or unattended reliability
guarantee.

Read [media acquisition](../../../references/media-acquisition.md) before capture.
It owns source access, retry limits, capture deadlines, storage bounds, and safe termination.

## Separate capture from analysis

Capture writes recoverable segments independently from model inference.
Start with five-minute segments, adjusting to the task's latency, keyframe cadence, and storage
budget.
For short tests, use shorter segments so at least one completes while capture continues.

Process only closed, decodable segments.
A growing file is not evidence of completed capture.
Maintain explicit states: capturing, ready, processing, analyzed, failed, and retained.
Retrying analysis must not overwrite source media or duplicate findings.

Use a durable process only after verifying its lifetime, logs, stop command, and limits.
Do not assume an agent turn, shell timeout, or terminal tab guarantees continued operation.
Capture must stop safely even when the analysis worker is unavailable.

## Process the queue

1. Probe each completed segment and record actual duration and timing metadata.
2. Transcribe relevant speech using `audio-transcription`.
3. Inspect required visual and non-speech audio evidence using [audiovisual
  inspection](visual-analysis.md).
4. Append source-linked findings and unresolved questions, marking conclusions provisional.
5. Review neighboring segment boundaries for split words, actions, or duplicate content.
6. Consolidate findings after the agreed interval or broadcast ends.

Keep stream offsets separate from wall-clock capture times and segment-relative offsets.
Reconnects may introduce missing or duplicated intervals.
When mapping is uncertain, preserve that uncertainty rather than inventing a continuous timeline.

## Manage contention and backlog

Measure processing time against segment duration before claiming sustained near-live throughput.
Limit concurrent inference to protect the operator's other sessions.
Keep one analysis job active initially; increase concurrency only within the agreed resource budget.
Check memory pressure, disk consumption, queued media duration, and oldest unprocessed segment.

When analysis falls behind, preserve capture within its bounds and disclose the growing delay.
At a storage boundary, stop safely or ask for a revised budget.
Do not silently lower quality, discard unprocessed segments, or enable automatic deletion.

## Retain before removing

Retain test recordings by default.
A future deletion policy needs explicit approval covering eligible files, review gates, storage
limits, and irreversibility.
Retain unresolved passages and evidence supporting consequential findings until review finishes.
A transcript cannot replace visual, musical, or temporal source evidence.

Near-live observations remain provisional until cross-segment consolidation.
Short successful tests do not prove multi-hour continuity, interruption recovery, or sustained
throughput.

Back to [video analysis](../SKILL.md).
