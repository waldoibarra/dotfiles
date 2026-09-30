# Foundations

Read before design-system, markup, CSS, compatibility, or dependency decisions.

## Decision order

Express intent in native HTML first: links navigate, buttons act, forms submit, and headings
structure content. A custom tag name does not supply accessibility semantics. Use labels,
fieldset/legend, and native controls instead of reconstructing their interaction contracts.
Use dialog, details, and popover where their actual behavior fits; do not treat them as interchangeable.

Use CSS layout, custom properties, media/container queries, and native interaction states before
JavaScript measurements. Preserve visible focus, responsive reflow, and reduced-motion preferences.
Avoid imposing a CSS framework or a new design system on an existing application.

## Ultra-light design systems

Implement the five manifesto priorities in SKILL.md as a platform-native system, not a component
framework. Follow the product's visual direction; reuse existing tokens before introducing new ones.

- Define a small set of CSS custom properties for the colors, typography, spacing, and other values
  the product actually repeats. Use semantic names for roles such as surface, text, and accent.
  Avoid speculative token tiers, runtime theme engines, or a generated token pipeline by default.
- Style semantic HTML patterns directly or with small scoped classes. Keep buttons, links, fields,
  and disclosure controls native. A CSS component does not need a custom tag or JavaScript class.
- Express themes through the cascade, custom properties, and appropriate media queries. Add script
  only for a requested interaction such as a persisted user-selected theme.
- Add custom elements only for reusable behavior that benefits from a lifecycle. Load that behavior
  where used; do not require a JavaScript bootstrap just to render the design system's basic controls.
- Ship only the styles, assets, and behaviors the requested flows need. Prefer existing or system
  fonts and lightweight assets unless the visual requirements call for more. Avoid an imported UI
  kit, CSS-in-JS runtime, universal component wrapper, or wholesale reset without a demonstrated need.

Demonstrate actual patterns and their focus, disabled, invalid, and responsive states where relevant,
not just a token swatch sheet. Verify the CSS-only baseline with JavaScript disabled. Report CSS/JS
transfer size and runtime dependencies for the representative page; distinguish measured size from
estimates. Do not invent a universal kilobyte budget or claim that small assets prove accessibility.

## Enhancement and compatibility

Render useful content and native actions before enhancement where feasible. Specify what still
works if a module fails, a request fails, or a feature is unavailable. An inherently interactive
app may require JavaScript; say which behavior does instead of inventing a backend fallback.

Take browser targets from repository configuration or product requirements. Check current MDN
compatibility data and, for consequential edge cases, the specification. Feature-detect optional
APIs and retain the underlying browser action when enhancement is unavailable. Do not freeze
browser version claims into application architecture.

## Dependencies and builds

Use native module imports and ordinary HTTP serving as the starting point. No runtime framework,
including a Web Component framework, is implied by standards-first development. Do not install
Lit, a UI kit, a CSS framework, or a state package because an adjacent skill recommends one.

Existing test runners, linting, development servers, and optional production optimization can stay.
No-build is a default, not a ban on tools. Do not add TypeScript compilation, bundling, a service
worker, or an import map without a demonstrated project need. Keep backend choices outside this
skill's scope. Server-rendered HTML is compatible with this approach.
