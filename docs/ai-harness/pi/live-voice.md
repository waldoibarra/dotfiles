# Pi live voice

**Use `/live` to start or stop voice, and `/live spruce` to select Spruce while stopped.**
The inspected `pi-live-codex` extension uses `gpt-live-1-codex`, independently of Pi's coding model.
Voice names change its sound, not the coding or voice model.
Commands below describe the tested extension; account access and later releases can differ.
Read [installation](installation.md) before changing packages or subscription authentication.

## Commands and controls

| Command or key | Behavior in the tested extension |
| --- | --- |
| `/live` | Toggles live voice; a new session uses Sol. |
| `/live spruce` | Starts with Spruce when voice is stopped. Explicit names do not become a saved default. |
| Ctrl+L | Toggles live voice; a new session uses Sol. |
| Esc | Ends the voice session. |
| Space with an empty editor | Mutes/resumes microphone input. |
| `/model` | Selects the coding model, not the voice model. |
| `pi --continue` | Resumes a saved coding session; it does not establish voice-context recovery. |

`/live` is a toggle, not an in-session voice-change command. A stopped session is needed before
starting another voice. The extension's prompt requests silence on connection.
Silence before the first spoken question does not by itself indicate failure.

## Tested voices

Waldo confirmed these nine voices during the [recorded trial](limitations.md#trial-environment):

| Voice | Command |
| --- | --- |
| Arbor | `/live arbor` |
| Breeze | `/live breeze` |
| Cove | `/live cove` |
| Ember | `/live ember` |
| Juniper | `/live juniper` |
| Maple | `/live maple` |
| Sol | `/live sol` |
| Spruce | `/live spruce` |
| Vale | `/live vale` |

Spruce is Waldo's manual choice.
The inspected extension hardcodes Sol for bare `/live`, Ctrl+L, and its controller fallback.
It had no supported default-voice setting.
A default-voice patch was declined; package updates must retain unmodified upstream behavior.

No reliable age, gender, or per-voice accent catalog was established for this model.
Changing text wording or claiming a British accent did not prove a change in audible delivery.

## Misleading autocomplete and access errors

The extension suggests Sol and public Realtime names.
Those names are Alloy, Ash, Ballad, Cedar, Coral, Echo, Marin, Sage, Shimmer, and Verse.
Several working Codex voices are absent from autocomplete.
The command handler passes explicit names through to `audio.output.voice`.

An attempt with Ash showed `Voice session access denied`.
Waldo reported the same error with other suggested alternatives.
The full set of failed names was not recorded. Sol and the eight other
confirmed voices worked.
The error does not establish a Sol-only restriction or identify an authentication failure.
Compare with a known-working voice before changing anything else.
Diagnose persistent rejection without a billing fallback.

[OpenAI Codex source](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs)
groups the nine confirmed names separately from public Realtime voices. An
[OpenClaw integration report](https://github.com/openclaw/openclaw/pull/133079) documents successful
Cove and Spruce speech round trips and a mismatched voice picker. Another
[subscription user report](https://github.com/openclaw/openclaw/issues/154468) confirms Cove. A
[Hermes Conduit change](https://github.com/kaishi00/hermes-conduit/pull/262) reports Cove and Ember.
These support the distinction but do not guarantee account availability. The
[public Realtime guide](https://developers.openai.com/api/docs/guides/realtime-conversations)
describes a different API contract.

## Connection and access boundary

The inspected extension posts voice signaling to
`https://chatgpt.com/backend-api/codex/realtime/calls` and uses an OpenAI live WebSocket sideband.
It identifies itself as Codex Desktop and attempts Apple DeviceCheck attestation on macOS arm64.
These are upstream behaviors, not a maintained public API guarantee. An access rejection is not
permission to alter identity or attestation or switch billing routes.

## Related references

- [Observed behavior and accepted limitations](limitations.md), including context loss and delegation.
- [Keybinding configuration](configuration.md#keybindings).
- [Reviewed voice package README](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/README.md)
  and [transport source](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/transport.ts).
