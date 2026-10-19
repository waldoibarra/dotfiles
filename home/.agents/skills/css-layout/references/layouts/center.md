# Center

## Contents

- Problem and mechanism
- Primary HTML/CSS
- Variants and composition
- Downloaded component
- Checks and sources

## Problem and mechanism

- Center a readable column without centering all its text.
- A maximum inline size limits measure; two auto inline margins share spare space.
- Unlike `margin: 0 auto`, `margin-inline: auto` leaves block margins supplied by a Stack intact.
- Use semantic HTML with CSS, not the obsolete `center` element.

Use this for article columns, main content alongside a Sidebar, or a centered control group.

Text alignment is a separate choice and usually unsuitable for long paragraphs.

Related background:

- `references/rudiments/axioms.md` for measure.
- `references/layouts/sidebar.md` for side-by-side composition.

## Primary HTML/CSS

An authored example, independent of downloaded components or tokens:

```html
<style>
  .reading-center {
    box-sizing: content-box; /* Preserve 58ch for content, excluding gutters. */
    max-inline-size: 58ch;
    margin-inline: auto;
    padding-inline: 1rem; /* Remains when there is no spare space for margins. */
  }
  .reading-center > * {
    margin-block: 0;
  }
  .reading-center > * + * {
    margin-block-start: 1rem;
  }
</style>
<main class="reading-center">
  <h1>A guide to collecting your order</h1>
  <p>Wait for your collection message before travelling to the shop.</p>
  <p>Bring the confirmation and a form of identification with you.</p>
</main>
```

- The sibling rules are a composed Stack, not part of centering.
- A block with automatic width contracts to its containing space.
- Avoid adding a fixed width that defeats this behavior.
- The chapter's diagrams distinguish three relationships:
  - One auto margin pushes a box to the opposite edge; two share the remaining space.
  - At narrow widths the auto space disappears but padding remains.
  - Content-box leaves the intended measure to text, whereas border-box counts gutters inside it.
- `ch` approximates text measure through the zero glyph, not an exact character count.

## Variants and composition

- **No gutters:** omit padding when an enclosing Box already supplies sufficient edge spacing.
  - Two inset-owning wrappers can create unnecessary narrowing.
- **Intrinsic children:** a column flex context with `align-items: center` centers children.
  - Children keep content-based widths rather than all stretching.
  - A short button becomes centered while substantial text can still occupy the column.
  - Constrain unusually wide children separately.
- **Text alignment:** use `text-align: center` only when desired for the text itself.
  - A short heading is one such case.
  - It is not needed to center the column.
- **Sidebar documentation layout:** put a generic wrapper in the Sidebar's growing content position.
  - Put a Center inside that wrapper.
  - The wrapper participates in the Sidebar sizing algorithm.
  - The Center retains its own width cap and margins.
- **Two-axis centering:** place an intrinsic Center in a Cover's centered slot.
  - Center owns the inline axis; Cover owns the block axis.
  - Related patterns: `references/layouts/cover.md` and `references/layouts/box.md`.

Variant CSS, added to the primary example only when intrinsic centering is wanted:

```css
.reading-center.intrinsic {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.reading-center.intrinsic > * {
  max-inline-size: 100%;
}
```

## Downloaded component

- Include `Center.css` and import `Center.js` as a module.
- Define `--measure` for the default maximum.
- `references/component-integration.md` documents setup and shared generation details.

Component usage:

```html
<center-l max="58ch" gutters="1rem" intrinsic>
  <button type="button">Track your order</button>
</center-l>
```

| API         | Downloaded default        | Meaning                                             |
| ----------- | ------------------------- | --------------------------------------------------- |
| `max`       | `var(--measure)`          | Maximum width value                                 |
| `andText`   | absent / false            | Presence requests centered text                     |
| `gutters`   | `null` when missing/empty | CSS padding value on both inline edges              |
| `intrinsic` | absent / false            | Presence adds column flex layout and centered items |

**Documented versus downloaded:**

- The website API labels `gutters` boolean with default `0`.
- The implementation reads a string and inserts it into padding declarations.
- Use `gutters="1rem"`, not a bare boolean attribute.

Implementation:

- `Center` extends `HTMLElement` and registers `center-l`.
- String getters/setters read/write attributes; boolean setters add/remove them.
- The observed list is `max`, `andText`, `gutters`, `intrinsic`.
- Connection and attribute callbacks invoke `render`.
- Render assigns a configuration-derived `data-i` and deduplicates a head stylesheet.
- It emits the maximum, optional gutters, optional text alignment, and optional flex rules.
- Companion CSS supplies block display, content-box sizing, inline auto margins, and logical
  `max-inline-size`.

Selected downloaded expression:

```js
// Empty gutters do not enable padding; a nonempty CSS value does.
this.getAttribute("gutters") || null;
```

- The JS-generated maximum uses physical `max-width`, whereas companion CSS uses `max-inline-size`.
  - Those coincide in horizontal writing but not vertical writing.
  - Verify or adapt that boundary rather than assuming full logical-axis awareness.
- Browser verification found a live `andText` attribute mutation did not change `data-i`.
  - The observed mixed-case name does not match HTML's lowercased notification.
  - Lowercase configuration attributes do not have this particular mismatch.

## Checks and sources

- Check at narrow containing widths and high zoom, not just a wide viewport.
  - Centered content must not move offscreen.
- Exercise long links, large controls, gutter presence, nesting in a Stack, and the intrinsic
  variant.
- Verify that the inline-only margin rule preserves separation from the preceding sibling.
- Keep readable paragraph alignment even when the column is centered.

Website chapter, diagrams, generator, and API: [Center](https://every-layout.dev/layouts/center/).

Inspected download (`README.txt`, `Center.css`, `Center.js`):
[Center.zip](https://every-layout.dev/downloads/Center.zip).
