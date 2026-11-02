# Transcribe YouTube videos and recordings locally

**Select a local speech model for the current machine before transcribing spoken words.**
Acquire the media first, then transcribe its audio locally without uploading the recording.
YouTube URLs and local recordings are the current scope, including downloaded WhatsApp `.opus` messages.
Other video hosts are future work, not verified support.
Transcription does not capture silent demonstrations, diagrams, or on-screen text.

Qwen3-ASR through MLX is the tested Apple Silicon baseline, not a fixed choice for every laptop.
Retain Whisper Small as a lightweight alternative.
Neither model produces verified verbatim speech without review against the recording.
Caption extraction through `save-md` is a separate operation, not independent speech recognition.
Use captions when explicitly requested; never substitute them silently for audio-based transcription.
A bare URL does not authorize downloads or establish whether transcription or visual analysis is wanted.

Download dependencies and model weights first; subsequent transcription can run offline.
This workflow needs no Ollama server, cloud transcription subscription, or API key.

Read [workstation tooling](/docs/tooling.md) for package ownership and installation guidance.

## Select a model for this machine

**Run `llmfit` on the machine that will perform inference before choosing a transcription model.**
Do not reuse another laptop's hardware measurements or assume its preferred model is best here.
Inspect current free memory as well as total RAM, GPU backend, and available disk space.

```sh
command -v llmfit
llmfit --json system
llmfit --json search Qwen3-ASR
llmfit --json search whisper
df -h .
```

Use `llmfit --json info 'MODEL_ID'` for candidates returned by the installed catalog.
Compare speech-recognition models, not general chat models or text-to-speech models.
Catalog coverage and classifications can be incomplete or incorrect.
Verify each candidate's actual speech task.
Check its model card, language support, license, runtime compatibility, and exact weight precision.
MLX requires compatible Apple Silicon hardware; choose another supported runtime elsewhere.

A larger machine may accommodate a stronger model or higher-precision weights.
Treat that as a candidate improvement, not proof of better word recognition.
Do not rank transcription accuracy using `llmfit` fit scores or generic token-speed estimates.
A missing catalog entry does not prove incompatibility.

1. Establish the current machine's available resources and cached speech models.
2. Compare the tested Qwen baseline with suitable alternatives, including Whisper large-v3 when available.
3. Recommend one candidate using word-fidelity evidence, language coverage, and measured resource needs.
4. Ask before installing missing runtimes or downloading new weights.
5. Run a representative audio excerpt without captions, previous transcripts, or vocabulary hints.
6. Measure runtime and memory, checking omissions, repetitions, numbers, names, and token limits.
7. Compare disputed words against listening or a human-checked reference before claiming improved accuracy.

When approval or access prevents comparison, report the limit.
Use a verified fitting baseline if authorized.
Record hardware, model identity, precision, runtime, and sample limitations with the result.
`uv run --offline --with` can still install cached packages into a new environment.
When installations are forbidden, inspect existing environments without invoking dependency resolution.
Use a verified existing interpreter directly; if none is available, stop and report the prerequisite.
Do not describe a laptop as tested from a simulated `llmfit` profile or another machine's results.

The recipes below implement the tested Qwen baseline and Whisper Small alternative.
Selecting another model requires its own supported invocation and verification.
Replacing the model ID alone is insufficient.

## Check prerequisites

These commands assume `uv`, Python, and FFmpeg are available:

```sh
command -v uv python3 ffmpeg ffprobe
# YouTube acquisition also requires these tools.
command -v yt-dlp node
```

| Component | Responsibility |
| --- | --- |
| `uv` | Launch Python with dependencies in an isolated, cached environment. |
| `yt-dlp` | Acquire authorized YouTube audio independently of captions. |
| `mlx-audio` | Run Qwen3-ASR inference through MLX on Apple Silicon. |
| Qwen3-ASR-1.7B BF16 | Tested Apple Silicon baseline; reassess fit and alternatives on each machine. |
| `mlx-whisper` | Run Whisper inference through MLX on Apple Silicon. |
| Whisper Small | Supply multilingual speech-recognition model weights. |
| FFmpeg | Decode audio formats, including WhatsApp `.opus` recordings. |
| `huggingface_hub` | Download model files and locate cached snapshots. |

