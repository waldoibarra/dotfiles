# Acquire authorized media

**Acquire only the approved source and interval, with explicit storage and process limits.**
YouTube recordings and broadcasts are supported sources; supplied local files need no download.
Other hosts, playlists, and credentials need separate authorization.
Resolve repository documentation links against this file's real source, not its installed symlink.

## Contents

- [Establish boundaries](#establish-boundaries)
- [Inspect and select tracks](#inspect-and-select-tracks)
- [Capture live media](#capture-live-media)
- [Recover and finalize](#recover-and-finalize)
- [Continue with analysis](#continue-with-analysis)

## Establish boundaries

Before writing media, agree destination, excerpt or capture duration, quality, and retention.
For scheduled streams, specify a waiting deadline separately from the recording deadline.
For longer captures, specify maximum output bytes and minimum remaining free disk space.
RAM use and accumulated disk storage are different resource limits.
Check disk space throughout capture; bounded media time alone does not bound elapsed wall time or
bytes.

Preserve existing outputs with unique run directories and no-overwrite behavior.
Keep provenance, logs, partial files, and completed segments together.
Do not automatically delete media; a summary is not a substitute for source evidence.
Stop on login walls, DRM, or bot challenges; never automatically extract browser cookies.
Obtain authorization before credentials, extra sources, paid APIs, dependencies, model downloads,
or external uploads.
Sending images or text to an agent exposes them to its provider despite local speech recognition.

## Inspect and select tracks

Check installed `yt-dlp`, JavaScript runtime, FFmpeg, and ffprobe before dependent operations.
Inspect current metadata and formats rather than assuming a previously live URL remains live.
Use `--ignore-config` and `--no-playlist` consistently to prevent hidden settings or playlist
expansion.
Explicitly select video quality and original audio, retaining track IDs and language provenance.

Keep downloads and transcripts in the task's authorized output directory, outside unrelated
repositories.
For YouTube, quote the URL and disable playlists so one request cannot expand into many videos.
Select the original audio track, not an automatically dubbed version.
An English-language selector does not establish that the speaker originally spoke English.
First inspect the video's formats:

```sh
VIDEO_URL='https://www.youtube.com/watch?v=LlhTEttKcwQ'
yt-dlp --ignore-config --js-runtimes node --no-playlist --list-formats "$VIDEO_URL"
```

Identify an audio-only format marked original, checking language and track metadata.
If original-track provenance is unclear, resolve it before downloading.
Do not silently choose a language fallback.
Replace `ORIGINAL_AUDIO_FORMAT_ID` below with that format's ID.
Run from the authorized output directory; the example creates a new child directory there.

```sh
RUN_DIR="$(mktemp -d ./transcription.XXXXXX)"
AUDIO_FORMAT='ORIGINAL_AUDIO_FORMAT_ID'
yt-dlp --ignore-config --js-runtimes node --no-playlist \
  -f "$AUDIO_FORMAT" -o "$RUN_DIR/source.%(ext)s" "$VIDEO_URL"
printf 'source_url=%s\naudio_format=%s\n' "$VIDEO_URL" "$AUDIO_FORMAT" \
  > "$RUN_DIR/source.txt"
printf 'Output directory: %s\n' "$RUN_DIR"
```

Retain `source.txt` beside the transcript and decoded audio.
For local recordings, skip downloading and use the supplied file directly.

The audio-only example supports transcription, not visual analysis.
For audiovisual analysis, select an available video format and original audio, or a suitable
combined format.
Do not assume a format ID applies to another source.
Inspect tool help before choosing excerpt options; FFmpeg-based seeking can include keyframe
padding.
Probe actual media duration and record the requested interval separately from the acquired interval.
Use an independent wall deadline and disk guard for bounded acquisition.
Stop owned subprocesses on cancellation or deadline; a killed parent may leave its downloader
running.

For supplied local media, preserve its path and source offset without copying or downloading
unnecessarily.
Read [local runtime setup](../../../docs/audio-transcription.md#acquire-and-decode-the-source)
before decoding for speech recognition.

## Capture live media

Prefer capture first and analysis afterward unless near-live work is explicitly requested.
For near-live work, write recoverable segments independently from inference.
Use continuous capture with segment rotation, not separate downloads that leave gaps between
segments.
Segment boundaries may follow keyframes; record measured durations instead of assuming exact
five-minute chunks.
Validate the recorder on a short sample before an unattended long run.
This reference defines an operating contract, not a preinstalled capture supervisor.
A bounded companion lives at `skills/video-analysis/scripts/record_livestream.py`.
It defaults to retained partial output when live checkpoint recovery is unverified.
Before use, read [recorder limits](../skills/video-analysis/references/livestream-recorder.md).

| Installed option | Meaning and limit |
| --- | --- |
| `--wait-for-video MIN[-MAX]` | Poll scheduled availability; values are retry intervals, not a total waiting deadline. |
| `--live-from-start` | Attempt earlier live content; experimental and dependent on available source fragments. |
| `--no-live-from-start` | Start from the current live position; does not preserve earlier content. |

Use current-position capture for a bounded live excerpt unless earlier content is explicitly
requested.
A late start cannot guarantee recovery of unavailable earlier segments.
A scheduled stream's start time may change; keep the separate waiting deadline.
Retain UTC capture times and stream-relative timing when available.
Unknown stream-relative positions must remain unknown.

Before leaving capture running, verify its process identity, owned children, logs, stop command,
and watchdog.
The watchdog must enforce time, output-size, and free-space limits independently from model
inference.
Do not rely on an agent reply, terminal lifetime, or a tool timeout as that watchdog.
An active sleep-prevention process does not guarantee network connectivity or storage availability.
Report whether the process is waiting, capturing, recovering, complete, partial, or stopped.

## Recover and finalize

For transient interruption, check every 30 seconds for at most ten minutes unless the agreement
differs.
The overall capture deadline and disk limits always take precedence.
Bound individual network attempts too; retries cannot compensate for a hung request.
Reset the interruption window only after verifying resumed media, not merely successful metadata
retrieval.

Preserve completed segments, partial tracks, and downloader checkpoint files before recovery.
Inspect the last retained fragment and media timestamp for each track.
First check whether the installed downloader can safely resume those files and checkpoints.
Verify that resumption advances beyond retained media rather than downloading the beginning again.
When checkpoint resumption is unavailable, start a uniquely named segment from the last verified boundary.
Record any gap or overlap; current-position capture cannot recover an earlier missing interval.
If neither method is supported, stop and report the recovery limitation.

**A new output directory is not a resume strategy.**
Do not automatically restart with `--live-from-start` after interruption.
A full redownload requires explicit approval covering duplicated storage and transfer.
An initial request to capture everything from the beginning does not authorize repeated full downloads.
Validate recovery behavior before unattended capture; retained progress must survive a simulated interruption.
Record missing and potentially duplicated intervals; reconnecting does not establish continuous
capture.
Finalize on a confirmed broadcast ending.
An isolated disconnect or one unavailable response does not establish that ending.
Authentication challenges and access restrictions stop acquisition rather than triggering bypass
attempts.

On normal stop, close the current segment and allow bounded finalization before terminating owned
children.
If forced termination is needed, retain partial files and report which outputs remain unverified.
Probe output duration, streams, and decodability before declaring capture successful.
No network request success, process exit, or file presence alone establishes complete recording.

### Remove verified duplicates

Delete duplicate media only with explicit user authorization.
Keep active capture files and files still needed by running consumers.
Compare source identity, selected tracks, timestamps, coverage, and decodability before choosing
retained media.
A longer duration or larger file alone does not prove that earlier content is preserved.
For byte-identical overlap, hash each old track against the same-length prefix of its retained
counterpart.
For remuxed or re-encoded copies, require equivalent content and coverage checks instead of byte
equality.
If equivalence remains uncertain, retain both copies and report the unresolved difference.

Before deletion, record hashes, checks, and old-to-retained path mappings beside the capture logs.
Verify that removed files have no active writers or readers; recheck file identities before deleting.
Remove only verified redundant media, preserving logs, provenance, checkpoints, and unique intervals.
Verify that retained media remains readable and recording continues afterward.
Sample decoding does not establish full-stream integrity; report its inspected intervals.

## Continue with analysis

- Use [audio transcription](../skills/audio-transcription/SKILL.md) for spoken words.
- Use [video analysis](../skills/video-analysis/SKILL.md) for goal-directed audiovisual findings.
- Read [near-live analysis](../skills/video-analysis/references/near-live-analysis.md) before
  processing a continuing capture.

[yt-dlp documentation](https://github.com/yt-dlp/yt-dlp#readme) owns option semantics and platform
limitations.
Local help confirms installed flags; only exercised source acquisition establishes current access.
