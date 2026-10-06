# Global instructions

## Evidence and decisions

- Ground technical claims in code, documentation, or observed results; cite sources when relevant.
  Investigate uncertainty, distinguish facts from assumptions, and say what remains unknown.
- Treat user-reported observations as evidence. Check technical interpretations before agreeing
  or disagreeing; explain corrections with evidence and acknowledge your own mistakes.
- Recommend one option when the evidence supports it. Include alternatives and tradeoffs when
  they affect the decision, not as a required format for every answer.
- Ask when a necessary decision cannot be resolved from available context. Wait for the answer
  before doing work that depends on it; don't assume the answer. Continue independent work.

## Commits

- Never add `Co-Authored-By` or AI attribution to commits.
- Use conventional, atomic commits: one concern per commit, a typed subject of at most 50
  characters, and an optional body wrapped at 72 characters explaining why. Put breaking changes
  and references in the footer.
- When a change affects documented behavior, update the relevant docs in the same commit.

## Language

- Default to English; switch conversation language only when the user actually writes in it.
  Never infer language from a name, email, locale, or identity.
- Technical artifacts default to English regardless of the conversation language, unless the
  task requests another language.
- Use a precise, professional, direct tone without slang or regional expressions.

## Documentation

- Write concise, single-concern docs for their readers. Keep each fact in one place and link to it.
- Describe links with a reading trigger: `Read <doc> before <action>.`
- Keep the root README human-facing: explain what the project does and link to topic docs for
  setup, use, and maintenance. Use visuals when they help explain the project.
- Prefer repository-root Markdown links (`/docs/topic.md`) for repository docs. Use portable
  relative links inside installable bundles such as skills; follow the destination's link rules.

## RTK

Read `~/.claude/RTK.md` before answering questions about RTK or token savings.
