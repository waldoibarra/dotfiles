---
name: audio-transcription
description: >-
  Transcribes speech locally from authorized recordings or YouTube media with provenance and coverage checks.
  Use when asked to transcribe audio, recover spoken words, or produce a timestamped speech transcript.
---

# Transcribe speech locally

**Outcome:** Preserve spoken words with honest timing, uncertainty, and processing coverage.

- **IS:** Independent speech recognition from authorized media, preserving the original language.
- **IS NOT:** Visual interpretation or business synthesis; use `video-analysis`.
  Caption extraction through `save-md` is a separate, explicitly requested operation.

## Choose the reading route

| Before… | Read |
| --- | --- |
| Downloading YouTube media or recording a broadcast | [Media acquisition](../../references/media-acquisition.md) |
| Selecting models, decoding audio, or running local recognition | [Local runtime guide](../../../../docs/audio-transcription.md) |
| Returning interpreted findings instead of just speech | [Video analysis](../video-analysis/SKILL.md) |

Resolve the runtime link against this bundle's real source when installed through symlinks.
This skill requires the dotfiles runtime guide; report it missing rather than inventing its
commands.

## Establish source and authority

Agree source, interval, original track, output destination, timing needs, and permitted resource
changes.
Use existing approval instead of repeating settled questions.
For supplied local files, skip acquisition.
A request for a transcript does not authorize translation, external uploads, or credential
extraction.

Read the runtime guide before selecting a model for the current machine.
Check current resources and cached dependencies; installation and offline execution are different
permissions.
A fitting baseline is preferable to an unauthorized model download.
Report unavailable prerequisites before dependent work.

## Produce the transcript

1. Decode the authorized interval and preserve its source offset.
2. Transcribe without captions, previous transcripts, or inferred vocabulary during an independent
  comparison.
3. Preserve raw recognition chunks separately from reviewed text.
4. Check duration coverage, token limits, unexpected empty chunks, repetition, and beginning/end
  completeness.
5. Review consequential names, numbers, dates, and ambiguous passages against source audio when
  possible.
6. Deliver the transcript with provenance, model identity, timing precision, and unresolved
  uncertainty.

Use automatic language detection unless the spoken language is established.
Do not rewrite grammar or convert uncertain words into plausible claims.
Mark uncertain passages with brackets and their actual available time range.
A second recognition pass exposes disagreement but does not establish correctness.
Context prompts can bias recognition; supplied vocabulary is not independent evidence of what was spoken.

## Timing and completeness

Chunk bounds locate a passage within an interval; they do not align individual sentences or words.
The Qwen recipe preserves chunk ranges while its plain-text output omits timestamps.
Use chunk-range citations unless another verified alignment method supplies finer timing.
Add the source excerpt offset before creating source-relative citations.
For live segments, preserve unknown stream offsets instead of inventing them.

Processing every sample establishes coverage, not word accuracy.
Boundary words can be split; review neighboring audio before claiming complete recovery.
If direct audio review is unavailable, label the transcript automated and unverified.
Keep completed chunks after failure and report partial status.

## Privacy and delivery

Local inference avoids uploading source audio to a transcription service.
Returning text or frames through an agent still exposes them to that session's provider.
Store source media, raw output, and reviewed transcripts with their authorized task owner.
Do not put private recordings or project evidence in reusable skills.

## Maintenance

Read `evals/evals.json` only when maintaining this skill.
Runtime measurements remain with the local runtime guide, not copied into this procedure.
