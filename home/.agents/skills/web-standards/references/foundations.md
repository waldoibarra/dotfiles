# Foundations

Read before design-system, markup, CSS, compatibility, or dependency decisions.

## Contents

- Decision order
- Ultra-light design systems
- Enhancement and compatibility
- Dependencies and builds

## Decision order

- Express intent in native HTML first.
  - Links navigate, buttons act, forms submit, and headings structure content.
- A custom tag name does not supply accessibility semantics.
- Use labels, fieldset/legend, and native controls instead of reconstructing their interaction
  contracts.
- Use dialog, details, and popover where their actual behavior fits.
  - Do not treat them as interchangeable.

Control and widget choice:

- For a binary preference, start with a labeled native checkbox.
  - Use switch semantics when on/off matches the setting.
- A numeric range input remains a slider even with only two possible values.
- Distinguish fragment navigation from a tabs widget: links to sections need not become tabs.
- A genuine tabs widget needs these parts:
  - tablist/tab/tabpanel roles, selection state, and panel relationships.
  - Keyboard/focus behavior for its orientation and activation model.
- Follow the APG tabs pattern.
  - Do not treat its optional keys as universal conformance requirements.

CSS before script:

- Use CSS layout, custom properties, media/container queries, and native interaction states before
  JavaScript measurements.
- Preserve visible focus, responsive reflow, and reduced-motion preferences.
- Avoid imposing a CSS framework or a new design system on an existing application.

## Ultra-light design systems

- Implement the five manifesto priorities in SKILL.md as a platform-native system, not a
  component framework.
- Follow the product's visual direction.
- Reuse existing tokens before introducing new ones.

System elements:

- Define a small set of CSS custom properties for values the product actually repeats.
  - Cover colors, typography, spacing, and other repeated values.
  - Use semantic names for roles such as surface, text, and accent.
  - Avoid speculative token tiers, runtime theme engines, or a generated token pipeline by
    default.
- Style semantic HTML patterns directly or with small scoped classes.
  - Keep buttons, links, fields, and disclosure controls native.
  - A CSS component does not need a custom tag or JavaScript class.
- Express themes through the cascade, custom properties, and appropriate media queries.
  - Add script only for a requested interaction such as a persisted user-selected theme.
- Add custom elements only for reusable behavior that benefits from a lifecycle.
  - Load that behavior where used.
  - Do not require a JavaScript bootstrap just to render the design system's basic controls.
- Ship only the styles, assets, and behaviors the requested flows need.
  - Prefer existing or system fonts and lightweight assets unless visual requirements call for
    more.
  - Avoid an imported UI kit, CSS-in-JS runtime, universal component wrapper, or wholesale reset
    without a demonstrated need.

Demonstration and evidence:

- Demonstrate actual patterns, not just a token swatch sheet.
  - Show their focus, disabled, invalid, and responsive states where relevant.
- Verify the CSS-only baseline with JavaScript disabled.
- Report CSS/JS transfer size and runtime dependencies for the representative page.
  - Distinguish measured size from estimates.
- When performance is in scope or a comparative claim is made, derive a small budget.
  - Derive it from the audience and requested journeys.
  - Use `verification.md` for measurement conditions and evidence.
- Do not invent universal byte/score targets.
- Do not claim that small assets prove accessibility.

## Enhancement and compatibility

- Render useful content and native actions before enhancement where feasible.
- Specify what still works if a module fails, a request fails, or a feature is unavailable.
- An inherently interactive app may require JavaScript.
  - Say which behavior does instead of inventing a backend fallback.

Browser targets:

- Take browser targets from repository configuration or product requirements.
- Check current MDN compatibility data.
  - For consequential edge cases, also check the specification.
- Verify JavaScript syntax, module loading, and runtime APIs across delivered code and imports.
  - Include dependencies.
- Runtime feature detection cannot rescue a script or module that the browser cannot parse.
- Feature-detect optional APIs.
  - Retain the underlying browser action when enhancement is unavailable.
- If a justified build already produces production output, check that output, not just source.
- Do not mandate legacy transforms or freeze browser version claims into application architecture.

## Dependencies and builds

- Use native module imports and ordinary HTTP serving as the starting point.
- Lit may serve a demonstrated component or rendering need.
  - It is an optional runtime library, not a required stack.
  - It is not a reason to skip native HTML, enhancement, or the Light DOM decision.
- An adjacent skill's recommendation never justifies installing libraries or substituting React,
  Vue, or another application framework.

Existing tooling and builds:

- Existing test runners, linting, development servers, and production optimization can stay.
- No-build is a default, not a ban.
  - TypeScript and Vite are optional tooling when project needs justify them.
- Respect explicit zero-dependency and no-build constraints.
- Do not add compilation, bundling, a service worker, or an import map speculatively.
- Keep backend choices outside this skill's scope.
- Server-rendered HTML is compatible with this approach.
