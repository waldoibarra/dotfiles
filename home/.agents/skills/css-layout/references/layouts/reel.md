# Reel

## Contents

- Problem and mechanism
- Primary HTML/CSS example
- Height, spacing, and affordance variants
- Downloaded component
- Pitfalls and checks
- Sources

## Problem and mechanism

Offer a horizontally browsable collection without turning the entire page into a two-axis scrolling
surface. A nonwrapping flex row with nonshrinking children creates the strip; local
`overflow-x: auto` makes the browser provide scrolling. This is an alternative to a scripted
carousel, not an auto-advancing slideshow.

The chapter's diagrams contrast page-wide horizontal overflow with a local horizontal strip inside a
vertically scrolling page. Its sequencer analogy explains the important relationship: content
determines the strip's length; the viewport reveals only part of it. Avoid text that itself needs
back-and-forth horizontal scrolling, and do not assume every nested horizontal scroller
automatically satisfies WCAG Reflow.

Use for product/category browsing, image galleries, and short navigation links. Prefer
`references/layouts/cluster.md` when wrapping is acceptable, or `references/layouts/grid.md` when
every item should participate in the page's normal vertical reading flow.

## Primary HTML/CSS example

This authored example uses native focus and scrolling, with no script required.

```html
<style>
  .catalog-strip {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    scrollbar-color: #333 #eee;
    padding-block: 0.5rem;
  }
  .catalog-strip > a {
    box-sizing: border-box;
    flex: 0 0 min(16rem, 85%); /* Leave a glimpse of the next item. */
    padding: 1rem;
    border: 1px solid;
    overflow-wrap: anywhere;
  }
  .catalog-strip:focus-visible {
    outline: 2px solid;
  }
</style>
<nav aria-label="Browse guides">
  <div class="catalog-strip" tabindex="0" role="group" aria-label="Scrollable guides">
    <a href="#basics">Start with layout basics</a>
    <a href="#composition">Combine small layout primitives</a>
    <a href="#accessibility">Check reflow and keyboard access</a>
    <a href="#examples">Explore worked examples</a>
  </div>
</nav>
```

## Height, spacing, and affordance variants

**Height.** Content cards normally determine the strip's height; flex stretching aligns them to the
tallest card. A nested Stack can push card attribution to the bottom
(`references/layouts/stack.md`). For direct-child images, a deliberately bounded gallery height plus
`block-size: 100%; inline-size: auto; flex-basis: auto` preserves each image's aspect ratio while
equalizing heights. Scope these rules with `>` so images inside cards remain unaffected. Avoid
constraining text-card height and then hiding its overflow.

**Between items.** The chapter retains logical sibling margins for its nonwrapping strip; modern
flex `gap` is an authored alternative, as above. Do not combine both unintentionally. For an inset
border around the scroller, the chapter documents an end-padding problem: the last item can meet the
scroll edge despite parent padding. Its workaround uses margins on children, zero inline-end margin,
and a final nonshrinking pseudo-item:

```css
/* Spacing variant: use instead of the primary example's gap. */
.inset-strip {
  display: flex;
  overflow-x: auto;
  gap: 0;
  border: 1px solid;
}
.inset-strip > * {
  margin: 1rem;
  margin-inline-end: 0;
}
.inset-strip::after {
  content: "";
  flex: 0 0 1rem;
}
```

That pseudo-item represents real trailing space in the flex strip. Unlike the site's global border
reset, the example explicitly supplies border style and color inheritance.

**Scrollbar.** A visible bar both permits dragging and advertises more content. `scrollbar-color`
takes thumb then track; the chapter also styles WebKit scrollbar pseudo-elements. Its
dark/light/dark gradient makes the thumb appear inset because those pseudo-elements do not accept
all ordinary box styling. OS preferences can still affect visibility; test the target platform.

**Overflow-only spacing.** Compare `scrollWidth > clientWidth`, toggle an `overflowing` class, and
add bottom padding only when needed. The class is concatenated with the component selector, so
unrelated `overflowing` elements are untouched. A ResizeObserver detects host size changes; a
child-list MutationObserver handles direct item additions/removals. Without these enhancements,
native scrolling still works, but conditional spacing may not appear.

