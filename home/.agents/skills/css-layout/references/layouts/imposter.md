# Imposter

## Contents

- Problem and mechanism
- Primary HTML/CSS example
- Variants and decisions
- Downloaded component
- Pitfalls and checks
- Sources

## Problem and mechanism

Deliberately superimpose content over another region. Absolute positioning removes the overlay from
normal flow; an explicitly positioned ancestor supplies its containing block. Fixed positioning
normally uses the viewport. Without a containing-block ancestor, absolute positioning uses the
initial containing block, not the overlay's immediate parent and not necessarily the full scrolling
document's height.

Place the overlay's corner halfway across the containing block, then translate by half the overlay's
own dimensions. The two percentages refer to different boxes; that relationship centers content of
unknown size without hard-coded negative margins. The chapter diagrams progress from corner
placement, through self-relative correction, to the risk of a tall overlay obscuring adjacent
content.

Use for intentional overlays, unavailable-content notices, or decorative layering. Prefer normal
flow with `references/layouts/center.md` or `references/layouts/cover.md` when nothing should be
obscured. Grid can overlap areas when the existing grid structure is appropriate; Imposter does not
require that prior grid structure.

## Primary HTML/CSS example

This authored demonstration overlays decorative content only; it is not a modal dialog.

```html
<style>
  .preview-region {
    position: relative; /* Containing block without leaving normal flow. */
    min-block-size: 18rem;
    background: repeating-linear-gradient(45deg, #ddd 0 1rem, #eee 1rem 2rem);
  }
  .preview-notice {
    box-sizing: border-box;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    inline-size: 24rem;
    max-inline-size: calc(100% - 2rem);
    max-block-size: calc(100% - 2rem);
    overflow: auto; /* Long content stays reachable within the region. */
    padding: 1rem;
    background: white;
    color: #111;
    border: 1px solid;
  }
</style>
<section class="preview-region" aria-label="Artwork preview">
  <div class="preview-notice">
    <h2>Preview unavailable</h2>
    <p>The illustration is being updated. The accompanying article remains available.</p>
  </div>
</section>
```

Physical `top`/`left` here deliberately match physical `translate(x, y)` and remain centered in RTL.
The website/download use logical start insets with that same physical translation; inspect direction
and writing-mode behavior before using that combination unchanged.

## Variants and decisions

- **Containment:** `max-inline-size` and `max-block-size` cap the overlay; `overflow: auto` keeps
  oversized contents reachable. Subtract twice the desired margin: `100% - 2rem` creates 1rem
  clearance on each side. Ancestor padding is not a substitute because absolute positioning need not
  respect that padding as an inset boundary.
- **Breakout:** omit those maxima to permit deliberate overhang. The surrounding layout will not
  reserve space for it. Check neighboring content and pointer targets.
- **Fixed:** replace `position: absolute` with `position: fixed`, or expose
  `position: var(--positioning, absolute)` and set `--positioning: fixed` for one instance. Verify
  transformed/filter/containment ancestors, which can establish a fixed-position containing block.
- **Intrinsic width:** a positioned auto-width box may shrink-wrap; with a start offset of 50% it
  can resolve to roughly half the available width before translation. Set a desired width plus safe
  maxima when that behavior is inappropriate.
- **Layers:** later source content normally paints over earlier comparable content. Use `z-index`
  only for an intentional stacking requirement, considering stacking contexts rather than escalating
  arbitrary numbers. Visual positioning does not change reading or focus order.
- **Dialogs:** an Imposter is only geometry. A dialog also needs an accessible name, opening/closing
  behavior, focus entry/return, Escape handling, and appropriate background interaction control. A
  closed `<dialog>` is not shown just because it is inside an Imposter; `showModal()` uses the
  browser's top layer. Prefer the native dialog lifecycle rather than treating the wrapper as modal
  behavior.

## Downloaded component

Include `Imposter.css` and import `Imposter.js` as a module. **Component usage:**

```html
<div style="position: relative; min-block-size: 16rem">
  <imposter-l margin="1rem"><p>A locally centered notice.</p></imposter-l>
</div>
```

| Property / attribute | Type    | Default                      | Effect                                                 |
| -------------------- | ------- | ---------------------------- | ------------------------------------------------------ |
| `breakout`           | boolean | false                        | Presence removes generated containment/scrolling rules |
| `margin`             | string  | `0` documented; `0px` getter | Minimum inner-edge clearance when contained            |
| `fixed`              | boolean | false                        | Presence overrides absolute positioning with fixed     |

The module exports `Imposter` and registers `imposter-l`. Boolean getters use attribute presence;
setters add/remove attributes. `margin` reads/writes its string attribute. All three lowercase
attributes are observed; connection and attribute changes render. There is no Shadow DOM or
disconnected cleanup.

Companion CSS supplies absolute positioning, logical 50% insets, and translation. JavaScript adds
containment unless `breakout`, and fixed positioning when requested. A **selected implementation
excerpt** shows why unitless zero is normalized before arithmetic:

```js
let margin = this.margin === "0" ? "0px" : this.margin;
// Generated maxima subtract (margin * 2) from 100%.
```

A configuration-derived `data-i` selects a cached document-head style block. Breakout with nonfixed
positioning needs no generated rules; it relies on companion CSS. Without JavaScript, that CSS does
not provide the default maximum sizes, overflow scrolling, or attribute-driven fixed positioning.
Shared enhancement-failure constraints are documented in `references/component-integration.md`.

## Pitfalls and checks

- The website claims a Shadow DOM host alone contains fixed descendants. Do not generalize that
  claim: Shadow DOM itself is not the fixed-position containing-block trigger. Inspect ancestor CSS
  and verify the actual target surface. This download is light DOM anyway.
- The website's prose says maxima override minimum dimensions as well as dimensions. Do not rely on
  that: conflicting minimum sizes can defeat containment. Reset or reconcile authored minimum sizes,
  and use border-box sizing when padding/borders must fit inside the cap.
- If content is actually unavailable, coordinate visual hiding, screen-reader availability, and
  keyboard access. `aria-hidden` does not prevent focus or secure paid content. Do not hide
  meaningful usable content merely because part of it is overlapped.
- Verify RTL/vertical writing, tall translated content, viewport resize, zoom, scrolling, stacked
  overlays, and keyboard reachability. An overlay should obscure only what the product intends.

## Sources

Website chapter, positioning diagrams, generator, API, and examples:
[Imposter chapter](https://every-layout.dev/layouts/imposter/).

Inspected download (`Imposter.js`, `Imposter.css`, `README.txt`):
[Imposter component archive](https://every-layout.dev/downloads/Imposter.zip).

Mechanisms above are source-inspected; this reference does not present untested website claims as
runtime observations.
