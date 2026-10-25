# Design

## Context

The user approved the prototype exclusion and a thin custom schema linked to the session guide.
The latest shared guidance clarifies intent and audience and uses `feedback-loop` for proposal-only
improvement.
Existing OpenSpec changes keep their recorded schema names.

## Goals / Non-Goals

**Goals:** Reduce duplicate planning documents, preserve approval, and keep the workflow portable
across three harnesses.

**Non-goals:** New orchestration services, automatic policy learning, prototype scaffolding, and
broad documentation migration.

## Decisions

| ID | Choice | Reason and alternative |
| --- | --- | --- |
| S1 | Use native `session-workflow` with proposal, specifications, and tasks | A full fork preserves unnecessary design artifacts; third-party schemas add overlapping procedures. |
| S2 | Use native `skip_specs` for unchanged behavior | Keeps two-file maintenance plans without inventing requirements or bypassing real behavior specifications. |
| S3 | Route prototypes before invoking OpenSpec | A prototype schema would create the ceremony the user explicitly rejected. |
| S4 | Link the session guide into shared references | Portable instructions avoid assuming dotfiles paths exist in every project. |
| S5 | Link the schema into OpenSpec's user-level directory | Both machines share one maintained source; project-local copies can override deliberately. |
| S6 | Keep `spec-driven` on existing changes | Changing project defaults must not silently reinterpret active artifacts. |
| S7 | Evaluate evolution through `feedback-loop` | Evidence informs approved changes; feedback never authorizes automatic schema edits. |

## Risks / Trade-offs

- **CLI evolution:** Native schema commands are experimental; integration tests exercise validation
  and archive behavior.
- **Instruction compliance:** Neither schema readiness nor artifact existence proves user approval.
- **Shared schema mutation:** Existing changes resolve current schema files, not frozen content.
  Use a new schema name for incompatible artifact changes.
- **Prototype promotion:** A successful experiment does not authorize production edits or Git
  publication.
- **Cross-machine delivery:** Local verification does not establish Lluvia's installation or runtime
  behavior.

## Migration Plan

1. Create the schema through the native CLI and customize only the approved artifact contract.
2. Add portable links, prototype routing, glossary terms, and reciprocal workflow navigation.
3. Run native lifecycle fixtures and isolated repeat-run delivery tests.
4. Install only the two new links and refresh the generated Cursor rule.
5. Keep pending behavioral checks explicit rather than archiving an unverified change.

**Recovery:** Restore the dotfiles default to `spec-driven` for new changes.
Keep schema files available while existing changes reference them.
Revert only this change's links and guidance; preserve other-session edits and historical records.
