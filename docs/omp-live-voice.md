# OMP live voice

In OMP 18.6.1, terminal `/live` starts a separate realtime model. It does not inherit the coding
session's instruction files or existing conversation. Read
[Agent instructions](/docs/agent-instructions.md) before changing the coding session's rules.

## Startup context

| Component | Behavior |
| --- | --- |
| Model | Requests `gpt-live-1-codex` through Codex OAuth; hardcoded independently of the coding model. |
| Voice | `live.voice` selects a voice preset, not the model; the inspected session uses `sol`. |
| Instructions | Uses the bundled live prompt, with `username` and `firstName` derived from the OS account. |
| Files excluded | `~/.omp/agent/AGENTS.md`, project `AGENTS.md` files and `APPEND_SYSTEM.md` are not injected. |

The personal `~/AGENTS.md` linked through `APPEND_SYSTEM.md` reaches the coding session but not
live startup. Names and preferences loaded in text mode are therefore absent from the default
voice prompt.

The voice prompt directs ordinary conversation to the realtime model. Coding, investigation,
tool use and verification are delegated to the coding session, which returns assistant progress
and its final answer, not its instruction files. Personal questions can therefore receive
different answers within the same UI.

## Custom instructions

The RPC command `live_start` accepts an `instructions` string that **replaces** the bundled prompt.
A custom caller must supply the voice conversation and delegation rules along with personal
instructions. Passing only names and preferences removes those bundled rules.

Terminal `/live` exposes no prompt override setting in this version. Editing `AGENTS.md` alone
does not change its startup prompt. No live prompt override is configured by this repository.
Dictation into the normal session with spoken assistant output avoids the separate conversational model.

## Evidence and limits

The investigation checked the installed model identifier and voice setting, traced the 18.6.1
startup code, and exercised its payload builder offline. No live network handshake was captured;
`gpt-live-1-codex` is the requested identifier, not a verified server-side model revision.

Read these version-pinned sources before changing or rechecking live startup:

- [Model and payload builder](https://github.com/can1357/oh-my-pi/blob/v18.6.1/packages/coding-agent/src/live/protocol.ts).
- [Instruction rendering and delegated results](https://github.com/can1357/oh-my-pi/blob/v18.6.1/packages/coding-agent/src/live/controller.ts).
- [Bundled voice instructions](https://github.com/can1357/oh-my-pi/blob/v18.6.1/packages/coding-agent/src/live/prompts/live-instructions.md).
- [Terminal startup options](https://github.com/can1357/oh-my-pi/blob/v18.6.1/packages/coding-agent/src/modes/controllers/live-command-controller.ts).
- [RPC override contract](https://github.com/can1357/oh-my-pi/blob/v18.6.1/docs/rpc.md#live-voice-sub-protocol).
