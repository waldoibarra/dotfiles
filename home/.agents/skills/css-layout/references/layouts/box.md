# Box

## Contents

- Problem and mechanism
- Primary HTML/CSS
- Variants and visual boundaries
- Downloaded component
- Checks and sources

## Problem and mechanism

A Box owns inward spacing and visible enclosure, not its position among other boxes. Keep margin
with the parent layout; let content or the surrounding flex/grid algorithm determine dimensions.
Inherit typography and other shared styling rather than making each Box a miniature design system.

Use a Box for notes, cards, grouped controls, or a dialog's inner wrapper. Combine it with
`references/layouts/stack.md` for outside spacing and `references/layouts/grid.md` for collections.
The chapter's branding diagram keeps proportions identical while changing fonts and colors: layout
and visual identity are independent decisions.

## Primary HTML/CSS

An authored example with explicit colors and no token dependency:

```html
<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }
  .notice-box {
    padding: 1.25rem; /* Equal inset on every edge. */
    border: 0.125rem solid;
    color: #202020;
    background: #f4f4f4;
    outline: 0.125rem solid transparent;
    outline-offset: -0.125rem;
  }
  .notice-box > * {
    margin-block: 0;
  }
  .notice-box > * + * {
    margin-block-start: 0.75rem;
  }
  .notice-box * {
    color: inherit;
  }
</style>
<aside class="notice-box" aria-labelledby="collection-title">
  <h2 id="collection-title">Collection reminder</h2>
  <p>Bring your confirmation email when collecting your order.</p>
</aside>
```

The sibling-spacing rules compose a small Stack with the Box; they are not a reason to give every
Box external margins. Border-box sizing includes border and padding in specified dimensions.
Background: `references/rudiments/boxes.md`.

## Variants and visual boundaries

- **Padding:** all-sided padding separates content from the perimeter. Using one-sided padding to
  separate peer boxes leaves their borders touching; the chapter contrasts this with margin, which
  separates the borders themselves. Use a more specific pattern when asymmetry is actually required.
- **Separators:** apply borders between siblings through their parent (`> * + *`), rather than
  giving every child a complete border. The diagram shows internal dividers that neither double up
  nor collide with the parent's perimeter.
- **Borderless surface:** retain the transparent inset outline when removing the border. Backgrounds
  may disappear in forced-colors modes; the outline provides a boundary when the browser substitutes
  a visible color. Outline does not consume layout space; a negative offset draws it inward. Verify
  in the target forced-colors environment.
- **Color inversion:** explicitly swap paired foreground/background tokens for predictable colors.
  `filter: invert(100%)` is the chapter's grayscale shortcut, but it affects descendants and
  reverses hues too; it is not a general theme system.
- **Header/body:** an unpadded outer Box can enclose two padded, borderless sibling Boxes. Invert or
  recolor the header. This preserves one outer boundary without doubling interior padding or
  borders.

Variant CSS, replacing only the chosen surface treatment:

```css
.notice-box.dark {
  color: #f4f4f4;
  background: #202020;
}
.notice-box.borderless {
  border: 0;
} /* Keep the transparent outline. */
```

Forcing every descendant to inherit color can erase intentional status colors and link
differentiation. Preserve meaningful cues through underlines, icons, or targeted exceptions.

## Downloaded component

Include `Box.css` and import `Box.js` as a module. Defaults depend on `--s1` and `--border-thin`;
inversion additionally references `--color-light`. Setup and the shared generation model are
documented in `references/component-integration.md`.

Component usage:

```html
<box-l padding="1rem" borderWidth="0.125rem">
  <p>Keep this confirmation for your records.</p>
</box-l>
```

| API           | Downloaded default   | Meaning                                                    |
| ------------- | -------------------- | ---------------------------------------------------------- |
| `padding`     | `var(--s1)`          | CSS padding value; use a uniform value for the Box pattern |
| `borderWidth` | `var(--border-thin)` | CSS border width; generated border style is solid          |
| `invert`      | absent / false       | Presence enables a whole-element inversion filter          |

`Box` extends `HTMLElement` and registers `box-l`. Its string property setters write attributes; the
boolean setter adds/removes `invert`. Connection and observed-attribute changes invoke `render`; the
observed list is `borderWidth`, `padding`, `invert`. Render derives a configuration key, assigns
`data-i`, and adds a head stylesheet only if that key is new. It generates padding and a solid
border plus conditional inversion declarations, without shadow DOM or child rewriting.

Selected downloaded expression:

```js
// Presence, not the literal string "false", controls inversion.
this.hasAttribute("invert");
```

Important implementation differences from the chapter's authored CSS:

- `Box.css` provides display, padding, border **width**, and transparent outline, but not a border
  style or full two-tone palette. Without JS, border width alone does not create a visible border;
  choose the desired fallback explicitly.
- Generated CSS always ends with `background-color: inherit` on the host. It overrides the earlier
  conditional `background-color: var(--color-light)` in the same generated stylesheet; the filter
  remains. Do not assume the download implements the chapter's explicit color-swap variant. This is
  source inspection, not a contrast guarantee.
- Browser verification found that changing `borderWidth` through `setAttribute` left `data-i`
  unchanged: the mixed-case observed name does not match HTML's lowercased attribute notification.
  Initial connection still reads the attribute. The shared integration reference documents the
  limits of live property updates.

## Checks and sources

Check nested header/body edges, spacing inside an outer Stack, link visibility, contrast, forced
colors, and JS-disabled boundaries. Content growth should enlarge the Box rather than be clipped to
a decorative fixed height.

Website chapter, diagrams, generator, and API: [Box](https://every-layout.dev/layouts/box/).

Inspected download (`README.txt`, `Box.css`, `Box.js`):
[Box.zip](https://every-layout.dev/downloads/Box.zip).
