# Pi workstation trial notes

Running record of Waldo's configuration decisions, observed behavior, and adoption requirements.
Read these notes before continuing the trial or proposing dotfiles integration. Read the
[trial plan](pi-live-codex-trial.md) before voice testing; the deviations below supersede its
installation and version-pinning instructions for this run.

This is a versioned trial record. Never record credentials, device codes, callback URLs, or raw
private audio here.

**Current direction:** Waldo has requested Phase 5 integration through `dots` and maintained
documentation using Ghostwriter. The [integration summary](pi-dotfiles-integration-summary.md)
consolidates the configuration, trial results, accepted limitations, and remaining implementation
decisions. Earlier statements below withholding adoption describe the decisions at those points
in the trial. Phase 5 is now implemented and applied through a successful `dots` run. Maintained
setup and limitation documentation lives in the [Pi guides](../../docs/coding-agents/pi/README.md).
See the Phase 5
verification record below; no fresh microphone test was run during provisioning.

## Configuration ownership correction

Waldo rejected the speculative merge layer (YAGNI), then questioned whether Pi needed the
managed-copy exception at all. The final implementation uses native Dotbot links for settings,
models, and keybindings. Pi was removed from the copy list. Its native settings writer was tested
against a disposable symlink: it updates the target without replacing the link. Pi UI edits can
therefore change tracked configuration, which should be reviewed before committing.

Credentials, sessions, and locks remain separate and untouched. The custom merge helper, its test
file, the extra `sync-pi.sh` wrapper, and `just check-pi` were removed. Voice-package reconciliation
is a short function in the existing updater. Earlier merge/copy implementation and test descriptions
below are historical and superseded by this decision.

Waldo also requested native Herdr integrations on OMP and Pi, and RTK on Pi. The existing updater
now maintains those generated extensions outside Git using Herdr status and RTK dry-run checks.
Native installers do not modify Pi's JSON settings. Herdr requires the extension directories to
exist; the updater creates them only when needed. No custom extension code was added.

Verification: isolated fresh and repeated installs passed without changing JSON settings. Native
Herdr extensions reported lifecycle/session events to a test socket; RTK's native Pi tool handler
rewrote `git status` to `rtk git status`. The real `dots` run completed with exit status 0, installed
the extensions, and replaced the previous Pi copies with links using Dotbot backups. Herdr reports
Pi v9 and OMP v10 current; RTK's subsequent Pi dry run has no changes. Pi's offline resource loader
loads voice, RTK, and Herdr without errors. Pi authentication and OMP configuration checksums remain
unchanged. Live Herdr pane rendering and new microphone interaction were not tested.

Committed as `e3bdc5e` (Pi setup/docs) and `433219e` (Herdr/RTK integrations), with lint and commit
hooks passing. Working tree clean; commits were not pushed. No skill-lockfile update or automatic
commit/push occurred during the final sync. Restart Pi and OMP to load the new integrations.

## Decisions and deviations

- Waldo chose his **normal workstation environment and normal Pi profile**, not the isolated trial
  workspace or a separate `PI_CODING_AGENT_DIR`.
- Install globally through **mise**, using **`latest` rather than pinned versions**. The voice package
  likewise uses the unversioned `npm:pi-live-codex` declaration, resolving to the latest release.
- Waldo explicitly accepted the incidental change to the symlinked global mise configuration in the
  dotfiles checkout. This does **not** authorize repeatable Pi provisioning, instruction/skill
  integration, workstation sync, or a commit.
- Preserve OMP, its configuration, and its credentials. Use existing subscription-backed Codex
  authentication; do not introduce API-key billing or purchase credits.
- Keep recording configuration choices during testing so Waldo can review them another day and
  decide what should become managed configuration after adoption.

## Installation and authentication baseline

Installed with:

```sh
mise use --global --fuzzy 'npm:@earendil-works/pi-coding-agent@latest'
```

- npm's latest release at installation was Pi **1.0.4**. The saved version selector is `latest`.
- Existing Node was **24.21.0**, selected through mise's `lts` declaration; no Node upgrade was made.
- The global declaration is in `~/.config/mise/config.toml`, linked to the repository's
  `home/.config/mise/config.toml`.
