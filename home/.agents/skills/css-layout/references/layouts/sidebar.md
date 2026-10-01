# Sidebar

Use for two unequal regions that sit alongside one another when the main region has enough room,
then become full-width rows. The decision belongs to the container, not the viewport.

## Contents

- [Problem and mechanism](#problem-and-mechanism)
- [Primary example](#primary-example)
- [Variants and selection](#variants-and-selection)
- [Downloaded component](#downloaded-component)
- [Pitfalls and checks](#pitfalls-and-checks)
- [Sources](#sources)

## Problem and mechanism

A viewport breakpoint cannot distinguish the same component in a narrow panel and a wide page. A
wrapping flex container can. Give the sidebar a preferred basis and modest growth; give the main
region a zero basis, much greater growth, and a percentage minimum. The main region consumes almost
all remaining space. When its minimum and the sidebar's basis no longer fit together, they wrap and
each grows across its own row.

The chapter's diagrams distinguish three relationships: ordinary flex wrapping can leave uneven
final rows; the Sidebar has just adjacent/stacked states; and the main region should remain the
larger member while adjacent. A `50%` main minimum expresses that last relationship. The sidebar's
width is a preference, not an exact fixed width: its nonzero growth still receives a small fraction
of free space.

## Primary example

Runnable HTML/CSS; the label and content make this usable without JavaScript or layout tokens.

```html
<style>
  * {
    box-sizing: border-box;
  }
  .profile-layout {
    display: flex;
    flex-wrap: wrap;
    gap: 1.25rem;
  }
  .profile-summary {
    flex-basis: 16rem; /* Preferred size while adjacent. */
    flex-grow: 1; /* Fill the row after wrapping. */
    min-inline-size: 0;
  }
  .profile-detail {
    flex-basis: 0;
    flex-grow: 999; /* Take nearly all remaining inline space. */
    min-inline-size: 50%;
  }
  .profile-layout > * {
    padding: 1rem;
    border: 1px solid;
    overflow-wrap: anywhere;
  }
</style>
<div class="profile-layout">
  <aside class="profile-summary" aria-label="Profile summary">
    <h2>River workshop</h2>
    <p>Open Tuesday through Saturday.</p>
  </aside>
  <section class="profile-detail" aria-label="Workshop details">
    <h2>Plan your visit</h2>
    <p>Bring your current project, or borrow tools and start something new.</p>
  </section>
</div>
```

`gap` works in both configurations without external margins. Flexbox's default stretch gives
adjacent regions equal block size; `align-items: flex-start` retains their natural heights.

## Variants and selection

- **Intrinsic sidebar:** remove its `flex-basis`; an image's declared width or a button's text then
  supplies the preferred size. This is particularly useful for an input plus submit button. Cap
  media at `max-inline-size: 100%` and retain its aspect ratio.
- **Trailing sidebar:** put the main region first and sidebar second in the DOM. Keep their
  corresponding flex rules; do not reverse visual order independently of reading/focus order. The
  component's `side="right"` changes which child is the sidebar, not DOM order.
- **Media object:** a direct image child needs natural-height alignment to avoid stretch distortion;
  alternatively wrap the image and constrain the image within its wrapper. Reverse the emphasis by
  making the text the trailing `30ch` sidebar while the image wrapper grows.
- **Search controls:** use an intrinsic trailing button, zero gap, and a main minimum such as
  `66.666%`. Keep an explicit input label; the layout does not provide accessibility semantics.

Configuration variants for the primary example:

```css
/* Intrinsic summary instead of the explicit 16rem basis. */
.profile-summary {
  flex-basis: auto;
}
/* Natural-height items; useful when media is a direct flex child. */
.profile-layout {
  align-items: flex-start;
}
/* Reserve more of an adjacent row for the main region. */
.profile-detail {
  min-inline-size: 66.666%;
}
```

Switcher (`references/layouts/switcher.md`) suits equal peers that should all switch together;
Cluster (`references/layouts/cluster.md`) suits content-sized items that can wrap independently.
`references/rudiments/composition.md` and `references/rudiments/axioms.md` cover composition and
content-derived dimensions.

## Downloaded component

After placing the acquired `Sidebar.js` and `Sidebar.css` beside the application example:

```html
<link rel="stylesheet" href="./Sidebar.css" />
<script type="module">
  import "./Sidebar.js";
</script>
<sidebar-l side="right" sideWidth="12rem" contentMin="60%" space="1rem">
  <section>
    <h2>Visit</h2>
    <p>Choose a workshop and reserve a place.</p>
  </section>
  <aside aria-label="Hours">Tuesday–Saturday, 10–6</aside>
</sidebar-l>
```

Explicit spacing avoids the default token dependency. `references/component-integration.md` covers
module registration, light DOM, tokens, shared style caching, and attribute normalization. Companion
CSS supplies wrapping flex layout and child growth; JavaScript alone does not.

| Attribute / JS property | Documented default | Effect                                                                                   |
| ----------------------- | ------------------ | ---------------------------------------------------------------------------------------- |
| `side`                  | `left`             | First child is sidebar; every other value selects the last child.                        |
| `sideWidth`             | unset / `null`     | Optional adjacent sidebar basis; otherwise intrinsic content width.                      |
| `contentMin`            | `50%`              | Main region's minimum inline size; use a percentage.                                     |
| `space`                 | `var(--s1)`        | Gap in either orientation.                                                               |
| `noStretch`             | absent / `false`   | Presence requests `align-items: flex-start`; property setter adds/removes the attribute. |

The module registers `sidebar-l`; string getters read attributes with the defaults above and setters
reflect to attributes. `connectedCallback()` renders. Its observed list is `side`, `sideWidth`,
`contentMin`, `space`, `noStretch`; `attributeChangedCallback()` calls render. Render warns for a
`contentMin` without `%`, assigns a configuration-derived `data-i`, and inserts a shared head style
only if that ID does not already exist. The generated selector gives the non-sidebar
`flex-basis: 0`, `flex-grow: 999`, and the requested minimum.

Selected downloaded expressions (not a complete implementation):

```js
// Side selection determines which child receives the main-region rules.
const mainSelector = this.side !== "left" ? ":first-child" : ":last-child";
// The cache key omits the alignment flag.
const configuration = [this.side, this.sideWidth, this.contentMin, this.space].join("");
```

**Material discrepancies:** the chapter promises rerendering for all props, but camelCase names in
`observedAttributes` do not match HTML's lowercased attribute names. Initial render reads those
attributes; do not assume later `sideWidth`, `contentMin`, or `noStretch` changes trigger it. A
Chromium mutation check confirmed that changing `contentMin` leaves `data-i` unchanged; the other
two properties were inspected in source, not independently exercised. Also, source inspection shows
`noStretch` is absent from the style cache key: two otherwise identical instances can reuse the
first alignment rule, and changing that flag cannot create a different cached rule. Prefer the CSS
pattern or adapt and verify the acquired implementation; these findings do not imply the download
has been repaired.

## Pitfalls and checks

- Keep exactly two direct layout children. Nest a Stack inside either region rather than making a
  third sibling.
- Check narrow and wide parent containers at the same viewport size, long unbroken content, large
  text, and direct-image proportions. A percentage minimum is not protection against every
  descendant's fixed width.
- `side` means first/last-child selection in this implementation; its left/right vocabulary is not a
  complete writing-direction policy.
- Without JavaScript the companion CSS retains a wrapping flex layout, but not the configured
  asymmetry, gap, or main-region minimum. Supply matching CSS if that behavior is required before
  upgrade.
- Verify dynamic configuration and opposite `noStretch` values on otherwise identical instances
  before relying on the downloaded component. `references/verification.md` records shared checks.

## Sources

Original summary and illustrative examples derived from the website chapter
[The Sidebar](https://every-layout.dev/layouts/sidebar/), including its generator, diagrams,
media-object examples, and API. Component details inspected in
[Sidebar.zip](https://every-layout.dev/downloads/Sidebar.zip) (`README.txt`, `Sidebar.css`,
`Sidebar.js`). No ebook/PDF source used; no full downloaded implementation reproduced.
