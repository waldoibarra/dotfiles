# Cover

Use for a principal element centered in the available block-axis space, with an optional header,
footer, or both. The container grows when its content needs more room.

## Contents

- [Problem and mechanism](#problem-and-mechanism)
- [Primary example](#primary-example)
- [Variants and composition](#variants-and-composition)
- [Downloaded component](#downloaded-component)
- [Pitfalls and checks](#pitfalls-and-checks)
- [Sources](#sources)

## Problem and mechanism

A fixed-height container with `50%` positioning and a half-height transform looks centered until the
child becomes taller than the container; then it breaches both edges. Fixed-height flex centering
also cannot make room for arbitrary content. The chapter's diagrams contrast these failures with a
minimum-height container that expands.

Make the Cover a column flex container with `min-block-size`, not a fixed block size. Give its
principal child automatic block margins. They divide the remaining space above and below that child,
whether either edge belongs to the container or to a header/footer sibling. This centers within
**remaining space**, not necessarily at the container's geometric midpoint when header and footer
heights differ.

When space runs out, automatic margins reach zero. Ordinary margins on the optional siblings
maintain separation; the outermost non-principal margins are removed. The four demonstrated
configurations (principal alone, header plus principal, principal plus footer, all three) therefore
use the same CSS. Border-box sizing keeps padding inside the declared minimum rather than adding it
to the viewport-sized minimum.

## Primary example

Runnable HTML/CSS with a `70vh` minimum to demonstrate that full viewport height is optional.

```html
<style>
  * {
    box-sizing: border-box;
  }
  .welcome-cover {
    display: flex;
    flex-direction: column;
    min-block-size: 70vh;
    padding: 1.5rem;
    border: 1px solid;
  }
  .welcome-cover > * {
    margin-block: 1.5rem;
  }
  .welcome-cover > :first-child:not(.welcome-title) {
    margin-block-start: 0;
  }
  .welcome-cover > :last-child:not(.welcome-title) {
    margin-block-end: 0;
  }
  .welcome-cover > .welcome-title {
    margin-block: auto; /* Absorb only the unused block-axis space. */
    overflow-wrap: anywhere;
  }
</style>
<section class="welcome-cover" aria-labelledby="welcome-heading">
  <header><a href="#workshops">Browse workshops</a></header>
  <h1 class="welcome-title" id="welcome-heading">Make room for a new craft</h1>
  <footer><p id="workshops">New workshops begin each month.</p></footer>
</section>
```

Remove the header and/or footer without changing the styles. Use block-specific margins rather than
a physical `margin` shorthand that would erase inline centering owned by another layout.

## Variants and composition

- **Principal only:** one direct heading receives both auto margins. It stays centered while there
  is spare space, and the container grows for longer content.
- **Principal group:** put the heading, description, and action inside one direct wrapper selected
  as the principal element. Compose a Stack inside it for internal rhythm; Cover controls only its
  own direct children.
- **Full-height introduction:** use `min-block-size: 100vh` as the source does. A content section
  can use another minimum. Test the intended mobile viewport behavior rather than replacing minimum
  size with fixed height.
- **Horizontal centering:** a Center around or inside Cover provides horizontal centering; its
  pattern is documented in `references/layouts/center.md`. Text centering is a separate choice. A
  header can contain a Cluster for a logo and navigation, as documented in
  `references/layouts/cluster.md`.
- **No padding:** set `padding: 0` where another container already owns edge spacing. Retain sibling
  separation.
- **Successive sections:** preserve heading hierarchy; after the page's main heading, use
  appropriate subsection headings and change the principal selector accordingly.

Optional observer enhancement, authored from the website's visibility example. This only exposes
state; it does not hide essential content or supply an animation:

```js
if ("IntersectionObserver" in window) {
  const covers = document.querySelectorAll(".welcome-cover");
  const visibility = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      entry.target.dataset.visible = String(entry.isIntersecting);
    }
  });
  covers.forEach((cover) => visibility.observe(cover));
  // The application calls visibility.disconnect() when this view is disposed.
}
```

The chapter sets a separate observation marker before observing its custom elements; this is an
application enhancement, not behavior built into `Cover.js`. Any motion driven by it still needs its
own reduced-motion and content-visibility decisions.

## Downloaded component

Usage after acquiring the named files; the centered wrapper groups its content into a single flex
item:

```html
<link rel="stylesheet" href="./Cover.css" />
<style>
  :root {
    --s1: 1.25rem;
  }
  * {
    box-sizing: border-box;
  }
</style>
<script type="module">
  import "./Cover.js";
</script>
<cover-l centered=".intro" minHeight="75vh" space="1.25rem">
  <header>River workshop</header>
  <div class="intro">
    <h2>Find your next project</h2>
    <p>Learn with local makers.</p>
  </div>
  <footer>Open Tuesday–Saturday</footer>
</cover-l>
```

Companion CSS supplies the column flex context, `100vh` minimum block size, and token-based padding.
The generated rules supply centering and contextual child margins.
`references/component-integration.md` covers the shared module, token, light-DOM, style-cache, and
attribute-normalization contract.

| Attribute / JS property | Default          | Effect                                                                                          |
| ----------------------- | ---------------- | ----------------------------------------------------------------------------------------------- |
| `centered`              | `h1`             | Simple selector for the principal direct child; a class selector is supported in the component. |
| `space`                 | `var(--s1)`      | Minimum sibling separation and, unless disabled, container padding.                             |
| `minHeight`             | `100vh`          | Generated minimum height.                                                                       |
| `noPad`                 | absent / `false` | Presence removes container padding; property setter adds/removes the attribute.                 |

The website generator asks for an element selector such as `h2` and says it does not support class
selectors there. That restriction is not the component API: the downloaded template interpolates the
selector into direct-child and `:not()` rules. Keep it simple and select exactly one principal
child.

The module registers `cover-l`. String properties read attributes with fallbacks and reflect setter
values; `noPad` reads presence. Connection and attribute changes call render; its observed list is
`centered`, `space`, `minHeight`, `noPad`. Render keys a shared head style by all four values,
updates `data-i`, and emits parent minimum/padding plus the child-margin rules. It neither moves
content nor observes viewport intersection.

Selected downloaded expressions:

```js
// All layout options participate in the generated-style key.
[this.centered, this.space, this.minHeight, this.noPad].join("");
// Padding is disabled by boolean presence, not a string "false" value.
!this.noPad ? this.space : "0";
```

**Material implementation caveats:** generated CSS uses physical `min-height`, while the companion
CSS and chapter use logical `min-block-size`; these agree in horizontal writing but not every
writing mode. The observed list contains camelCase `minHeight` and `noPad`, which HTML normalizes to
lowercase attributes. A Chromium mutation check confirmed that changing `minHeight` leaves the
component's `data-i` unchanged; the equivalent `noPad` problem is source-inspected, not
independently runtime-verified. Initial configuration is read on connection. Adapt and verify the
acquired implementation before depending on these dynamic props.

## Pitfalls and checks

- Test all four optional-header/footer arrangements, an oversized principal group, large text, and a
  short viewport. No content should become inaccessible above the page's scroll origin.
- Unequal header/footer sizes intentionally shift the principal child's center within the remaining
  space. The Imposter pattern in `references/layouts/imposter.md` provides an alternative for exact
  geometric overlay centering, with different overlap tradeoffs.
- More than one matching principal child introduces multiple auto-margin recipients; this pattern
  expects one.
- `noPad="false"` is still present and therefore true. Remove the attribute to disable it.
- Without JavaScript, the downloaded CSS gives a column/minimum-height shell but does not vertically
  center the chosen child. Use the primary CSS for a complete no-JS baseline.
- Shared integration checks and runtime provenance live in `references/verification.md`; no
  universal writing-mode or browser compatibility is implied.

## Sources

Original summary and illustrative examples derived from
[The Cover](https://every-layout.dev/layouts/cover/): overflow and sizing diagrams, four
configurations, auto margins, logical shorthand scope, horizontal composition, observer enhancement,
generator, and API. Download inspected: [Cover.zip](https://every-layout.dev/downloads/Cover.zip)
(`README.txt`, `Cover.css`, `Cover.js`). Website only; no ebook/PDF or complete downloaded
implementation reproduced.
