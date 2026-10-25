# Maintain current knowledge

**Goal:** Keep maintained documentation and comments clear, current, and easy to navigate without
erasing useful rationale.
Read [the glossary](/GLOSSARY.md) before changing terminology and
[architecture](/docs/architecture.md) before changing ownership.

## Choose the owner

| Material | Owner | Treatment |
| --- | --- | --- |
| Global instructions | `agents-md` workflow | Keep universal boundaries visible; load procedures when needed. |
| Skill definitions | `skill-maintenance` and `agent-skills-creator` | Preserve workflow contracts and verify discovery separately. |
| Maintained Markdown | `docs-maintenance` | Check facts, clarity, scope, links, and lifecycle. |
| Model prompts | [Prompting guide](/docs/prompting.md) | Follow prompt-specific pruning and validation. |
| Original or frozen evidence | Its source and retention rules | Do not rewrite it as current guidance. |

Read [docs-maintenance](/home/.agents/skills/docs-maintenance/SKILL.md) before creating, editing, or
reviewing Markdown documentation.
Read [conventions](/home/.agents/skills/docs-maintenance/references/conventions.md) before naming
files or changing navigation.

## Keep guidance useful

1. Establish the document's audience, concern, canonical owner, and evidence.
2. Explain the big picture first; route readers to task-specific detail instead of duplicating it.
3. Search affected docs and comments for changed identifiers, defaults, commands, and constraints.
4. Correct verified stale claims; distinguish accepted future behavior from implemented and
  exercised behavior.
5. Retire obsolete operational steps within scope; preserve consequential rationale with status and
  successor links.
6. Update incoming links and indexes alongside moves, removals, and glossary changes.

**Authority:** Reading grants no edit permission; unrelated documents and other contributors'
changes remain outside the task.
Substantial rewrites and structural moves require approval unless the request already covers them.
Markdown guidance loads through instructions and skills, not a guaranteed file watcher.

**Shared language:** Each maintained repository and vault has a meaningful root `GLOSSARY.md`.
Definitions describe existing domain concepts; procedures and implementation details stay in their
own documents.
Do not copy every global term into every project or create empty glossaries to satisfy a checklist.

## Retire without losing rationale

**Current guidance:** Update the maintained source and remove obsolete instructions from active
navigation.
**Consequential history:** Keep the decision, its status, successor, and useful rejected
alternatives in an existing history location.
**Temporary agreements:** State scope and an end or recheck condition; age alone does not establish
expiry.
**Uncertain claims:** Preserve the evidence gap; do not replace it with confident prose.

Read [memory lifecycle](/home/.agents/references/memory.md) before changing retention or ADR policy.
Its three ADR gates prevent reference facts and routine tasks becoming permanent decision records.
No ADR is created merely because a refactor finished.

**Comments:** Explain intent and hidden constraints near the code they affect.
Update or remove stale comments with the authorized behavior change; verify unfamiliar rationale
before deleting it.
Documentation maintenance does not authorize a repository-wide code cleanup.

**Protected sources:** Preserve original-language `raw/`, legal text, upstream copies, generated
output, fixtures, and frozen evidence.
Use the owning generation or source process when those materials need change.
Historical evidence remains available but does not authorize replaying old commands.

## Verify and close

```sh
just lint-md
just lint-ec
git diff --check
```

**Ignored skills:** Validate edited shared skills through stdin because normal Markdown discovery
skips `home/.agents/`.

```sh
markdownlint-cli2 - < home/.agents/skills/docs-maintenance/SKILL.md
markdownlint-cli2 - < home/.agents/skills/docs-maintenance/references/conventions.md
```

**Meaning:** Check unique facts, safety conditions, successor links, command accuracy, and sentence
limits explicitly.
Formatting checks alone do not prove preservation or model behavior.
At closure, `session-improvement` reviews session-edited Markdown and proposes corrections without
applying them.

**Invocation:** Use `/skill:docs-maintenance` in Pi or `/docs-maintenance` in Claude Code.
Reload Pi or start a fresh Claude session after installation; discovery alone does not prove
execution.
Read [historical verification](/.agents/plans/ai-harness-roadmap.md#documentation-maintenance)
before citing earlier behavioral results.
