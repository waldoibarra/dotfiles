# Stack

## Contents

- Problem and mechanism
- Primary HTML/CSS
- Variants and composition
- Downloaded component
- Checks and sources

## Problem and mechanism

Space belongs to the relationship between siblings, not to a paragraph in isolation. A bottom margin
on every paragraph leaves excess space against a padded container. A Stack puts block-start margin
only on elements with a preceding sibling: `> * + *`. Reset only the block-axis margins it owns;
preserve inline margins used by other layouts.

Use it for article flow, form sections, and card interiors. Grid cells should not acquire Stack
spacing _between_ cells, but each cell can contain a Stack. Related patterns:
`references/layouts/grid.md` and `references/rudiments/modular-scale.md`.

## Primary HTML/CSS

An authored example; paste into an HTML document. The column flex context also permits the split
variant below.

```html
<style>
  .flow-stack {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .flow-stack > * {
    margin-block: 0;
  }
  .flow-stack > * + * {
    margin-block-start: var(--flow-space, 1.5rem);
  }
</style>
<section class="flow-stack" aria-labelledby="delivery-title">
  <h2 id="delivery-title">Delivery options</h2>
  <p>Choose where your order should arrive.</p>
  <button type="button">Choose an address</button>
</section>
```

The first child has no injected margin, and the last child has no trailing margin. Taking spacing
from the body line height creates a useful rhythm; use scale steps for larger separations, not
unrelated values for each element.

## Variants and composition

- **Nested:** give each Stack responsibility for its own immediate children. Large spacing separates
  form fields; a nested smaller Stack separates each label, control, and error. Labels must be
  block-level (or flex items) for block margins to work. The chapter's form diagram shows these two
  distinct rhythms rather than one uniform spacing everywhere.
- **Recursive:** replace `> * + *` with `* + *`, and scope any margin reset consistently. This
  reaches every nesting level: the nesting diagram has equal spacing inside and outside a nested
  group, without doubled edge gaps. It can also unintentionally space list items and inline content;
  explicit nested Stacks are safer for mixed content.
- **Exceptions:** set the spacing variable on a particular child and its next sibling to increase
  space both before and after the exceptional item. Do not hoist a child-facing spacing variable
  indiscriminately onto Stack containers: a nested container is also an outer Stack's child.
- **Split:** an auto block-end margin after a chosen child consumes unused height. There must
  actually be spare block space, supplied by a definite parent size or stretching alongside taller
  content. `block-size: 100%` on an only-child Stack needs a resolvable containing size; it does not
  manufacture height.

Variant CSS, added after the primary rules:

```css
/* More space on either side of one important child. */
.flow-stack > .milestone,
.flow-stack > .milestone + * {
  --flow-space: 3rem;
}
/* A tall card can leave its final actions at the bottom. */
.flow-stack.split {
  min-block-size: 20rem;
}
.flow-stack.split > :nth-child(2) {
  margin-block-end: auto;
}
```

The chapter's slide-editor example gets its spare space from a taller neighboring Cover. This is a
layout relationship, not a viewport breakpoint. Related pattern: `references/layouts/cover.md`.

## Downloaded component

Load `Stack.js` as a module and include `Stack.css`; define `--s1` or provide `space`. Light-DOM
setup, shared CSS generation, and attribute hazards are documented in
`references/component-integration.md`.

Component usage, not a replacement for the standalone example:

```html
<stack-l space="1rem">
  <h2>Order summary</h2>
  <p>Two items ready to ship.</p>
  <button type="button">Continue</button>
</stack-l>
```

| API          | Downloaded default | Meaning                                                                            |
| ------------ | ------------------ | ---------------------------------------------------------------------------------- |
| `space`      | `var(--s1)`        | CSS margin value between siblings                                                  |
| `recursive`  | absent / false     | Presence removes the direct-child restriction                                      |
| `splitAfter` | `null`             | One-based child position receiving an auto end margin; read as an attribute string |

`Stack` extends `HTMLElement` and registers `stack-l`. Getters read attributes; setters write them.
`connectedCallback` and `attributeChangedCallback` call `render`; the observed list is `space`,
`recursive`, `splitAfter`. Render assigns a configuration-derived `data-i`, creates one matching
style in the document head if absent, and emits the sibling-spacing selector. A truthy `splitAfter`
also emits the `:only-child` height rule and `:nth-child(...)` split rule. There is no shadow root
or child-content rewrite.

Selected downloaded expressions (not the complete implementation):

```js
// The selector switches depth without walking the descendants.
this.recursive ? "" : " >";
// The split value is used as CSS selector input, not parsed as a number.
this.getAttribute("splitAfter") || null;
```

`Stack.css` supplies flex-column layout and default sibling spacing; it does **not** reset existing
child margins. Supply a scoped reset if headings and paragraphs retain browser margins.

Source inspection found that the `recursive` property setter calls `setAttribute` with one argument
rather than a name/value pair; use attribute presence/removal rather than that setter. Browser
verification found that mutating `splitAfter` left `data-i` unchanged: its mixed-case observed name
does not match HTML's lowercased notification. Initial connection still reads the attribute. Treat
attributes as trusted configuration rather than arbitrary CSS input.

## Checks and sources

Check empty, one-child, nested, recursive-list, and split cases; verify no trailing gap, no doubled
native margins, and usable flow when a card grows beyond its minimum height. A custom element has no
list semantics: prefer a native `ul` with the CSS class, or use `role="list"` and direct
`role="listitem"` children when appropriate.

Website chapter, diagrams, generator, and API: [Stack](https://every-layout.dev/layouts/stack/).

Inspected download (`README.txt`, `Stack.css`, `Stack.js`):
[Stack.zip](https://every-layout.dev/downloads/Stack.zip).
