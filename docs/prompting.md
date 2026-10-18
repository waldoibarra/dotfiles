# Write effective AI prompts

**Use:** Start with the template, refine unclear instructions, and verify the response before relying
on it.

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

## Refine an unhelpful response

- Check whether the role, context, or goal needs correction.
- Supply relevant conversation history or a summary; do not assume cross-session memory is available.
- Ask clarifying questions one at a time, then revise using the answers.
- Request two sharper versions of an unclear question before choosing one.
- Name relevant experts or frameworks when you need a specific perspective; request their supporting
  sources.
- Request a concise rationale with key assumptions and evidence.
- Test revisions against the task; more context alone does not guarantee better results.

## Verify before relying

- Identify assumptions and uncertainty; model-reported confidence is not proof.
- Request two independent sources per major claim, including titles, URLs, and supporting quotations.
- Open those sources yourself and confirm the quotations support the claims.
- Seek credible counterevidence and identify which conditions or assumptions explain disagreements.
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
