---
name: web-app-craft
description: "Use when building, debugging, or reviewing web app interfaces that combine behavior and layout. Coordinate web-standards and css-layout."
license: MIT
metadata:
  author: waldoibarra
  version: "1.0"
---

# Web App Craft

## Activation Contract

- **IS:** coordinating platform behavior and layout for complete web app interface changes.
- **IS NOT:** backend architecture, brand direction, framework scaffolding, or a framework migration.

Use for combined interface work or explicit invocation. Route isolated layout work to `css-layout`
and isolated platform work to `web-standards` without loading this orchestrator.

## Hard Rules

- Read both `web-standards` and `css-layout` before implementation or review. Resolve them through
  the host's skill discovery; the shared installation uses `~/.agents/skills/<name>/SKILL.md`.
  If either is unavailable, report the missing dependency; do not invent its guidance.
- Let `web-standards` own semantics, progressive enhancement, native interaction, component
  lifecycle, DOM isolation, and platform tooling. Let `css-layout` own layout geometry and tokens
  required by its layout components. Keep their implementation rules in those skills.
- Preserve the existing framework, build system, design tokens, and component conventions.
  Apply platform guidance within those contracts; do not replace the stack without a request.
- Child skills hand off directly to each other when needed; do not route back through this skill.

## Decision Gates

| Request | Action |
| --- | --- |
| Build or extend | Complete the requested flow, including applicable failure states |
| Debug | Reproduce the failure, identify its owner, then verify the corrected flow |
| Review | Report located findings and observed impact; do not silently edit |

## Execution Steps

1. Inspect the requested flow, existing implementation, browser targets, and project constraints.
2. Read both skills, then only their task-relevant references. Establish semantic structure and
interaction contracts before selecting and composing layout relationships.
3. Implement or diagnose the integrated flow using each specialist's rules. Keep DOM reading order,
keyboard behavior, and intrinsic reflow consistent when the layout changes.
4. Use both skills' verification references to exercise the actual page. Check the requested flow,
keyboard access, narrow and wide containers, long content, and applicable failure or lifecycle
states. Reuse overlapping checks instead of running two separate verification passes.
5. Fix observed failures within scope and update affected documentation. Finish the requested
behavior; do not stop at a scaffold or add an unsolicited approval checkpoint.

## Output Contract

Report changed behavior or review findings, material platform/layout decisions, browser states
actually exercised, and remaining limits. Distinguish observations from assumptions; one browser
is not cross-browser coverage.

## References

Read the installed `web-standards` and `css-layout` skills before work; resolve their references
from their own skill directories. `evals/evals.json` is maintenance-only.
