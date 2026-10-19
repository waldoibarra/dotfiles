# Units

Choose units for the relationship they preserve:

- Root-relative dimensions for a shared scale.
- Local font-relative dimensions for inline content.
- Character-relative measures for text.
- Viewport-relative values only when the viewport is the relevant input.

## Contents

- Pixels and accessibility
- Root-relative sizing and proportionality
- Viewport-based scaling
- Local sizing with em
- Character metrics with ch and ex
- Pitfalls and related layouts
- Sources

## Pixels and accessibility

A CSS pixel is not necessarily a single hardware pixel.

- The subpixel illustration shows different arrangements of color components.
- The grid illustration shows multiple device pixels representing one CSS pixel.
- Display density and zoom change the mapping.
- `inline-size: 400px` still specifies 400 CSS pixels under page zoom.
  - The physical rendering and available CSS viewport change instead.
- Do not read the chapter's zoom discussion as a literal change to the declared CSS length.

Pixel units are valid; matching one screenshot's device pixels is not a resilient layout objective.

- Pixel-fixed font sizes disregard changes to the browser's preferred default font size.
- Full-page zoom is a separate feature, not a replacement for honoring that preference.

Use a root font size that preserves the user's baseline, then scale text and layout from it.

- `rem`, `em`, `ch`, and `ex` help only while their reference font remains responsive.
- Setting the root to a fixed pixel font size defeats the user-default benefit of `rem`.

## Root-relative sizing and proportionality

`1rem` is the computed root font size.

- Leave the root's font size alone unless there is a reason to change it.
- Paragraphs inherit their parent's font size; they do not intrinsically have a `1rem` declaration.
- In ordinary body flow that inheritance supplies the base size without redundant rules.
- A paragraph nested inside deliberately smaller or larger text inherits that local choice.

```html
<style>
  /* No fixed root font-size: preserve the browser/user baseline. */
  body {
    font-family: system-ui, sans-serif;
    line-height: 1.5;
  }
  .article {
    max-inline-size: 62ch;
    margin-inline: auto;
    padding: 1.25rem;
  }
  .article h1 {
    font-size: 2rem;
    line-height: 1.15;
  }
  .article h2 {
    font-size: 1.5rem;
    line-height: 1.2;
  }
  .article > * + * {
    margin-block-start: 1.25rem;
  }
</style>
<article class="article">
  <h1>Plan a walking route</h1>
  <p>Choose a distance that leaves room for pauses and changes of plan.</p>
  <h2>Keep the route adaptable</h2>
  <p>Larger text also enlarges the spacing and the maximum reading measure.</p>
</article>
```

The `rem` dimensions maintain their ratios when the root font size changes.

- Spacing and padding can use text-relative units too; font sizing is not their only purpose.
- A single intentional root-scale change propagates through the interface.
  - Pixel values would need separate retuning for every heading and gap.

```css
/* Proportionality demonstration, not a recommended default breakpoint. */
@media (min-width: 70rem) {
  :root {
    font-size: 112.5%;
  }
}
```

Here every rem-based value grows by the same root-size factor.

- The source demonstrates this maintenance advantage with a discrete breakpoint.
- Its next section then questions that abrupt transition.

Rem values need not convert into whole numbers of pixels.

- Fractional layout values are legitimate; rendering handles the eventual device-pixel mapping.
- Prefer a meaningful ratio or simple fraction, or let `calc()` derive a scale.
- Do not preserve a supposed 16px baseline through laborious conversion.
- See `references/rudiments/modular-scale.md`.

## Viewport-based scaling

`1vw` is one percent of viewport width and `1vh` one percent of viewport height.

- Neither is one percent of an element's parent.
- A wide viewport can contain a narrow panel.
  - Viewport conditions do not establish the space available to every component.

The chapter's 959px/960px diagram contrasts almost identical widths with sharply different text
sizes.

- It illustrates the discontinuity introduced by an arbitrary breakpoint.
- A continuous formula avoids that jump:

```css
/* Optional fluid root scale; alternative to the breakpoint example. */
:root {
  font-size: calc(1rem + 0.5vw);
}
```

