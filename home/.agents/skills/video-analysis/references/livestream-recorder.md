# Bounded livestream recorder

Use the installed skill's `scripts/record_livestream.py` for a bounded local capture attempt.
Read [media acquisition](../../../references/media-acquisition.md) before invoking it.

## Invoke

```sh
SKILL_DIR="${SKILL_DIR:?Set SKILL_DIR to the installed video-analysis skill}"
python3 "$SKILL_DIR/scripts/record_livestream.py" SOURCE RUN_DIRECTORY \
  --video-format VIDEO_FORMAT_ID --audio-format ORIGINAL_AUDIO_FORMAT_ID \
  --capture-seconds 300 \
  --request-seconds 30 --stall-seconds 60 \
  --max-bytes 5000000000 --min-free-bytes 10000000000
```

`RUN_DIRECTORY` must not exist.
The recorder writes `agreement.json`, `events.jsonl`, and atomic `status.json` there.
The agreement records source, selected format identifiers, and enforced limits.

Use `--from-start` only when earlier live content is explicitly authorized.
The first transfer never uses unverified checkpoint resume.
The recorder supplies `--no-continue` and never repeats a from-start transfer automatically.

Current-position fallback is not implemented while live checkpoint behavior remains unverified.
A failed capture retains the first attempt and reports `partial`.
Status lists playable and unverified retained tracks after a bounded probe.
It records each playable track's sampled interval, not full-file integrity.
That failed run cannot report `complete`.

## Observe and stop

Read `status.json` and `events.jsonl` for process identity, heartbeat, and selected-track observations.
Send `SIGINT` or `SIGTERM` to the recorder for a bounded owned-child stop.
Cancellation and deadline stops send SIGTERM, then SIGKILL after two seconds if needed.
They end partial; retained tracks may remain unmerged.
Resource caps stop capture for deadline, per-track stall, byte budget, or disk reserve.
Confirmed access errors remain terminal even when a stall guard stops the child first.
The byte budget counts every retained file in the run directory, including logs and metadata.

## Limits

The recorder does not verify YouTube checkpoint recovery or broadcast completeness.
`complete` means the source ended and retained audio/video passed a sampled decode.
Status records the sampled duration; captured coverage and broadcast completeness remain unknown.
Local tests simulate downloader and ended metadata behavior using installed FFmpeg fixtures.
For tests only, `RECORDER_TEST_COMMAND` passes a fixture mode directly to a fake downloader.
Never set that variable for real capture; it bypasses normal downloader flags and format validation.
They do not exercise YouTube acquisition or live recovery.

`SIGKILL` cannot run cleanup handlers.
An external supervisor must inspect stale status and kill any surviving process group.
The recorder never deletes media, checkpoints, logs, or existing user output.

**Live acquisition remains experimental and unverified.**
Installed `yt-dlp` output names, JavaScript runtime needs, and merge timing remain untested.
If only a combined output grows before both selected tracks advance, capture stops partial.
After both tracks advance, merged growth prevents a false stall only while both tracks are idle.
A growing selected track never hides another selected track's stall.
A stalled merge still ends partial; this does not prove continuous broadcast coverage.
