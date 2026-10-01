# Grid

Use for a collection whose columns should align across rows while their number adapts to the
available container width. Build a grid **of content**, rather than requiring unknown content to fit
a predetermined diagram.

## Contents

- [Problem and mechanism](#problem-and-mechanism)
- [Primary example](#primary-example)
- [Variants and alternatives](#variants-and-alternatives)
- [Downloaded component](#downloaded-component)
- [Pitfalls and checks](#pitfalls-and-checks)
- [Sources](#sources)

## Problem and mechanism

Wrapping flex items such as `flex: 1 1 30ch` are a valid content-first layout, but each line
distributes free space independently. The chapter's comparison diagram shows discontinuous vertical
gutters in flex versus aligned columns in Grid. Grid accepts an incomplete last row rather than
making its final items wider than the others.

`repeat(auto-fit, minmax(min(18rem, 100%), 1fr))` combines three decisions:

- `auto-fit` calculates how many tracks fit, rather than prescribing a column count at viewport
  breakpoints.
- `minmax(..., 1fr)` lets the tracks share available width equally while retaining a wrapping
  threshold.
- The nested `min(18rem, 100%)` caps the threshold at the container's width. A bare
  `minmax(18rem, 1fr)` would overflow a container narrower than `18rem`.

The source's overflow/solution diagrams isolate this last distinction: a nominally responsive grid
can still be too wide as a single column unless the minimum itself can shrink. Setting the minimum
to zero instead is not equivalent; it removes the useful track-size threshold for wrapping.

## Primary example

Runnable HTML/CSS with a single-column baseline and a feature-tested intrinsic grid. The `18rem`
minimum is an authored example, not the download's `250px` default.

```html
<style>
  * {
    box-sizing: border-box;
  }
  .workshop-grid {
    display: grid;
    grid-template-columns: 100%;
    gap: 1rem;
    align-content: start;
  }
  @supports (width: min(18rem, 100%)) {
    .workshop-grid {
      grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
    }
  }
  .workshop-card {
    min-inline-size: 0;
    padding: 1rem;
    border: 1px solid;
    overflow-wrap: anywhere;
  }
  .workshop-card > * {
    margin-block: 0;
  }
  .workshop-card > * + * {
    margin-block-start: 0.75rem;
  }
  .workshop-card p {
    max-inline-size: 60ch;
  }
</style>
<div class="workshop-grid">
  <article class="workshop-card">
    <h2>Wood</h2>
    <p>Shape a small object with hand tools.</p>
  </article>
  <article class="workshop-card">
    <h2>Clay</h2>
    <p>Explore useful forms and textured surfaces.</p>
  </article>
  <article class="workshop-card">
    <h2>Weaving</h2>
    <p>Learn a pattern, then make it your own.</p>
  </article>
  <article class="workshop-card">
    <h2>Print</h2>
    <p>Build a design from reusable marks.</p>
  </article>
</div>
```

Grid items stretch to their row's block size by default. Different rows can still have different
heights; the pattern does not make every card in the entire collection equally tall. The card styles
illustrate composition: outer padding/border corresponds to Box, inner rhythm to Stack, and text
measure remains independent of track width.

## Variants and alternatives

- **Typographic minimum:** choose a `ch`/`rem` value or `calc(var(--measure) / 3)` when a global
  measure token exists. The layout minimum describes useful content width, not a device category.
- **Flex alternative:** a wrapping flex container with growing/shrinking `30ch` bases fills
  incomplete rows. Keep a text measure inside wide final items so filling the row does not produce
  excessively long lines. `references/rudiments/axioms.md` covers content-derived constraints.
- **`auto-fill` versus `auto-fit`:** `auto-fill` retains empty tracks; `auto-fit` collapses them and
  distributes that room to occupied tracks. With fewer cards than a row could hold, this changes
  card width. It is not a cosmetic spelling difference.
- **Fallback:** preserve the one-column grid if the enhanced expression is unsupported. The chapter
  also suggests a flex fallback when its uneven final row is acceptable.
- **Explicit placement:** named areas or manually positioned editorial grids solve a different
  problem. Use content-driven queries when those relationships really need to change; the chapter's
  intrinsic method is not a ban on modern container queries.

Historical observer alternative, not needed for the primary CSS: the chapter first measures a
configured CSS minimum with a temporary element, converts it to pixels, and toggles a class using
`ResizeObserver`. Only that class enables a bare fixed-minimum track rule. If the API is absent, the
single-column baseline remains. The later `min()` solution removes this JavaScript requirement.

Selected mechanism, expressed as an authored fragment; `grid` is the target element and
`minimumPixels` is the measured configured minimum:

```js
const observer = new ResizeObserver((entries) => {
  for (const entry of entries) {
    grid.classList.toggle("has-room", entry.contentRect.width > minimumPixels);
  }
});
observer.observe(grid);
// Disconnect when the owning view is removed; remeasure if the minimum changes.
```

The source's `<watched-box>` mention is a general container-observation alternative, not a Grid
dependency. Prefer the CSS minimum cap for this particular problem. Switcher
(`references/layouts/switcher.md`) avoids all multirow intermediate states; Reel
(`references/layouts/reel.md`) provides deliberate horizontal scrolling.

## Downloaded component

Usage after acquiring the JS and companion CSS files:

```html
<link rel="stylesheet" href="./Grid.css" />
<style>
  :root {
    --s1: 1rem;
    --measure: 60ch;
  }
</style>
<script type="module">
  import "./Grid.js";
</script>
<grid-l min="calc(var(--measure) / 3)" space="1rem">
  <article>
    <h2>Wood</h2>
    <p>Work with hand tools.</p>
  </article>
  <article>
    <h2>Clay</h2>
    <p>Explore useful forms.</p>
  </article>
  <article>
    <h2>Print</h2>
    <p>Build a repeatable design.</p>
  </article>
</grid-l>
```

Box (`references/layouts/box.md`) and Stack (`references/layouts/stack.md`) provide card styling
within each cell; their custom elements also require their own JS and CSS imports. Grid does not
style card internals. Shared light-DOM and token setup is in `references/component-integration.md`.

| Attribute / JS property | Default     | Effect                                                                |
| ----------------------- | ----------- | --------------------------------------------------------------------- |
| `min`                   | `250px`     | CSS length used as the first argument of the nested `min()` function. |
| `space`                 | `var(--s1)` | Gap between rows and columns.                                         |

`Grid.js` registers `grid-l`. Both properties have fallback-reading getters and attribute-reflecting
setters; `observedAttributes` is `min`, `space`. Connection and attribute changes invoke render.
Render derives a key from both values, assigns `data-i`, and appends a shared head style only for a
new key. The generated gap is unconditional; the generated tracks are inside a
`@supports (width: min(..., 100%))` rule. There is no `ResizeObserver` in this download.

Selected downloaded CSS-template expressions:

```css
/* ${this.min} is interpolated by Grid.js, not valid standalone CSS. */
@supports (width: min(${this.min}, 100%)) {
  [data-i="${this.i}"] {
    grid-template-columns: repeat(auto-fill, minmax(min(${this.min}, 100%), 1fr));
  }
}
```

**Material discrepancy:** the website narrative and generator use `auto-fit`, but the downloaded
component uses `auto-fill`. The primary example follows the website; the component retains empty
tracks. Decide deliberately which behavior the product needs instead of assuming they are identical.
The companion CSS independently establishes `display: grid`, `align-content: start`, a token-based
gap, and `grid-template-columns: 100%`; JavaScript alone is insufficient.

## Pitfalls and checks

- Test a parent narrower than the configured minimum, not just a typical mobile viewport. Also test
  one item, an incomplete row, and enough items for several rows.
- Check long unbroken content, intrinsically wide media, and user-enlarged text. A track fitting its
  container does not make every descendant fit its track; constrain media and handle wrapping
  intentionally.
- Do not confuse shared track width with shared height across all rows. If a different alignment is
  chosen, inspect the resulting gaps rather than assuming a masonry layout.
- Runtime smoke in Chromium with downloaded `min="18rem"` observed two `388px` tracks at an `800px`
  container and one `180px` track at `180px`, without grid overflow. Those measurements confirm
  those cases, not all content or browser combinations.
- With JavaScript disabled, the companion stylesheet retains the single-column baseline; configured
  `min` is not read by CSS. `references/verification.md` covers further checks.

## Sources

Original summary and authored examples derived from
[The Grid](https://every-layout.dev/layouts/grid/): content-first diagrams, flex comparison and
measure mitigation, fixed-minimum failure, observer alternative, `min()` solution, card composition,
generator, and API. Download inspected: [Grid.zip](https://every-layout.dev/downloads/Grid.zip)
(`README.txt`, `Grid.css`, `Grid.js`). Website only; no ebook/PDF or full implementation
reproduction.
