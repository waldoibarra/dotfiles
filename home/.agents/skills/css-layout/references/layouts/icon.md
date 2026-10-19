# Icon

## Contents

- Problem and mechanism
- Primary HTML/CSS example
- Sizing, spacing, and semantic variants
- Downloaded component
- Pitfalls and checks
- Sources

## Problem and mechanism

Make a small SVG accompany text as though it were another character:

- Share the text's color.
- Scale with its font.
- Align to its baseline.
- Preserve an appropriate gap in either writing direction.

This is an inline pattern, unlike the block-level layout primitives.

- An SVG `viewBox` defines an internal coordinate system, independently of rendered size.
- Width/height presentation attributes provide a reasonable small size even before CSS loads.
- `currentColor` connects SVG paint to surrounding text color.
- Keep stroke geometry inside the viewBox; a stroke centered on its outer boundary is partly clipped.

Use icons as visual supplements to button/link labels, not automatic replacements for words.

- For groups of labeled controls, see `references/layouts/cluster.md`.
- For typography-relative units, see `references/rudiments/units.md`.

## Primary HTML/CSS example

- This authored icon is decorative because the adjacent word supplies the button's name.
- The normal HTML space is intentional.

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

- **Baseline and height.** Inline SVG sits on the baseline.
  - `vertical-align: middle` aligns relative to the parent's baseline plus half its x-height.
  - It does not align to the center of capital letters; the chapter's alignment diagrams contrast
    both.
  - A deliberate negative vertical-align length can lower an oversized icon.
    - It may collide with subsequent lines.
  - Baseline-aligned, capital-height icons avoid that adjustment.
  - `1em` measures the font size, not the visible capital height.
  - `0.75em` is the chapter's approximate fallback; `1cap` follows the actual font's capital metric.
  - For a lowercase label, `1ex` matches x-height.
  - Test the font rather than assuming the fallback is exact.
  - Icons here are square, so physical width/height and logical sizes produce the same square.
  - Relative units automatically follow larger/smaller surrounding text.
- **SVG delivery.** Inline SVG supports `currentColor` without an extra image request.
  - For repeated icons, `<use href="/icons.svg#add">` can reference symbols in a shared file.
  - Preserve the referenced symbol's viewBox and painting conventions.
  - Do not replace SVG with icon fonts; their failure and semantics differ from readable text.
- **Natural space.** A single ordinary word space scales and reverses with text direction.
  - Repeated source spaces collapse.
  - An icon-only control does not need a separate margin-removal rule.
  - `dir="rtl"` changes the visual ordering and keeps the space between the icon and text.
  - Use direction for actual directional content, not to reorder a control indiscriminately.
- **Explicit space variant.** Inline flex removes the whitespace-only flex item.
  - Baseline alignment and logical margin then control spacing:

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

- This variant assumes the SVG precedes its accompanying text in source.
- The diagrams show inline-end becoming the left margin in RTL, unlike physical margin-right.
- Do not retain this wrapper/margin for an icon without text.
  - `:only-child` counts element siblings, not text nodes.
  - So it cannot distinguish those cases reliably.
- Ordinary inline text is the simpler default.
- **Icon-only semantics.** Prefer an explicit accessible name on the actual control.
  - For example, put `aria-label="Add item"` on a button and hide its decorative SVG.
  - Alternatives include visually hidden text or an appropriately exposed SVG title.
  - Avoid duplicate naming channels.
  - The chapter's component also offers a labeled image wrapper, described below.
  - By default, keep a visible label on an unfamiliar icon, even when its accessible name is
    correct.

## Downloaded component

- Include `Icon.css` and import `Icon.js` as a module.
- Unlike the block primitives, an unconfigured `icon-l` retains inline display.
- The companion CSS sizes descendant SVGs to `0.75em`, then `1cap`.
- It does not provide artwork or accessible labels.

**Component usage** with a visible label reuses the primary example's complete SVG, not an
unavailable symbol file:

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

- The module exports `Icon`, registers `icon-l`, and observes `space` and `label`.
- It renders on connection and attribute changes.
- Getters return the attribute or null; setters call `setAttribute`.
  - Setting the JS property to null is not the same as removing an attribute.

The semantic **implementation excerpt** is intentionally small:

```js
if (this.label) {
  this.setAttribute("role", "img");
  this.setAttribute("aria-label", this.label);
}
```

- Outside a control, that labels the wrapper as an image.
- Within a button/link, it can contribute the control's accessible name.
  - Exact announcements depend on browser and assistive technology.
- Keep artwork decorative within a labeled wrapper to avoid duplicate output.
- Verify the resulting control name.

- With `space`, rendering sets a configuration `data-i` and creates a cached head style.
  - That style makes the host inline-flex with baseline alignment.
  - It applies margin to direct-child SVGs.
- Without `space`, no spacing rule is generated.
- This is light DOM; shared loading/style constraints are in `references/component-integration.md`.

## Pitfalls and checks

- **Source-inspected removal caveat:** rendering only adds semantics/styles.
  - Removing `label` does not remove previously generated `role`/`aria-label`.
  - Removing `space` does not clear the previous `data-i`.
  - Do not assume attribute removal restores the unconfigured state.
  - Adapt cleanup or explicitly manage these attributes when such transitions are required.
- Keep presentation width/height on each SVG for CSS failure.
- Ensure SVG artwork fits the viewBox, including stroke edges.
- Check label wrapping, large text, font changes, RTL spacing, icon-only naming, keyboard focus, and
  forced colors.
- The layout does not wire click actions or increase a small button's hit area.
- A label on an image is not a guarantee of an understandable action.
- Name the action, not merely the depicted shape.

## Sources

Website chapter, SVG/alignment/spacing diagrams, generator, API, and examples:
[Icon chapter](https://every-layout.dev/layouts/icon/).

Inspected download (`Icon.js`, `Icon.css`, `README.txt`):
[Icon component archive](https://every-layout.dev/downloads/Icon.zip).
