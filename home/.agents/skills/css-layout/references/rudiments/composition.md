# Composition

Build meaningful interfaces by combining small layout responsibilities.

- Do not rewrite their geometry under each component's name.
- Layout primitives describe relationships; a form, dialog, or slide supplies semantics and purpose.

## Contents

- Separate component identity from layout
- Read the chapter's compositions
- Compose a working form
- Intrinsic responsiveness
- Pitfalls and related layouts
- Sources

## Separate component identity from layout

Extract the shared layout relationship; keep dialog-specific appearance and behavior with the
dialog.

- A dialog-specific header and a card-specific header can both need the same wrapping row.
- Repeating flex, alignment, and spacing under `.dialog__header` and `.card__header` hides the
  shared behavior.

This is the useful part of composition over inheritance.

- Small independent parts combine without a large shared ancestor or growing component variants.
- It does **not** mean avoiding CSS inheritance for text styles.
- It does **not** mean eliminating semantic component names.

A primitive has a narrow responsibility, not a product identity:

| Responsibility                                   | Primitive | What it does not decide                                  |
| ------------------------------------------------ | --------- | -------------------------------------------------------- |
| Space successive blocks                          | Stack     | Whether those blocks are form fields or article sections |
| Pad and bound a region                           | Box       | Whether the region is an alert, card, or dialog          |
| Limit measure and center                         | Center    | The meaning of the centered content                      |
| Wrap and separate inline-axis peers              | Cluster   | Whether peers are navigation links or action buttons     |
| Separate major and minor regions                 | Sidebar   | Which application feature fills either region            |
| Center a principal region with optional bookends | Cover     | Whether the result is a hero or presentation slide       |

These pieces become meaningful through their content and arrangement, like vocabulary in
sentences.

- They can be parents, children, or siblings.
- Nested instances can serve different scales of the same relationship.

## Read the chapter's compositions

- **Dialog:** the decomposition diagram finds reusable geometry inside a recognizable dialog.
  - Box supplies the boundary and padding.
  - Stack separates close-control, message, and action regions.
  - Cluster arranges controls; Center constrains/centers content.
  - None of those primitives implements modal behavior or focus management.
- **Registration form:** many of the same pieces work unchanged.
  - A larger Stack separates fields.
  - Smaller nested Stacks keep each label close to its input.
  - Box supplies the surrounding padding, Center the overall measure, and Cluster the action row.
  - The smaller label-to-input interval communicates grouping, not a special field-layout engine.
- **Presentation slide:** Cover handles the central message with navigation near the lower edge.
  - Box provides padding; Stack organizes message content.
  - Sidebar apportions navigation regions.
  - Reuse relationships; do not force every interface to use the same four primitives.

## Compose a working form

This authored HTML/CSS example combines Center, Box, nested Stack, and Cluster behavior.

- It uses no JavaScript or custom elements.
- Submission performs a native GET to the current route.
  - Replace that application behavior independently of the layout.

```html
<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }
  body {
    margin: 0;
    padding: 1rem;
    font-family: system-ui, sans-serif;
  }

  .center {
    box-sizing: content-box;
    max-inline-size: 36rem;
    margin-inline: auto;
    padding-inline: 1rem;
  }
  .box {
    padding: 1.25rem;
    border: 0.125rem solid;
  }
  .stack {
    display: flex;
    flex-direction: column;
  }
  .stack > * {
    margin-block: 0;
  }
  .stack > * + * {
    margin-block-start: 1.25rem;
  }
  .stack--compact > * + * {
    margin-block-start: 0.375rem;
  }
  .cluster {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    align-items: center;
  }

  input,
  button {
    font: inherit;
  }
  input {
    min-inline-size: 0;
    inline-size: 100%;
    padding: 0.5em;
  }
  button {
    padding: 0.5em 0.875em;
    white-space: normal;
  }
</style>

<main class="center">
  <form class="box stack" method="get">
    <h1>Find a workshop</h1>
    <p>Choose a topic and location to explore available sessions.</p>
    <div class="stack stack--compact">
      <label for="topic">Topic</label>
      <input id="topic" name="topic" required />
    </div>
    <div class="stack stack--compact">
      <label for="location">Location</label>
      <input id="location" name="location" autocomplete="address-level2" />
    </div>
    <div class="cluster">
      <button type="submit">Search workshops</button>
      <button type="reset">Clear fields</button>
    </div>
  </form>
</main>
```

Each Stack owns spacing only between its direct children.

- The outer Stack separates complete fields.
- Compact Stacks control label/input spacing without changing that outer rhythm.
- The action Cluster owns its internal gaps.
  - The outer Stack owns the interval before the whole action row.
- Center limits the content width but does not impose a fixed width.
- Box adds its own padding and border.

These classes are illustrative local implementations, not names exported by downloadable
components.

- For optional native custom elements and required companion CSS, use
  `references/component-integration.md`.

## Intrinsic responsiveness

The chapter's primitives respond to their own content and allocated space.

- A Cluster wraps when its children no longer fit.
- A Stack grows as text wraps.
- A Center uses a maximum rather than a mandatory width.
- The same composition therefore can work in both a broad page and a narrow parent.
  - No viewport breakpoint needs to declare a separate layout.

Make a layout decision at the level that owns it:

- Identify the relationship: sequential blocks, wrapping peers, a major/minor split, or a
  constrained measure.
- Choose the primitive and express its meaningful constraint, such as a gap, preferred basis, or
  maximum measure.
- Nest another primitive when the children need a different relationship.
- Add a media or container query only for a real conditional requirement.
  - The requirement must be one the intrinsic algorithm does not express.
  - The chapter's no-breakpoint baseline is not a ban on queries throughout an application.

## Pitfalls and related layouts

- A class called Stack does not prevent overflow from a descendant.
  - The cause may be a fixed width or an unbreakable string.
  - Check the content constraints as well as the parent algorithm.
- Avoid broad descendant spacing selectors that make an outer primitive restyle nested ones.
  - Assign one owner to each interval instead of compensating with negative margins.
- Layout primitives do not supply semantics, labels, keyboard behavior, or dialog modality.
  - Preserve native elements and their application responsibilities.
- Do not manufacture a primitive for every small selector.
  - Do not force unusual requirements into an unsuitable pattern.
  - Extract relationships that actually recur; retain specific styling where it is specific.
- Check the same composition in narrow and wide parents, with longer labels and more content.
  - Reuse is demonstrated by behavior in both contexts, not by matching class names.
- Read these for the form/dialog relationships:
  - `references/layouts/stack.md`, `references/layouts/box.md`.
  - `references/layouts/center.md`, `references/layouts/cluster.md`.
- Read `references/layouts/cover.md` and `references/layouts/sidebar.md` for the slide
  composition.

## Sources

- Original summary and authored example derived from
  [Every Layout: Composition](https://every-layout.dev/rudiments/composition/).
  - Includes the dialog decomposition, nested form, and presentation-slide diagrams.
- This rudiment has no component download.
