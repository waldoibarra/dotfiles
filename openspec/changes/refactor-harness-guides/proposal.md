# Proposal

## Why

The harness guides mix orientation, operational reference, and historical trial results.
Readers must distinguish current configuration from older observations without losing useful constraints.

## What Changes

Refactor `docs/ai-harness/` and repair related documentation links.
Preserve safety boundaries, unique current information, and consequential evidence.
Leave configuration, scripts, skills, schema semantics, private data, and frozen records unchanged.

## Approach and tradeoffs

| Decision | Choice | Reason |
| --- | --- | --- |
| D1 | Keep the existing directory and focused guides | A wholesale redesign adds navigation churn without demonstrated benefit. |
| D2 | Extract configuration and Ghostwriter references from the README | Readers reach maintenance details directly; the overview stays concise. |
| D3 | Separate behavioral cases from verification procedures | Optional probe specifications no longer obscure ordinary checks. |
| D4 | Retain voice evidence under limitations | Historical results remain distinguishable from current runtime guarantees. |
| D5 | Preserve referenced README anchors with concise destination links | Existing external reading routes continue working. |

A wording-only pass would leave duplicated ownership and mixed page purposes intact.
Recover by reverting this documentation change; no workstation rollback or synchronization is required.

## Capabilities

No runtime behavior or instruction policy changes.
Specifications are skipped because this change reorganizes and corrects documentation only.

## Impact

- `README.md`: purpose, task routes, and compatibility links.
- `configuration.md`: shared delivery ownership, Claude settings, and Cursor rendering.
- `ghostwriter.md`: profile routing, privacy, and delivery constraints.
- `harness-verification.md`: acceptance, static checks, loading, execution, and recovery.
- `verification-cases.md`: retained synthetic cases and optional probe examples.
- `pi/README.md`: orientation and routes; version evidence moves to `pi/limitations.md`.
- Existing focused guides: verified corrections, clearer qualifications, and reduced duplication.
- Related setup, architecture, instructions, MCP, and workspace links: repaired where affected.

No private work sources are required to clarify work-parity boundaries.
No historical plan migration or new ADR is included.

## Verification

Check claims against tracked configuration, delivery scripts, tests, and applicable installed documentation.
Resolve local links and anchors, including incoming references to moved sections.
Run `just lint-md`, `just lint-ec`, and `git diff --check`.
Run isolated schema checks because the installed session guide remains linked.
Review preservation and prose separately from formatting.
Do not run workstation sync, inference, OAuth, microphone tests, or external service writes.
Static documentation checks do not establish current runtime behavior.

## Approval

The user approved the directory-wide plan and related-file refactor in this conversation.
The user separately requested a push when complete.
