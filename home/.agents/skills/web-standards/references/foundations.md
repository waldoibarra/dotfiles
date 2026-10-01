# Foundations

Read before design-system, markup, CSS, compatibility, or dependency decisions.

## Decision order

Express intent in native HTML first: links navigate, buttons act, forms submit, and headings
structure content. A custom tag name does not supply accessibility semantics. Use labels,
fieldset/legend, and native controls instead of reconstructing their interaction contracts.
Use dialog, details, and popover where their actual behavior fits; do not treat them as interchangeable.

For a binary preference, start with a labeled native checkbox; use switch semantics when on/off
matches the setting. A numeric range input remains a slider even with only two possible values.
Distinguish fragment navigation from a tabs widget: links to sections need not become tabs.
A genuine tabs widget needs tablist/tab/tabpanel roles, selection state, panel relationships,
and the keyboard/focus behavior for its orientation and activation model. Follow the APG tabs
pattern; do not treat its optional keys as universal conformance requirements.

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
estimates. When performance is in scope or a comparative claim is made, derive a small budget from
the audience and requested journeys; use `verification.md` for measurement conditions and evidence.
Do not invent universal byte/score targets or claim that small assets prove accessibility.

## Enhancement and compatibility

Render useful content and native actions before enhancement where feasible. Specify what still
works if a module fails, a request fails, or a feature is unavailable. An inherently interactive
app may require JavaScript; say which behavior does instead of inventing a backend fallback.

Take browser targets from repository configuration or product requirements. Check current MDN
compatibility data and, for consequential edge cases, the specification. Verify JavaScript syntax,
module loading, and runtime APIs across delivered code and imports, including dependencies.
Runtime feature detection cannot rescue a script or module that the browser cannot parse.
Feature-detect optional APIs and retain the underlying browser action when enhancement is unavailable.
If a justified build already produces production output, check that output, not just source code.
Do not mandate legacy transforms or freeze browser version claims into application architecture.

## Dependencies and builds

Use native module imports and ordinary HTTP serving as the starting point. Lit may serve a
demonstrated component or rendering need; it is an optional runtime library, not a required stack
or a reason to skip native HTML, enhancement, or the Light DOM decision. Do not install libraries
or substitute React, Vue, or another application framework because an adjacent skill recommends it.

Existing test runners, linting, development servers, and production optimization can stay.
No-build is a default, not a ban: TypeScript and Vite are optional tooling when project needs justify
them. Respect explicit zero-dependency and no-build constraints; do not add compilation, bundling,
a service worker, or an import map speculatively. Keep backend choices outside this skill's scope.
Server-rendered HTML is compatible with this approach.
