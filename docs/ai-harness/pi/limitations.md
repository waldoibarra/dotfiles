# Pi voice limitations and trial evidence

**Voice context can be lost, and spoken requests can arrive after their intended cancellation.**
Check uncertain request status before repeating consequential work.
These accepted limitations remain relevant until a new test establishes otherwise.

The results below combine Waldo's trial reports with visible coding-agent file operations.
They are historical observations, not a controlled benchmark or verification of current releases.
No raw private audio or exact delegation payload was retained.
Read [live voice](live-voice.md) for controls and [configuration](configuration.md) for current settings.

## Trial environment

| Component | Recorded trial version or result |
| --- | --- |
| Pi | 1.0.4; Node 22.19 or newer required |
| Node | 24.21.0, selected through Mise's `lts` configuration |
| Voice extension | Unmodified `pi-live-codex` 0.1.9 |
| File search | Pi's private `~/.pi/agent/bin/fd`, verified as 10.5.0 |
| Voice dependencies | `ws` 8.22.0 and `@oh-my-pi/pi-natives` 18.4.9 |
| Platform | Apple Silicon macOS; Debian voice operation was not tested |
| Login | Device-code and browser authorization were available; the method used was not recorded |

The native package supplied audio exports; it did not run the OMP agent.
An optional Apple Silicon package loaded successfully without a blanket dependency-build exception.
Pi, voice, and delegation follow release updates; these versions are evidence, not pins.
The [integration summary](/docs/plans/pi-dotfiles-integration-summary.md) and
[trial notes](/docs/plans/pi-live-codex-trial.notes.md) retain the original integration record.

## Observed behavior

| Area | Result | Current decision |
| --- | --- | --- |
| Basic conversation | Spoken input and audible responses worked. Waldo likes aspects of both Pi and OMP. | Pi kept; OMP support was later dropped. |
| Interrupting playback | Playback stopped mid-sentence, with a small unmeasured delay. | Usable initial result; repeated reliability was not established. |
| Mute/resume | Muted speech was ignored and conversation resumed after Space. | Passed in the reported test. |
| Coding while talking | Note edits and empty-file creation completed during the voice workflow. | Accepted for this workflow; the original Node assertion exercise was not run. |
| One question at a time | Three questions were asked separately with an answer between each. Waldo confirmed the spoken behavior. | Passed in this sample, without a global enforcement mechanism. |
| Automatic context after voice restart | Previous voice context did not carry over. | Accepted limitation for now; manual requests to consult the coding agent can help. |
| Context delegation | Relevant speech sometimes failed to reach the coding agent despite repeated requests, creating clarification loops. | Investigation deferred. Voice and coding must not be described as sharing a complete transcript. |
| Queued delivery | Requests spoken during 20- and 40-second waits later reached the coding agent and executed. | Queuing is acceptable if requests are delivered. The buffering layer was not identified. |
| Cancellation | Cancellation requests reached the agent after the files already existed. Nothing was deleted as an implied undo. | Waldo accepts proceeding without cancellation; these tests do not prove a pending request can never be cancelled. |
| Speech recognition | Some names and words were misunderstood. | Known usability issue; transcription and assistant interpretation were not isolated. |
| Voice during coding updates | Voice sometimes cut across Waldo's speech while coding work was underway. | Keep as an improvement candidate. A progress/completion trigger is suspected, not established. |
| Instructions | The voice prompt is hardcoded. | No customization requested. Coding-agent instructions do not establish a configurable voice prompt. |
| Pi restart, network recovery, pending work | Separate tests were not completed. | Unverified, including loss/duplication risks. Voice restart is not proof of broader recovery. |

## Context handoff

A manual handoff can retrieve coding context after voice restarts.
It cannot recover speech the coding agent never received.
A recall exercise using facts already visible in coding chat was inconclusive.
Later attempts to delegate a separate spoken topic omitted the details.
The evidence could not distinguish recognition, summarization, or transport as the cause.

## Queuing and cancellation

Repeated cancellation attempts used empty files in a disposable temporary directory.
Creation completed before each cancellation reached the agent.
Eventual delivery was observed.
Exactly-once execution and persistence across errors or restarts were not established.
Waldo chose to stop pursuing cancellation tests or fixes.
A future consequential request should not be blindly resubmitted when its status is uncertain.

## Subscription usage

Waldo monitored weekly subscription usage during approximately one to two hours of conversation.
He observed little increase. No starting/ending percentages or reset time were recorded.
Separate voice/coding attribution was not recorded.
This supports his practical assessment of the experience.
It does not establish a per-minute cost, remaining-hours estimate, or zero-cost claim.
It does not guarantee that the meter immediately reflects all activity.

## Deferred improvements

Context handoffs, recognition, update-triggered interruptions, and
[autocomplete](live-voice.md#misleading-autocomplete-and-access-errors) are candidates for later
improvement, not approved extension work. No fork, voice-default patch, or recovery fix is included
in the dotfiles integration.
