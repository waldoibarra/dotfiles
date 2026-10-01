# Verifying a layout in its context

## Contents

- Start with the container
- Stress the content, not just the viewport
- Checks by primitive
- Optional component checks
- Diagnose rather than mask
- Finish with evidence

Use the actual changed page and select the checks below that exercise its layout contract. This is a
browser procedure, not a requirement to add a test framework. Distinguish the skill's authored CSS
examples from optional downloaded components: they can use different mechanisms and defaults.

## Start with the container

Render real content at the region's smallest and largest supported sizes. Resize the containing
region independently of the viewport: the same Sidebar or Grid may appear in a full page, a split
pane, and a narrow card. For a wrapping or threshold rule, inspect just below and just above the
transition as well as the endpoints.

Observe both the result and its cause: computed `display`, available inline size, gap/margins,
min-size constraints, wrapping, and document overflow. A screenshot cannot by itself establish
keyboard access or prove that a declaration won the cascade. Record browser, container sizes,
content conditions, and the observed relationship; do not claim cross-browser coverage from one
browser.

## Stress the content, not just the viewport

- Replace short labels with long translated text; add an unbroken URL or identifier. Decide whether
  that content should wrap, truncate with an accessible alternative, or scroll intentionally.
- Increase text size/zoom and use multiple lines. Check clipped controls, inaccessible overlay
  edges, and unintended page-level horizontal scrolling.
- Exercise empty, one-item, and several-item states where meaningful. For a count-dependent
  Switcher, cross the configured count limit too.
- Include an image with its actual intrinsic dimensions and a missing/slow-loading image when media
  affects sizing.
- Nest the primitive in another layout. Check double spacing from child margins plus parent gap,
  inherited token scope, and whether the narrow child can shrink.
- If the product supports RTL or vertical writing, inspect it explicitly. Logical properties help,
  but mixed physical declarations and transforms are not proof of correct behavior.

## Checks by primitive

| Primitive | Observable contract                                                                                                                                                  |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stack     | Equal intended space only between participating siblings; recursive/nested rules do not unintentionally space internals; a split consumes genuinely available height |
| Box       | Padding/border stay inside the intended sizing budget; inversion does not damage media; a meaningful boundary survives forced colors where required                  |
| Center    | Measure is bounded, outer margins balance when space exists, and gutters remain at narrow sizes; text alignment changes only when requested                          |
| Cluster   | Items wrap without overlap and keep intended gaps; long controls remain usable; visual arrangement does not change keyboard order                                    |
| Sidebar   | The pair becomes adjacent only with adequate main-content space; stacked items fill available width; long content does not force page overflow                       |
| Switcher  | Peers switch together rather than leaving an accidental partial row; threshold and maximum-item policy both work                                                     |
| Cover     | Main content is centered when room exists, but growing content expands the region rather than clipping header/footer or controls                                     |
| Grid      | Tracks meet the minimum when space permits and shrink to the container when narrower; partially filled rows follow the chosen auto-fill/auto-fit behavior            |
| Frame     | Reserved ratio is correct before media loads; crop preserves important content; intrinsic image dimensions do not distort the frame                                  |
| Reel      | Only the intended region scrolls; offscreen content is reachable using the target input methods; scrollbar visibility and focus cues remain understandable           |
| Imposter  | Positioning uses the intended containing block; long content can be reached; focus, dismissal, and modality work if the surrounding feature requires them            |
| Icon      | Icon/text alignment holds at multiple font sizes; accessible naming is not duplicated or lost; interactive controls retain a usable name                             |
| Container | The query responds to the named ancestor's size, not merely viewport changes; containment does not unexpectedly collapse or change intrinsic sizing                  |

## Optional component checks

- Load the actual module, companion CSS, and required tokens. Check registration, console errors,
  computed structural styles, and generated configuration rules.
- Compare default configuration with one non-default value the application uses. Check rendered
  output, not only getters or successful imports.
- Mutate the exact attribute/property path used by application code and observe both rule
  regeneration and the resulting layout. Initial markup success does not establish live-update
  support, especially with camelCase observed attributes.
- Put differently configured instances in the same document to expose reused-style identity
  problems. For boolean options, check the disabled state and reversal if the application changes
  it at runtime.
- If the component can be disconnected/reconnected, exercise that transition. For Reel, check
  content insertion and width changes that change overflow state.
- Disable JavaScript or block module loading if progressive fallback is claimed. The companion
  stylesheet provides a baseline, not necessarily configured parity; report the actual remaining
  behavior.

## Diagnose rather than mask

Locate the owner of the broken relationship: wrapper, direct child, nested content, containing
block, or inherited token. Check unresolved custom properties, companion CSS omissions, intrinsic
minimums, and ordinary margins before adding breakpoints. Avoid using document-level
`overflow-x: hidden` to hide a sizing defect: it can hide unreachable content instead of fixing it.

Use media/container queries when the requirement genuinely changes at that boundary; do not replace
a valid product rule with intrinsic wrapping merely to follow a slogan. Likewise, a CSS positioning
solution does not replace a dialog's behavior or an icon's accessible name.

## Finish with evidence

For implementation, report the intended relationship, representative states exercised, observed
result, and any untested target/browser limitation. For review, identify the affected element/rule
and a reproducible state with user-visible impact. Keep source-inspected caveats separate from
browser-observed failures. Maintenance routing and with/without-skill evaluations live in
`evals/evals.json`, not in ordinary page verification.

The layout mechanisms and chapter-specific concerns derive from the
[Every Layout website](https://every-layout.dev/layouts/); source inventory is in
`references/sources.md`. This procedure is an authored application of those mechanisms, not a claim
that the website or every download passed these checks.
