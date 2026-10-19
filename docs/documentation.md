# Maintain documentation as you work

**Goal:** Keep touched documentation understandable, accurate, and complete without expanding into
repository-wide cleanup.

**Owner:** Read [docs-maintenance](/home/.agents/skills/docs-maintenance/SKILL.md) before creating,
editing, or reviewing Markdown documentation.

## What happens automatically

- Shared instructions require the skill during Markdown documentation tasks across repositories
  using this harness.
- Small doc edits beside code changes and edits by workers also load it.
- After a code or config change, it searches docs for changed identifiers, flags, recipes, and
  numbers.
- Plans are in scope; it marks superseded decisions instead of deleting them.
- It reads the project's shared language (its glossary file) before choosing terms.
- Within authorized edits, it improves clarity and verifies facts without requiring separate
  cosmetic approval.
- It explains the big picture first, preserving unique information and distinguishing current
  behavior from planned changes.
- Structural changes and substantial rewrites remain proposals unless their exact scope is already
  approved.
- It follows repository-specific owners, confidentiality, and approval boundaries.

## Review at session end

**Closure:** Run `session-improvement` for read-only proposals covering Markdown documentation
edited during the session.

- It reads `docs-maintenance` for review criteria and skips the review when no documentation was
  edited.
- It does not apply rewrites, create directories, or inspect unrelated documentation.

## Load it explicitly

| Host | Invocation |
| --- | --- |
| Pi | `/skill:docs-maintenance` |
| Claude Code | `/docs-maintenance` |

**Discovery:** Reload Pi or start a fresh Claude Code session after installation.

**Limit:** This is model-followed guidance, not a file watcher or guaranteed automatic execution.

**Boundary:** Reading grants no edit permission; instructions, skill definitions, and frozen
archives have separate owners.

**Prompts:** Read [Write effective AI prompts](/docs/prompting.md) before editing prompt files sent
to models.

## Verify a change

**Checks:** Run this repository's formatting checks after editing its documentation:

```sh
just lint-md
just lint-ec
git diff --check
```

**Skills:** Check edited skill Markdown through stdin because normal discovery skips
`home/.agents/`.

```sh
markdownlint-cli2 - < home/.agents/skills/docs-maintenance/SKILL.md
markdownlint-cli2 - < home/.agents/skills/docs-maintenance/references/structure.md
```

**Evidence:** Read the [roadmap](/.agents/plans/ai-harness-roadmap.md#documentation-maintenance)
before claiming installation or behavioral verification.
