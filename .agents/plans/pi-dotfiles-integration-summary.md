# Pi dotfiles integration: trial summary

Phase 5 is implemented and a full `dots` run completed successfully. Maintained documentation is
[Pi guides](../../docs/coding-agents/pi/README.md), written using Ghostwriter; the
[execution notes](pi-live-codex-trial.notes.md#phase-5-implementation-and-verification) contain the
verification record. OMP remains available. The original pre-implementation summary below is kept
as decision history; its pending-work descriptions are superseded by those documents.

This summary carries forward the [execution notes](pi-live-codex-trial.notes.md) and
[original plan](pi-live-codex-trial.md). It supersedes their earlier statements that adoption had
not been requested. Both the notes and this handoff are versioned decision records. Maintained setup
instructions live in the Pi guides linked above.

## Installation and ownership

| Component | Decision or observed state |
| --- | --- |
| Pi | Mise owns `npm:@earendil-works/pi-coding-agent`, following `latest`. Trial version: 1.0.4. |
| Node | Existing Mise `lts` selection; trial runtime: 24.21.0. Pi required Node 22.19 or newer. |
| Voice package | Pi owns `npm:pi-live-codex`, following latest without a version pin. Trial version: 0.1.9. Keep the package unmodified. |
| Profile | Normal `~/.pi/agent` profile, not the isolated profile proposed in the original plan. |
| Authentication | Existing subscription-backed `openai-codex` login. No API-key fallback, credit purchase, or automatic top-up. |
| Coding model | Normal-profile default `gpt-6-astra`, provider `openai-codex`. Session overrides remain possible. |
| Voice model | `gpt-live-1-codex`, selected by the extension independently of the coding model. |
| File search | Pi downloaded `fd` 10.5.0 into `~/.pi/agent/bin`. Do not add a second package owner without a reason. |
| Shell | Existing `pi='caffeinate -i pi'` alias; preserve it. |
| OMP | Keep installed, with its configuration and credentials intact. |

The trial's global Mise installation already added the Pi declaration to
`home/.config/mise/config.toml`. That tracked file is modified in the working tree; preserve the
existing change. Do not install a competing Homebrew Pi package.

`dots` already calls `just sync`, which runs the Dotbot installer, Homebrew updates/cleanup, Mise
install/upgrade/prune, the coding-agent updater, and hook installation. The Pi declaration therefore
covers the binary through the existing Mise path. The inspected updater does not yet provision
Pi's voice package or manage its profile configuration.

Phase 5 must finish the package/configuration path through these existing owners. Installing the
Pi binary alone does not reproduce the trial. First-run account login and microphone permission
remain interactive user actions; `dots` must not open a microphone or copy credentials.

## Configuration to preserve

Track safe configuration sources under `home/`, then apply them through the existing installer and
updater conventions. Keep `~/.pi/agent` a real directory. Choose individual file links or managed
copies during implementation; do not link the entire profile or import it wholesale.

The accepted profile preferences are:

- Default provider/model: `openai-codex` / `gpt-6-astra`.
- Voice package declaration: `npm:pi-live-codex`.
- Model metadata in `models.json`, not the generated `models-store.json` cache.
- Automatic compaction enabled, with the per-model reserves below.
- Keybindings that leave Ctrl+L available for voice and move the tree filter to Option+L.

The trial's keybinding file contains:

```json
{
  "app.model.select": [],
  "app.tree.filter.labeledOnly": "alt+l"
}
```

`/model` still opens model selection. Ctrl+L starts/stops voice; Esc ends voice; Space with an empty
editor mutes/resumes. Pi's native bindings loaded during setup. Native binaries remain managed
package artifacts, not tracked files.

Exclude authentication, sessions, caches, locks, native binaries, and machine-specific paths from
Git. The shared voice lock is `~/.pi/pi-live-codex.lock`, outside the agent directory. Never remove
an active session's lock as part of installation or validation.

### Extended context

Preserve `contextWindow: 1050000` for these exact `openai-codex` model IDs:

- `gpt-5.5`
- `gpt-5.6-luna`
- `gpt-5.6-sol`
- `gpt-5.6-terra`
- `gpt-6-astra`
- `gpt-6-luna`
- `gpt-6-sol`
- `gpt-6.1-sol`

Leave `gpt-5.3-codex-spark` at 128,000. For each expanded model, the trial uses
`compaction.modelOverrides["openai-codex/<model-id>"].reserveTokens: 128000` and
`compaction.enabled: true`. Pi displays the expanded window as `1.1M (auto)`.

These preferences load successfully in Pi. Requests beyond the old 272,000-token boundary were not
tested against the subscription backend. The 1,050,000 total window is not all input capacity;
128,000 tokens are reserved for output. The reserve also affects compaction summary limits.
Recheck current Pi support and model specifications before carrying the overrides forward. Do not
apply them indiscriminately to future models. Source links are in the execution notes.

## Voice selection

Waldo confirmed all nine voices work in his trial:

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

Waldo selects Spruce manually. Bare `/live` and Ctrl+L remain on Sol. The installed extension
hardcodes that default and does not remember the last voice. He declined a patch or customization.
Stop the current session before starting another voice; `/live` toggles the session.

Autocomplete is misleading: the extension suggests public Realtime voices such as Ash that did
not work in this trial, and omits several working Codex voices. Explicit arguments still pass
through. The observed error was `Voice session access denied`; it alone does not establish an
account entitlement problem. The complete set of rejected voices was not recorded.

OpenAI Codex source separates the nine working names from the public Realtime family. Third-party
reports also describe successful Cove and Spruce calls. These sources support the distinction but
do not guarantee every account's availability. Preserve that qualification in user documentation.
Do not reuse the earlier unverified voice age, gender, or accent descriptions.

## Results and accepted limitations

| Area | Result and disposition |
| --- | --- |
| Text and voice access | Working with the subscription-backed setup. |
| Conversation | Waldo likes both Pi and OMP and plans to use Pi more while keeping both. |
| Interruption | Playback yielded mid-sentence, with some delay. Reliability and latency were not measured. |
| Mute/resume | User-confirmed pass: muted speech was ignored and conversation resumed. |
| Coding while talking | Accepted as demonstrated by real note edits and temporary file creation during conversation. The original Node assertion exercise was not run. |
| One question at a time | User-confirmed pass in a three-question exercise. Not enforced globally. |
| Weekly subscription usage | Waldo observed little increase during approximately one to two hours of conversation. No exact before/after values or voice/coding breakdown. |
| Voice stop/restart | Automatic context recovery failed. Waldo accepts asking the coding agent for context as a manual workaround. |
| Delegation context | Relevant spoken context sometimes failed to reach the coding agent despite repeated requests, causing clarification loops. Root cause unverified; investigation deferred. |
| Queued delivery | Requests spoken during waits were later delivered and executed. The buffering layer was not identified. |
| Cancellation | Requests arrived after file creation, so creation was not prevented. Waldo accepts queued delivery without cancellation; stop testing or fixing it for now. |
| Speech recognition | Difficulty with some names and words. Recognition and assistant interpretation were not isolated. |
| Coding updates during speech | Voice sometimes interrupted Waldo abruptly while coding work was underway. A coding-update trigger is suspected, not proven. |
| Pi restart, network errors, pending work | Separate recovery and exactly-once delivery remain unverified. |
| Voice instructions | Hardcoded in the baseline package. No configurable prompt or accent-control behavior was established. |

Manual context recovery cannot restore speech the coding agent never received. Do not describe
voice and coding as sharing a complete transcript. Source inspection and visible messages establish
configuration and delivery behavior, not the exact missing audio or delegation payloads.

The original plan's isolation and pinning decisions were superseded by Waldo's normal-profile and
latest-version choices. Preserve the remaining privacy and billing boundaries. Acceptance of these
limitations is not evidence that the untested scenarios pass.

## Documentation and integration requirements

Use Ghostwriter for maintained prose. No local Ghostwriter profile was present during this summary;
plain technical documentation is the fallback. Keep trial chronology in these local notes and
publish only durable setup, ownership, usage, and limitations in tracked docs.

| Location | Required coverage |
| --- | --- |
| `docs/setup.md` | Pi installation through the existing workflow; interactive subscription login and microphone permission. |
| `docs/tooling.md` | Mise ownership, latest-version policy, voice-package update behavior, and sync side effects. |
| `docs/coding-agents/README.md` | Pi file ownership, safe managed settings, credentials excluded, and links to the Pi guides. |
| A tracked Pi voice guide, if needed | The two model roles, tested voice commands, shortcuts, manual Spruce selection, errors, and accepted limitations. |
| `scripts/README.md` | The actual Pi provisioning step and its place in the existing updater once implemented. |

Implementation still needs to decide the exact settings ownership, how Pi package install/update
runs idempotently, and how shared instructions and skills reach Pi without duplication. Verify
those against the installed Pi documentation and existing repository conventions. Do not assume
coding instructions also configure the separate voice model.

Validate provisioning first with an isolated home/configuration. Check that repeated runs preserve
unrelated user settings, never touch credentials, and avoid duplicate package declarations. Verify
Pi resolution, package loading, keybindings, model metadata, and instruction/skill discovery.
Waldo performs any live microphone check. Run relevant lint for the changed sources and docs.

Do not run a full sync as validation. When applying the actual workstation changes requires `dots`,
announce it first and follow `docs/tooling.md`. Full sync can remove packages and the skill updater
can commit and push changes, including earlier unpushed commits.

Combining Pi and OMP voice experiences is a future idea. No extension fork, voice-default patch,
context-recovery fix, cancellation fix, or OMP retirement is part of this integration summary.
