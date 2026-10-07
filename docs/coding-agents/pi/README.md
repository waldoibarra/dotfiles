# Pi and live voice

Pi runs the coding agent. The `pi-live-codex` extension adds a separate voice model that can delegate
work to it while conversation continues. Both use the configured OpenAI Codex subscription login.

**Experimental:** the extension uses an internal Codex voice connection, not a supported public
Realtime API contract. Working account access and voices can change independently of this repository.

`dots` installs or upgrades Pi through Mise, links its shared instructions and profile preferences
through Dotbot, then installs or updates `pi-live-codex` through the coding-agent updater. Login
and microphone permission remain interactive.

| Task | Guide |
| --- | --- |
| Understand installation, updates, authentication, and verification | [Installation and sync](installation.md) |
| Change model defaults, context windows, shortcuts, or instructions | [Configuration](configuration.md) |
| Choose a voice, use the controls, or diagnose access errors | [Live voice](live-voice.md) |
| Review test evidence, accepted limitations, and future improvements | [Limitations](limitations.md) |

For a new machine, start with [workstation setup](../../setup.md). Read the
[sync boundaries](../../tooling.md#sync-the-workstation) before running `dots`.

## Components and ownership

| Component | Owner and configuration |
| --- | --- |
| Pi binary | Mise: `npm:@earendil-works/pi-coding-agent = "latest"` in [global tools](../../../home/.config/mise/config.toml). Trial version: 1.0.4. |
| Node | Mise's existing `lts` selection. Trial runtime: 24.21.0; Pi required Node 22.19 or newer. |
| Voice extension | Pi package `npm:pi-live-codex`, unpinned and unmodified. Trial version: 0.1.9. |
| Profile | Normal `~/.pi/agent` directory, not a separate trial profile. |
| Coding model | Provider `openai-codex`, default model `gpt-6-astra`. A session can override this default. |
| Voice model | `gpt-live-1-codex`, selected by the extension independently of the coding model. |
| Voice choice | Sol by default. Spruce is selected manually with `/live spruce`. |
| File search | Pi's private `~/.pi/agent/bin/fd`; the trial verified version 10.5.0. No second package owner was added. |
| Shell alias | Existing `pi='caffeinate -i pi'` keeps the workstation awake while Pi runs. |
| OMP | Remains installed with its configuration and credentials intact. |

Both Pi and the voice package follow latest releases. The tested versions describe the trial;
they are not version pins or guarantees about later releases. Homebrew does not own a second Pi
installation. The existing Codex CLI is not required for Pi's login, and its login does not transfer
automatically to Pi.

The extension's trial dependencies included `ws` 8.22.0 and `@oh-my-pi/pi-natives` 18.4.9, with an
optional Apple Silicon native package. This dependency does not run the OMP agent. Native audio
exports loaded successfully; no blanket dependency-build exception was added. Live voice was
validated on Apple Silicon macOS, not Debian.
