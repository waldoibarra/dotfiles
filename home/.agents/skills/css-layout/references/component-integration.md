# Integrating the optional layout components

## Contents

- Load the complete contract
- Companion CSS and tokens
- What rendering does
- Configuration limits
- Integration choices
- Sources

Use this reference only when a downloaded native component is useful. Plain HTML and the CSS
mechanisms in `references/layouts/` remain the default; the components package configuration, not a
new layout engine.

## Load the complete contract

Every inspected archive contains `README.txt`, a same-named `.css`, and a same-named `.js`. The
scripts extend `HTMLElement`, register a `*-l` tag, and operate in light DOM: no Shadow DOM,
framework runtime, or imports inside the component files. Ordinary descendant selectors and
inherited tokens therefore still apply.

The following is an authored integration example, assuming the user has obtained Stack and placed
its files at these application-local paths. The CSS and token are essential, not optional
decoration:

```html
<link rel="stylesheet" href="/components/Stack.css" />
<style>
  :root {
    --s1: 1.5rem;
  }
  .example > * {
    margin: 0;
  }
</style>
<script type="module" src="/components/Stack.js"></script>
<stack-l class="example" space="1rem">
  <h2>Shipping address</h2>
  <p>We deliver on working days.</p>
</stack-l>
```

A module script works for all thirteen downloads. Twelve export a default class; Container registers
its element but has no export, so use a side-effect import rather than `import Container from ...`.
Import each registration once per document/module graph: the source checks for `customElements`
support, not whether its tag was already defined by another copy. Serve browser modules over HTTP
using the application's existing tooling.

The archive README's older-browser polyfill/ES5 advice is historical source guidance, not a
requirement to install those packages. Decide support and enhancement strategy with `web-standards`
and the project's browser targets.

## Companion CSS and tokens

The companion stylesheet establishes structural defaults such as `display: flex`, wrapping,
clipping, or positioning. Generated JavaScript rules mainly supply configured values. A successful
custom-element registration does not prove that those structural rules loaded.

| Token                           | Downloaded use                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------ |
| `--s1`                          | Common spacing/padding defaults across Stack, Box, Cluster, Sidebar, Switcher, Cover, Grid |
| `--s0`                          | Reel's configured default item spacing                                                     |
| `--measure`                     | Center's maximum measure and Switcher's fallback threshold                                 |
| `--border-thin`                 | Box border/forced-colors outline                                                           |
| `--color-light`, `--color-dark` | Box inversion and Reel scrollbar treatment                                                 |
| `--item-width`                  | Reel's companion CSS before configuration supplies item sizing                             |

Define the tokens actually used, adapt defaults to existing project tokens, or supply explicit valid
values where the API supports them. Do not import an entire token system solely to satisfy one
layout. See `references/rudiments/modular-scale.md` and
`references/rudiments/global-and-local-styling.md`. Removing JavaScript leaves the companion CSS's
baseline, not necessarily parity with non-default attributes.

## What rendering does

The shared implementation reads configuration through getters, assigns a configuration-derived
`data-i` value, and appends a document-head style block if that ID is not already present. Selectors
target that `data-i`, allowing instances with the same configuration to share rules. The component's
children are not re-rendered or replaced.

`connectedCallback` and `attributeChangedCallback` invoke this CSS generation. Setters generally
reflect properties to attributes; presence-based booleans are enabled by attribute presence, so
`fixed="false"` is still enabled. Chapter references list exact attributes, defaults, exceptions,
and the selected implementation mechanism.

The downloads do not remove generated styles after disconnection. Reel additionally creates
resize/mutation observers on connection and has no disconnected cleanup. If the application
repeatedly mounts/unmounts or generates many unique configurations, inspect this lifecycle rather
than assuming framework-style disposal. For an application-owned alternative, use `web-standards`;
do not silently rewrite upstream behavior while explaining the downloaded API.

## Configuration limits

These are source-level constraints unless an observation is explicitly identified:

- **HTML attribute casing:** several downloads put camelCase strings in `observedAttributes`, while
  HTML normalizes attribute names to lowercase. Initial getters can read values, but live updates
  may miss callbacks. Chromium verification observed `borderWidth` on Box and `itemWidth` on Reel
  changing without changing `data-i`. This is not a claim that every camelCase path has been
  exercised. Prefer initial configuration or a verified application-owned correction when dynamic
  updates are required.
- **Generated rule identity:** keys concatenate values and generated rules interpolate strings into
  selectors/declarations. Treat configuration as trusted application-controlled CSS/selector input,
  not arbitrary user data. Changing the generated `data-i` or sharing it manually breaks that
  association.
- **Style reuse:** the cached key must describe all generated differences. Sidebar omits `noStretch`
  from its key; inspect `references/layouts/sidebar.md` before depending on that variant across
  instances.
- **Boolean/property edge cases:** Stack's `recursive` setter does not follow the other
  presence-attribute setters. Icon adds naming/spacing effects without a symmetric reset path. Their
  chapter references carry the local caveats; do not infer reversibility from the shared lifecycle.
- **Documented versus downloaded API:** Switcher's documented default limit is `4`, but the
  downloaded getter returns `'5'`. Center's documented boolean `gutters` is read as a CSS string by
  the download. Set deliberate values rather than translating documentation labels literally.
- **Stylesheet policy:** injected inline style elements may conflict with the application's CSP.
  Check the actual policy; do not weaken it automatically to accommodate a convenience component.

## Integration choices

Keep semantic structure inside or around the layout wrapper: for example, a list still needs valid
list markup, and an Imposter is not a modal dialog implementation. Light DOM also means application
resets and margin rules can change the result. Check computed styles at the wrapper and its direct
children before blaming the primitive.

For each integration, verify initial markup, the attribute changes the application actually
performs, a second instance with different configuration, and the claimed no-JS baseline. Import
success alone is not layout correctness.

## Sources

Shared findings come from the thirteen archives' `README.txt`, CSS, and JavaScript, inventoried with
hashes in `references/sources.md`. Per-component source links and API analysis live in
`references/layouts/{name}.md`. No complete downloaded implementation is bundled here.
