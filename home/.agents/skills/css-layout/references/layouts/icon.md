# Icon

## Contents

- Problem and mechanism
- Primary HTML/CSS example
- Sizing, spacing, and semantic variants
- Downloaded component
- Pitfalls and checks
- Sources

## Problem and mechanism

Make a small SVG accompany text as though it were another character: share its color, scale with its
font, align to its baseline, and preserve an appropriate gap in either writing direction. This is an
inline pattern, unlike the block-level layout primitives.

An SVG `viewBox` defines an internal coordinate system, independently of rendered size. Width/height
presentation attributes provide a reasonable small size even before CSS loads. `currentColor`
connects SVG paint to surrounding text color. Stroke geometry must leave enough room inside the
viewBox: a stroke centered on its outer boundary would be partly clipped.

Use icons as visual supplements to button/link labels, not automatic replacements for words. For
groups of labeled controls see `references/layouts/cluster.md`; for typography-relative units see
`references/rudiments/units.md`.

## Primary HTML/CSS example

This authored icon is decorative because the adjacent word supplies the button's name. The normal
HTML space is intentional.

```html
<style>
  .label-icon {
    width: 0.75em;
    height: 0.75em;
    width: 1cap; /* Capital-letter height when supported. */
    height: 1cap;
  }
</style>
<button type="button">
  <svg
    class="label-icon"
    width="0.75em"
    height="0.75em"
    viewBox="0 0 16 16"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    aria-hidden="true"
    focusable="false"
  >
    <path d="M3 8h10M8 3v10" />
  </svg>
  Add
</button>
```

## Sizing, spacing, and semantic variants

**Baseline and height.** Inline SVG sits on the baseline. The chapter's alignment diagrams contrast
that with `vertical-align: middle`, which aligns relative to the parent's baseline plus half its
x-height, not the center of its capital letters. A deliberate negative vertical-align length can
lower an oversized icon, but may collide with subsequent lines. Baseline-aligned, capital-height
icons avoid that adjustment.

`1em` measures the font size, not the visible capital height. `0.75em` is the chapter's approximate
fallback; `1cap` follows the actual font's capital metric. For a lowercase label, `1ex` matches
x-height. Test the font rather than assuming the fallback is exact. Since icons here are square,
physical width/height and logical sizes produce the same square. Relative units automatically follow
larger/smaller surrounding text.

**SVG delivery.** Inline SVG supports `currentColor` without an extra image request. For repeated
icons, `<use href="/icons.svg#add">` can reference symbols in a shared file; preserve the referenced
symbol's viewBox and painting conventions. Do not replace SVG with icon fonts, whose failure and
semantics differ from ordinary readable text.

**Natural space.** A single ordinary word space scales and reverses with text direction. Repeated
source spaces collapse; an icon-only control does not need a separate margin-removal rule.
`dir="rtl"` changes the visual ordering and keeps the space between the icon and text. Use direction
for actual directional content, not indiscriminately to reorder a control.

**Explicit space variant.** Inline flex removes the whitespace-only flex item; baseline alignment
and logical margin then control spacing:

```css
/* Optional wrapper variant, not needed by the primary example. */
.with-label-icon {
  display: inline-flex;
  align-items: baseline;
}
.with-label-icon > svg {
  margin-inline-end: 0.4em;
}
```

This assumes the SVG precedes its accompanying text in source. The diagrams show inline-end becoming
the left margin in RTL, unlike physical margin-right. Do not retain this wrapper/margin for an icon
without text: `:only-child` counts element siblings, not text nodes, so it cannot distinguish those
cases reliably. Ordinary inline text is the simpler default.

**Icon-only semantics.** Prefer an explicit accessible name on the actual control, for example
`aria-label="Add item"` on a button while hiding its decorative SVG. Alternatives include visually
hidden text or an appropriately exposed SVG title. Avoid duplicate naming channels. The chapter's
component also offers a labeled image wrapper, described below. An unfamiliar icon should usually
keep a visible label even when its accessible name is correct.

## Downloaded component

Include `Icon.css` and import `Icon.js` as a module. Unlike the block primitives, an unconfigured
`icon-l` retains inline display. The companion CSS sizes descendant SVGs to `0.75em`, then `1cap`;
it does not provide artwork or accessible labels.

**Component usage** with a visible label (reuse the primary example's complete SVG rather than
relying on an unavailable symbol file):

```html
<button type="button">
  <icon-l space="0.4em">
    <svg
      width="0.75em"
      height="0.75em"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      aria-hidden="true"
    >
      <path d="M3 8h10M8 3v10" />
    </svg>
    Add
  </icon-l>
</button>
```

| Property / attribute | Type   | Default | Effect                                                        |
| -------------------- | ------ | ------- | ------------------------------------------------------------- |
| `space`              | string | null    | If supplied, use inline-flex and apply logical SVG end margin |
| `label`              | string | null    | Set wrapper `role="img"` and `aria-label` to this value       |

The module exports `Icon`, registers `icon-l`, observes `space` and `label`, and renders on
connection and attribute changes. Getters return the attribute or null; setters call `setAttribute`
(setting the JS property to null is not the same as removing an attribute).

The semantic **implementation excerpt** is intentionally small:

```js
if (this.label) {
  this.setAttribute("role", "img");
  this.setAttribute("aria-label", this.label);
}
```

Outside a control, that labels the wrapper as an image. Within a button/link, it can contribute the
control's accessible name; exact announcements depend on browser and assistive technology. Keep
artwork decorative within a labeled wrapper to avoid duplicate output, and verify the resulting
control name.

With `space`, rendering sets a configuration `data-i` and creates a cached head style that makes the
host inline-flex with baseline alignment and applies margin to direct-child SVGs. Without `space`,
no spacing rule is generated. This is light DOM; shared loading/style constraints are in
`references/component-integration.md`.

## Pitfalls and checks

- **Source-inspected removal caveat:** rendering only adds semantics/styles. Removing `label` does
  not remove previously generated `role`/`aria-label`; removing `space` does not clear the previous
  `data-i`. Do not assume attribute removal restores the unconfigured state. Adapt cleanup or
  explicitly manage these attributes when such transitions are required.
- Keep presentation width/height on each SVG for CSS failure, and ensure its artwork fits the
  viewBox including stroke edges.
- Check label wrapping, large text, font changes, RTL spacing, icon-only naming, keyboard focus, and
  forced colors. The layout does not wire click actions or increase a small button's hit area.
- A label on an image is not a guarantee of an understandable action. Name the action, not merely
  the depicted shape.

## Sources

Website chapter, SVG/alignment/spacing diagrams, generator, API, and examples:
[Icon chapter](https://every-layout.dev/layouts/icon/).

Inspected download (`Icon.js`, `Icon.css`, `README.txt`):
[Icon component archive](https://every-layout.dev/downloads/Icon.zip).
