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
Start every reply with `[<name>]` so the lead can tell it from the operator's messages.
When `<path>` exists, send one reply naming the path and the <n> most contested choices. Then stop.
```

**Worker replies look like operator messages.** In Claude Code they surface mid-turn as "the
user sent a new message", with no sender field. The `[<name>]` prefix is the only reliable
sender mark; without it the lead must infer the sender from the content. Learned on 2026-11-02.

**A worker in a fresh worktree has no dependencies.** Say in Actions that it may install them
there, or it stops at the first test run.

- Mission, Output, and Stop condition are mandatory. Prune fields that cannot change the result.
- The lead closes the worker's workspace after verification; the stop condition ends the worker's
  turn, not its container.
- Keep approval boundaries explicit: a worker never gains the lead's Git, publication, or model
  authority.
- Reuse focused context for follow-ups; do not resend the whole history.
