# Where reusable client-delivery guidance belonged

**Historical recommendation:** Keep the human-facing client-delivery playbook in `docs/client-delivery/`.
The [current project-delivery guide](/docs/project-delivery/README.md) succeeds that location.
The observations below reflect the original client-delivery question, not the broadened scope.
Do not put it under `home/.agents/references/`.

This is research, not approval to move the existing playbook or alter agent behavior.
The lead reports six reusable documents in the current client workspace's `reference/` tree.
They comprise an entrypoint, four `playbook/` pages, and `research/ai-assisted-delivery.md`.
This inventory is lead-reported, not independently inspected; client-specific evidence remains excluded.
The playbook covers general discovery, pricing, prototyping, delivery, and support.

## Scope and inspected sources

Accessed 2026-11-10: [Agent Skills format](https://agentskills.io/specification.md)
and [integration guidance](https://agentskills.io/integrate-skills.md).
Accessed 2026-11-10: [Codex skills](https://developers.openai.com/codex/skills.md) and [Codex instructions](https://developers.openai.com/codex/guides/agents-md.md).
Accessed 2026-11-10: [Claude skills](https://code.claude.com/docs/en/skills.md)
and [Claude memory](https://code.claude.com/docs/en/memory.md).
The lead's independent Claude retrieval returned HTTP 403; these claims rely on this worker's access.
Accessed 2026-11-10: [Cursor skills](https://cursor.com/docs/skills.md) and [Cursor rules](https://cursor.com/docs/rules.md).
Context7 guided source discovery for Codex, Claude Code, Cursor, Pi, and Agent Skills.
The cited publisher pages and installed Pi files supplied the evidence below.

Local sources inspected: [`install.conf.yaml`](/install.conf.yaml),
[`docs/documentation.md`](/docs/documentation.md),
[`docs/architecture.md`](/docs/architecture.md), and [`docs/workspace.md`](/docs/workspace.md).
Also inspected [`docs/ai-harness/instructions.md`](/docs/ai-harness/instructions.md),
[`docs/ai-harness/configuration.md`](/docs/ai-harness/configuration.md),
and [`docs/ai-harness/skills.md`](/docs/ai-harness/skills.md).
The harness-supplied Pi documentation path resolved under the installed
`@earendil-works/pi-coding-agent@1.5.2` package's `docs/` directory.
Inspected source files were that package's `docs/skills.md`, `dist/core/skills.js`,
and `dist/core/resource-loader.js`.
The installed `package.json` and `pi --version` both report `1.5.2`.
The lead reports another prompt path referencing `1.5.0/dist/bundle/chunks`.
That path was not supplied here or verified; it must not replace the inspected path.

## Discovery is format-specific, not a universal `.agents/` contract

| Surface | Inspected evidence | Implication |
| --- | --- | --- |
| Skill format | Agent Skills [specification](https://agentskills.io/specification.md): “A skill is a directory containing, at minimum, a `SKILL.md` file”. | Its `references/` directory is optional **inside a skill**. |
| Skill installation | Agent Skills [integration guide](https://agentskills.io/integrate-skills.md): “the Agent Skills specification does not mandate where skill directories live”. | The guide recommends `.agents/skills/` as a cross-client convention, not arbitrary `.agents/` content. |
| Codex | [Skills](https://developers.openai.com/codex/skills.md) lists repository ancestor `.agents/skills` and `$HOME/.agents/skills`. [Instructions](https://developers.openai.com/codex/guides/agents-md.md) documents `AGENTS.md` discovery. | Skill catalogs and startup instructions use different mechanisms. |
| Claude Code | [Skills](https://code.claude.com/docs/en/skills.md) lists `.claude/skills/` and `~/.claude/skills/`. [Memory](https://code.claude.com/docs/en/memory.md#agents-md) documents conditional `AGENTS.md` support. | Local dotfiles link shared sources into native Claude locations; `.agents/references/` has no demonstrated native loading. |
| Cursor | [Skills](https://cursor.com/docs/skills.md) lists project and user `.agents/skills/`. [Rules](https://cursor.com/docs/rules.md) supports `AGENTS.md` and `.cursor/rules/`. | Cursor skills, rules, and ordinary documentation have distinct discovery routes. |
| Installed Pi | Installed `docs/skills.md:61` names `~/.agents/skills/` and `.agents/skills/`. Installed `dist/core/resource-loader.js:130` lists `AGENTS.md` candidates. | Pi discovers named skill and instruction surfaces, not every sibling reference. |

Claude's current [memory guide](https://code.claude.com/docs/en/memory.md#agents-md)
says direct `AGENTS.md` reading requires version 2.1.277 or later.
It also says `CLAUDE.md` takes precedence when both exist.
Dotfiles explicitly links [`~/.claude/CLAUDE.md`](/install.conf.yaml)
to its shared global instruction source.
These sources cannot establish every active Claude session's version or loaded context.

**Local convention:** `home/.agents/references/` houses documents selected through
local instruction links.
[`install.conf.yaml`](/install.conf.yaml) links individual Markdown references using `home/.agents/references/*.md`.
That glob does not include nested `home/.agents/references/client-delivery/*.md` files.
It separately links `docs/prompting.md` and `docs/ai-harness/session-workflow.md` into `~/.agents/references/`.
Their source ownership and installed access paths already differ.
A link, however, only establishes configured delivery, not session loading or exercised compliance.

**Inference:** An arbitrary `.agents/references/` file requires an explicit instruction,
link, or native configuration.
The inspected discovery mechanisms do not establish automatic loading for that directory.
This is a bounded conclusion about the cited clients and installed Pi version, not every agent.

## Choose a documentation owner by audience

| Destination | Benefit | Cost or trigger |
| --- | --- | --- |
| `docs/client-delivery/` | Direct human reading and one concern owner; matches existing dotfiles guides. | Agent use requires a relevant reading link or explicit request. |
| `docs/playbooks/client-delivery/` | Signals procedural format if multiple playbooks already share ownership. | Adds a grouping layer for one concern without demonstrated need. |
| Separate repository | Allows separate audience, governance, and distribution. | Adds maintenance and linking overhead; consider only after ownership diverges. |
| Agent skill | Offers discoverable, task-triggered workflow across supported clients. | Changes content into agent instructions; requires skill design, enrollment, and verification. |
| `home/.agents/references/` | Fits existing harness-selected procedural references. | Mislabels a human playbook as harness content; nested files need new delivery wiring. |

**Recommendation:** The reported six-page playbook supports `docs/client-delivery/` as a destination.
Validate its page inventory, incoming links, and ownership before any approved move.
Preserve the procedure as human-facing documentation, with agent use through scoped links if approved.
Do not duplicate the playbook inside a skill or reference directory.

## Bounded proposal, not a migration

| Existing source or concern | Proposed destination or handling |
| --- | --- |
| Reported client-workspace `reference/` entrypoint and `playbook/` pages | One maintained `docs/client-delivery/` owner, after validating pages and incoming links. |
| Reported `reference/research/ai-assisted-delivery.md` | Evaluate its reader purpose before choosing a retained owner; do not assume research is current guidance. |
| Any existing agent-specific reading triggers | Retain in their instruction owner; link the playbook only where relevant and approved. |
| Existing general harness references | Leave at `home/.agents/references/`; review individually, not wholesale. |
| Client-specific project evidence | Leave in its owning project; do not import or link private sources. |
| This investigation | Keep indexed under `docs/spikes/`, separate from operational guidance. |

Exact policy sentence worth revising later, from
[`docs/documentation.md`](/docs/documentation.md):

> **Dotfiles ownership:** Shared procedures live under `home/.agents/`; workstation maintenance guides
> live under `docs/`.

That sentence classifies all shared procedures as harness content.
The existing `docs/prompting.md` and `docs/ai-harness/session-workflow.md` links
contradict exclusive source placement.
A narrower rule could assign **agent runtime procedures** to harness-owned sources.
It could assign human-facing reusable guides to maintained `docs/` concerns.
Do not edit this policy until the owning reader routes and migration scope receive approval.

[`docs/workspace.md`](/docs/workspace.md) already distinguishes research from shared harness configuration.
[`docs/architecture.md`](/docs/architecture.md) assigns procedures to skills
and product knowledge to owning repositories.
Neither requires every human playbook to become a skill.

## Verification and unresolved facts

Citations above point to opened publisher Markdown, not search summaries alone.
Local path claims were compared with installed Pi files and Dotbot mappings.
The lead supplied a six-document source inventory; this worker did not inspect its contents.
Exact page mapping, incoming links, and the destination remain unvalidated or unapproved.
No behavior was exercised in Codex, Claude, Cursor, or Pi during this research.
Documentation discovery cannot demonstrate actual agent selection, loading, or correct use.
A later migration should inventory incoming links and verify navigation after approval.
