# Proposal

## Why

Bounded livestream capture needs local supervision that retains partial evidence safely.
Existing downloader options do not prove live checkpoint recovery.

## What Changes

Add a standard-library Python recorder under the video-analysis skill.
It creates a unique run directory with agreement, events, status, and retained outputs.
It bounds capture, requests, disk reserve, and output bytes.
It never deletes media or silently repeats a from-start transfer.

## Approach and tradeoffs

The recorder invokes installed `yt-dlp`, FFmpeg, and ffprobe through process groups.
It defaults to a single capture attempt and stops retained output as `partial` after failure.
This protects coverage when checkpoint safety remains unverified.

Current-position fallback is deliberately not implemented.
A failed capture retains its first segment and reports `partial`.
This avoids a lossy recovery claim without current source confirmation.

No checkpoint resume feature is implemented.
`yt-dlp` documentation describes `--continue`, but not verified live checkpoint advancement.
`--no-overwrites` does not imply `--no-continue`.

## Capabilities

- `bounded-livestream-recording`: bounded capture, safe stopping, status, and provenance.
- `livestream-recovery-boundaries`: partial retention without lossy fallback.

Local fixture checks verify the bounded behavior but do not define another capability.

## Impact

The video-analysis skill gains a local recorder entrypoint and operational invocation.
The media-acquisition reference gains companion limits and recovery guidance.
The implementation depends on installed `yt-dlp`, FFmpeg, and ffprobe only.
No installation, credential, network-media, or user-media mutation occurs.

## Verification

Focused tests use temporary directories and fake downloader subprocesses.
They exercise cancellation, child cleanup, limits, status, access restrictions, and recovery boundaries.
FFmpeg generates and ffprobe decodes tiny local fixtures.
These tests do not establish YouTube availability or checkpoint recovery.

## Approval

The operator waived further plan approval for this task.
The approved scope is the supplied brief and `maintained-livestream-recorder` plan.