**Hidden bar.** Short slidable navigation may omit the bar, but must communicate overflow another
way. The partly visible next-item diagram explains why exact fractional item widths can misleadingly
look complete. An instruction revealed by `.overflowing` indicates that more content exists, not
whether the user has reached an endpoint. Endpoint-aware instructions need scroll-position logic.
The chapter also describes scroll shadows: stationary shadow backgrounds with locally scrolling
cover backgrounds hide the shadow at an endpoint.

## Downloaded component

Include `Reel.css`, import `Reel.js` as a module, and define `--s0`, `--color-light`, and
`--color-dark` or replace their uses. For a meaningful CSS-only fallback, also define
`--item-width`: the companion stylesheet references it without a fallback. Shared integration:
`references/component-integration.md`.

**Component usage** (article widths are independent of viewport breakpoints):

```html
<reel-l itemWidth="18rem" space="1rem" role="list">
  <article role="listitem">
    <h2>Field notes</h2>
    <p>A short guide.</p>
  </article>
  <article role="listitem">
    <h2>Reference</h2>
    <p>Detailed examples.</p>
  </article>
</reel-l>
```

| Property / authored attribute | Type    | Default     | Effect                                                   |
| ----------------------------- | ------- | ----------- | -------------------------------------------------------- |
| `itemWidth`                   | string  | `auto`      | Child flex basis; no growth or shrink                    |
| `space`                       | string  | `var(--s0)` | Logical inter-item margin and overflow scrollbar padding |
| `height`                      | string  | `auto`      | Reel height; direct images fill it                       |
| `noBar`                       | boolean | false       | Presence hides scrollbar; does not disable scrolling     |

The module exports `Reel` and registers `reel-l`. Getters read attributes; string setters write
them, and `noBar`'s setter adds/removes its presence attribute. Rendering constructs a configuration
`data-i` and caches one document-head style block per configuration. Generated rules set physical
height, child flex basis, direct image dimensions, logical sibling margin, conditional bottom
padding, and optional hidden-scrollbar rules.

`connectedCallback` renders and creates feature-detected ResizeObserver and MutationObserver
instances. The selected **implementation excerpt** captures the overflow and mutation scope:

```js
elem.classList.toggle("overflowing", this.scrollWidth > this.clientWidth);
// MutationObserver observes this element with { childList: true }.
```

The observed-attribute list is `['itemWidth', 'height', 'space', 'noBar']`;
`attributeChangedCallback` renders. HTML lowercases attribute names, so the camelCase entries are an
upstream reactivity hazard. **Observed in the parent browser smoke:** changing `itemWidth` through
`setAttribute` left `data-i` unchanged. Do not promise reactive width changes from this download
without adapting its observed names. `noBar` has the same source-inspected naming risk; initial
connection reads attribute values.

The implementation does not retain/disconnect observer handles or provide `disconnectedCallback`;
reconnection can add observers. Mutation observation excludes descendant text/attribute changes.
Host ResizeObserver alone does not detect every change to overflowing child width. There is no
built-in endpoint detection, focus management, or navigation-button script.

## Pitfalls and checks

- Exercise keyboard access to every item, focus-ring visibility, touch/trackpad scrolling, narrow
  containers, RTL, large text, and long titles. The download's `overflow-y: hidden` can clip content
  or focus outlines.
- If children are not focusable, consider a labeled focusable scroll region. Focusable links often
  bring themselves into view, but verify actual keyboard scrolling rather than assuming it.
- A hidden scrollbar does not remove the need for an affordance. Never describe `noBar` as turning
  scrolling off.
- Check item insertion/removal and late-loading media; observer presence is not evidence that every
  overflow transition is detected.
- Native scrolling is the baseline; optional buttons should increment that same scroll position
  instead of replacing it with an inaccessible parallel interaction.

## Sources

Website chapter, diagrams, generator, API, and examples:
[Reel chapter](https://every-layout.dev/layouts/reel/).

Inspected download (`Reel.js`, `Reel.css`, `README.txt`):
[Reel component archive](https://every-layout.dev/downloads/Reel.zip).
