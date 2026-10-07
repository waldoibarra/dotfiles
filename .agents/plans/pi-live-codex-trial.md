# Plan: trial Pi with pi-live-codex before dotfiles integration

## Outcome and authority

Give Waldo a real, reversible trial of original Pi with subscription-backed live voice. First prove
installation, authentication, speech, and concurrent coding with the unmodified package. Measure the
known gaps before deciding whether to extend it. Integrate with dotfiles only after it works well
enough for Waldo and he explicitly chooses adoption.

This is the authoritative execution plan, written October 6, 2026. Planning did not install anything,
authenticate, open a microphone, or make a model call. Read the
[spike](../spikes/pi-media-learning-and-live-voice.md#voice-migration-decision) before executing for
prior findings and the full requirement comparison. This plan and that spike are versioned research
records; read the [trial notes](pi-live-codex-trial.notes.md) before resuming work for later decisions.

## Decisions and boundaries

| Question | Decision and evidence | Reconsider only if |
| --- | --- | --- |
| Installation owner | Waldo chose mise first, Homebrew second on October 6. Repository tooling also prefers mise for development CLIs. | A documented mise-specific blocker remains after a narrow diagnosis. |
| Initial candidate | Test unmodified `pi-live-codex` 0.1.9, the version already researched. | The release is unavailable or incompatible; record the evidence and review a replacement version before using it. |
| Pi version | Start with `@earendil-works/pi-coding-agent` 1.0.4, the registry version observed during planning. Node requires 22.19+. | Actual compatibility requires another version; pin and record it rather than silently tracking latest. |
| Trial location | Dedicated workspace and Pi agent directory outside dotfiles; local mise declaration only. | Waldo approves permanent adoption after the trial. |
| Authentication and cost | OpenAI Codex OAuth using existing paid access; no API-key fallback, paid-credit purchase, or automatic top-up. | Waldo separately authorizes a changed billing route. |
| Implementation | No extension modifications during the baseline trial. Known gaps remain requirements, not installation blockers. | Baseline passes and Waldo explicitly authorizes focused remediation. |
| Migration | Preserve OMP, its credentials, and its configuration throughout. | A later, separate decision authorizes retiring OMP; this plan does not. |

No Orb installation, custom local speech stack, course-learning pipeline, new browser tooling, or
unrelated agent integrations are part of this trial. A private Pi directory isolates configuration,
not operating-system access: Pi tools and extension code still run with the user's permissions.
Use only disposable task data and do not describe this as a security sandbox.

## Grounded starting state

Observed during planning:

- `mise --version`: 2026.10.3, macOS arm64.
- `node --version`: v24.21.0, resolved through mise; satisfies the documented Node minimum.
- `command -v pi`: no executable on the current PATH. Check again at execution time; this does not
  prove that no other Pi installation or settings exist.
- npm reports Pi 1.0.4. Homebrew has `pi-coding-agent` 1.0.2, so fallback is a different version.
- `pi-live-codex` 0.1.9 uses the current `@earendil-works/pi-*` peers and native dependency
  `@oh-my-pi/pi-natives` 18.4.9. This does not require running the OMP agent.
- Upstream documents `PI_CODING_AGENT_DIR`, versioned package installs, `/login openai-codex`,
  `/live`, Ctrl+L, Esc, and Space with an empty editor.
- The repository's global mise configuration is linked into `$HOME`. Consequently,
  `mise use --global` would change tracked dotfiles and is forbidden during the trial.

Unverified: the selected Pi/package pair at runtime, native audio loading, microphone permissions,
account eligibility, subscription allowance impact, real interruption quality, and user preference.
Published documentation and source support the setup path; they are not runtime proof.

## Phase 1: install Pi without adopting it into dotfiles

Read [Tooling](/docs/tooling.md) before package operations. Recheck executable paths and existing
trial directories without reading or printing credentials. If the proposed trial directory already
exists, inspect its ownership and recorded purpose; reuse only if it belongs to this trial, otherwise
choose a fresh sibling and record it. Do not overwrite existing Pi settings.

Run these commands only when executing the plan, in a dedicated interactive terminal:

```sh
export TRIAL_ROOT="$HOME/.local/share/pi-live-codex-trial"
umask 077
mkdir -p "$TRIAL_ROOT/workspace" "$TRIAL_ROOT/agent"
export PI_CODING_AGENT_DIR="$TRIAL_ROOT/agent"
cd "$TRIAL_ROOT/workspace"
mise use --path "$TRIAL_ROOT/workspace/mise.toml" --pin \
  node@24.21.0 'npm:@earendil-works/pi-coding-agent@1.0.4'
mise exec -- node --version
mise exec -- pi --version
mise exec -- pi --help
```

Review any mise trust prompt against the new local configuration. Do not enable all dependency
build scripts to work around an error: normal Pi npm installation does not require them. Review
and diagnose any specific installation failure first. Pinning Pi does not by itself pin every
transitive dependency; retain the resolved dependency information for reproducibility.

**Gate:** `pi --version` reports the selected version and `pi --help` starts without a module or
runtime error. Record the Node/Pi versions and actual executable paths. No tracked package lists,
startup files, or default Pi agent settings have changed.

**Fallback:** if mise is the actual blocker, record it, inspect `brew info pi-coding-agent`, and use
`brew install pi-coding-agent` without editing `home/.Brewfile`. Record the version difference and
use the resolved Homebrew executable explicitly so a partial mise installation cannot shadow it.
Retain the same isolated agent directory and workspace. Do not use fallback to bypass package
security concerns. Do not run `just brew`, `just mise-sync`, `dots`, or updater scripts in the trial;
those upgrade/prune unrelated tools or can publish commits. An unlisted Homebrew trial package can
also be removed by a later bundle cleanup, so avoid overlapping workstation syncs.

## Phase 2: install the voice package and authenticate

1. Review the pinned package manifest, native dependency installation behavior, credential access,
   and `transport.ts` before installing or granting account access. The voice connection uses an
   experimental internal Codex protocol, not a supported public API contract. Check whether its
   audio ownership lock/control endpoint is outside `PI_CODING_AGENT_DIR`; record shared paths and
   do not delete another session's locks. Stop other live microphone sessions normally for testing,
   without removing or reconfiguring OMP.
2. Keep `TRIAL_ROOT` and `PI_CODING_AGENT_DIR` exported in this terminal. Remove inherited
   `OPENAI_API_KEY` from this process environment (`unset OPENAI_API_KEY`). Use only the Codex
   provider; do not select other ambient-credential providers. Never copy credentials out of OMP,
   Codex, or a normal Pi profile.
3. Install and verify the package in the trial profile:

   ```sh
   mise exec -- pi install npm:pi-live-codex@0.1.9
   mise exec -- pi list
   ```

   Expect the pinned source in the trial settings and package list. Record where Pi installed it.
   Review any native dependency failure before approving installation scripts or changing versions.
4. Start the isolated UI without unrelated discovered context, skills, templates, themes, or MCP:

   ```sh
   mise exec -- pi --no-context-files --no-skills --no-prompt-templates \
     --no-themes --no-mcp
   ```

   Check the installed help first because flags can change. Keep extensions enabled so the installed
   voice package loads. Confirm no unexpected extension is loaded; only the trial voice package
   should be added. These discovery flags do not remove Pi's built-in system instructions.
5. Run `/login openai-codex` and select **Device code login (headless)**. Pi displays a temporary
   code; Waldo opens <https://auth.openai.com/codex/device> on his phone or another browser, signs
   into the account with his subscription, and enters that code. Pi polls for completion; the
   inspected implementation allows 15 minutes. No browser is needed on the machine running Pi.
   This selectable method was verified in the
   [published Pi 1.0.4 OAuth implementation](https://cdn.jsdelivr.net/npm/@earendil-works/pi-ai@1.0.4/dist/auth/oauth/openai-codex.js),
   but has not been exercised with Waldo's account. If device login is unavailable, record the
   error; browser login with a pasted authorization code/redirect URL is the supported alternative.
   Do not change authentication routes silently.

   No API key, separate authentication application, or Codex desktop app is required for this
   flow. The repository already declares `codex = "latest"` through mise, and the installed CLI
   reported `codex-cli 0.160.1` during the follow-up check. Pi handles its own login; the installed
   Codex CLI is not a prerequisite, and its existing login is not assumed to transfer to Pi.

   Waldo completes authorization himself. Do not persist or share device codes, tokens, callback
   URLs, or `auth.json` in notes or chat. Confirm credentials are stored in
   `$PI_CODING_AGENT_DIR/auth.json`, outside the repository, and are private. In `/model`, explicitly
   select an available `openai-codex` coding model and record its ID. The coding model selection is
   distinct from the extension's voice model.
6. Ask a harmless text question first and observe a successful response. Then run `/live`, approve
   the terminal application's macOS microphone permission if requested, and exchange a short
   spoken question and audible answer. No separate local ASR/TTS service is expected for this path.

**Gate:** text coding access and real voice both work with the intended subscription. A successful
text login alone does not prove voice eligibility. If voice is rejected, capture the redacted status
and stop at that boundary; do not switch to API billing or spoof additional client requirements.

## Phase 3: baseline live evaluation

Waldo must be present for microphone interaction and subjective judgment. Run a short initial
session of about 10–15 minutes, stopping earlier for auth, billing, privacy, or audio failures. If it
passes the basic experience check, repeat with a representative 20–30 minute coding session.
These are proposed trial windows, not claims about included voice allowance.

Record each case as **pass**, **fail**, or **not exercised**, with an observation. Separate advertised
or source-inspected behavior from what happened on the microphone. Do not patch failures mid-run.

| Requirement | Real scenario | Pass criterion / expected gap |
| --- | --- | --- |
| Natural ongoing conversation | Several English turns, short pauses, and technical names; ask a follow-up without restarting voice. | Understandable audio in both directions, usable turn-taking; Waldo judges whether it feels comparable to OMP. Record noticeable response delays, false cutoffs, and misrecognitions. |
| Interruption | Interrupt a long spoken answer softly three times with a different question. | Playback yields and the next response addresses the interruption, not the abandoned answer. Record misses rather than assuming perfect barge-in. |
| Mute and stop | With an empty editor, toggle Space mute/resume; speak a harmless unique phrase while muted. End with Esc, then start again with `/live`; exercise Ctrl+L separately. | Muted speech is not acted on; resume restores input; stop releases the microphone and playback. Space mute is not assumed to be a context-preserving session pause. |
| Talk while Pi works | By voice, request a disposable Node module exporting `sum`, plus a Node assertion script for `[1, 2, 3] -> 6` and `[] -> 0`. While Pi works, ask for its current progress. Run the resulting script and inspect the files. | Real files and assertions succeed; conversation remains usable; progress and completion claims agree with tool activity. No edits outside the trial workspace are requested. |
| Queues and cancellation | Use a harmless bounded task long enough to overlap speech (for example, wait 20 seconds then write a trial marker). Submit two distinguishable follow-up requests and cancel one. | Noncancelled work executes once, cancelled work does not later execute, and status accurately distinguishes queued/running/completed work. |
| Configurable voice instructions | Check the installed package's supported configuration. Ask coding Pi to use a distinct harmless style, then compare voice behavior without editing the package. | Known gap: 0.1.9 has hardcoded voice instructions. A one-off compliant answer or a coding-system-prompt change is not proof of a configurable voice prompt. |
| One spoken question at a time | Request help with a task deliberately missing two independent details. Answer each question by voice. | It asks one question, waits, then asks the next; no ordinary question UI is needed. Record the known lack of enforcement even if the sample passes. Absence of an extra question-tool package does not prove a global restriction. |
| Recovery after full voice stop | State a unique objective, make a decision, leave a question pending, then Esc and `/live`. Ask what remains to do. | Correctly restores the objective, decision, recent speech, and pending question. Prior isolated checks predict failure; record the actual loss. |
| Recovery after error / process restart | With only disposable work, briefly interrupt the voice network connection and restore it; separately quit/relaunch Pi and resume its saved coding session with `--continue` plus the same discovery flags. | No invented recovered context; identify what survives in coding versus voice. Record actionable errors. Do not expose session files or disrupt unrelated network-dependent work without Waldo's agreement. |
| Context follows ongoing coding | Stop voice, let the coding task finish, restart voice, then ask for the result and next action. | Voice reports the real outcome and retained objective. Prior findings suggest an incomplete fresh-session handoff. |
| Pending-work recovery | Queue a distinctive marker-writing request behind bounded work; stop/start voice before it dispatches. Inspect files and activity before deciding whether to resubmit. | No lost or duplicated request. Prior isolated checks found stranded work. Never blindly resubmit an uncertain consequential request. |
| Subscription use and headroom | Inspect the account's usage display before and after the trial; record elapsed voice time, concurrent coding, and quota/rate-limit messages. | No separately billed API route or newly authorized credit spend. Report measured changes only; a coarse meter cannot establish an exact minute cost or remaining hours. |

Do not infer automatic approval from voice. If a consequential confirmation appears, Waldo must
explicitly answer it; do not test destructive operations to exercise confirmation handling.

## Phase 4: user verdict and remediation gate

Present the observed matrix, usage evidence, and Waldo's assessment of interruption, latency,
voice quality, and coding usefulness. Distinguish **baseline usable** from **all requirements met**.
The baseline may pass even though the already-known configuration and recovery requirements fail.
Those gaps remain open; a successful demo does not silently waive them.

Ask Waldo to choose based on the evidence:

- **Reject / pause:** preserve findings, stop the trial, keep OMP. Do not automatically try Orb or
  build a local stack under this plan.
- **Continue evaluation:** keep the isolated installation; run only the unresolved scenarios.
- **Authorize focused remediation:** if he likes the baseline, separately scope configurable voice
  instructions, one-question/tool policy, and durable context/queue recovery using the observed
  failures. Implement nothing merely because this plan mentions those gaps. Re-run the affected
  scenarios after any separately approved changes.
- **Approve adoption:** proceed to Phase 5 only once the required behavior works or Waldo explicitly
  accepts named remaining limitations, and confirms he likes the experience.

The normal trial finish is a reproducible pass/fail record and an explicit user verdict, not a
mandatory implementation project. Account ineligibility or incompatible native audio is also a
valid finish if the exact blocking boundary and attempted narrow diagnosis are documented.

## Phase 5: conditional dotfiles integration, last

**Current handoff:** Waldo has now requested repeatable Pi setup through `dots` and maintained
documentation. Read the [integration summary](pi-dotfiles-integration-summary.md) and
[execution notes](pi-live-codex-trial.notes.md) for accepted limitations and superseding decisions,
including normal-profile installation and latest-version policy. Phase 5 is now implemented;
`dots` completed successfully. Read the
[verification record](pi-live-codex-trial.notes.md#phase-5-implementation-and-verification) and
[maintained Pi documentation](../../docs/coding-agents/pi/README.md) before further changes.

The original gate below is retained for context; trial execution alone did not authorize adoption.
After the adoption
gate, read [Coding agents](/docs/coding-agents/README.md), [Tooling](/docs/tooling.md), and
[Scripts](/scripts/README.md) before changing ownership or sync behavior.

1. Add the validated Pi version to `home/.config/mise/config.toml`, using its existing npm backend
   convention. Use `home/.Brewfile` instead only if the evidenced Homebrew fallback was selected;
   do not maintain two competing owners of `pi`.
2. Decide minimal persistent Pi settings and package ownership from the actual validated profile.
   Keep auth, sessions, caches, microphone locks, and machine-specific paths outside tracked files.
   If settings are linked, preserve a real `~/.pi/agent` directory and link individual safe files via
   `install.conf.yaml`, not the entire credential-containing directory. Do not blindly copy the trial.
3. Use existing installer/updater conventions for repeatable package provisioning if it is needed.
   Specify how a fresh machine obtains the pinned voice package and how approved updates happen;
   do not create a second updater or silently float past the tested versions. If an extension fork
   was separately approved, record its actual source and revision instead of the baseline package.
4. Integrate only the instruction/skill behavior required for the accepted experience; validate
   coding instructions and voice instructions separately. Update `docs/coding-agents/README.md`, and
   `docs/tooling.md` or `scripts/README.md` only where their documented responsibilities change.
5. Smoke-run provisioning in an isolated home/configuration first, then validate a new interactive
   terminal against the resulting real Pi setup: version, package loading, login, speech, and the
   concurrent coding scenario. Run relevant repository lint once for the changed files.
6. Apply workstation changes only through the documented sync rules, announcing any required
   `dots` run beforehand; account for its upgrade/prune and possible commit/push effects. Do not
   run `just brew` as validation. Leave OMP available even after Pi adoption.

## Recovery and execution notes

- Stop `/live` normally and exit Pi; confirm the microphone is released. Never delete a lock while
  its owning session is still alive. Close the dedicated trial terminal to discard exported vars.
- Use `/logout` in the trial profile to remove its stored credential when abandoning the trial.
  This does not revoke the provider grant; Waldo can revoke it through the provider if desired.
- Preserve redacted results, then obtain approval before deleting the trial workspace or private
  profile. Never delete ordinary `~/.pi`, OMP, or Codex credentials as trial cleanup.
- A mise install lives in its shared tool store even when selection is local. Remove only the
  recorded trial-specific tool version after checking no other configuration uses it; keep shared
  Node. If Homebrew was used, uninstall Pi only if this trial installed it and it is not now used
  elsewhere. Do not run a broad prune or bundle cleanup.
- If adoption is rolled back, restore only the files changed for Pi from the recorded pre-change
  state, preserve user data, and verify OMP still launches. Do not revert unrelated workstation work.

At execution time, create `.agents/plans/pi-live-codex-trial.notes.md` with **Deviations** and
**How the run ended** headings. Include versions, executable paths, package/native-load results,
the scenario matrix, redacted usage observations, and Waldo's verdict. Log deviations without
secrets or raw private audio. If a deviation reverses a decision above, stop and consult Waldo.

## Sources and verification limits

Read these before executing the corresponding setup step; recheck installed-version help if current
upstream documentation differs:

- [Pi installation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md)
- [Pi CLI](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md)
- [Pi environment variables](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/environment-variables.md)
- [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)
- [Pi authentication](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md)
- [mise npm backend](https://mise.jdx.dev/dev-tools/backends/npm.html)
- [Pinned voice README](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/README.md)
- [Pinned voice manifest](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/package.json)
- [Pinned voice transport](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/transport.ts)
- [Pinned audio ownership notes](https://cdn.jsdelivr.net/npm/pi-live-codex@0.1.9/global-voice-broker.md)

Planning checked local mise command help, installed Node, npm version/engine metadata, Homebrew
formula availability, repository conventions, and upstream documentation. No installation or live
compatibility claim is established until the corresponding execution gate passes.
