---
name: css-layout
description:
  "Build and diagnose intrinsic, composable CSS layouts using Every Layout's primitives. Use when
  fixing responsive wrapping, spacing, alignment, overflow, or choosing Stack, Sidebar, Switcher,
  Grid, and related patterns. For Web Component architecture rather than layout, use web-standards."
---

# CSS Layout

- **IS:** choosing, composing, implementing, and reviewing content-driven CSS layout, in any
  framework or plain HTML.
- **IS NOT:** application architecture, a framework migration, or a requirement to use custom
  elements. Use `web-standards` for native semantics, progressive enhancement, component lifecycle,
  Light/Shadow DOM, and platform tooling; `ui-design` for broader visual/interface design.

Prefer relationships that adapt to their available space over device-specific exceptions. Intrinsic
CSS is a default, not a prohibition on media or container queries. Preserve the project's tokens,
semantics, browser targets, and existing component conventions.

Load `web-standards` when a layout change also changes semantics, native interaction, or component
lifecycle; geometry-only fixes do not need it. `web-app-craft` coordinates combined app-interface
work, but is not a dependency of this skill.

## Workflow

- Identify the relationship: space between siblings, readable measure, wrapping group, asymmetric
  pair, threshold switch, repeated tracks, bounded media, or overlay. Inspect the actual containing
  block, not just the viewport.
- Load the matching layout reference below and the rudiment behind the uncertainty. Read
  `references/rudiments/composition.md` when combining primitives; do not load the entire library.
- Implement the CSS mechanism on semantic HTML first. When importing, configuring, or verifying
  optional downloaded components, read `references/component-integration.md` and the chapter's
  component section. Choose those components only when their attribute API is useful. Do not add a
  runtime to obtain a CSS layout.
- Exercise the changed surface using `references/verification.md`: resize its container, stress its
  content, and inspect accessibility-relevant behavior. Fix the requested implementation through
  the observed states; a working screenshot at one width is not completion.
- Deliver the changed behavior, why the mechanism fits, and the browser states actually checked.
  For review-only requests, give located findings and evidence rather than silently editing.

## Rudiments: load for the decision

All paths resolve from this installed skill directory, not the application root.

| Read when                                                             | Reference                                          |
| --------------------------------------------------------------------- | -------------------------------------------------- |
| Padding, borders, sizing, or overflow are surprising                  | `references/rudiments/boxes.md`                    |
| Nesting layouts or deciding which element owns spacing                | `references/rudiments/composition.md`              |
| Choosing font-relative, root-relative, viewport, or intrinsic lengths | `references/rudiments/units.md`                    |
| Resolving inherited defaults, local exceptions, or token scope        | `references/rudiments/global-and-local-styling.md` |
| Establishing a coherent spacing/type progression                      | `references/rudiments/modular-scale.md`            |
| Replacing special-case breakpoints with durable constraints           | `references/rudiments/axioms.md`                   |

## Layouts: choose the relationship

| Need                                                                     | Load                              | Distinguish from                                                |
| ------------------------------------------------------------------------ | --------------------------------- | --------------------------------------------------------------- |
| Space successive flow elements consistently                              | `references/layouts/stack.md`     | Box owns inside padding; Stack owns sibling rhythm              |
| Enclose content with padding and a boundary                              | `references/layouts/box.md`       | A Box is not a whole card design                                |
| Center a bounded, readable region with gutters                           | `references/layouts/center.md`    | Cover centers on the block axis; text alignment is separate     |
| Wrap variable-width controls, links, or tags                             | `references/layouts/cluster.md`   | Grid aligns tracks; Cluster follows content widths              |
| Keep a narrow region beside a flexible main region until they cannot fit | `references/layouts/sidebar.md`   | Switcher gives peers one collective threshold                   |
| Switch peer items directly between a row and a column                    | `references/layouts/switcher.md`  | Cluster permits partial wrapping; Grid permits several rows     |
| Center main content vertically while accommodating header/footer content | `references/layouts/cover.md`     | Imposter removes content from normal flow                       |
| Distribute repeated items into responsive, aligned tracks                | `references/layouts/grid.md`      | Reel scrolls rather than wrapping                               |
| Reserve a media ratio and control cropping                               | `references/layouts/frame.md`     | Center limits measure, not aspect ratio                         |
| Keep a horizontal collection scrollable                                  | `references/layouts/reel.md`      | Grid avoids horizontal scrolling by reflowing                   |
| Position an overlay relative to a region or viewport                     | `references/layouts/imposter.md`  | Positioning does not implement a dialog's interaction contract  |
| Align an inline icon with text and its font metrics                      | `references/layouts/icon.md`      | Accessible naming remains a semantic decision                   |
| Style descendants according to the containing region's size              | `references/layouts/container.md` | Use intrinsic wrapping first when it already expresses the rule |

## Integration and evidence

- `references/component-integration.md`: before importing, configuring, or verifying any downloaded
  component; covers companion CSS, token dependencies, light DOM, registration, and shared
  implementation limits.
- `references/verification.md`: when implementing or diagnosing a layout; select checks matching the
  changed behavior.
- `references/sources.md`: when checking provenance, refreshing a reference, or reconciling website
  documentation with a download.

## Gotchas

- Downloaded components need their companion CSS and referenced tokens; importing JavaScript alone
  does not establish the baseline layout.
- A custom tag supplies no landmark, list, button, or dialog semantics. Preserve semantic children
  and native interaction.
- The downloaded Switcher defaults to `5` items, although its documented API says `4`; set `limit`
  explicitly when the count matters. Center's `gutters` is a CSS length string in the download, not
  the documented boolean.
- Configuration changes are not uniformly safe in the downloaded implementations. Read the relevant
  chapter before relying on live attribute updates; source inspection is not runtime confirmation.

## Sources and maintenance

Derived from the [Every Layout website](https://every-layout.dev/) by Heydon Pickering and Andy
Bell: six rudiments, thirteen layouts, and their native component downloads. References are original
concise explanations and illustrative examples, not redistributed book chapters or full paid
implementations. No ebook or PDF source is used. `references/sources.md` records the inventory and
retrieval evidence.

`evals/evals.json` is maintenance-only; do not load it during ordinary layout work.
