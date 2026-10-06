# Agent UI design tools

Read this before choosing a design-to-code workflow. Use
[OpenPencil](https://github.com/open-pencil/open-pencil) when you need an editable design file:
its CLI supports file-based inspection, editing and export without an agent-specific integration.

The requirements are an open-source preference, support across coding agents, and a design the
agent can use as an implementation reference. OMP and Pi are different tools; CLI access avoids
making MCP support a prerequisite.

## Managed installation

[Tooling](/docs/tooling.md#openpencil) assigns the desktop app to Homebrew and the CLI/MCP packages
to Mise. Installing the packages does not register an MCP server with every coding agent.

Use the CLI directly. This repository has no `open-design` recipe or tracked design document;
project-specific launch commands and `.fig` files belong to their respective projects.

## Inspect and render

Set `DESIGN_FILE` to the path of your existing design, then run:

```sh
openpencil info "$DESIGN_FILE" --json
openpencil tree "$DESIGN_FILE" --json
openpencil export "$DESIGN_FILE" --format png --font-policy strict --output /tmp/design-preview.png
```

The export writes or replaces `/tmp/design-preview.png`. Strict font policy rejects unavailable
fonts instead of silently accepting substitutions. Use node data, renders and extracted assets as
implementation references; build responsive components rather than copying fixed-position output.

[CLI import/export](https://openpencil.dev/reference/cli) supports HTML/CSS/Tailwind import and
JSX/HTML export. It does not keep the design and application code synchronized.

## Live desktop control

Omitting the file argument connects to the running desktop app. With the app and its bridge
running, `openpencil documents --json` lists available documents. Keep default authentication
enabled; follow the [MCP setup guide](https://openpencil.dev/programmable/mcp-server) for agent
registration and connection troubleshooting.

## When to choose another workflow

- No separate design file: use the
  [frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
  and review the running application.
- A shared, self-hosted design workspace: evaluate
  [Penpot's MCP integration](https://github.com/penpot/penpot/tree/develop/mcp) with a compatible
  agent. It is an alternative, not installed by this repository.
