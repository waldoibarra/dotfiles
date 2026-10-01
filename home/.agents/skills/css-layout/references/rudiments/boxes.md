# Boxes

Let content and available space determine a box's size; prescribe constraints only where they
express a real design requirement. A rounded or clipped element still participates in a rectangular
layout model.

## Contents

- Box model and browser defaults
- Display, axes, and formatting contexts
- Logical spacing
- Content-driven dimensions
- Box sizing and exceptions
- Pitfalls and related layouts
- Sources

## Box model and browser defaults

The chapter's concentric-rectangle diagram separates four layers: content, padding around content,
border around padding, and margin outside the border. Padding belongs to the painted box; margin
separates it from neighbors. Margin is not included in either `content-box` or `border-box` sizing.

An unstyled document already has layout. Browser styles make paragraphs block-level with block-axis
margins and give lists both margins and indentation for markers. Before resetting these, decide
which primitive will replace their spacing; removing list indentation without a replacement can
leave markers outside the intended region.

```css
/* Authored example: replace incidental browser spacing deliberately. */
.article p {
  margin-block: 0 1em;
}
.article ul {
  margin-block: 0 1em;
  padding-inline-start: 1.5em; /* Preserve room for list markers. */
}
```

## Display, axes, and formatting contexts

| Display         | Layout consequence                                                                                                | Decision                                                                                           |
| --------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `block`         | In ordinary flow, takes available inline space and follows the previous block along the block axis.               | Use for paragraphs, regions, and containers whose block size should grow with content.             |
| `inline`        | Runs with text and can fragment across lines; ordinary non-replaced inline elements ignore explicit width/height. | Use for text-level emphasis and links rather than rectangular widgets.                             |
| `inline-block`  | Occupies an atomic place in an inline line, but accepts box dimensions.                                           | Use when an inline item needs a complete sized box; its box and margins can increase the line box. |
| `none`          | Generates no layout box and ordinarily removes the subtree from the accessibility tree.                           | Use for genuinely unavailable content, not visually hiding content that should remain readable.    |
| `flex` / `grid` | Keeps a block-level outer box while changing the layout of direct children.                                       | Choose the inner formatting context separately from how the container sits among siblings.         |

The chapter's writing-mode diagrams distinguish **inline direction** (how text runs) from **block
direction** (how lines or blocks follow one another). With `horizontal-tb`, blocks usually stack
vertically; with `vertical-lr`, blocks progress left to right. Do not equate inline with horizontal
in reusable code.

The inline/inline-block diagram illustrates line-box disruption: block-axis margins on an ordinary
inline do not push surrounding text lines apart, whereas an inline-block's outer size can. Inline
block-axis padding and borders can still paint beyond the line; they are not prohibited, but do not
reserve corresponding line spacing. This distinction is more precise than the chapter's shorthand
about permitting only horizontal padding.

```css
/* An outer block whose direct children form a wrapping row. */
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
```

A flex row follows the inline axis, not an unconditional physical horizontal axis. Nesting
formatting contexts makes composite layouts possible; see `references/rudiments/composition.md`.

## Logical spacing

Attach spacing to the relationship, not the physical edge. In the icon diagrams, `margin-right`
separates icon and label in left-to-right text but ends up outside the pair in right-to-left text.
`margin-inline-end` stays between the icon and the following label in both directions.

```html
<style>
  .label-icon {
    margin-inline-end: 0.4em;
  }
</style>
<p><span class="label-icon" aria-hidden="true">✓</span>Saved</p>
<p dir="rtl"><span class="label-icon" aria-hidden="true">✓</span>تم الحفظ</p>
```

Use `inline-size`/`block-size`, `padding-inline`, and `margin-block` when the requirement concerns
reading or flow direction. Physical properties remain appropriate when the requirement truly
concerns a fixed physical edge.

## Content-driven dimensions

Text wraps, so narrowing a paragraph usually increases its block size. The wide/narrow-box diagram
communicates this tradeoff; doubling height when halving width is illustrative, not a mathematical
guarantee for actual words and line breaks. A fixed height can turn ordinary wrapping, translation,
or zoom into clipped content.

```css
.notice {
  padding: 1rem;
  /* No fixed height: additional lines make the box grow. */
}
.hero {
  min-block-size: 24rem;
} /* A floor, not a ceiling on content. */
.aside {
  flex-basis: 18rem;
} /* Preferred size for a flex item, not a rigid width. */
```

Work in a browser with real content rather than treating a static mockup as a complete sizing
specification. The browser's wrapping and scrolling behavior supplies much of responsiveness before
special rules are added.

## Box sizing and exceptions

With `content-box`, an explicit inline size covers content only; padding and border add to the outer
size. With `border-box`, they are included. For example, `inline-size: 12rem; padding: 1rem`
produces a 14rem border box under `content-box` (without borders), but a 12rem border box under
`border-box`.

```css
/* Useful baseline; pseudo-elements can generate boxes too. */
*,
*::before,
*::after {
  box-sizing: border-box;
}

/* A deliberate exception: the measure describes content, excluding gutters. */
.reading-center {
  box-sizing: content-box;
  max-inline-size: 60ch;
  padding-inline: 1rem;
  margin-inline: auto;
}
```

The chapter's overflow pair contrasts a normal-flow child with `inline-size: 100%` against one with
the default `auto`. Under `content-box`, 100% assigns all of the parent's content width to the
child's content, then adds its padding: it overflows. Auto sizing instead accounts for padding,
border, and margins while filling the available space.

```css
.padded-child {
  box-sizing: content-box;
  padding: 1rem;
  inline-size: auto; /* Usually omit this: it is the default. */
}
```

That auto behavior describes an ordinary block in normal flow; flex/grid sizing and intrinsic
minimums need their own analysis. `box-sizing` matters when dimensions or their constraints are
specified, not as a universal fix for overflowing content.

## Pitfalls and related layouts

- Diagnose explicit sizes, padding, border, margins, and formatting context before adding clipping.
  Hidden content is not a successful layout.
- Do not use `inline-size: 100%` merely to make a normal block fill its parent; it already does so
  with auto sizing.
- Prefer minimums and flexible bases to fixed block sizes when content can change.
- Use `references/layouts/box.md` for padding/border encapsulation, `references/layouts/center.md`
  for content measure and its `content-box` exception, `references/layouts/cover.md` for a
  minimum-height composition, and `references/layouts/sidebar.md` for flexible preferred widths.
- Check narrow containers, enlarged text, right-to-left direction, and the actual writing modes the
  interface supports.

## Sources

Original summary and authored examples derived from
[Every Layout: Boxes](https://every-layout.dev/rudiments/boxes/), including its box-model,
writing-mode, inline-box, icon-spacing, content-reflow, and box-sizing diagrams. This rudiment has
no component download; optional component setup belongs to `references/component-integration.md`.