This source-described formula combines a user-relative floor with a viewport contribution.

- In the root's own `font-size`, `rem` resolves against the initial font size.
  - It does not resolve recursively against the result.
- The viewport term goes to zero as viewport width goes to zero.
  - It cannot reduce the result below the baseline.

Do not conclude that this formula alone proves accessible scaling.

- Pure `vw` text can counteract zoom.
- Mixed formulas still need checks with zoom and changed default text size.
- A fluid root does not make a layout container-aware.
  - Use intrinsic layout algorithms for local wrapping.
- Media/container queries remain appropriate for genuinely conditional requirements.
  - Do not use them for device-category guesses.

## Local sizing with em

`em` tracks the local font size.

- For `font-size`, `em` refers to the inherited font size.
- For most other properties, it refers to the element's own computed font size.
- Use it when a child or decoration should track its immediate typography, not the document-wide
  scale.

```css
.title {
  font-size: 2rem;
}
.title strong {
  font-size: 1.125em;
} /* 2 × 1.125 = 2.25rem. */

.text-icon {
  inline-size: 0.85em;
  block-size: 0.85em;
  margin-inline-end: 0.35em;
  fill: currentColor;
}
```

Changing `.title` now also changes its emphasis.

- A rem-sized emphasis would remain tied to the root and need a second edit.
- Nested em font-size multipliers compound.
  - Use that deliberately; do not apply the same multiplier indiscriminately at every level.

The chapter's download-icon diagram demonstrates optical matching.

- A nominal `1em` box may look too large beside a particular font's visible letters.
- Adjust the em coefficient to that font's metrics.
  - Its illustrated `0.75em` is not a universal icon size.
- Rem for shared block-scale values and em for local inline values is a useful default.
  - It does not restrict which properties accept either unit.

**Source correction:** the chapter's `1.125 × 2.5rem` example has the wrong result.

- It evaluates to `2.8125rem`, not the printed `2.53125rem`.
- The dependency on the parent remains the intended lesson.

## Character metrics with ch and ex

The metric diagram defines two font-dependent dimensions:

- `1ch` is the advance measure of the font's zero glyph.
- `1ex` is its x-height.
- They are not an average width and height of every possible character.

```css
.prose {
  max-inline-size: 62ch;
}
.prose h2,
.prose h3 {
  max-inline-size: 28ch;
}
.prose h2 {
  font-size: 1.75rem;
}
.prose h3 {
  font-size: 1.375rem;
}
.marker {
  block-size: 1ex;
  inline-size: 1ex;
} /* Match the local x-height. */
```

Character-relative units make measure follow typography.

- The two headings share a character-relative measure.
  - Their physical maximum widths still differ with font size.
- The prose width likewise follows typography rather than a frozen pixel width.
- `62ch` does not guarantee exactly 62 actual characters on a line in a proportional font.
  - Inspect real content, language, and typeface.
- The source favors ch for measure because it expresses the reading relationship directly.
  - Other units are not invalid CSS.

## Pitfalls and related layouts

- Do not set a pixel root, then claim rem units automatically honor the user's chosen default font size.
- Do not equate default-font-size changes, text zoom, and full-page zoom.
  - Exercise the relevant modes separately.
- Avoid fixing heights in px while allowing text to grow in rem.
  - Reflow needs room on the block axis as well as a scalable font.
- Do not use `ch` as a precise character counter.
- Do not assume every font's icon alignment matches the source font.
- Check changed root/default font size, page zoom, long content, and narrow parent containers.
  - Text and controls should remain readable and reachable without clipping.
- Use these related references:
  - `references/layouts/center.md` and `references/rudiments/axioms.md` for readable measure.
  - `references/layouts/icon.md` for inline glyph alignment.
  - `references/layouts/stack.md` and `references/layouts/box.md` for text-relative spacing and
    padding.

## Sources

- Original summary and authored examples derived from
  [Every Layout: Units](https://every-layout.dev/rudiments/units/).
  - Includes its subpixel, CSS/device-pixel, breakpoint-jump, icon-metric, and ch/ex diagrams.
- The optional fluid-root formula is the chapter's mechanism.
- This rudiment has no component download.
