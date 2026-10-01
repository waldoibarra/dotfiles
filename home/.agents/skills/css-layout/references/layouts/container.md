# Container

## Contents

- Problem and mechanism
- Primary HTML/CSS example
- Naming, nesting, and variants
- Downloaded component
- Pitfalls and checks
- Sources

## Problem and mechanism

Establish a queryable ancestor when intrinsic layout alone cannot express a useful local adaptation.
Container is a containment utility, not another arrangement of children.
`container-type: inline-size` lets descendant rules respond to the ancestor's inline dimension;
`container-name` lets those rules identify a particular ancestor.

The chapter's diagrams compare three approaches: a viewport query knows the viewport width but not
the nested component's available width; a container query measures the relevant ancestor; intrinsic
wrapping needs neither width measurement nor a manually maintained breakpoint. Prefer the last when
it captures the relationship. Container queries complement the other layouts rather than replacing
them.

For example, growing flex children with a sensible basis can wrap naturally without toggling
percentage widths at a query threshold. A Sidebar responds to both its sidebar width and the main
region's minimum width; increasing the sidebar automatically changes its wrapping threshold. A
manually chosen container breakpoint must instead be maintained when those inputs change. `:has()`
can select based on descendant variants, but a growing matrix of variant-specific thresholds is
often evidence that the intrinsic relationship was lost. Related intrinsic arrangements are
documented in `references/layouts/sidebar.md` and `references/layouts/switcher.md`.

## Primary HTML/CSS example

This authored example adapts a heading's typography to local space. The article is the query target;
its ancestor is the container. The normal readable baseline remains when container queries are
unavailable.

```html
<style>
  .feature-slot {
    container: feature / inline-size;
  }
  .feature-story {
    padding: 1rem;
    border: 1px solid;
  }
  .feature-story h2 {
    font-size: 1.5rem;
    line-height: 1.2;
  }
  .feature-story p {
    max-inline-size: 60ch;
  }
  @container feature (inline-size > 32rem) {
    .feature-story h2 {
      font-size: 2.25rem;
    }
  }
</style>
<div class="feature-slot">
  <article class="feature-story">
    <h2>Layout follows the available space</h2>
    <p>
      This heading changes size with its containing region, even when that region occupies only part
      of a wide page.
    </p>
  </article>
</div>
```

## Naming, nesting, and variants

- **Unnamed:** `.slot { container-type: inline-size; }` and `@container (inline-size > 32rem)` use
  the nearest eligible ancestral container for the queried element. A query does not use an element
  as its own size-query container.
- **Named:** `container: feature / inline-size` combines name and type. `@container feature (...)`
  searches for a matching eligible ancestor, bypassing nearer differently named containers. Reusing
  the same name at several levels still selects the nearest matching one; it is not a global ID
  lookup.
- **Nested:** inserting a new unnamed container can change which dimensions an unnamed query sees.
  Name a stable outer context when nested layout wrappers should not intercept the query. The
  chapter's nested-box example marks the innermost ancestor as the default measuring box.
- **Typography:** container units can scale text with the available region. An authored optional
  rule such as `font-size: clamp(1.5rem, 1rem + 2cqi, 2.25rem)` bounds the growth while relating it
  to container inline size. Check text zoom and actual eligible-container selection rather than
  treating the unit as a substitute for readable limits.
- **Scope:** query any justified layout-dependent property, such as typography or wrapping. Changing
  colors or typefaces merely to demonstrate a breakpoint adds unrelated states. Media queries still
  serve viewport/user-environment concerns; they are not universally forbidden.

The website's generator emits a class with `container-name` and `container-type`; the shorthand
above expresses the same relationship. Its owl illustration is a joke about the remaining design
work: defining a query context does not define useful descendant adaptations for you.

## Downloaded component

Include `Container.css` and use a **side-effect module import** of `Container.js`; unlike the other
inspected components, this module has no default export. **Component usage:**

```html
<link rel="stylesheet" href="./Container.css" />
<script type="module">
  import "./Container.js";
</script>
<container-l name="feature">
  <article class="feature-story"><h2>A locally responsive heading</h2></article>
</container-l>
```

This usage needs the descendant styles/query from the primary example. Omitting `name` creates an
unnamed container.

API: `name` is an optional string, with a downloaded getter returning null when absent/empty. Its
setter writes the attribute. The module registers `container-l`; `name` is the only observed
attribute. Connection and attribute changes call `render`. There are no child observers or Shadow
DOM.

Rendering derives `data-i` from the name and caches a document-head stylesheet per configuration.
Generated CSS sets `display: block`, `container-type: inline-size`, and `container-name` only when
present. A **selected implementation excerpt** identifies the optional-name contract:

```js
get name() {
  return this.getAttribute('name') || null;
}
```

The companion CSS only sets `display: block`: it does **not** establish containment when JavaScript
is unavailable. If query behavior is required without JavaScript, author the containment rule in
your own CSS rather than relying on this download's fallback. No spacing tokens are required.
Attribute trust, style caching, and module-loading conventions are documented in
`references/component-integration.md`.

## Pitfalls and checks

- A size query styles descendants based on an ancestor; it cannot make a container react to its own
  queried size without another eligible ancestor. Keep the primary wrapper/target separation.
- Inline-size containment changes intrinsic sizing participation. Do not add it indiscriminately to
  shrink-wrapped components whose width should come from their children; establish sensible
  available width through the surrounding layout.
- Test the same content in a full-width region and a narrow nested column at the same viewport
  width. Then add a nested query container to confirm whether named/unnamed selection behaves as
  intended.
- Test missing JavaScript and unsupported queries: content should remain readable, even if enhanced
  typography is absent.
- Query breakpoints still require a reason. If the only purpose is to force one/two columns at a
  width that natural flex wrapping already handles, prefer the simpler intrinsic arrangement.

## Sources

Website chapter, media/container/intrinsic-layout diagrams, generator, API, and examples:
[Container chapter](https://every-layout.dev/layouts/container/).

Inspected download (`Container.js`, `Container.css`, `README.txt`):
[Container component archive](https://every-layout.dev/downloads/Container.zip).

Component details above are source-inspected, not claims of runtime verification.
