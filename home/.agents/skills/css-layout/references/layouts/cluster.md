# Cluster

## Contents

- Problem and mechanism
- Primary HTML/CSS
- Variants, diagrams, and fallback
- Downloaded component
- Checks and sources

## Problem and mechanism

- Tags, buttons, and navigation links have different natural widths.
- They need to wrap like words, not align to rigid grid columns.
- `display: flex`, `flex-wrap: wrap`, and `gap` distribute content-sized items.
- The gap spaces rows and columns without adding perimeter spacing.

Use a Cluster for action groups, tags, metadata, or wrapping navigation.

Choose instead:

- Grid for aligned tracks (`references/layouts/grid.md`).
- Switcher when the whole group should switch together (`references/layouts/switcher.md`).
- Reel when horizontal scrolling is intentional (`references/layouts/reel.md`).

## Primary HTML/CSS

An authored list example with no custom-property dependencies:

```html
<style>
  .topic-cluster {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: flex-start;
    align-items: center;
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .topic-cluster a {
    display: block;
    padding: 0.4em 0.75em;
    border: 1px solid currentColor;
    overflow-wrap: anywhere;
  }
  .topic-cluster > * {
    min-inline-size: 0;
    max-inline-size: 100%;
  }
</style>
<ul class="topic-cluster" role="list" aria-label="Topics">
  <li><a href="#delivery">Delivery</a></li>
  <li><a href="#returns">Returns and exchanges</a></li>
  <li><a href="#support">Customer support</a></li>
</ul>
```

- List reset rules are specific to this example.
- Not every Cluster must erase margins supplied by an enclosing Stack.
- The explicit list role preserves the grouping when list markers are removed.
  - Some browser/assistive-technology combinations need it.

## Variants, diagrams, and fallback

- **Alignment:** `justify-content` distributes along the row; `align-items` aligns within each row.
  - Use `flex-end` for end-aligned actions or `center` for a centered group.
  - Use `space-between` to distribute remaining space.
  - Gap remains the minimum separation; distributed free space can make the apparent gap larger.
- **Header composition:** an outer Cluster can contain a logo and a navigation wrapper.
  - Nest a second Cluster inside that wrapper for links.
  - The outer group uses `space-between` and `center`; the inner group stays start-aligned.
  - In the chapter's diagram, the whole navigation group moves below the logo before its links wrap.
  - The links do not scatter beside and below the logo.
  - Preserve that wrapper; flattening every link into the outer Cluster changes the wrapping unit.
- **Why not inline-block:** source whitespace introduces an extra word-space width.
  - Setting the parent's font size to zero hides it but complicates inherited and `em`-based sizing.
  - It also does not solve wrapping margins.
- **Historical margin fallback:** equal half-gaps around every child combine into full gaps between
  items.
  - They leave half a gap at the perimeter.
  - A negatively margined inner flex wrapper offsets those outside half-gaps.
  - An outer wrapper insulates adjacent content and Stack spacing.
  - The chapter's diagrams show one-sided margins causing indented wrapped lines or doubled apparent
    parent padding.
  - They then show the negative wrapper pulling items back to the intended edges.
- **Prefer gap:** it eliminates the extra wrapper, arithmetic, and potential horizontal overflow of
  negative margins.
  - The chapter recommends accepting flush items in older flex-gap-less browsers unless the fallback
    is genuinely required.
  - `@supports (gap: 1rem)` alone cannot distinguish Grid-only gap support from Flexbox gap support.

The optional legacy variant is separate from the primary example.

It requires an outer `.legacy-cluster`, one inner wrapper, then the items:

```css
.legacy-cluster > * {
  display: flex;
  flex-wrap: wrap;
  margin: -0.375rem; /* Negates one child's half-gap at each perimeter edge. */
}
.legacy-cluster > * > * {
  margin: 0.375rem;
}
```

- Do not add that margin fallback on top of gap: the spaces accumulate.
- Test its overflow instead of concealing it with arbitrary clipping.

## Downloaded component

- Include `Cluster.css` and import `Cluster.js` as a module.
- Define `--s1` or set `space`.
- `references/component-integration.md` documents the light-DOM contract and shared setup.

Component usage with list semantics:

```html
<cluster-l space="0.75rem" align="center" role="list" aria-label="Services">
  <div role="listitem"><a href="#pickup">Pickup</a></div>
  <div role="listitem"><a href="#shipping">Home delivery</a></div>
</cluster-l>
```

| API       | Downloaded default | Meaning                              |
| --------- | ------------------ | ------------------------------------ |
| `justify` | `flex-start`       | CSS `justify-content` value          |
| `align`   | `flex-start`       | CSS `align-items` value              |
| `space`   | `var(--s1)`        | CSS gap; minimum space between items |

- The chapter's generator initially displays `align-items: center`.
- The component API and downloaded code default to `flex-start`; choose the desired alignment
  explicitly.
- `Cluster` extends `HTMLElement` and registers `cluster-l`.
- All three getters read strings and all setters write attributes.
- All three lowercase names are observed; connection and attribute changes call `render`.
- Render sets a configuration-derived `data-i`.
- Per unseen configuration, it adds one matching head stylesheet with justification, alignment, and
  gap.
- The component neither rearranges children nor creates shadow DOM.

Selected downloaded expression:

```js
// The spacing default is a token, not a built-in length.
this.getAttribute("space") || "var(--s1)";
```

- `Cluster.css` supplies wrapping flex layout and default alignment, but no gap declaration.
- The untouched companion stylesheet therefore produces a flush CSS-only fallback.
- Add a deliberate default gap if spacing must survive unavailable JavaScript.

## Checks and sources

- Resize the _container_ through wrapping thresholds.
  - Check short and long labels, multiple rows, and all chosen justifications.
  - Check items wider than the container.
- Confirm equal row/column gaps with no false padding at the outside edges.
- Preserve DOM reading and focus order; visual reordering is unnecessary.
- A `cluster-l` is not a native list.
  - Use roles as above, or retain a native `ul` with the CSS layout.

Website chapter, diagrams, generator, and API: [Cluster](https://every-layout.dev/layouts/cluster/).

Inspected download (`README.txt`, `Cluster.css`, `Cluster.js`):
[Cluster.zip](https://every-layout.dev/downloads/Cluster.zip).
