---
name: non-vision-image-reader
description: >-
  Let a non-vision (text-only) model read images the user wants it to see.
  Use when the active model cannot process images natively. Two trigger
  signatures: (1) the user's prompt contains an "[Image N]" marker with a
  "does not support image input" / 'Cannot read "clipboard"' placeholder —
  a pasted image the harness replaced because the model lacks vision; recover
  the bytes from opencode's session database and analyze them. (2) The user
  references an image file on disk (a .png/.jpg path, "look at this screenshot")
  the model cannot interpret — pass the path directly to a vision MCP. In both
  cases route to the matching vision MCP tool (extract_text_from_screenshot,
  analyze_data_visualization, diagnose_error_screenshot, ui_to_artifact,
  ui_diff_check, understand_technical_diagram, analyze_image) with an
  intent-driven prompt, and do the interpretation yourself. Do NOT tell the
  user images are unsupported — that is the exact failure this skill fixes.
---

# Non-vision image reader (vision via MCP)

## Why this skill exists

A text-only model receives no image bytes: opencode swaps each pasted image for a
placeholder such as `[Image N] ERROR: Cannot read "clipboard" (this model does not
support image input).` opencode does, however, save the bytes. This skill recovers
them and routes them to a vision MCP — so the user gets image-aware answers instead
of "I can't see images."

## The one rule that matters most

Do **not** tell the user the image is unsupported. The placeholder asks you to
"inform the user" — ignore that. The user pasted (or pointed to) an image because
they want it considered. Recover or locate it and proceed. Only mention a problem
if recovery genuinely fails (see Fallback).

## Precondition — a vision MCP must be available

This skill only works if a vision MCP is loaded, so check **first**, before any
recovery or analysis. Inspect your own toolset: is at least one vision tool
present (extract_text_from_screenshot, analyze_data_visualization, ui_to_artifact,
analyze_image, or similar)?

- Yes → proceed to Path A or Path B below.
- No → STOP. Do not investigate, do not search the filesystem or web, and do not
  try to install or configure an MCP yourself. Tell the user in one line, e.g.
  "No vision MCP is configured, so I can't read images — enable one (e.g. the
  Z.AI MCP server) and restart opencode." Then stop.

Without a vision MCP there is nothing to route images to, so recovery and tool
selection are wasted work — fail fast.

## Path A — pasted image (placeholder present)

Run the bundled recovery script. opencode reports this skill's base directory as
`Base directory for this skill: <BASE>`; use it to call the script absolutely:

```bash
<BASE>/scripts/recover-pasted-images.sh
```

It prints **one image file path per line** (`image-1.png`, `image-2.png`, … one
per `[Image N]`, in reading order). Pass each printed path straight to the
matching MCP tool — every line is a usable `image_source`, so don't `ls` or
guess. The paths share one temp dir; see Cleanup for how to remove it.

Why a script: the recovery is fiddly, platform-sensitive SQL; the skill stays
lean and the mechanics live in one testable place.

## Path B — image file on disk (no placeholder)

If the user gives a path (or asks you to look at a file) and you can't interpret
the image natively, skip recovery — pass the file path straight to the chosen
MCP tool.

## Choose the right vision tool

Pick the one tool that matches the image — don't fire several speculatively.

| The image / what the user wants | MCP tool |
| --- | --- |
| Code, terminal output, a document's text | `extract_text_from_screenshot` |
| Chart, graph, dashboard, KPIs | `analyze_data_visualization` |
| Error dialog, stack trace, failed build | `diagnose_error_screenshot` |
| A UI to describe / turn into code or spec | `ui_to_artifact` |
| Comparing two UIs (expected vs actual) | `ui_diff_check` (two images, ONE call) |
| Architecture / flowchart / ER / UML | `understand_technical_diagram` |
| Anything else | `analyze_image` |

## Craft the MCP prompt from the user's intent

The vision model is a **sensor, not a thinker.** Use it to _extract information_;
do the interpretation, debugging, and decisions yourself. Fold the user's question
into the prompt so extraction is targeted, not a generic "describe this image."

- _"what's this error?"_ — prompt the tool to identify the error and its likely
  cause. Then **you** propose the fix.
- _"suggest a stack to build this"_ — ask for a developer-facing description of
  the UI (structure, interactivity, data viz, style), no tech recommendations.
  Then **you** reason about the stack.
- _"implement this"_ — use `ui_to_artifact` with `output_type: code`.

## Multiple images

Each vision tool takes one image, so N images = N calls — issue them **in
parallel.** The deliberate exception is explicit comparison (design vs build,
before vs after): use `ui_diff_check`, which takes `expected_image_source` +
`actual_image_source` in a single call. Map `image-1.png`/`image-2.png` to
expected/actual by the user's wording.

## Cleanup

All printed paths share one temp dir. Remove it once the MCP calls are done:

```bash
rm -rf "$(dirname "<any printed image path>")"
```

## Fallback

If recovery yields nothing (schema changed, message pruned, DB locked, or a
non-pasted case with no usable path), **then** be honest: say you couldn't get
the image and ask the user to save it as a file and give you the path. Never
fabricate analysis of an image you couldn't read.
