# Write effective AI prompts

**Use:** Start with the template, refine unclear instructions,
and verify responses before relying on them.

## Clarify intent in its rhetorical situation

**Intent clarification combines the requested outcome with the circumstances of communication.**
It is our practical synthesis, not an established four-dimensional theory or mandatory message
schema.
The [communication
rules](/home/.agents/references/communication-rules.md#clarify-intent-and-audience) own the agent's
pre-response checks.
The [glossary](/GLOSSARY.md) defines our terms; this guide explains their application.

| Source lens | Contribution | Harness interpretation |
| --- | --- | --- |
| Video: goal | Desired result | Distinguish the requested operation from the outcome that makes it useful. |
| Video: constraint | Conditions to preserve | Separate requirements from discretionary editing choices. |
| Video: assumption | Beliefs left implicit | Identify unsupported beliefs, including inferred readers and their knowledge. |
| Video: entity | Thing being addressed | Use target for the precise subject, artifact, version, or decision. |
| Purdue: text | Actual communication | Identify the existing text and intended output. |
| Purdue: author | Person communicating | Preserve whose voice and position the message represents. |
| Purdue: audience | Recipients | Identify readers, including secondary readers, and their information needs. |
| Purdue: purposes | Reasons for communicating | Consider what both author and readers need to accomplish. |
| Purdue: setting | Time, place, and environment | Account for medium, relationship, timing, and surrounding conversation. |

Audience can be stated context or an unsupported assumption; it is not inherently an assumption.
A Slack channel does not establish whether readers need implementation details, delivery
implications, or business exposure.
Job titles alone do not establish knowledge or imply a formal tone.

**Example:** “Tighten this paragraph” identifies an operation and a target but may leave the outcome
unclear.
Ask when context is insufficient: “Who will read this? What should they understand or decide?”
Preserve established facts and constraints; do not quietly add a professional audience or greater
certainty.
If readers and purpose are already known, use that context without asking again.
The response's own choices should remain inspectable: explain consequential interpretations without
exposing an internal checklist.

## Writing defaults and sources

Shared [communication
rules](/home/.agents/references/communication-rules.md#edit-for-the-actual-reader)
own editorial defaults, including no prose em or en dashes and literal-content exceptions.
Ghostwriter owns voice-specific drafting; `feedback-loop` evaluates mismatches and observed
improvement without applying changes.
We adapt selected Humanizer ideas rather than install a second overlapping rewriting skill.
Style clues are not reliable authorship tests; no word blacklist or invented personality is
required.

- [What Do We Build Now That AI Can Do the Work?](https://www.youtube.com/watch?v=H2bYz5kIYk4)
  supplies the four-part lens and augmentation argument.
- [Purdue OWL: Elements of Rhetorical
  Situations](https://owl.purdue.edu/owl/general_writing/academic_writing/rhetorical_situation/elements_of_rhetorical_situations.html)
  supplies text, author, audience, purposes, and setting.
- [Humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) informs selective editorial checks.
  The reviewed skill states version 3.1.0; it does not establish detection accuracy or personal voice.

## Prompt template

**AIM:** Define the actor, input, and mission; include only fields relevant to your task.

```text
Actor: Act as [ROLE OR PERSPECTIVE].
Input: Use [RELEVANT CONTEXT, DATA, FILES, AND SOURCES].
Mission: Produce [OUTCOME] for [AUDIENCE].
Actions: Use [AVAILABLE, AUTHORIZED OPERATIONS].
Constraints: Respect [SCOPE, LIMITS, AND REQUIREMENTS].
Output: Return [FORMAT AND LENGTH], with the answer first.
Clarification: Ask about missing information that would change the answer.
Verification: Identify assumptions, support major claims, and flag uncertainty.
```

**Prune:** Keep saved prompt rules only when their removal could change a correct output.

## Refine an unhelpful response

- Check whether the role, context, or goal needs correction.
- Supply relevant conversation history or a summary; do not assume cross-session memory is available.
- Batch independent, consequential clarification questions; ask dependent questions after their
  prerequisites are resolved.
- Request two sharper versions of an unclear question before choosing one.
- Name relevant experts or frameworks when you need a specific perspective; request their supporting
  sources.
- Request a concise rationale with key assumptions and evidence.
- Test revisions against the task; more context alone does not guarantee better results.

## Verify before relying

- Identify assumptions and uncertainty; model-reported confidence is not proof.
- Request two independent sources per major claim, including titles, URLs, and supporting quotations.
- Open those sources yourself and confirm the quotations support the claims.
- Seek credible counterevidence. Identify conditions or assumptions explaining disagreements.
- Recompute figures and inspect the math or code.
- Use another model to critique claims when useful, then check the underlying evidence.

**Limit:** “Stop making stuff up” does not establish accuracy; generative output can contain fabricated
claims.

**Limit:** Agreement between models is not independent evidence; check the underlying sources and calculations.

## Assess quality with OCEAN

- **Original:** Explore non-obvious alternatives, identify risks, and recommend one; do not assume
  novelty proves originality.
- **Concrete:** Use specific names, credible numbers, and real examples.
- **Evident:** Give the answer first, followed by a concise rationale and supporting evidence.
- **Assertive:** State a defensible position and address the strongest counterpoint.
- **Narrative:** When storytelling fits, use a hook, problem, insight, proof, and actions.