- `pi --version`, `pi --help`, and launch resolution in a fresh interactive Zsh shell succeeded.
  The existing shell alias is `pi='caffeinate -i pi'`; it was not added or changed during this trial.
- Waldo confirmed that the normal Pi TUI opens, he completed subscription login, selected a GPT
  model, and received working text responses.
- Normal-profile defaults are provider `openai-codex` and model `gpt-6-astra`.
- The voice package is installed and its command/native bindings load. Waldo subsequently reported
  a working spoken trial and a preference for Pi over OMP; see the manual results below.

## 1. fd dependency

### Observation and explanation

Waldo reported Pi's startup message that `fd` was missing, followed by its download/installation
into Pi's agent bin directory. The exact installation interaction was not observed by the assistant.
A subsequent direct check confirmed:

```text
~/.pi/agent/bin/fd --version
fd 10.5.0
```

`fd` searches for files and directories by name or pattern. It is a supporting CLI utility, not an
agent or model, and is distinct from searching file contents. It respects `.gitignore` and skips
hidden files by default. Pi's private executable does not by itself establish shell-wide availability.

### Adoption consideration

Record Pi's dependency ownership explicitly when adopting it. The current working arrangement is
Pi's own `~/.pi/agent/bin/fd`; no global mise or Homebrew `fd` declaration was added. Do not add a
second package owner merely because the initial startup needed this executable. On a fresh-machine
smoke run, verify the dependency is available to Pi and startup no longer reports it missing.

## 2. Maximum OpenAI Codex context windows

### Requested behavior

Waldo wants each available OpenAI Codex model to use its maximum context capacity, rather than
Pi's smaller default. He clarified that he meant approximately **one million**, not one billion,
tokens. This is a normal-profile preference, not yet a managed dotfiles feature.

### Findings

- Pi's catalog and CLI initially reported **272,000** context tokens for `gpt-6-astra` and the other
  larger Codex models below. Spark reported **128,000**.
- OMP has an `extendedContext` boolean, already enabled in Waldo's global OMP configuration. Its
  description warns that larger windows can incur premium pricing. OMP was not changed.
- Pi **1.0.4** has no equivalent toggle in its settings reference or built-in slash-command list.
  The actual `/settings` TUI was inspected; a `context` search found no matching settings.
- Pi supports per-model metadata overrides in `~/.pi/agent/models.json`. Do not edit the generated
  `models-store.json` cache to express this preference.
- OpenAI's model documentation lists **1,050,000** total context tokens and **128,000** maximum
  output tokens for the eight expanded models. The GPT-5.6 and GPT-6 family pages additionally
  specify **922,000** maximum input tokens.

### Applied configuration

Created `~/.pi/agent/models.json` with `providers.openai-codex.modelOverrides`. Each of these exact
model IDs has `contextWindow: 1050000`:

- `gpt-5.5`
- `gpt-5.6-luna`
- `gpt-5.6-sol`
- `gpt-5.6-terra`
- `gpt-6-astra`
- `gpt-6-luna`
- `gpt-6-sol`
- `gpt-6.1-sol`

Left `gpt-5.3-codex-spark` at its catalog limit of **128,000**; no override was needed.

Updated `~/.pi/agent/settings.json`:

- `compaction.enabled: true`.
- `compaction.modelOverrides["openai-codex/<model-id>"].reserveTokens: 128000` for each expanded model.
- The resulting compaction threshold is above **922,000** context tokens, reserving output space
  rather than treating the entire total window as input. This reserve also influences compaction
  summary output limits; it is not solely a trigger threshold.
- Existing provider/model defaults and unrelated settings were preserved.

### Verification and limits

- `mise exec -- pi --list-models openai-codex` resolved all eight expanded windows and retained
  Spark's original limit.
- A fresh normal-profile TUI showed Astra at `0.0%/1.1M (auto)` and `Auto-compact true`.
  Pi rounds **1,050,000** to **1.1M** for display.
- Verification sent no model prompts and consumed no inference allowance. Requests above the old
  272K boundary have **not** been tested against the subscription backend. Client metadata and API
  documentation do not alone prove subscription-route acceptance at the maximum window.
- Restart Pi to load both files; `pi --continue` resumes the saved conversation. Waldo has not yet
  reported the result of restarting after this change.