Ollama does not participate in this workflow.
Kokoro voice models generate speech from text; they cannot replace a transcription model.

## Acquire and decode the source

Keep downloads and transcripts in the task's authorized output directory, outside unrelated repositories.
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

Read yt-dlp's destination output for the downloaded filename and extension.
Set `SOURCE_FILE` to that file or a local recording, preserving quotes around paths.
Decode the entire source, without a sample-duration limit:

```sh
SOURCE_FILE="$RUN_DIR/source.webm" # Replace with the actual file, including its extension.
ffmpeg -hide_banner -loglevel error -nostdin -n -i "$SOURCE_FILE" \
  -map 0:a:0 -ar 16000 -ac 1 -c:a pcm_s16le "$RUN_DIR/audio.wav"
ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate,channels \
  -of json "$RUN_DIR/audio.wav"
```

Create `RUN_DIR` for local files too; preserve existing sources and never overwrite another task's output.
Check the selected stream when a video contains multiple audio tracks.
Stop on login walls, DRM, or bot challenges; do not automatically extract browser cookies.
Obtain authorization before credential use, additional downloads, paid APIs, or external uploads.
Future host support belongs in acquisition; the local transcription procedure can reuse decoded audio.

## Prepare Qwen

**Check the cache first.** Missing dependencies or weights require network access.
The model weights occupy approximately 4.1 GB.
The tested model revision is pinned below; runtime dependencies remain unpinned.
These download commands do not read or upload audio.

```sh
uv run --no-project --with mlx-audio python - <<'PY'
from huggingface_hub import snapshot_download

print(snapshot_download(
    "mlx-community/Qwen3-ASR-1.7B-bf16",
    revision="e1f6c266914abc5a46e8756e02580f834a6cf8a7",
))
PY
```

Weights use Hugging Face's default cache unless environment settings override it.
The tested runtime was MLX Audio 0.6.4 with MLX 0.32.4 and Transformers 5.22.1.
Check installed versions before assuming later releases retain these interfaces.

## Transcribe with Qwen offline

Use the decoded WAV and a new output directory.
This example writes raw chunk records and plain text without timestamps.
It preserves original wording rather than rewriting grammar or generating a summary.

```sh
HF_HUB_OFFLINE=1 uv run --offline --no-project --with mlx-audio \
  python - "$RUN_DIR/audio.wav" "$RUN_DIR/qwen" <<'PY'
import hashlib
import json
import sys
import time
import wave
from pathlib import Path

import mlx.core as mx
import numpy as np
from huggingface_hub import snapshot_download
from mlx_audio.stt.utils import load_model

source, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=False)
with wave.open(str(source), "rb") as wav:
    rate = wav.getframerate()
    assert rate == 16000 and wav.getnchannels() == 1 and wav.getsampwidth() == 2
    samples = np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2")
    audio = samples.astype("float32") / 32768
model_path = snapshot_download(
    "mlx-community/Qwen3-ASR-1.7B-bf16",
    revision="e1f6c266914abc5a46e8756e02580f834a6cf8a7",
    local_files_only=True,
)
started = time.perf_counter()
model = load_model(model_path, model_type="qwen3_asr", strict=True)
load_seconds = time.perf_counter() - started
records = []
for index, offset in enumerate(range(0, len(audio), 120 * rate)):
    chunk = audio[offset:offset + 120 * rate]
    started = time.perf_counter()
    result = model.generate(
        chunk, language="English", temperature=0.0,
        max_tokens=8192, batch_size=1, verbose=False, stream=False,
    )
    record = {
        "start": offset / rate, "end": (offset + len(chunk)) / rate,
        "text": result.text, "generation_tokens": result.generation_tokens,
        "seconds": time.perf_counter() - started,
    }
    (output / f"chunk-{index:03d}.json").write_text(json.dumps(record, indent=2))
    assert result.generation_tokens < 8192, "Token limit reached; inspect this chunk"
    records.append(record)
    print(f"Processed {record['end']:.2f} seconds", flush=True)
    mx.clear_cache()
(output / "transcript.txt").write_text("\n\n".join(r["text"] for r in records) + "\n")
metadata = {
    "source": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "duration": len(audio) / rate, "model": model_path,
    "load_seconds": load_seconds, "inference_seconds": sum(r["seconds"] for r in records),
    "peak_mlx_gb": mx.get_peak_memory() / 1e9, "chunks": records,
}
(output / "result.json").write_text(json.dumps(metadata, indent=2))
PY
```

