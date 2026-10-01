---
name: web-standards
description: "Use when building or reviewing standards-first or frameworkless apps, ultra-light design systems, vanilla JavaScript, Web Components, or Pure Web. Start with native HTML/CSS; Lit and TypeScript/Vite are optional, justified choices."
license: MIT
metadata:
  author: waldoibarra
  version: "1.0"
---

# Web Standards

## Activation Contract

Build, extend, debug, or review standards-first web apps and ultra-light design systems.
Pure Web is an architecture, not a mandatory stack. Own platform implementation, not brand
direction or backend architecture. Do not migrate an existing framework app unless requested,
or substitute React, Vue, or another application framework for a standards-first request.
Explicit zero-dependency, no-build, or frameworkless requirements take precedence over defaults
and framework-oriented scaffolding skills.

For layout selection, composition, intrinsic reflow, spacing, overflow, or Every Layout component
CSS/token requirements, use `css-layout` (`~/.agents/skills/css-layout/SKILL.md` in the shared
installation). It owns layout geometry across frameworks; this skill retains semantic HTML,
enhancement, custom-element lifecycle, Light/Shadow DOM, and platform tooling. Use both when
a layout task also changes those platform contracts; do not load platform guidance for geometry alone.
For combined app-interface work, `web-app-craft` coordinates both skills. When invoked directly,
load `css-layout` only for layout decisions; do not load the orchestrator as a dependency.

## Hard Rules

### Pure Web Manifesto: five ground rules

Apply these priorities in order; components are an escalation, not the starting point.

1. **Start with pure HTML**, preferably semantic constructs, and leverage CSS fully.
2. **Use progressive enhancement** before even thinking about Web Components.
3. **Extend HTML with custom elements** when needed; attach JavaScript behavior later,
    only when the element needs it. Custom tags alone supply no accessibility semantics.
4. **Prefer Light DOM** before considering Shadow DOM.
5. **Understand Shadow DOM** before building complex components; account for styling,
    events, focus, accessibility, and forms. It is not a security boundary.

### Implementation constraints

- Default to browser-native ES modules and no runtime dependencies. Lit is an optional runtime
  library when a concrete need justifies it; TypeScript and Vite are optional tooling, not requirements.
  None bypass the five priorities or explicit user constraints. Prefer the smallest suitable tool.
  Lit's default Shadow DOM must not silently override the Light DOM decision; choose the render
  root deliberately. Development and testing tools are allowed within the project's constraints.
- Build design systems from CSS custom properties, semantic HTML patterns, and minimal optional
  behavior. Require a concrete encapsulation need for Shadow DOM, not a component convention.
- Do not replace a framework with a homemade renderer, router toolkit, or reactive engine.
- Preserve native navigation, form behavior, keyboard access, and useful HTML where feasible.
  Identify genuinely JavaScript-dependent functionality rather than promising universal no-JS parity.
- Verify target-browser support before adopting APIs. Never interpolate untrusted values into HTML.

## Decision Gates

| Need | Default | Escalate only when |
| --- | --- | --- |
| Interaction | Native element and CSS | Behavior needs script |
| Design system | CSS tokens and semantic HTML patterns | Repeated needs justify new abstractions |
| Reuse | Markup and focused functions | A custom element needs its own lifecycle |
| Isolation | Light DOM | Reusable internals require style/DOM encapsulation |
| Navigation | Real links and documents | Product behavior requires same-document routing |
| State | Local state and explicit updates | Multiple owners need an explicit shared contract |
| Tooling | Serve native source over HTTP | An existing requirement justifies a build step |

## Execution Steps

1. Inspect the project, requested behavior, browser targets, and existing tooling. Preserve its
    contracts; choose build, debug, or review mode from the request.
2. Read the relevant bundled references below before the corresponding decisions. Resolve paths
    from this installed skill directory, not from the application's working directory.
3. Implement the smallest complete user flow. Keep state ownership, events, and DOM updates explicit.
    Review mode reports evidenced findings without silently rewriting the application.
4. Exercise the actual page in a browser: happy path, failure path, keyboard use, and applicable
    navigation or lifecycle transitions. Follow the verification reference; fix observed failures.
5. Finish the requested scope, update affected documentation, and report evidence. Do not stop at
    a scaffold or insert an approval checkpoint unless the user requested one.

## Output Contract

Return changed behavior, material platform decisions, verification performed, and remaining limits.
For review, return actionable findings with locations and observed impact. Distinguish verified
results from assumptions; do not claim cross-browser coverage from one browser.

## References

Read these files relative to this skill's directory:

- `references/foundations.md` before design-system, markup, CSS, or compatibility decisions.
- `references/components.md` before creating or modifying custom elements.
- `references/application-patterns.md` before forms, rendering, state, routing, or requested
  installation/PWA or cross-origin functionality.
- `references/verification.md` before browser verification.
- `references/sources.md` when checking provenance or updating this skill.

`evals/evals.json` is maintenance-only; do not load it during application work.
