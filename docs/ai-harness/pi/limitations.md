# Pi voice limitations and test evidence

**Evidence:** These results combine Waldo's live reports with the coding agent's visible file operations.
They are not a controlled benchmark. No raw private audio or exact delegation payload was retained.
Read the [Pi overview](README.md) before comparing tested versions or component ownership.

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
The cause
could not be assigned to recognition, summarization, or transport from the evidence collected.

## Queuing and cancellation

Repeated cancellation attempts used empty files in a disposable temporary directory.
Creation completed before each cancellation reached the agent.
Eventual delivery was observed.
Exactly-once execution and persistence across errors or restarts were not established.
Waldo chose to stop
pursuing cancellation tests or fixes. A future consequential request should not be blindly
resubmitted when its status is uncertain.

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
