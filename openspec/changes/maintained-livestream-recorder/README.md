# Maintained livestream recorder

**Status:** Synthetic acceptance passed. The maintained recorder remains experimental for live acquisition.

This change adds a bounded companion to the [video-analysis skill](../../../home/.agents/skills/video-analysis/SKILL.md).
It stops partial when safe live checkpoint recovery is unavailable.
No automatic full redownload, lossy fallback, credential use, or media deletion is implemented.

## Verification

Run these commands from the repository root:

```sh
python3 scripts/tests/test-livestream-recorder.py
just lint-md
just lint-ec
openspec validate maintained-livestream-recorder --strict --no-interactive
python3 -m py_compile home/.agents/skills/video-analysis/scripts/record_livestream.py scripts/tests/test-livestream-recorder.py
git diff --check
```

The Python suite passed 30 tests after formatting.
Three earlier 30-test runs passed against the frozen candidate before formatting.
Markdown and EditorConfig lint passed.
Strict OpenSpec validation, compilation, skill validation, and whitespace checks passed.
The skill validator used `--policy private home/.agents/skills/video-analysis`.

The frozen candidate recorder hash was `2948774443a2e13741532b625d264b85c18f213bd81cbe44a6e1a8492527f601`.
Its formatting-only source hash is `68c7ee4929adee0b2cbcd14a8e948525ff3fdbdad7df61270d19578c582acd8e`.
The test file changed from `391af34737eb08c8d33fc2377b9c65fc26c2a1b06f6b52fe10cef890bd2d710d`.
Its formatting-only hash is `c1f7814b1ad0a4fba1ca289e261503c03358e2f2680874785069a2d098c44db5`.
Parsed Python ASTs and string-constant sequences matched for both formatting changes.

A fresh worker named `recorder-luna-accept` started at `2026-11-11T02:58:52Z`.
It used `openai-codex/gpt-5.6-luna` with medium reasoning, separate from the author.
It discovered the isolated candidate skill through its `SKILL.md`, not the global installation.
Local synthetic failure retained two partial tracks without a repeated from-start transfer.
Synthetic interruption retained both tracks and stopped partial.
A local completed fixture decoded audio and video, with a matching source-file hash.
No child process remained after testing.
The tester asked no questions and received no author assistance.
Its first output briefly used the task scratch root, then moved into its designated evidence directory.
The report's example command names the moved path, not the original invocation path.

| State | Evidence |
| --- | --- |
| Configured | The isolated candidate used selected format IDs and finite resource limits. |
| Installed | `yt-dlp`, FFmpeg, and ffprobe were present locally. |
| Loaded | Fresh Pi discovery selected the isolated candidate skill over the global copy. |
| Authenticated | YouTube access was not exercised or established. |
| Exercised | Synthetic downloader supervision and local FFmpeg decoding only. |

Independent Fable review passed the frozen candidate and its acceptance evidence.
Independent review confirmed AST and fixture-string equivalence after formatting.
The reviewer found no remaining publication blocker within the simulated scope.

## Limits and recovery

Mocked downloader behavior does not establish YouTube live recovery or broadcast completeness.
Installed `yt-dlp` output names and JavaScript runtime needs remain unverified.
Merge timing and signal behavior also remain unverified.
The current-position combined-output case stops partial when selected tracks cannot be observed separately.
`complete` means a reported source end and sampled audiovisual decodability, not exact broadcast completeness.
Uncatchable `SIGKILL` may leave stale status and an owned child requiring external cleanup.
No actual livestream or private media was acquired during verification.
