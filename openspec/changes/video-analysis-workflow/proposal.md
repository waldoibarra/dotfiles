# Proposal

## Why

Video analysis needs traceable audiovisual evidence, not summaries presented as complete
observation.
Reusable guidance must cover recorded YouTube videos and bounded live capture without importing
project-specific goals.

## What Changes

Add repository-owned `video-analysis` and `audio-transcription` skills with conditional reading
routes.
Separate shared media acquisition from local transcription runtime setup.
Document segmented near-live analysis, interruption recovery, coverage, storage limits, and
retained evidence.
Update glossary terms, instruction routing, and skill discovery documentation.
Exercise short recorded-video and live-capture cases using a fresh Sol worker.

Exclude automatic deletion, unattended indefinite recording, new installations, credentials,
publication, and production streaming infrastructure.
Actual test media and findings belong to the operator's AI income challenge workspace, not dotfiles.

## Approach and tradeoffs

| ID | Choice | Reason |
| --- | --- | --- |
| V1 | Separate analysis, transcription, acquisition, and workstation setup | Each concern has independent users and verification. |
| V2 | Use adaptive audiovisual inspection | Fixed frame intervals miss motion, brief text, and non-speech audio. |
| V3 | Capture segments independently from analysis | Failed analysis must not silently terminate capture or erase evidence. |
| V4 | Default recovery to 30-second checks for ten minutes | Bound retries while allowing transient interruptions to recover. |
| V5 | Retain test media without automatic deletion | Reinspection remains possible until a separate retention policy is approved. |
| V6 | Test approximately three minutes per supplied source | Establish bounded execution without claiming endurance reliability. |
| V7 | Use explicit Sol selection and medium reasoning | Match the operator's model choice and shared delegation policy. |

Extending `save-md` would conflate faithful source extraction with interpretation.
One workstation guide would reduce files but obscure reusable procedure ownership and task
discovery.
A new streaming service would exceed the documented-workflow request and require separate
operational design.
Near-live execution uses available capture and analysis tools, not an implied always-running
service.

Rollback restores scoped source changes and removes only newly created, verified discovery links.
Retain authorized task evidence unless its owner approves deletion.

## Capabilities

### New Capabilities

- `video-analysis`: Goal-directed audiovisual findings with traceable evidence and bounded live
  workflows.
- `audio-transcription`: Independent local speech transcription with coverage and uncertainty
  checks.

### Modified Capabilities

None.

## Impact

Affected owners include `home/.agents/skills/`, shared acquisition references, and existing local
transcription documentation.
The root glossary owns workflow terms; the global contract owns short reading triggers.
Dotbot already discovers repository-owned skill bundles through its existing glob.
No updater execution or external skill replacement is required.
The test workspace is `$HOME/projects/learning/ai-income-challenge`; it currently has no Git root.

## Verification

Validate OpenSpec artifacts, skill structure, Markdown, links, and isolated harness delivery.
Review documentation preservation, progressive disclosure, and authored sentence lengths
independently.
Use fresh Sol contexts with explicit source loading and bounded media acquisition.
Check transcript coverage, selected frames, source timestamps, and the distinction between
observations and claims.
Report inaccessible sources, missing prerequisites, and untested modalities without inventing
results.
Short tests do not establish uninterrupted recording, automatic routing, endurance, or sustained
near-live throughput.

## Approval

The operator approved the generalized workflow, documentation, short source tests, and Sol worker
selection.
The subsequent “Go” approved segmented near-live analysis and the proposed interruption recovery
defaults.
Automatic deletion remains excluded; longer capture requires explicit time and storage budgets.
This artifact records the existing conversation agreement, not a new approval request.