Set `language=None` for automatic detection when the spoken language is unknown.
The English hint is appropriate only when English has been established.
Do not supply captions, previous transcripts, or inferred vocabulary during an independent comparison.

**Long recordings need explicit coverage checks.**
MLX Audio 0.6.4 shares `max_tokens` across internal chunks within one call.
Separate calls above reset that budget for each two-minute chunk.
Fixed boundaries can split words; review neighboring audio before claiming complete word recovery.
Preserve raw chunks when producing any separately reviewed transcript.

Check that chunk ranges cover the entire decoded duration without gaps or unexpected empty text.
Inspect the beginning, ending, repeated passages, and every token-limit warning.
Coverage proves processing, not correctness; silence may legitimately produce empty text.
Keep source URL, selected track, runtime versions, and limitations alongside output metadata.
If a run fails, retain completed chunks and report partial status instead of publishing a complete transcript.

## Whisper Small alternative

### Download the runtime and model

**This step uses the network and consumes local disk space.** It does not read or upload audio.

```sh
uv run --no-project --with mlx-whisper python - <<'PY'
from huggingface_hub import snapshot_download

print(snapshot_download("mlx-community/whisper-small-mlx"))
PY
```

`uv` downloads missing dependencies without adding them to the current project's configuration.
Its cached environment persists after the command exits.
Temporary execution does not imply automatic deletion.
Versions are unpinned, so later dependency resolution can select newer releases.

Default cache locations on this workstation:

- Runtime dependencies: `~/.cache/uv/`.
- Model: `~/.cache/huggingface/hub/models--mlx-community--whisper-small-mlx/`.

Cache environment settings can override these locations.
Use the returned snapshot path rather than hardcoding a machine-specific snapshot identifier.

### Transcribe offline

Replace the example filename with your recording's path. Quote paths containing spaces.

```sh
HF_HUB_OFFLINE=1 uv run --offline --no-project --with mlx-whisper \
  python - "$HOME/Downloads/recording.opus" <<'PY'
import sys

import mlx_whisper
from huggingface_hub import snapshot_download

model = snapshot_download(
    "mlx-community/whisper-small-mlx",
    local_files_only=True,
)
result = mlx_whisper.transcribe(
    sys.argv[1],
    path_or_hf_repo=model,
    verbose=False,
)
print("Detected language:", result["language"])
print(result["text"])
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}-{segment['end']:.2f}] {segment['text']}")
PY
```

The command prints original-language text and segment timestamps, measured in seconds.
It does not translate, modify the recording, or create a transcript file.
Language detection is automatic; add `language="es"` only when Spanish is already established.

`--offline` prevents `uv` downloads; `HF_HUB_OFFLINE=1` and `local_files_only=True` prevent model downloads.
These settings control dependency and model retrieval, not system-wide network access.
Missing caches cause failure rather than an online fallback.
Complete the download step before retrying offline.

**Local inference does not upload audio.**
Returning its transcript through an agent exposes text to that session.
Keep sensitive recordings and transcripts outside repositories unless their storage is explicitly authorized.

## Review uncertain passages

