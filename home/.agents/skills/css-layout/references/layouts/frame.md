# Frame

## Contents

- Problem and mechanism
- Primary HTML/CSS example
- Variants and decisions
- Downloaded component
- Pitfalls and checks
- Sources

## Problem and mechanism

Give media a consistent shape without distorting its contents. Natural responsive images need only
`max-inline-size: 100%` and an automatic height: their file determines the ratio. A Frame
deliberately replaces that ratio with a viewing window.

`aspect-ratio: width / height` establishes the window; `object-fit: cover` fills it with undistorted
media and crops the excess. The chapter's wide-image diagram shows why a narrower frame removes the
sides rather than compressing the image. Centered flex alignment also accommodates a non-media
fallback. `overflow: hidden` clips content outside the window.

Use for thumbnails, video previews, and cards with interchangeable media/text placeholders. Leave
editorial images uncropped when the whole image matters. For a collection, compose with
`references/layouts/grid.md` or `references/layouts/reel.md`.

## Primary HTML/CSS example

This authored example is self-contained; the inline image deliberately has a wider natural ratio
than its frame.

```html
<style>
  .portrait-window {
    aspect-ratio: 4 / 3;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .portrait-window > img,
  .portrait-window > video {
    inline-size: 100%;
    block-size: 100%;
    object-fit: cover; /* Crop, never stretch. */
  }
</style>
<div class="portrait-window">
  <img
    alt="Gold sun above a blue landscape"
    src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 100'%3E%3Cpath fill='steelblue' d='M0 0h240v100H0z'/%3E%3Ccircle fill='gold' cx='120' cy='35' r='20'/%3E%3C/svg%3E"
  />
</div>
```

## Variants and decisions

- Focal point: change `object-position`, for example `70% 35%`, when central cropping removes the
  subject. The default is `50% 50%`.
- Orientation: an intentional `@media (orientation: portrait)` rule can switch the frame to
  `aspect-ratio: 1`. This is a content decision, not a required viewport breakpoint.
- Arbitrary HTML/canvas: flex centers the child; overflow performs clipping. Text wraps normally, so
  a deliberately oversized inline size may be needed for horizontal clipping. Check flex shrinking
  and minimum sizes before assuming an oversized child will remain oversized.
- Decorative backgrounds can use `background-size: cover`, but backgrounds have no direct
  alternative-text channel and may disappear in forced-color environments. Use an actual image for
  meaningful content.
- Historical ratio fallback: vertical percentage padding resolves against the containing width. For
  16:9, the height-producing padding is `9 / 16 * 100% = 56.25%`, the inverse of the aspect ratio.
  Prefer `aspect-ratio` rather than reproducing that workaround. Keep numerator/denominator
  conventions explicit; do not accidentally apply `16 / 9` as the padding multiplier.

## Downloaded component

Include `Frame.css` and import `Frame.js` as a module, then use this **component example**:

```html
<frame-l ratio="3:2"><span>Artwork unavailable</span></frame-l>
```

API: `ratio` is a string, default `"16:9"`; its getter reads the attribute and its setter writes it.
The module exports `Frame` and registers `frame-l`. Both `connectedCallback` and the observed
`ratio` attribute call `render`. No Shadow DOM is created.

The companion CSS supplies the flex window, clipping, media sizing, and default ratio. JavaScript
only generates the configured ratio rule. A short **implementation excerpt** shows the parsing
boundary:

```js
let ratio = this.ratio.split(":");
// The generated declaration uses ratio[0] / ratio[1].
```

Rendering warns if the element has anything other than one child element; it does not prevent
rendering. A `Frame-…` configuration key becomes `data-i`, and one matching style element per key is
appended to the document head. There is no ratio validation or child-mutation observer. A
child-count warning during upgrade is therefore not a content-management feature. Shared loading,
generated-style, and trust constraints: `references/component-integration.md`.

## Pitfalls and checks

- Treat clipping as deliberate information loss: check faces, embedded labels, subtitles, controls,
  alternative text, and zoomed content. Do not use a Frame as a general text container.
- `aspect-ratio` is a preferred sizing relationship, not a promise that arbitrary minimum-content
  constraints cannot affect size. Verify the rendered box with the actual child and surrounding
  layout.
- Exactly one direct media child receives the intended simple window behavior; nested images do not
  match the companion child selector.
- The chapter's modern CSS and the inspected download both use `aspect-ratio`; neither requires the
  historical padding technique.

## Sources

Website chapter and its rendered diagrams, generator, API, and examples:
[Frame chapter](https://every-layout.dev/layouts/frame/).

Inspected download (`Frame.js`, `Frame.css`, `README.txt`):
[Frame component archive](https://every-layout.dev/downloads/Frame.zip).

This reference paraphrases website content and distinguishes authored examples from source-inspected
component behavior; it does not claim runtime verification.
