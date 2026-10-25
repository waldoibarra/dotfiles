# Pi and live voice

**Use Pi for coding, with optional voice conversation while the coding agent works.**
The `pi-live-codex` extension runs a separate voice model and can delegate requests to Pi.
Both use the configured OpenAI Codex subscription login.
Voice and coding do not share a complete transcript.

**Experimental:** the extension uses an internal Codex voice connection, not a supported public
Realtime API contract. Working account access and voices can change independently of this
repository.

## Choose a task

| Need | Guide |
| --- | --- |
| Install, update, authenticate, or verify Pi | [Installation and sync](installation.md) |
| Change settings, context windows, shortcuts, or instruction loading | [Configuration](configuration.md) |
| Select worker roles and models | [Delegation](delegation.md) |
| Choose a voice or troubleshoot access | [Live voice](live-voice.md) |
| Understand context loss, cancellation, and evidence limits | [Limitations and trial evidence](limitations.md) |

## Components and ownership

Mise owns the Pi binary; Dotbot links configuration into the normal `~/.pi/agent` profile.
The updater reconciles voice, delegation, and Lens packages from tracked settings.
Login, microphone permission, credentials, and session data remain machine-local.

[Configuration](configuration.md#managed-files) owns the file inventory and coding defaults.
[Live voice](live-voice.md) owns voice choices and controls.
[Trial evidence](limitations.md#trial-environment) records tested versions without treating them as
current pins.

Read [workstation setup](/docs/setup.md) before provisioning a new machine.
Read [sync boundaries](/docs/tooling.md#sync-the-workstation) before running `dots`.
