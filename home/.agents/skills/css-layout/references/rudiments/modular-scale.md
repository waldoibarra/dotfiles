# Modular scale

Generate type and spacing from a base length and one ratio.

- Reuse the resulting CSS custom properties across global styles, layout rules, and optional
  component configuration.
- Do not select each dimension independently.

## Contents

- Core principle and visual harmony
- A practical token scale
- Scope, inheritance, and JavaScript access
- Shadow DOM and property-based configuration
- Optional scale-only contracts
- Pitfalls and related layouts
- Sources

## Core principle and visual harmony

A modular scale is geometric: step `n` is base times ratio to the power `n`.

- Negative steps divide rather than producing negative lengths.
- **Example:** a `1rem` base with ratio `1.5`.
  - Successive positive steps are `1.5rem`, `2.25rem`, and `3.375rem`.

The chapter uses musical harmony as an analogy for visual coherence.

- It introduces harmony through arithmetic sequences and their reciprocals.
- A harmonic series and a geometric scale are not the same sequence.
- The frequency diagram illustrates coordinated repetition.
- The increasingly large squares form a curved incline.
  - Multiplication produces proportional, not constant, growth.

Text provides a useful starting point for the scale.

- `1rem` type with unitless `line-height: 1.5` occupies a `1.5rem` line box.
- Spacing can relate to that rhythm.
- Adding `1.5rem` repeatedly creates an arithmetic series; multiplying by `1.5` creates the scale.
- Multiplicative increments eventually exceed additive ones.
  - Choose a useful range; do not assume they are always smaller.

Consistency matters more than a supposedly perfect ratio.

- The golden ratio is an option, not a requirement.
- Select a ratio that supports the design’s hierarchy and density, then use it coherently.

## A practical token scale

Authored example with a deliberately short scale; extend the multiplication/division pattern only
to steps actually needed:

```html
<style>
  :root {
    --ratio: 1.5; /* Unitless multiplier, separate from the base length. */
    --s0: 1rem;
    --s-1: calc(var(--s0) / var(--ratio));
    --s-2: calc(var(--s-1) / var(--ratio));
    --s1: calc(var(--s0) * var(--ratio));
    --s2: calc(var(--s1) * var(--ratio));
    --s3: calc(var(--s2) * var(--ratio));
    font-family: system-ui, sans-serif;
    line-height: 1.5;
  }
  .scale-card {
    padding: var(--s1);
    border: 1px solid;
  }
  .scale-card > * {
    margin: 0;
  }
  .scale-card > * + * {
    margin-block-start: var(--s-1);
  }
  .scale-card h2 {
    font-size: var(--s2);
    line-height: 1.2;
  }
</style>
<article class="scale-card">
  <h2>Related dimensions</h2>
  <p>Heading size, padding, and separation come from the same scale.</p>
</article>
```

The website defines steps from `--s-5` through `--s5`.

- This smaller example preserves its dependency model, not the entire token inventory.
- A component using `var(--s4)` still needs that token defined.
  - Custom-property names do not synthesize missing scale steps.

The chapter discusses `pow()` as a future simplification.

- Treat that support statement as historical, not current compatibility advice.
- Do not copy its dimensional `pow()` illustration.
  - Exponentiation uses numbers, with the length applied separately.
- Where supported, an authored optional expression is `calc(1rem * pow(1.5, 3))`.
- The chained `calc()` scale above avoids needing exponentiation.

## Scope, inheritance, and JavaScript access

Root tokens are inherited defaults, not immutable constants.

- Define system-wide tokens on `:root`.
- Define component-specific values nearer their consumer when that is the intended scope.

Custom-property `var()` references resolve where the property is computed, before inheritance.

- Overriding only `--ratio` on a nested card does **not** rebuild steps computed at the root.
- For a genuinely local scale, redeclare the dependent steps in that scope.
  - Alternatively, override the consumed spacing token directly.

JavaScript can read the same configuration; use the consuming element, not the root, when local
overrides matter:

```js
// Run after the example card exists in the document.
const card = document.querySelector(".scale-card");
const styles = getComputedStyle(card);
const scaleStep = styles.getPropertyValue("--s2").trim();
const actualPadding = styles.paddingInlineStart;
console.log({ scaleStep, actualPadding });
```

The custom property is a CSS value string and may still contain a `calc()` expression.

- It is not JSON, a JavaScript number, or necessarily pixels.
- Read a computed consuming property when you need the resolved length.
- Do not use `parseFloat()` on an arbitrary token expression.

## Shadow DOM and property-based configuration

Inherited custom properties can cross a shadow host.

- Ordinary outside selectors still do not target shadow internals.
- Inside an existing shadow stylesheet, `:host { padding: var(--s2); }` uses the inherited token.
  - It applies on the host.
- `:host` is not a selector for ordinary document styles.

The chapter’s hypothetical padding component demonstrates a permissive contract:

- An HTML attribute is a string: `padding="var(--s2)"` or `padding="1.25rem"`.
- A getter reads the attribute and supplies `var(--s1)` when absent or empty.
  - A setter reflects assignments back to the attribute.
- The string becomes the CSS padding value, retaining the browser’s token resolution.
  - It does not translate the scale into JavaScript numbers.
- Getters and setters alone do not schedule rerendering.
  - A live component also needs its documented connection/attribute-change behavior.

Those Shadow DOM examples explain token sharing only.

- **Every Layout’s downloaded layout components use light DOM**, so global element styles remain
  available.
- Light DOM also lets a server or build emit initial configuration styles.
  - That is an integration step; a browser module import does not do it automatically.
- Without JavaScript, companion CSS can provide defaults.
  - Non-default attribute configuration needs pre-generated CSS if it must work before upgrade.

## Optional scale-only contracts

A permissive length prop supports composition and exceptions.

- A stricter application API can instead accept only a step identifier.
  - It then constructs a known token name.
- Do not silently impose that policy on Every Layout’s components.

Authored helper for the exact steps declared in the example:

```js
function spacingToken(step) {
  const value = String(step);
  // Signed integers in the supported range; rejects fractions and extra text.
  if (!/^(?:-[12]|[0-3])$/.test(value)) {
    throw new RangeError("Spacing step must be an integer from -2 through 3");
  }
  return `var(--s${value})`;
}
```

For example, `spacingToken(-1)` produces `var(--s-1)`.

- Match validation to the defined scale, including negative indices.
- The chapter’s illustrative single-digit regex does not implement its stated signed-index
  contract.
- Its interpolation also omits the `s` in the declared token names.
- The authored helper above deliberately does neither.

## Pitfalls and related layouts

- Keep the base length and unitless ratio distinct.
  - Negative indices mean smaller positive spaces, not negative margins.
- A `rem` base respects the root font size.
  - Do not override that preference with a fixed pixel root solely to simplify arithmetic.
- Do not assume a locally changed ratio propagates backward into inherited derived tokens.
- Do not assume a missing token automatically falls back to an earlier declaration.
- Shared scale values are especially useful for Stack separation, Box padding, and Cluster gaps:
  - `references/layouts/stack.md`, `references/layouts/box.md`, and
    `references/layouts/cluster.md`.
- Read `references/rudiments/global-and-local-styling.md` for the cascade architecture and
  `references/rudiments/axioms.md` for measure as another shared design rule.

## Sources

- Original summary and authored examples based on the complete rendered website chapter.
  - Coverage includes its diagrams and all substantive sections.
- The historical `pow()` and validation examples are qualified, not presented as a verified
  current API.

- [Every Layout: Modular scale](https://every-layout.dev/rudiments/modular-scale/)
