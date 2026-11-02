# Brief a worker

Back to [agent coordination](README.md). Used by [spawning](spawning.md) step 6.

**The first message to any agent follows the [prompting guide](/docs/prompting.md).** Its AIM
template names the actor, input, mission, actions, constraints, output, clarification, and
verification, one Markdown header each.
Send that message itself; a path to a file is input, not a prompt. Save the message
under the session's scratch directory so it can be sent verbatim and kept as evidence.

```markdown
# <Mission in one line>

## Actor
You are the worker `<name>`, an <role>. Your lead is `<lead-name>` (Herdr agent name).

## Input
- Files and directories to read, with paths.
- The lead's draft or position to challenge, when one exists.

## Mission
<Outcome> for <audience>. Why it matters, in one sentence.

## Actions
Allowed operations and tools.

## Constraints
- Directories that must not be edited. Sentences of at most 17 words.
- House conventions that apply.

## Output
Write `<path>` containing <format>. Answer first, then rationale and evidence.

## Clarification
Ask the lead about missing information that would change the result. Name assumptions.

## Verification
Support each major claim with a source the lead can open.

## Reply and stop
Reply with `herdr agent prompt <lead-name> "<text>"` without `--wait`; chat output reaches nobody.
When `<path>` exists, send one reply naming the path and the <n> most contested choices. Then stop.
```

- Mission, Output, and Stop condition are mandatory. Prune fields that cannot change the result.
- The lead closes the worker's workspace after verification; the stop condition ends the worker's
  turn, not its container.
- Keep approval boundaries explicit: a worker never gains the lead's Git, publication, or model
  authority.
- Reuse focused context for follow-ups; do not resend the whole history.
