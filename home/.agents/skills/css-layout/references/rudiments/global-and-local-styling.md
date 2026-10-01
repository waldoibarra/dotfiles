# Global and local styling

Use global defaults for shared appearance, content-agnostic primitives for arrangement, and small
utilities for deliberate exceptions. Scope configuration without isolating content from the design
system.

## Contents

- Global reach and inheritance
- Utilities without changing semantics
- Local scope and its costs
- Layout primitives and configurable defaults
- Pitfalls and related references
- Sources

## Global reach and inheritance

“Global” describes several different mechanisms; they are not interchangeable:

| Mechanism                                   | Reach and consequence                                                                                                                                     |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inherited declarations on `:root` or `body` | Supply defaults to descendants for inheritable properties such as font and color. A declaration on a descendant takes precedence over an inherited value. |
| Universal selector `*`                      | Assigns a declaration directly to every matching element, rather than passing it down through inheritance. It does not cross shadow boundaries.           |
| Element selectors                           | Style every matching element in their tree, including unclassed Markdown or rich-text output.                                                             |
| Classes                                     | Reuse one rule on different element types and in different places, but require control of the markup.                                                     |

Prefer inherited typography and element-level defaults to restating the same appearance on every
component. Form controls may need an explicit `font: inherit` to participate. Keep branding (fonts,
colors, shadows) separate from the arrangement of boxes.

The chapter’s nested-box diagram represents recursive composition: each layout container arranges
children that can be another layout or a content end node. Its two-layer diagram separates that
arrangement from visual skin. Neither diagram suggests every piece of content needs its own
component.

## Utilities without changing semantics

A heading’s level describes document structure, not its desired visual size. Keep an `h2` an `h2`
when making it smaller; a reusable size utility is less coupled than a contextual selector such as
`.sidebar h2`.

Authored example, with appearance and layout kept separate:

```html
<style>
  :root {
    font-family: system-ui, sans-serif;
    --type-small: 1rem;
    --type-large: 1.5rem;
    --space: 1rem;
  }
  h2 {
    font-size: var(--type-large);
  }
  p,
  h2 {
    margin: 0;
  }
  .flow > * + * {
    margin-block-start: var(--space);
  }
  /* Escape punctuation in CSS, not in the HTML class value. */
  .font-size\:small {
    font-size: var(--type-small) !important;
  }
</style>
<section class="flow" aria-labelledby="delivery-heading">
  <h2 id="delivery-heading" class="font-size:small">Delivery details</h2>
  <p>The heading keeps its semantic level while its presentation changes.</p>
</section>
```

Use shared custom properties for element styles and utility values. Derive production sizes from the
system’s scale rather than accumulating unrelated numbers. Add a utility when a real use appears,
rather than shipping an exhaustive unused vocabulary.

The chapter uses `!important` for final-adjustment utilities. This changes cascade importance, **not
selector specificity**, and is not an absolute guarantee against other important declarations.
Follow the project’s cascade strategy rather than starting an importance contest.

The inverted-triangle diagram expresses broad reach with low specificity at the top and narrow,
deliberate overrides below. Utility-heavy styling can be useful for rapid prototypes or unusually
disparate designs; Every Layout instead prioritizes shared rules and algorithms to reduce manual
intervention. This is an architectural preference, not a requirement to replace an existing utility
framework.

## Local scope and its costs

| Technique            | Benefit                                             | Trade-off                                                                                                                                       |
| -------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Unique `id` selector | Addresses one element                               | Requires document-unique identifiers and adds high specificity; avoid using IDs merely to style reusable layouts.                               |
| Inline `style`       | Makes an instance override explicit                 | Duplicated declarations become difficult to maintain. A local custom-property value is usually less invasive than duplicating all layout rules. |
| Shadow DOM           | Contains ordinary selectors within a component tree | Also blocks ordinary outside selectors from styling shadow internals, including useful global element rules.                                    |

The Shadow DOM diagram shows selector containment in both directions, **not total isolation**:
inherited font/color values and inheriting custom properties can still pass through the host. Shadow
DOM is an encapsulation option, not a prerequisite for custom elements. The chapter surveys these
mechanisms; it is not an exhaustive catalogue of current CSS scoping features.

## Layout primitives and configurable defaults

The intended order is **global/inherited styles → layout primitives → utilities**. A primitive owns
relationships among children, not their tag names or content. A qualified selector such as
`.flow > * + *` targets every immediate child after the first without imposing paragraph-only or
card-only content.

Native custom elements make these primitives usable across frameworks. Their JavaScript is optional
architecture: the website’s CSS generators can also inform ordinary CSS or a framework-specific
wrapper.

The chapter’s Stack example illustrates the configuration model:

- Companion CSS establishes the default display and spacing. Custom elements otherwise start inline;
  a Stack needs block behavior.
- The documented `space` getter reads an attribute and defaults to `var(--s1)` when it is absent or
  empty.
- A supplied `space="var(--s3)"` chooses a different scale step without changing the content or the
  shared rule’s purpose.
- JavaScript derives a configuration key, puts it in `data-i`, and adds a matching stylesheet only
  when that configuration has not already been emitted.
- The key identifies **configuration, not instance**. Multiple Stacks with the same settings share
  one style element; the style element’s ID is unique while the matching `data-i` value is
  intentionally repeated.

This is light-DOM styling: children continue to receive global styles. The chapter’s one-property
Stack illustration explains the mechanism, not the full downloaded component’s current key format or
API. Use `references/layouts/stack.md` for the implementation-specific contract and
`references/component-integration.md` for CSS imports, tokens, registration, and generated styles.
Do not assume importing JavaScript also loads companion CSS or embeds server-rendered styles.

## Pitfalls and related references

- A direct declaration on every child can prevent a parent’s inherited change from taking effect.
  Decide whether you need inheritance or direct assignment.
- Global element styling is especially valuable when content comes from a CMS; class-only defaults
  may leave that content unstyled.
- Avoid turning reusable layout selectors into content selectors. The diagram’s “any element”
  children are the reason for qualified `*` selectors.
- `references/rudiments/composition.md` covers recursive layout ownership;
  `references/rudiments/modular-scale.md` covers token generation and scope.
- `references/rudiments/axioms.md` covers shared measure defaults, `references/layouts/box.md`
  covers containment, and `references/layouts/stack.md` covers spacing relationships.

## Sources

Original summary and illustrative example based on the complete rendered website chapter, including
its diagrams and code; not a redistributed chapter or downloaded implementation.

- [Every Layout: Global and local styling](https://every-layout.dev/rudiments/global-and-local-styling/)
