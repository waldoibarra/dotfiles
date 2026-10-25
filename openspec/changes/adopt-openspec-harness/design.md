# Design

## Context

See [the proposal](proposal.md) for the problem and scope.
Waldo approved the scope, selected `latest`, and requested a full `dots` run.
The full documentation refactor is deferred to the next session.

Pi already handles third-party Skill-tool requests through its tracked `APPEND_SYSTEM.md`.
Existing planning and documentation skills remain responsible for reasoning quality.
OpenSpec supplies native change structure, validation, and lifecycle operations.

## Goals / Non-Goals

**Goals:** Reuse upstream tooling, preserve human approval, and reproduce setup across both
machines.

**Non-goals:** Custom schemas, terminal orchestration frameworks, company adoption, and wholesale
conversion of historical records.
Live multi-agent collaboration and Lluvia's workstation verification require their own observed
results.

## Decisions

| ID | Choice | Rationale and tradeoff |
| --- | --- | --- |
| D1 | Mise-managed `npm:@fission-ai/openspec = latest` | Matches the requested upgrade policy; changing upstream behavior requires validation after upgrades. |
| D2 | Native core profile with skills-only delivery | Ordinary conversation remains usable; removing the CLI would break upstream skill operations. |
| D3 | Generate shared skills in `.agents/skills/`; link both clients to them | One upstream-generated source avoids separate edited skill copies. |
| D4 | Track native global configuration and link it with Dotbot | Both machines receive identical portable defaults; runtime state remains local. |
| D5 | Refresh generated skills through native dry-run/update commands | Preserve upstream ownership and avoid rewriting unchanged inputs. |
| D6 | Retain one lead per approved change | Shared files enable handoffs but do not lock tasks or coordinate concurrent writes. |
| D7 | Defer historical-record restructuring | Avoid another blanket move before the dedicated documentation session. |

## Risks / Trade-offs

- **Upstream drift:** Validate native operations and generated skills after updates.
- **Partial synchronization:** Report which steps completed; do not equate file delivery with
  fresh-session behavior.
- **Concurrent writes:** Isolate writers and serialize canonical task updates and archiving through
  the lead.
- **Personal evidence:** Keep operator details outside public product repositories.
- **Publication:** The existing `dots` workflow can publish skill-lock changes and other unpushed
  commits.

## Migration Plan

1. Declare the CLI and skills-only preferences; initialize with the native shared-skills target.
2. Link generated skills into both clients and add idempotent native updates to workstation
  synchronization.
3. Update shared approval policy, current integration guidance, and the vault's existing
  verification procedure.
4. Run isolated delivery tests, native validation, repeat-run checks, and the user-authorized `dots`
  workflow.
5. Leave this change active until its remaining acceptance checks are complete.

**Recovery:** Revert this change's owned configuration and remove only its verified links.
Keep change artifacts and preserved evidence; never reset unrelated working-tree changes.
