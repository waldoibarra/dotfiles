# Maintain current knowledge

**Goal:** Keep documentation understandable, current, and navigable without duplicating facts or
preserving obsolete instructions.
Read [the glossary](/GLOSSARY.md) before domain edits and [architecture](/docs/architecture.md)
before changing ownership.

## Choose the owner

| Material | Workflow or source |
| --- | --- |
| Maintained Markdown, including plans | [`docs`](/home/.agents/skills/docs/SKILL.md) |
| Agent instruction files | `agents-md` |
| Repository-owned skills | `skill-maintenance`, with `agent-skills-creator` for authoring |
| Model prompts | [Prompting guide](/docs/prompting.md) |
| Retention, temporary agreements, and ADR gates | [Memory lifecycle](/home/.agents/references/memory.md) |
| Original, generated, or frozen evidence | Its source, publisher, and retention rules |

**Read `docs` before creating, editing, organizing, or reviewing maintained Markdown.**
It owns scope, evidence, preservation, affected-document discovery, and verification.
The other workflows retain their specialist responsibilities; reading a file never grants edit
permission.

## Apply the shared documentation architecture

Read [information architecture](/home/.agents/skills/docs/references/structure.md) before creating,
rewriting, or reviewing a guide's organization.
It owns concerns, Diátaxis page purposes, progressive disclosure, directory boundaries, and
reader-route checks.
Use it incrementally within the task; do not impose a new tree on unrelated documentation.

Read [conventions](/home/.agents/skills/docs/references/conventions.md) before naming files or
writing entrypoints.
Its [README
guidance](/home/.agents/skills/docs/references/conventions.md#readmemd-earn-the-readers-interest)
owns human orientation; its
[AGENTS
guidance](/home/.agents/skills/docs/references/conventions.md#agentsmd-define-the-working-contract)
owns instruction content conventions.

**Dotfiles ownership:** Shared procedures live under `home/.agents/`; workstation maintenance guides
live under `docs/`.
[Plans and research](/.agents/README.md) own project records, outside shared harness configuration.
The root glossary defines existing domain concepts; implementation details belong with their
maintained guides.
Do not copy global vocabulary or create empty documentation to satisfy a template.

## Remove stale guidance within scope

**Retirement:** Remove obsolete instructions; retain rationale only when it still explains a current
constraint or decision.
Git preserves ordinary edit history; do not create archives for routine rewrites.
Update successors and incoming links when consequential retained material moves.
Use the memory lifecycle reference for temporary exceptions, disputed claims, and all three ADR
gates.
A completed refactor alone does not justify an ADR.

**Comments:** Check intent and hidden constraints beside changed code; verify unfamiliar rationale
before removing it.
Documentation maintenance does not authorize unrelated code cleanup or changes to other
contributors' work.

**Protected sources:** Preserve original-language `raw/`, legal text, upstream copies, generated
output, fixtures, and frozen evidence.
Use their owning process for changes; historical evidence does not authorize replaying old commands.

## Verify the change

Run from the repository root:

```sh
just lint-md
just lint-ec
git diff --check
```

**Ignored skills:** Normal Markdown discovery skips `home/.agents/`; check edited skill documents
through stdin.

```sh
markdownlint-cli2 - < home/.agents/skills/docs/SKILL.md
markdownlint-cli2 - < home/.agents/skills/docs/references/conventions.md
markdownlint-cli2 - < home/.agents/skills/docs/references/structure.md
```

**Content:** Use the skill's preservation checks and the structure reference's reader-route
questions.
Verify command accuracy, safety wording, links, and applicable prose limits separately from
formatting.
Report failures outside the task without changing protected sources to make lint pass.

## Load and exercise the workflow

Use `/skill:docs` in Pi or `/docs` in Claude Code.
Reload Pi or start a fresh Claude session after installation.
[Skill delivery](/docs/agent-skills.md#repo-managed-skills) owns installation and discovery checks.
Discovery proves availability, not automatic selection or successful documentation work.

At closure, `session-improvement` reviews session-edited Markdown and proposes warranted corrections
without applying them.
Read [historical verification](/.agents/plans/ai-harness-roadmap.md#documentation-maintenance)
before citing earlier results; those records do not verify the current workflow.