**Treat the output as an automated draft, not verified verbatim speech.**
Successful execution proves the model ran, not that every word is correct.
Names, acronyms, numbers, background noise, and unclear speech can produce mistakes or invented words.

- Preserve the original language unless translation is requested.
- Mark uncertain passages with brackets and timestamps instead of guessing.
- Recheck consequential names, compensation, dates, and benefits against the audio.
- A second pass can expose disagreement but cannot establish which version is correct.
- Context prompts can bias recognition; never treat supplied vocabulary as independent evidence.
- Consider larger models only when accuracy needs justify additional downloads and resource usage.

## Verification and troubleshooting

### Observed Qwen suitability

On an Apple M2 with 24 GB unified memory, four English excerpts were transcribed independently.
Each excerpt lasted 60 seconds; combined inference took 46.4 seconds.
This excludes downloads and model loading.
Initial model loading took 3.2 seconds; peak MLX allocations reached 5.45 GB.
MLX allocations are not total system memory.

Qwen produced “AI slop” where captions and Whisper Small produced “slot.”
It also recovered an apparently omitted clause in the shared service's text.
These comparisons lacked a human-checked reference.
They establish no accuracy percentage or universal winner.

### Fresh-session YouTube verification

A fresh Pi worker started outside dotfiles with no model, command, or guide hints.
It discovered this guide through global instructions and transcribed video `LlhTEttKcwQ` without captions.
It processed all 1999.019 decoded seconds through 17 contiguous, nonempty chunks.
No chunk reached its token limit.
Inference took 355.7 seconds; model loading took 2.2 seconds, with 5.72 GB peak MLX allocations.
The delivered transcript matched the raw chunk assembly and included the recording's closing words.

The first recipe required unavailable `soundfile`.
The worker recovered using Python `wave` and cached NumPy.
The example above incorporates that correction.
This was recovery evidence, not an uninterrupted recipe pass.
Original English audio was selected without dependency installations, model downloads, or external
transcription.
Processing coverage and successful discovery do not establish word accuracy.
Other video hosts remain unverified.

`llmfit` detected the hardware and rated a quantized Qwen variant “Perfect.”
Its quantization assumptions and generic scores do not establish BF16 memory use or transcription accuracy.
Use measured inference and audio review when selecting a model.

### Machine-selection retest

A second fresh Pi session received a 60-second transcription request without model or guide hints.
It discovered this guide and ran `llmfit system` and candidate searches.
It also inspected Whisper large-v3's fit.
It selected cached Qwen BF16 on the current M2 rather than downloading an untested alternative.
The complete excerpt took 12.0 seconds of inference, with 5.45 GB peak MLX allocations.
Word accuracy and performance on other laptops remain unverified.

The worker's exploratory offline Whisper probe installed 36 cached packages into a uv environment.
That violated the test's no-installation constraint despite requiring no model downloads.
Discovery and transcription succeeded, but this was not a clean no-mutation pass.
The selection guidance now distinguishes offline retrieval from installation-free execution.

### Observed Whisper suitability

This workflow processed Spanish WhatsApp `.opus` recordings locally using the cached Whisper Small model.
Both offline dependency resolution and cached model loading succeeded.
Some names and phrases remained uncertain; transcription accuracy was not independently verified.

| Symptom | Next action |
| --- | --- |
| `uv`, Python, or FFmpeg missing | Resolve prerequisites before running transcription. |
| Offline dependency resolution fails | Repeat the download step with network access. |
| Cached model unavailable | Check cache overrides and repeat the model download. |
| Audio cannot be opened | Confirm the quoted path exists and FFmpeg can decode it. |
| Poor transcription | Review the audio, mark uncertainty, and assess whether another model is warranted. |

[MLX Audio](https://github.com/Blaizzy/mlx-audio) owns Qwen's runtime interfaces.
[MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) owns the alternative API.
[yt-dlp](https://github.com/yt-dlp/yt-dlp#readme) documents acquisition and track selection.
