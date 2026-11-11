# Tasks

## 1. Recorder

- [x] 1.1 Add bounded process-group supervision and persistent run records.
  Check with fake child limits.
- [x] 1.2 Enforce safe partial stopping without recovery retries.
  Check retained hashes and invocation counts.
- [x] 1.3 Verify retained local outputs with ffprobe and bounded decode.
  Check generated audiovisual fixtures.

## 2. Documentation and checks

- [x] 2.1 Document invocation, limits, provenance, progress, stop action, and recovery gaps.
  Check Markdown lint.
- [x] 2.2 Add deterministic temporary-directory tests for requirements R1 through R12.
  Check focused test output.

## Evidence

The [verification summary](README.md#verification) records commands, outcomes, and limitations.
It also records independent review and fresh-worker acceptance.
The final 30-test suite, Markdown lint, EditorConfig lint, and strict OpenSpec validation passed.
Fresh-worker acceptance used an isolated candidate and local synthetic fixtures.

## Limitations

Mocks establish supervision and synthetic end metadata only.
They do not establish YouTube recovery or source-end detection.
`SIGKILL` leaves stale `capturing` status and can leave a child process group.
External supervision must inspect and stop that process group.
