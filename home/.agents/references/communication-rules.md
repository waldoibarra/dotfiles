# Communication rules

**You MUST read and follow these rules before composing any reply or artifact.**
Check applicable requirements before delivery; reading them without applying them is insufficient.

These rules cover lead and worker replies, documentation, plans, skills, prompts, code comments, and
commit messages.

## Lead with the point

- **Put the answer, decision, or request first**; identify the reader's next action when needed.
- State positions plainly; **match confidence to evidence** rather than implying unsupported
  certainty.
- Explain material uncertainty and its cause; **keep qualifications beside the claims they
  constrain**.
- **Cut filler and repetition, never risks or conditions.** State risks plainly.
- Use a precise, professional tone without slang.
- Prefer concrete words and the project's shared language in its glossary.

## Keep sentences within 17 words

Use **at most 17 words per sentence** in authored prose.

- Express **one main idea per sentence**; develop complex explanations across connected sentences.
- Vary sentence length within the limit to preserve natural rhythm.
- Rewrite overloaded sentences rather than deleting necessary qualifications or creating fragments.
- Keep **causes, conditions, and consequences explicitly connected** when splitting sentences.

**Exact quotations, diagnostic output, required syntax, and safety content retain their wording
regardless of length.**

## Choose a primary intent

Choose **one primary intent**; combine supporting sections when the task requires them.
Use the smallest structure that preserves necessary evidence, risks, and comparisons.

| Intent | Lead with | Include or stop at |
| --- | --- | --- |
| Inform | Main point | Relevant reasoning and evidence. |
| Decide | Recommendation | Supporting evidence and material tradeoffs. |
| Request | Ask | Necessary context; a blocking ask closes the reply. |
| Confirm | Action in one line | Act next; do not surround completion with a report. |
| Deliver | Artifact | Artifact only, without a lead-in or sign-off. |
| Report | Outcome | Changes, blockers or risks, and the next action. |

## Match structure to information

Choose **formatting by information structure, not decoration**; lists and tables do not
automatically improve scannability.

| Structure | Use when |
| --- | --- |
| Paragraphs | Explaining reasoning and relationships; keep connected explanations together. |
| Bulleted lists | Presenting related rules or independent items; keep their phrasing parallel. |
| Numbered lists | Showing ordered steps or explicit priorities. |
| Tables | Comparing the same attributes across items or mapping consistent lookup fields. |
| Headings | Helping readers navigate distinct topics, findings, decisions, or actions. |

### Group ideas for scanning

- Front-load each section's main point.
- Keep one idea per paragraph or list item; paragraphs usually contain one to three sentences.
- **Group long lists under descriptive headings** when their items cover distinct concerns.
- Prefer headings that name the finding, decision, or action over generic labels.
- Separate distinct ideas with whitespace; avoid unnecessary nesting and decorative structure.
- Keep short answers short; do not add headings or lists merely to satisfy a template.

### Give each format a purpose

Headings reveal structure; **bold phrases reveal essentials**.
Lists and tables organize details; they do not replace meaningful emphasis.

| Format | Purpose | Example |
| --- | --- | --- |
| **Bold** | Surface conclusions, requirements, actions, and warnings for skimming. | **Lead with the answer.** |
| _Italics_ | Introduce terms or provide restrained secondary emphasis. | This is called _front-loading_. |
| `Inline code` | Mark literal paths, commands, identifiers, keys, and values when exact characters matter. | `AGENTS.md`, `git status`, `AUTH_TOKEN` |
| Fenced code | Preserve multiline code, commands, or exact diagnostic output. | A runnable command sequence or an unchanged error message. |

- **Make emphasis purposeful, not scarce**; bold phrases should communicate the main message, not
  merely flag exceptions.
- Prefer short, meaningful bold phrases over generic labels such as “Important.”
- Emphasize a whole sentence when warranted; do not bold every sentence or label every paragraph.
- Use italics occasionally; **never rely on italics alone for essential meaning**.
- **Code formatting marks literal text**, not importance; write general technical concepts such as
  authentication normally.
- Use code fences for literal blocks, not decorative callouts or ordinary explanations.

### Keep links and presentation useful

- Use **descriptive link text** and place citations near the claims they support.
- Avoid arrows, closing summaries, and restating the answer.

## Preserve literal content and artifact requirements

- Preserve errors, failing tests, and safety warnings verbatim in fenced blocks.
- **Never shorten safety content**, including destructive-action confirmations, to fit a word
  budget.
- An artifact's **required syntax and structure take precedence** over reply formatting.
- Adapt presentation to the medium; clarity applies everywhere, Markdown formatting does not.
- Keep chat formatting out of source code.

## Keep language and terminology consistent

### Conversation language

- **Default to English**; switch conversation language only when the user writes in another
  language.
- Never infer language from names, email, locale, or identity.

### Repository language

- **Keep repository content in English**, including documentation, prototypes, UI text, comments,
  filenames, and identifiers.
- Preserve original-language source material in repository-root `raw/`; translate only when
  explicitly requested.
- Conversation language does not change repository language.
- Require an explicit exception for non-English repository content outside `raw/`.

### Shared context

- Use the project's shared language (its glossary file): **one term per concept**, no synonym
  cycling.
- State shared context once across related tickets, PRs, and messages.
- Omit material the reader already has through attachments, links, or the surrounding context.

## Check before delivery

- Can readers immediately identify the point and any required action?
- Do headings and bold phrases communicate the main requirements without misrepresenting
  qualifications?
- Do opening sentences provide clear entry points into the supporting detail?
- Are risks and qualifications visible beside the relevant claims?
- Does formatting help rather than dominate?
- Is the full explanation still coherent when read normally?

Perform a _skim pass_: read only headings and bold phrases, then check the full text for coherence.
**Treat lint compliance as necessary, not sufficient**; verify meaning, flow, and completeness.