- Overrides cover the exact current IDs, not future models automatically. Recheck documented
  capacities when adding models. Do not set every model to 1M indiscriminately.

### Context configuration adoption

After explicit approval, preserve these model-window and per-model compaction preferences through
safe individual files using existing dotfiles conventions. Re-evaluate whether the adopted Pi
version has gained a native extended-context setting before retaining manual overrides. Keep auth,
sessions, caches, and machine-local data unmanaged; do not link or copy the entire `~/.pi/agent`
directory. No dotfiles integration was made for this context configuration.

### References

- Read [Pi model configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md)
  before changing model metadata or choosing a future replacement for the overrides.
- Read [Pi compaction configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md#per-model-overrides)
  before adjusting the output reserve or threshold.
- Read the OpenAI model specifications before changing maximum windows:
  [GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5),
  [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna),
  [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol),
  [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra),
  [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra),
  [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
  [GPT-6 Sol](https://developers.openai.com/api/docs/models/gpt-6-sol), and
  [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol).
- Read [OpenAI's Spark announcement](https://openai.com/index/introducing-gpt-5-3-codex-spark)
  before assuming Spark shares the larger models' capacity.

## 3. Live voice package setup

### Voice installation and source review

Waldo asked the assistant to prepare the installation and leave actual voice testing to him.
The npm latest release was still **pi-live-codex 0.1.9**, compatible with the installed Pi **1.0.4**
and Node **24.21.0**. Installed without a version pin from outside the dotfiles checkout:

```sh
env -u OPENAI_API_KEY mise exec -- pi install npm:pi-live-codex --no-approve
```

- Installation succeeded and added four npm packages.
- `pi list` reports a user package, `npm:pi-live-codex`, at
  `~/.pi/agent/npm/node_modules/pi-live-codex`. Pi saved its declaration in the normal profile's
  `settings.json`; no project-local package declaration was created.
- The package depends on `ws` **8.22.0** and `@oh-my-pi/pi-natives` **18.4.9**, with an optional
  platform package providing the Apple Silicon binary. Those versions are upstream dependency
  choices, not a pinned top-level trial package. No blanket build-script exception was added.
- Source review covered the manifest, README, extension startup/command registration, native
  loader, credential lookup, transport, attestation, and shared voice-lock location.
- Voice requests use Pi's `openai-codex` provider credential. No credential file was printed or
  copied. The setup/probe processes removed inherited `OPENAI_API_KEY` from their environments;
  the user's shell environment was not changed.
- The transport uses experimental Codex Desktop signaling at
  `https://chatgpt.com/backend-api/codex/realtime/calls` and an OpenAI live WebSocket sideband.
  It identifies itself as Codex Desktop and attempts Apple DeviceCheck attestation on macOS arm64.
  This is the unmodified upstream implementation, not an officially supported public voice API.
- The shared microphone lock is `~/.pi/pi-live-codex.lock`, outside the agent directory. Its
  token-authenticated loopback handoff endpoint coordinates Pi voice sessions. Do not delete
  another session's lock or assume it prevents conflicts with other applications using the mic.
- The voice model is `gpt-live-1-codex`, distinct from coding model `gpt-6-astra`; default voice is
  `sol`. This setup did not change the voice model, prompt, or voice selection.

### Observed voice load result

- Loaded the native `AudioCapture`, `LiveWebRtcPeer`, and `deviceCheckGenerateToken` exports
  successfully under Node, without constructing audio objects or calling attestation.
- Opened the actual Pi TUI with extensions enabled and unrelated discovery disabled. Startup
  listed `pi-live-codex`; typing `/li` showed the registered `/live` command.
- Did **not** submit `/live`, open the microphone, connect voice to OpenAI, or send a model prompt.
  The probe exited normally.
- Existing expanded context settings still showed Astra at `1.1M (auto)`.

### Ctrl+L voice shortcut

Initially Pi skipped the extension's `ctrl+l` shortcut because `app.model.select` already owned it.
Waldo then explicitly requested Ctrl+L for voice. Created `~/.pi/agent/keybindings.json`:

```json
{
  "app.model.select": [],
  "app.tree.filter.labeledOnly": "alt+l"
}
```

Disabling the model-selector binding exposed a second conflict with the tree's labeled-only filter.
That filter now uses **Option+L** (Alt+L); `/model` still opens the model selector. No extension patch
was needed.

A fresh Pi TUI started without extension issues, and `/hotkeys` showed **Ctrl+L — Toggle
gpt-live-1-codex voice mode**. The assistant did not press the shortcut or activate audio during that
probe. Restart Pi to load the change; Pi also documents `/reload` for keybinding changes. Preserve
this keybindings file alongside the accepted voice configuration if dotfiles adoption is approved.

### Waldo's manual voice checks

1. Stop any other live microphone session normally. Restart Pi (`pi --continue` to resume).
2. Press **Ctrl+L** or enter `/live`; grant macOS microphone permission if requested.
   Wait for connection, then ask a short spoken question. The prompt tells voice to remain silent
   on connection, so silence before speaking is not by itself a failure.
3. Interrupt a longer answer and check that playback yields and the next response follows the new
   question. Record latency, missed interruptions, and recognition errors.
4. With an empty editor, press Space to mute/resume. Check that a unique phrase spoken while muted
   is not acted on. Press Esc to end voice and confirm the mic is released.
5. In a disposable workspace, ask for a small coding task while continuing to talk; verify actual
   files/results rather than accepting spoken completion claims.
6. Record pass/fail/not-exercised observations here. If authentication or eligibility fails, retain
   only the redacted error and stop at that boundary; do not switch to API billing or alter client
   identity/attestation to work around rejection.

Queue/cancellation, restart recovery, one-question behavior, and allowance measurement still need
the scenarios in the original plan. Known hardcoded-prompt and recovery gaps remain open.

### Initial manual results reported by Waldo

Evidence: Waldo's account of a quick live trial, not an assistant-run microphone test. No timing,
quota measurement, repeated-trial count, or coding output was supplied.

| Scenario | Status | Waldo's observation |
| --- | --- | --- |
| Overall spoken experience | Positive initial assessment | It worked better than OMP overall; he liked it and had a good feeling about the experience. |
| Interrupting the voice model mid-sentence | Pass in the quick sample, with latency caveat | Playback stopped mid-sentence when interrupted, but not immediately. No delay was measured. |
| Ordinary conversational turn-taking | Positive initial assessment | Voice generally did not interrupt him while he was speaking. |
| Speech while the coding agent is working | Issue observed | Voice sometimes cut across his speech abruptly while coding work was in progress. |
| Source of the abrupt interruption | Not verified | Waldo suspects the coding agent sends an update that causes the voice model to speak. The exact event and whether it is progress or completion are not established. |

The reported spoken exchange establishes that basic live voice worked in this trial. It does not
establish interruption reliability across repeated samples, correct handling of the replacement
question, or verified concurrent coding results. Waldo subsequently confirmed mute/resume works:
muted speech was ignored and conversation resumed after pressing Space again. Record this as a
user-reported pass, not an assistant-run microphone test. Queued delivery and cancellation were
subsequently exercised; see the results and Waldo's acceptance decision below. One-question policy
and subscription usage have not yet been reported. Voice stop/restart context recovery was
subsequently tested by Waldo; see the result below.

**Carry-forward issue:** preserve user speech when coding-work updates arrive. Keep it distinct from
the small delay when the user interrupts playback; these are different directions of interruption.
No extension modification or specific remediation has been authorized. Positive initial preference
is not approval for dotfiles adoption or OMP retirement.

### Voice-to-coding-agent handoff context

Waldo reports that he had already confirmed mute/resume in spoken conversation, but the coding
agent asked for confirmation again. He suspects the voice delegation omitted the surrounding
conversation. Record this as a reported handoff-context issue, not a verified cause: the exact
delegation payload was not inspected. Do not assume the coding agent receives the full spoken
conversation. This is distinct from context loss after stopping/restarting voice. Mute/resume
remains user-confirmed passed; the subsequent queue/cancellation results are recorded below.

A subsequent handoff test produced a repeated clarification loop. Waldo discussed a monetization
topic with voice, then repeatedly asked it to pass that context to the coding agent. The requests
visible to the coding agent contained generic delegation instructions or the topic name, but not
the discussion details. Waldo also reported that a delegated request differed from what he had
actually said. No raw voice transcript or internal delegation payload was inspected, so do not
attribute the failure specifically to transcription, voice summarization, or transport.

The practical failure is that relevant spoken context did not reach the coding agent despite
repeated explicit requests. The earlier successful manual context handoff is not proof of reliable
handoffs in both directions. The proposed Lantern recall test was inconclusive because its facts
already appeared in the coding conversation. Waldo requested documentation only and chose to move
on: do not investigate, patch, or repeat this test without a new request.

#### Idea: incremental transcript handoff

Waldo now reports that `/live` delegation sends only his last spoken message, omitting earlier
conversation. This is user-reported behavior; the exact payload and cause remain unverified.

**Proposal:** have the voice model send transcript sections to the coding agent. Each section
contains all conversation since the previous section was sent, including both speakers' turns in
order—not just the latest request or a summary. The first section starts at the beginning of the
voice session. This preserves the requirements, clarifications, and decisions behind delegated work.

- Include the unsent section when delegating. Whether to send context-only sections between
  delegations remains an open design question.
- Track successful delivery so failures do not discard unsent turns and retries do not duplicate work.
- Preserve speaker labels; sharing context does not itself authorize execution.
- Verification scenario: discuss requirements over several turns, then say “implement it.” The
  coding agent should receive all unsent turns. The next handoff should include only new turns,
  with earlier sections retained in the coding session's context.

Idea only: documentation requested, not investigation, testing, or extension changes.

### Queued delivery and cancellation trial

Waldo reports speaking file-creation and cancellation requests while harmless 20- and 40-second
waits were running. The coding agent received and executed the creation requests after the waits;
cancellation requests reached it after the files already existed. This pattern repeated for
`test-two.md`, `learned.obj`, and `content.obj`. All files were empty and created in a disposable
temporary directory, not the repository. Completed creations were not undone or deleted.

Evidence supports eventual delivery and execution of the tested creation requests. It does not
locate the buffering layer (voice delegation versus coding-agent queue), establish exactly-once
semantics generally, or prove pending delegations are technically impossible to cancel. No queue
trace or speech/delegation timestamps were captured. Cancellation did not prevent creation in
these attempts; cancellation of a demonstrably pending task remains unverified.

**Waldo's acceptance decision:** queued, non-abortable delivery is acceptable to him as long as
requests are delivered. Stop pursuing cancellation tests or fixes under this trial unless he asks
again. Treat this as acceptance of the observed limitation, not a successful cancellation test.
It does not establish delivery guarantees across voice stops, network errors, or process restarts,
and does not authorize overall dotfiles adoption.

### Voice stop/restart context recovery

Waldo reports that stopping and restarting voice **does not automatically carry over the previous
conversation context**. The plan's automatic recovery requirement therefore fails in his trial.

A manual workaround works: after restarting voice, Waldo can explicitly ask it to delegate to the
main coding agent for context, and that agent can provide a contextual handoff. This is
user-requested reconstruction, not automatic voice-session continuity or proof that every spoken
turn, decision, and pending question survives. Exact completeness was not measured.

This finding applies to stopping/restarting voice, not quitting/relaunching Pi or recovering from a
network error. Those scenarios, and recovery of queued work, remain unverified. No fix was applied.
Waldo says context recovery is important, but the manual workaround is better than nothing and he
wants to move on for now. Keep automatic recovery marked as not working in the current setup;
this is not a passed test, a request for remediation, or approval for overall adoption.

### Voice selection findings and manual results (October 6)

Waldo confirmed **Sol, Cove, and Ember** work in his setup. He subsequently identified the voice
he was using as **Spruce**, requested it as the default, then chose to select it manually instead
of customizing the extension. Treat Spruce as user-reported working, not an independently captured
session configuration. The assistant cannot identify the active voice from conversation text alone.

#### Models versus voices

Direct inspection of installed files, rather than relying only on these notes, confirmed:

- `~/.pi/agent/settings.json`: default coding provider `openai-codex`, model `gpt-6-astra`.
  These are profile defaults; a session may override the coding model.
- `~/.pi/agent/npm/node_modules/pi-live-codex/protocol.ts`: live model `gpt-live-1-codex`.
  The session payload sends the selected voice in `audio.output.voice`.
- Voice names such as `sol`, `cove`, `ember`, and `spruce` select the sound of the live model;
  they are not separate coding or voice models.

| Voice | Evidence in this trial | Command |
| --- | --- | --- |
| Sol | Explicitly confirmed working by Waldo | `/live sol` |
| Cove | Explicitly confirmed working by Waldo | `/live cove` |
| Ember | Explicitly confirmed working by Waldo | `/live ember` |
| Spruce | Waldo identified the current working voice as Spruce and chose manual use | `/live spruce` |
| Arbor, Juniper, Maple, Vale | Subsequently confirmed working by Waldo | `/live <name>` |
| Breeze | Subsequently confirmed working by Waldo | `/live breeze` |

Waldo subsequently confirmed that **all nine voices in the table work**: Sol, Cove, Ember, Spruce,
Arbor, Breeze, Juniper, Maple, and Vale. These are user-reported live results, not assistant-run
microphone tests.

#### Misleading suggestions and access errors

The installed extension's `index.ts` suggests `sol` plus the public Realtime voices `alloy`, `ash`,
`ballad`, `cedar`, `coral`, `echo`, `marin`, `sage`, `shimmer`, and `verse`. Its command handler passes
explicit voice arguments through; suggestions are not an enforced allowlist or proof of backend
support. This is why Cove, Ember, and Spruce can be requested even though absent from autocomplete.

Waldo's screenshot showed **"Voice session access denied"** after attempting Ash. He reported the
other alternatives he tried failed the same way while Sol continued to connect. The complete set
of failed names was not individually recorded; do not mark every suggested voice as tested.
The assistant initially inferred a Sol-only account restriction, then corrected that unsupported
claim. Successful alternative voices disprove the Sol-only explanation for this setup. The generic
error alone does not distinguish a rejected voice from an authentication or entitlement problem.

Internet research found stronger evidence for separate voice families:

- [OpenAI Codex source](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/protocol.rs):
  `RealtimeVoicesList::builtin()` groups Juniper, Maple, Spruce, Ember, Vale, Breeze, Arbor, Sol,
  and Cove in `v1`, with Cove as its default. The public Realtime names appear in the separate
  `v2` list. Those are the source's list labels, not a claim about this extension's protocol version.
  A source declaration is not a successful backend test for each voice.
- [OpenClaw repair and live results](https://github.com/openclaw/openclaw/pull/133079): reports
  successful subscription speech round trips with Spruce and Cove, and a mismatched voice picker
  offering GA Realtime names rejected by the Codex GPT-Live contract. This is third-party evidence,
  not an OpenAI availability guarantee.
- [OpenClaw user report](https://github.com/openclaw/openclaw/issues/154468): reports
  `gpt-live-1-codex` with Cove working through subscription authentication.
- [Hermes Conduit voice picker](https://github.com/kaishi00/hermes-conduit/pull/262): lists the nine
  names but explicitly limits its confirmation to Cove and Ember.
- [OpenAI public Realtime guide](https://developers.openai.com/api/docs/guides/realtime-conversations):
  lists the public API voices, not proof that they work on this experimental Codex connection.

Upstream links are mutable; these describe what was inspected during this session. The practical
finding is a voice-family mismatch in suggestions, not proof of every backend eligibility rule.

#### Selection decision and remaining limits

- Waldo declined extension customization. **Keep the package unmodified and select Spruce manually
  with `/live spruce` whenever wanted.** Stop the current voice session normally before starting
  another; `/live` is a toggle, not an in-session voice-change command.
- Installed `index.ts` hardcodes **Sol** for bare `/live` and **Ctrl+L**. No supported default-voice
  setting was found. They do not remember the last explicitly selected voice. The controller's
  fallback is also Sol. Do not confuse the upstream Codex default Cove with this package's default.
- No voice default, package source, keybinding, or profile setting was changed in this session.
  This decision does not authorize a patch, fork, dotfiles integration, or OMP retirement.
- Earlier assistant tables assigning voice gender/character were not verified for this model.
  No reliable age, gender, or per-voice accent catalog was established. A text reply claiming to
  switch to British English did not establish an actual audio-accent change.
- Waldo reports that transcription struggles with certain names and words, including the agent's
  name. Several spoken requests were misunderstood during the exchange. Recognition versus
  assistant interpretation was not isolated or measured; no raw audio was retained. Keep this as
  a general usability observation rather than a record of each misheard word. Do not mark speech
  recognition quality, restart-context recovery, or concurrent coding correctness as fully passed
  from this conversation alone.

### Evaluation scope accepted by Waldo

After reviewing the remaining plan checks, Waldo chose to use the behavior observed in this session
rather than repeat every synthetic scenario:

| Check | Current disposition |
| --- | --- |
| Coding while talking | Accepted as demonstrated for his workflow: conversation continued while the coding agent edited these notes and created disposable files. The original Node-module/assertion scenario was not run; this is not a general coding-correctness guarantee. |
| Context after coding finishes and voice restarts | No automatic voice context was observed; Waldo accepts that limitation and can ask voice to consult the coding agent. Exact completion-state recovery was not separately demonstrated. |
| Pi restart / network recovery | Not separately tested. Waldo is comfortable proceeding with manual context requests, but voice restart is not proof of process/network recovery, reconnect behavior, or preservation of pending work. |
| Pending-work recovery across interruptions | Still unverified. Acceptance of queued delivery does not establish persistence or absence of duplicate execution after a restart. |
| One spoken question at a time | Passed in the three-question monetization exercise. Questions were asked separately, and Waldo confirmed the spoken experience also behaved that way. |
| Subscription usage | Waldo monitored his OpenAI subscription's weekly usage during approximately one to two hours of conversation and observed little increase. Qualitative evidence only; no before/after values or separate voice/coding attribution were recorded. |

Waldo's working understanding is that voice holds its own conversation and selects what to delegate
to the coding agent; he accepts proceeding on that basis. Do not promise that asking the coding
agent restores the entire spoken conversation: earlier attempts showed omitted context and
clarification loops. This is acceptance of practical limitations and reduced test scope, not proof
that untested recovery scenarios pass. No new investigation, modification, or dotfiles adoption
was authorized by this assessment.

### One-question-at-a-time result

The monetization exercise asked three questions sequentially about experience, reachable customers,
and preferred monetization path. Each answer preceded the next question. Waldo subsequently
clarified that he had answered **yes** to whether the spoken experience also followed that pattern.
Record a user-confirmed pass for this sample, not enforcement or a guarantee across future sessions.
His spoken confirmation was initially missing from the coding agent's recap, reinforcing the
previously recorded handoff-context limitation.

### Subscription usage observation

Waldo reports monitoring his OpenAI subscription's weekly usage limit throughout approximately one
to two hours of conversation and seeing little increase. This is useful real-use evidence without
requiring another dedicated timed trial. No exact starting/ending percentages, reset time, or
voice-versus-coding breakdown were recorded. Do not infer zero cost, a per-minute rate, remaining
voice hours, or whether the meter immediately reflects all activity. The assistant did not inspect
the account usage display. No billing-route change or credit purchase was requested.

### Current preference and future idea — notes only

Waldo describes the Pi voice experience as decent to really good, and likes aspects of both Pi
and OMP voice. For now he may switch between the two, while trying to use Pi more. Keep both
available; this is not a decision to retire OMP or adopt managed Pi dotfiles configuration.

He is interested in potentially combining the best aspects of both voice experiences when more
time is available. This is a future idea only: no design, research, implementation, migration,
or extension customization is requested now. Specific features to combine have not been selected.
This nuanced preference supersedes treating the earlier positive Pi comparison as an exclusive
choice of Pi over OMP.

### Voice adoption consideration

After adoption approval, provision the voice package through Pi's normal package mechanism, retain
the chosen latest-version policy, and preserve the Ctrl+L/Option+L configuration above.
Keep native binaries, credentials, sessions, and voice locks out of tracked files. Installation and
load success alone do not satisfy the voice adoption gate.

Read the [reviewed package README](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/README.md) before
manual testing and the [reviewed transport](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/transport.ts)
before diagnosing connection or eligibility failures.

## Phase 5 implementation and verification

Waldo authorized implementation and a real `dots` run. Mise remains Pi's binary owner at `latest`.
Dotbot links shared `AGENTS.md`; Pi discovers shared skills natively. The coding-agent updater now
merges tracked settings, models, and keybindings into real profile files, preserving unrelated
preferences, then reconciles only `npm:pi-live-codex` through Pi's package mechanism. Spruce remains
manual and the extension remains unmodified. The implementation and accepted limitations are
maintained in the [Pi guides](../../docs/coding-agents/pi/README.md), linked from the
setup/tooling/agent guides and README.

Verification completed:

- `just check-pi`: five isolated tests passed for fresh/repeated merges, preservation, invalid JSON,
  symlink rejection, normal-profile scope, and propagation of package failures.
- A fresh temporary home installed the real voice package; a second reconciliation succeeded
  without duplicate declarations. Dotbot create/link checks passed after supplying the existing
  `~/AGENTS.md` prerequisite. The setup guide now states that requirement before installation.
- The actual `dots` alias ran from `$HOME` in a fresh interactive login Zsh, in the background with
  a pseudo-terminal for prompts. It completed with exit status 0, including the Pi updater and hooks.
- Full sync upgraded Ollama and AWS CLI (2.37.9 to 2.37.10). No skill-lockfile update occurred, so
  the updater did not commit or push. The pre-existing unpushed alias commit remains unpushed.
- Fresh interactive Zsh still resolves `dots` to the repository's `just sync` and `pi` to its
  caffeinated Mise binary. Pi reports 1.0.4; `pi list` includes `npm:pi-live-codex`.
- Model listing shows eight expanded windows and Spark at 128,000. This does not test large-context
  inference. The package and native-loading checks did not open a microphone or make a model call.
- Offline SDK resource discovery passed for both the isolated and normal profiles: `/live` and
  Ctrl+L registered, shared and personal instructions loaded, and no extension/skill diagnostics.
  The isolated profile discovered four repo-authored skills; the normal profile discovered 47.
- Checksums confirmed Pi's auth file and OMP's config were unchanged by sync.
- Repository lint passed before sync; final documentation review uses Ghostwriter. Changes remain
  uncommitted, so another machine cannot fetch this integration until it is committed and published.

The unrelated `TODO.md` working-tree change was left alone. No extension remediation, credential
migration, OMP retirement, or extra billing was performed. Earlier trial verdict text below is
historical; this verification record supersedes its integration-pending status.

## How the run ended

**Trial complete enough to prepare Phase 5; integration summary written, implementation pending.**
Waldo wants repeatable Pi setup through `dots`, with OMP preserved and the documented limitations
accepted. See the [Phase 5 handoff](pi-dotfiles-integration-summary.md). Pi installation and
subscription-backed text use work. The private `fd` binary is present and executable. Expanded
context settings load in Pi, but large-context backend acceptance remains unverified.
`pi-live-codex` and its Ctrl+L shortcut load without conflicts. Waldo reports working spoken
conversation, successful mid-sentence interruption with some delay, and an overall preference for
Pi over OMP. Abrupt voice interruptions during coding work remain an observed issue.
Sol, Cove, and Ember are explicitly user-confirmed working; Spruce is also user-reported working
and is Waldo's chosen manual selection via `/live spruce`. Bare `/live` and Ctrl+L remain on Sol.
The extension was not customized. Voice-family research and its verification limits are recorded
above; no adoption or permanent voice-default change was approved. Waldo subsequently confirmed
all nine voices work, including Arbor, Breeze, Juniper, Maple, and Vale. Transcription difficulty
with certain names and words remains a reported usability issue. Automatic context recovery after
voice stop/restart fails by Waldo's test; explicitly asking voice to consult the main coding agent
provides a working manual context handoff, with completeness unmeasured. Subsequent delegation
attempts also exposed missing-context loops, recorded above. File requests were delivered after
waits, but cancellations arrived too late to prevent creation. Waldo accepts queued delivery without
cancellation for now and wants to move on; no cancellation fix or further test is requested.
He also accepts coding-while-talking as demonstrated by this session's real note/file edits, and
accepts missing automatic voice context. Separate process/network and pending-work recovery remain
unverified rather than failed or passed by analogy; see the accepted evaluation scope above.

Continue collecting Waldo's test feedback and the remaining scenarios above. Investigate the
coding-update interruption only when he asks to diagnose or remediate it; do not silently patch the
baseline. Preserve the trial plan's billing, privacy, microphone, and explicit-adoption gates except
where superseded above. No commits, pushes, `dots`, or updater scripts were run.
