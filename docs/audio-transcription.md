# Transcribe audio locally

**Use Whisper through MLX to transcribe audio on an Apple Silicon Mac without uploading the recording.**
Download dependencies and model weights first; subsequent transcription can run offline.
This workflow needs no Ollama server, cloud transcription subscription, or API key.

Read [workstation tooling](/docs/tooling.md) for package ownership and installation guidance.

## Check prerequisites

These commands assume `uv`, Python, and FFmpeg are available:

```sh
command -v uv python3 ffmpeg
```

| Component | Responsibility |
| --- | --- |
| `uv` | Launch Python with dependencies in an isolated, cached environment. |
| `mlx-whisper` | Run Whisper inference through MLX on Apple Silicon. |
| Whisper Small | Supply multilingual speech-recognition model weights. |
| FFmpeg | Decode audio formats, including WhatsApp `.opus` recordings. |
| `huggingface_hub` | Download model files and locate cached snapshots. |

Ollama does not participate in this workflow.
Kokoro voice models generate speech from text; they cannot replace a transcription model.

## Download the runtime and model

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

## Transcribe offline

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

[MLX Whisper documentation](https://github.com/ml-explore/mlx-examples/tree/main/whisper)
owns the upstream API and additional options.
