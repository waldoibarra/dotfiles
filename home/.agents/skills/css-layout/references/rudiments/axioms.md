# Axioms

Express design rules as constraints the browser can preserve across content, containers, and user
settings. A readable maximum text measure is an example: share one token among global defaults,
layout configuration, and explicit exceptions rather than tuning every screen independently.

## Contents

- Core principle: constraints rather than pictures
- Measure and the right declaration
- Global defaults and exception-based styling
- Shared values and utilities
- Measure in composite layouts
- Pitfalls and related layouts
- Sources

## Core principle: constraints rather than pictures

An axiom is a short, foundational design rule from which many outcomes follow. “Text should not
exceed the chosen readable measure” is more reusable than “this paragraph should be this many pixels
wide.” Font choice or heading color can often be global declarations; layout axioms must
additionally tolerate changes in size, configuration, orientation, and user preferences.

The chapter contrasts fixed print columns with web text wrapping. Print allocates a known page width
among columns, margins, and gutters. Web content must reflow as viewport, container, font size,
zoom, and orientation change. Spaces normally provide wrap opportunities; a fixed text width can
overflow a narrow viewport and make zoomed reading require horizontal scrolling.

Designing by axiom means specifying relationships, not predicting every resulting image. The browser
generates arrangements from those rules. Unexpected visual differences are not automatically errors
if the intended constraints still hold.

## Measure and the right declaration

Measure is the length of a line of text in characters. The chapter cites roughly 45–75 characters as
a useful reading range and chooses `60ch` as its example ceiling, not a universal obligation.

Use `max-inline-size`, not a fixed `width`: it caps the inline dimension in the current writing mode
while allowing shorter lines in smaller containers. A minimum of 45 characters is not required in a
narrow viewport.

A pixel cap has no stable relationship to character size. The chapter’s equal-width-column diagram
shows that smaller and larger type fit different character counts into the same pixel width. A `ch`
cap instead tracks the font’s zero-glyph advance. It approximates measure; `60ch` does **not**
guarantee exactly 60 arbitrary characters, especially across proportional fonts and languages.

The different-font-size diagram shows larger type occupying a wider maximum box with the same `ch`
value. That is the rule functioning correctly, not an alignment bug. If the design needs equal outer
widths too, give that separate responsibility to the containing layout.

## Global defaults and exception-based styling

There are three useful scopes, with different costs:

- **Opt-in utility:** easy to add locally, but every author must remember it; arbitrary rich text
  can be missed.
- **Text-element defaults:** target paragraphs, headings, list items, and captions without changing
  their markup. Keep the list consistent with actual content.
- **Universal default with exceptions:** start with the cap everywhere, then exempt structural
  wrappers that may need to contain several full-measure columns. This is the chapter’s
  exception-based approach.

An exception is not a failed axiom. A multicolumn wrapper is not itself one line of prose. Broad
low-specificity defaults and narrower overrides use the cascade as intended: the same
inverted-triangle relationship between reach and specificity described in
`references/rudiments/global-and-local-styling.md`.

Authored, self-contained example of the exception-based approach:

```html
<style>
  :root {
    --measure: 60ch;
    font-family: system-ui, sans-serif;
    line-height: 1.5;
  }
  * {
    box-sizing: border-box;
    max-inline-size: var(--measure);
  }
  /* Structural regions can contain more than one column of text. */
  html,
  body,
  main,
  header,
  footer,
  nav,
  div,
  .reading-region {
    max-inline-size: none;
  }
  body {
    margin: 0;
    padding: 1rem;
  }
  .reading-region {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
  }
  .reading-region > article {
    flex: 1 1 22rem;
    min-inline-size: 0;
  }
  h2 {
    font-size: 1.5rem;
  }
</style>
<main class="reading-region">
  <article>
    <h2>A maximum, not a fixed width</h2>
    <p>
      This column may narrow with the container. On a wide screen its lines remain limited by the
      shared measure rather than expanding indefinitely.
    </p>
  </article>
  <article>
    <h2>Another reading column</h2>
    <p>
      The structural parent may span several readable columns without forcing each paragraph to span
      the entire page.
    </p>
  </article>
</main>
```

Adapt the exception list to the real document. The chapter’s short list is not a complete reset for
every site: custom layout elements, media, tables, sections, and other wrappers need intentional
treatment. Normal non-replaced inline content such as `em` does not establish an independently
capped line box; its containing text block supplies the measure.

## Shared values and utilities

Put the shared `--measure` token on `:root` so defaults, props, and utilities agree. Custom
properties can also be local, but a local override is an intentional scope change, not a separate
global constant.

Optional utility variants, using the token from the primary example:

```css
.max-inline-size\:measure {
  max-inline-size: var(--measure);
}
.max-inline-size\:measure\/2 {
  max-inline-size: calc(var(--measure) / 2);
}
```

Use `class="max-inline-size:measure/2"` in HTML: CSS selector punctuation is escaped, the HTML class
value is not. A fractional utility supports a narrower caption or note while preserving the common
basis. Add these only when needed; do not turn the default text rule into repetitive markup.

## Measure in composite layouts

A layout can use the same token for a different but related decision. The Switcher’s documented
default `threshold` is `var(--measure)`: available container width determines whether children sit
beside one another or form a vertical stack. Its getter reads the attribute with that default; its
setter reflects the value to the attribute. A value such as `threshold="20rem"` is an explicit
alternate threshold, not a new prose measure.

The mechanism uses wrapping flexbox and a large signed preferred size, summarized by this CSS
expression:

```css
/* Mechanism excerpt, not a complete Switcher stylesheet. */
flex-basis: calc((var(--measure) - 100%) * 999);
```

Above the threshold the expression becomes negative, tending toward a zero basis so siblings can
share a line. Below it the large positive basis makes each item take its own line. The shared token
connects the layout decision to readable text without viewport-specific breakpoints.
`references/layouts/switcher.md` covers the complete algorithm, child-count behavior, spacing, and
component contract.

The chapter says an illegitimate threshold declaration is dropped so the companion default
stylesheet takes over. That is conditional: a declaration rejected during parsing can leave an
earlier valid declaration in force, but one that becomes invalid only after custom-property
substitution does not generally revive the earlier declaration. Do not rely on arbitrary malformed
values as a fallback mechanism. Supply valid CSS values and define their tokens. Companion CSS
loading is covered in `references/component-integration.md`.

## Pitfalls and related layouts

- A maximum length is a ceiling, not a promise of fixed line length or an obligation to fill all
  available width.
- Check the rule with changed font size, zoom, narrow containers, and differing writing modes, not
  only one screenshot. A fixed height can still clip otherwise well-measured text.
- A universal cap can accidentally restrict layout containers or controls. Exempt the appropriate
  structure while retaining caps on its text, rather than disabling the rule globally.
- Long unbreakable content can overflow even inside a capped box; measure and wrapping policy solve
  different problems.
- `references/layouts/center.md` covers centering a capped region, `references/layouts/sidebar.md`
  covers adjacent regions, and `references/layouts/switcher.md` covers threshold-based composition.
- `references/rudiments/units.md` covers font-relative units;
  `references/rudiments/modular-scale.md` covers another rule shared through tokens.

## Sources

Original summary and authored examples based on the complete rendered website chapter, including its
measure diagrams and component discussion. The invalid-value fallback claim is qualified rather than
treated as universal runtime behavior.

- [Every Layout: Axioms](https://every-layout.dev/rudiments/axioms/)
