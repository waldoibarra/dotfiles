# Switcher

Use when a small group of peers should form either one row or one column, without an intermediate
two-plus-one arrangement that accidentally makes the last item look more important.

## Contents

- [Problem and mechanism](#problem-and-mechanism)
- [Primary example](#primary-example)
- [Variants and selection](#variants-and-selection)
- [Downloaded component](#downloaded-component)
- [Pitfalls and checks](#pitfalls-and-checks)
- [Sources](#sources)

## Problem and mechanism

Ordinary wrapping flex items grow independently on each line. The chapter's diagrams show how an
incomplete last row then contains wider items, and how a Switcher bypasses that intermediate
arrangement. Numbered steps and equally important offers often benefit from a single reading axis
instead.

The switching expression is `calc((threshold - 100%) * 999)` for each child's flex basis. Here
`100%` is the flex container's inline size, not the viewport. Above the threshold the negative
calculation reaches the property's nonnegative lower bound, leaving growth to distribute the row.
Below it the large positive basis forces separate lines. This is a practical switching technique,
not an actual conditional statement; extreme child minimum sizes and values very close to the
threshold still merit checking.

The chapter describes the negative result both as an invalid declaration being dropped and as
correction to zero. Do not depend on it reverting to intrinsic `auto` sizing: the useful mechanism
is the calculated basis's zero lower bound. Equal growth also assumes no child's content-based
minimum dominates its peers.

## Primary example

Runnable HTML/CSS. This uses a four-item quantity limit, independently of the width threshold.

```html
<style>
  * {
    box-sizing: border-box;
  }
  .steps {
    --switch-at: 36rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 0;
    list-style: none;
  }
  .steps > li {
    flex-grow: 1;
    flex-basis: calc((var(--switch-at) - 100%) * 999);
    min-inline-size: 0;
    padding: 1rem;
    border: 1px solid;
    overflow-wrap: anywhere;
  }
  /* Five or more children: force every item onto its own line. */
  .steps > :nth-last-child(n + 5),
  .steps > :nth-last-child(n + 5) ~ * {
    flex-basis: 100%;
  }
</style>
<ol class="steps" aria-label="Reservation steps">
  <li>
    <h2>1. Choose</h2>
    <p>Find a workshop that suits your project.</p>
  </li>
  <li>
    <h2>2. Reserve</h2>
    <p>Select a date and save your place.</p>
  </li>
  <li>
    <h2>3. Visit</h2>
    <p>Meet your tutor and get started.</p>
  </li>
</ol>
```

The quantity selector counts from the end: with at least five children, `:nth-last-child(n+5)` finds
the earlier children and `~ *` reaches the rest. Fewer children match neither branch. This keeps
excessive item counts from producing arbitrarily thin columns even in a wide parent.

## Variants and selection

- **Proportions:** `.steps > :nth-child(2) { flex-grow: 2; }` gives the second item twice the share
  of free space in the row. Borders, padding, and intrinsic minima mean its measured outer width
  need not be exactly double. Stacked items still fill a line.
- **Content width:** constrain images and other wide descendants with `max-inline-size: 100%`; make
  long text wrap intentionally. The chapter's content-width diagram illustrates a large nested
  element defeating otherwise equal proportions.
- **Different quantity limit:** change both selectors' `n+5` to `n+(limit + 1)` expressed as an
  actual number. This is an element-count limit, not a viewport breakpoint.
- **Legacy gutters:** the chapter also covers a wrapper with negative half-gap margins and half-gap
  child margins. Because that wrapper becomes wider, its calculation subtracts the gap from `100%`.
  Prefer `gap` for new implementations; do not combine the two spacing schemes.

Historical margin-based variant, distinct from the primary example; `.legacy-switcher` wraps a
`.row` whose children are the items:

```css
.legacy-switcher {
  --space: 1rem;
  --threshold: 36rem;
}
.legacy-switcher > .row {
  display: flex;
  flex-wrap: wrap;
  margin: calc(var(--space) / -2);
}
.legacy-switcher > .row > * {
  flex-grow: 1;
  margin: calc(var(--space) / 2);
  flex-basis: calc((var(--threshold) - (100% - var(--space))) * 999);
}
```

Grid (`references/layouts/grid.md`) suits multiple rows with aligned columns, Cluster
(`references/layouts/cluster.md`) permits independent wrapping, and Sidebar
(`references/layouts/sidebar.md`) provides two deliberately unequal regions. A normal wrapping flex
layout remains valid when a wider final row is not misleading.

## Downloaded component

Component usage after acquiring the named JS and companion CSS files:

```html
<link rel="stylesheet" href="./Switcher.css" />
<style>
  :root {
    --measure: 60ch;
    --s1: 1rem;
  }
</style>
<script type="module">
  import "./Switcher.js";
</script>
<switcher-l threshold="36rem" space="1rem" limit="4">
  <section>
    <h2>Choose</h2>
    <p>Select your workshop.</p>
  </section>
  <section>
    <h2>Reserve</h2>
    <p>Save your place.</p>
  </section>
  <section>
    <h2>Visit</h2>
    <p>Bring your project.</p>
  </section>
</switcher-l>
```

The companion CSS establishes wrapping flex layout, child growth, and a fallback threshold using
`--measure`; JavaScript generates the instance gap, configured basis, and quantity selectors.
`references/component-integration.md` covers light-DOM integration, shared style caching, tokens,
and import ownership.

| Attribute / JS property | Website default  | Downloaded behavior                                                                  |
| ----------------------- | ---------------- | ------------------------------------------------------------------------------------ |
| `threshold`             | `var(--measure)` | CSS length used as the container threshold.                                          |
| `space`                 | `var(--s1)`      | Flex gap.                                                                            |
| `limit`                 | integer `4`      | Getter defaults to string `'5'`; `parseInt` supplies the quantity selector's number. |

**Material discrepancy:** the API and source JSDoc say four horizontal items, but the downloaded
getter permits five; six triggers its quantity override. Specify `limit="4"` to get the documented
default. The string `'5'` getter result was also observed in Chromium, not merely inferred from
source.

Selected downloaded implementation expressions:

```js
// Getter fallback is a string, not the API table's integer 4.
this.getAttribute("limit") || "5";
// Interpolated into both :nth-last-child selector branches.
parseInt(this.limit) + 1;
```

`switcher-l` registers on import. All three properties have attribute-reflecting setters and
fallback-reading getters. `observedAttributes` contains `threshold`, `space`, and `limit`;
connection and attribute changes call render. Render joins those values into a configuration key,
sets `data-i`, and creates a matching head style only once per key. Quantity adaptation itself is
CSS: adding/removing children does not require an observer. There is no validation of malformed or
negative limits; provide a deliberate positive integer.

## Pitfalls and checks

- Check the same viewport with wide and narrow parent containers; changing viewport alone does not
  prove container independence.
- Check just below/above the chosen threshold and at the maximum item count plus one. Very narrow
  parents, large gaps, and forced minimum widths can interfere with the intended row.
- Keep DOM order meaningful in either orientation. A visual sequence still needs ordered-list or
  equivalent content semantics.
- Companion CSS alone does not implement the configured `limit` or gap. Supply those in a CSS
  baseline if needed without JavaScript.
- Chromium smoke of the acquired component observed three peers in one row at an `800px` container
  and three rows at `300px`. This establishes those cases, not every threshold or browser. Further
  checks belong in `references/verification.md`.

## Sources

Original summary and examples derived from
[The Switcher](https://every-layout.dev/layouts/switcher/): intrinsic sizing, symmetry diagrams,
switching expression, gutters, proportions, quantity query, generator, and API. Component details
inspected in [Switcher.zip](https://every-layout.dev/downloads/Switcher.zip) (`README.txt`,
`Switcher.css`, `Switcher.js`). Website-only evidence; no ebook/PDF or full downloaded
implementation reproduced.
