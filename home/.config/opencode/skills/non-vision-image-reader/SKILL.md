---
name: non-vision-image-reader
description: "Use when a text-only model gets an [Image N] unsupported-input placeholder or cannot interpret a referenced image file. Recover OpenCode pasted images and route them to a vision MCP."
---

# Non-vision image reader

## Prerequisite

Check your available tools for a vision MCP before recovering files. If none is loaded, stop:
state that image analysis needs a vision MCP, such as Z.AI, enabled and the host restarted.
Do not search for substitutes, install packages, or configure a server.

With a vision MCP available, do not treat the unsupported-input placeholder as a final answer.
Recover or locate the image, analyze it, and answer the user's question without narrating the
recovery steps. Never fabricate analysis of an image you could not read.

## Locate the image

| Input | Action |
| --- | --- |
| `[Image N]` with `does not support image input` or `Cannot read "clipboard"` | Run the recovery script below. |
| User-provided image path | Skip recovery; pass that path to the vision tool. Never delete this file or its directory. |

OpenCode reports `Base directory for this skill: <BASE>`. Substitute that absolute directory:

```sh
<BASE>/scripts/recover-pasted-images.sh
```

The script needs Bash, SQLite with JSON functions, and `base64`. It reads
`${XDG_DATA_HOME:-$HOME/.local/share}/opencode/opencode.db` and prints one path per line on
success. All returned files share a newly created temporary directory. Use those exact paths;
do not list directories or guess filenames.

**Recovery limit:** the query selects the latest user message containing images across the
whole database, not the current session or prompt. Parts are ordered by ID and named
`image-1.png`, `image-2.png`, and so on; the suffix does not verify the original format.
Do not claim these are the current prompt's images when their identity is ambiguous. Ask for
explicit file paths instead. A failed or empty recovery also requires that honest fallback.

## Analyze

Resolve these tool names in the loaded MCP namespace and follow its argument schema. Pick one
matching tool per image, not several speculative calls:

| User intent | Tool |
| --- | --- |
| Read code, terminal output, or document text | `extract_text_from_screenshot` |
| Read a chart, graph, dashboard, or KPIs | `analyze_data_visualization` |
| Diagnose an error dialog, stack trace, or failed build | `diagnose_error_screenshot` |
| Describe a UI or turn it into code/specification | `ui_to_artifact` |
| Compare expected and actual UIs | `ui_diff_check` |
| Read architecture, flowchart, ER, or UML diagrams | `understand_technical_diagram` |
| Other image analysis | `analyze_image` |

Pass the path as `image_source` for single-image tools. Use the user's intent to target
extraction; make the final interpretation and decisions yourself. For a stack recommendation,
extract UI structure, behavior, data visualization, and style without asking the vision tool
to choose the stack. For implementation, use `ui_to_artifact` with `output_type: code`.

Analyze independent images in parallel. For explicit comparison, make one `ui_diff_check`
call with `expected_image_source` and `actual_image_source`, assigned from the user's wording,
not guessed from filenames. If the needed tool or image is unavailable, state the limitation.

## Cleanup and result

After analysis, or when abandoning recovered images, remove only the exact files printed by
this recovery invocation, then remove their shared directory with `rmdir`. Use quoted paths
and `rm --` for the files. Never recursively delete a directory derived from a user-provided
image path. If recovery fails before printing paths, do not guess which directory to delete.

Answer the user's question from the returned evidence. If you could not recover or analyze
the image, explain the failure and ask the user to save it as a file and provide its path.

Read [the recovery script](scripts/recover-pasted-images.sh) when maintaining its database or
output contract.
