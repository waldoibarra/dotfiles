---
name: web-interface
description: >-
  Coordinates web-standards and css-layout for interface changes combining behavior and layout.
  Use when building, debugging, or reviewing a complete web interface flow across both concerns.
  Isolated platform work belongs to web-standards; isolated geometry belongs to css-layout.
license: MIT
metadata:
  author: waldoibarra
  version: "1.0"
---

# Coordinate a web interface change

**Outcome:** Complete or review one interface flow using the existing platform and layout contracts.
This skill coordinates specialists; it does not own backend architecture, brand direction, or
application scaffolding.
Preserve the existing framework, build system, design tokens, and component conventions.
A request for interface work does not authorize a framework migration.

## Choose the responsible workflow

| Work | Owner |
| --- | --- |
| Combined behavior and layout, or explicit invocation | This coordinator |
| Isolated platform behavior | `web-standards` |
| Isolated layout geometry | `css-layout` |

Do not load this coordinator for isolated work.
Specialists hand off directly when needed; they do not route back through this skill.

## Read the specialist contracts

Read both `web-standards` and `css-layout` before implementation or review.
Resolve them through host discovery; shared installation uses `~/.agents/skills/<name>/SKILL.md`.
Report either missing dependency rather than inventing its guidance.

- `web-standards` owns semantics, progressive enhancement, native interaction, lifecycle, DOM
  isolation, and platform tooling.
- `css-layout` owns layout geometry and the tokens its layout components require.
- Keep implementation rules with those owners; read only their task-relevant references.
- Apply platform guidance within existing project contracts; do not replace the stack without a
  request.

## Complete the requested mode

| Mode | Acceptance |
| --- | --- |
| Build or extend | Complete the requested flow, including applicable failure states |
| Debug | Reproduce the failure, identify its owner, and verify the corrected flow |
| Review | Report located findings and observed impact without silently editing |

1. Establish the outcome, protected behavior, existing implementation, browser targets, and project
    constraints.
2. Reuse settled decisions; ask only about ambiguities that change behavior, risk, or scope.
3. Compare domain terms across the interface, code, and existing glossary.
4. Use `domain-modeling` only for unresolved meanings, not routine work or automatic glossary
    creation.
5. Establish semantic structure and interaction contracts before selecting and composing layout.
6. Implement or diagnose the flow using each specialist's rules.
7. Keep DOM reading order, keyboard behavior, and intrinsic reflow consistent when layout changes.

## Verify the integrated flow

Use both specialists' verification references, resolving paths from their own skill directories.
Establish the local preview, safe test data, and browser access before claiming runtime
verification.
If access is blocked, name the missing prerequisite and continue source inspection without inventing
observations.

Check the requested flow, keyboard access, narrow and wide containers, and long content.
Include applicable failure or lifecycle states.
Reuse overlapping checks instead of running two separate verification passes.
Implementation and debugging finish with in-scope failures corrected and affected documentation
updated.
Do not stop requested implementation at a scaffold or add an unsolicited approval checkpoint.
Review ends with findings and proposed remedies, not file changes.

## Report evidence and limits

Report changed behavior or review findings, material platform/layout decisions, and browser states
actually exercised.
Keep observations separate from assumptions and identify remaining limits.
One browser does not establish cross-browser coverage.

**Maintenance:** Read `evals/evals.json` only when changing this skill; it does not load during
interface work.
