# Communication rules

You MUST read and follow these rules before composing any reply or artifact.
Check applicable requirements before delivery; reading them without applying them is insufficient.

These rules cover lead and worker replies, documentation, plans, skills, prompts, code comments, and
commit messages.

## State the point clearly

- Identify the intent and reader's next action. Put the answer, decision, or request first.
- Use at most 17 words per sentence. Keep one idea per paragraph or list item.
- Cut filler and repetition, never risks or conditions. Preserve safety content verbatim; state
  risks plainly.
- State positions plainly without hedging. State each real uncertainty once, with its cause.
- Use a precise, professional tone without slang.
- Prefer concrete words and the project's shared language in its glossary.
- Default to English; switch conversation language only when the user writes in another language.
- Never infer language from names, email, locale, or identity.
- Keep repository content in English, including documentation, prototypes, UI text, comments,
  filenames, and identifiers.
- Preserve original-language source material in repository-root `raw/`; translate only when
  explicitly requested.
- Conversation language does not change repository language.
- Require an explicit exception for non-English repository content outside `raw/`.

## Choose one intent

Name the reader's next action, then choose one shape. Never mix reply shapes.

- **Inform (PREP):** point first, one reason block, one evidence block. Stop.
- **Decide (pyramid):** recommendation first, at most three distinct supports, one risk block.
- **Request:** ask first, at most two context blocks. A blocking ask closes the reply.
- **Confirm:** name the action in one line, then act. Do not surround completion with a report.
- **Deliver:** return the artifact only, without a lead-in or sign-off.
- **Report:** outcome first, then changes, blockers or risks, and the next action.

## Shape the text

- Keep paragraphs focused; several short sentences may develop one idea.
- Split by idea, not merely to satisfy the sentence-length limit.
- Start prose blocks with **bold lead-ins** of at most four words; the bold alone carries the
  message.
- Use lists for parallel items; lead-ins are optional.
- Use tables for comparisons, with at most five rows.
- Use `code` for identifiers, files, and values.
- Keep chat formatting out of source code.
- Avoid arrows, closing summaries, and restating the answer.
- Preserve errors, failing tests, and safety warnings verbatim in fenced blocks.
- Never shorten safety content, including destructive-action confirmations, to fit a word budget.

## Keep artifacts coherent

- Use the project's shared language (its glossary file): one term per concept, no synonym cycling.
- State shared context once across related tickets, PRs, and messages.
- Omit material the reader already has through attachments, links, or the surrounding context.
- An artifact's required syntax and structure take precedence over reply formatting.
