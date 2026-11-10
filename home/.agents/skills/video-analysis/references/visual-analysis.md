# Inspect audiovisual evidence

**Choose inspection density from the question and observed content, not a universal frame
interval.**

## Establish coverage

Probe duration, frame dimensions, audio tracks, and available timing metadata before sampling.
Retain original resolution for text and numerical inspection.
Record extracted frames separately from frames actually opened and inspected.

For broad orientation, start with timestamped frames approximately ten seconds apart, including
the ending.
Add scene-change frames when slides, camera views, or application screens change.
Contact sheets help navigation; they do not establish small text, exact numbers, or action
sequences.

This baseline is a heuristic.
Rapid editing, subtle interface changes, flashing text, and motion can occur between samples.
Adjust density against observed material and the task's coverage budget.

## Follow relevant evidence

| Question | Inspection |
| --- | --- |
| What does a slide or chart establish? | Inspect full-resolution frames, labels, units, legends, and relevant context. |
| How does a workflow proceed? | Inspect before-and-after states and intervening actions, including failures. |
| How does movement or editing work? | Review continuous short sequences when supported; dense frames alone can miss temporal behavior. |
| What does music or delivery contribute? | Review original audio directly with a capable tool or listener. |
| Is a displayed result credible? | Record what is visible separately from its authenticity and external validity. |

Transcript phrases referencing demonstrations are additional cues, not the only reason to inspect
visuals.
Silent sequences require independent visual coverage.
Start targeted frame review around one-second intervals, tightening around brief events when
justified.

## Preserve timing and uncertainty

Record each frame's source offset, segment identifier, extraction method, and local path.
Use actual presentation timestamps where available, not filenames interpreted as timestamps.
Frame indices alone are insufficient after seeking or irregular scene-change sampling.
Check seek accuracy and keyframe effects before claiming exact alignment.
For live media, distinguish segment offsets, stream-relative time, and UTC capture time.
Do not create a YouTube timestamp link when the stream-relative offset is unknown.

OCR supplies candidate text, not verified screen content.
Preserve cropped detail alongside the wider frame when context affects meaning.
Mark unreadable text, ambiguous actions, or unsupported audio inspection rather than guessing.

## Verify capability

An image-reading tool does not imply video playback or audio-listening capability.
A speech recognizer does not evaluate music, tone, or sound design.
Report unavailable capabilities before conclusions that depend on them.
A second model's agreement is not independent verification of the underlying event.

Back to [video analysis](../SKILL.md).
