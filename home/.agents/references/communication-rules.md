# Communication rules

You MUST read and follow these rules before composing any reply or artifact.
Check applicable requirements before delivery; reading them without applying them is insufficient.

These rules cover lead and worker replies, documentation, plans, skills, prompts, code comments, and
commit messages.

## State the point clearly

- Identify the intent and reader's next action. Put the answer, decision, or request first.
- Use at most 17 words per sentence in authored prose.
- Express one main idea per sentence; develop complex explanations across connected sentences.
- Vary sentence length within the limit to preserve natural rhythm.
- Rewrite overloaded sentences rather than deleting necessary qualifications or creating fragments.
- Keep causes, conditions, and consequences explicitly connected when splitting sentences.
- Preserve exact quotations, diagnostic output, required syntax, and safety content regardless of length.
- Cut filler and repetition, never risks or conditions. Preserve safety content verbatim; state
  risks plainly.
- State positions plainly; match confidence to evidence rather than implying unsupported certainty.
- Explain material uncertainty and its cause; keep qualifications beside the claims they constrain.
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

## Choose a primary intent

Choose one primary intent; combine supporting sections when the task requires them.
Use the smallest structure that preserves necessary evidence, risks, and comparisons.
Name the reader's next action when action is needed.

- **Inform:** point first, followed by relevant reasoning and evidence.
- **Decide:** recommendation first, followed by supporting evidence and material tradeoffs.
- **Request:** ask first, followed by necessary context. A blocking ask closes the reply.
- **Confirm:** name the action in one line, then act. Do not surround completion with a report.
- **Deliver:** return the artifact only, without a lead-in or sign-off.
- **Report:** outcome first, then changes, blockers or risks, and the next action.

## Make the text scannable

- Front-load the answer and each section's main point.
- Keep one idea per paragraph or list item; paragraphs usually contain one to three sentences.
- Add descriptive headings when readers need to navigate several topics.
- Prefer headings that name the finding, decision, or action over generic labels.
- Use parallel bullets for related items and numbered lists for ordered steps.
- Use tables when readers need to compare the same attributes across items.
- Bold key takeaways, actions, or warnings sparingly; do not label every paragraph.
- Prefer short bold phrases; emphasize a whole sentence only when its importance warrants it.
- Separate distinct ideas with whitespace; avoid unnecessary nesting and decorative structure.
- Use descriptive link text and place citations near the claims they support.
- Keep short answers short; do not add headings or lists merely to satisfy a template.
- Adapt presentation to the medium; clarity applies everywhere, Markdown formatting does not.
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

## Check before delivery

- Can readers immediately identify the point and any required action?
- Do headings, opening sentences, and emphasis expose the important information?
- Are risks and qualifications visible beside the relevant claims?
- Does formatting help rather than dominate?
- Is the full explanation still coherent when read normally?
- Treat lint compliance as necessary, not sufficient; verify meaning, flow, and completeness.
