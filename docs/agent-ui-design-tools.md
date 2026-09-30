# Agent UI Design Tools

Read this before choosing a tool that lets coding agents design a UI and then implement it in code.

Status: OpenPencil adopted for the portfolio on 2026-09-30. File inspection, strict-font PNG
rendering, and saved edits verified with 0.15.1. Read [tooling.md](/docs/tooling.md#openpencil)
before installing or upgrading it.

## Requirements

- Open source preferred.
- Harness-agnostic, with Pi/OMP as the primary harness. Claude Code and OpenCode are secondary.
- The agent generates a design, then implements that same design in code.

## Harness constraints

| Harness | MCP | Agent Skills (`SKILL.md`) | CLI via bash |
| --- | --- | --- | --- |
| Pi (`badlogic/pi-mono`) | No native support; community `pi-mcp-adapter` only | Yes | Yes |
| OMP (`can1357/oh-my-pi`) | Yes, native | Yes | Yes |
| Claude Code | Yes | Yes | Yes |
| OpenCode | Yes | Yes, also reads `.claude/skills` | Yes |

A CLI or skill works in every harness. An MCP-only tool leaves vanilla Pi out unless you
install the adapter.

Sources:

- <https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md>
- <https://mariozechner.at/posts/2025-11-30-pi-coding-agent/>
- <https://github.com/can1357/oh-my-pi>
- <https://opencode.ai/docs/skills/>

## Recommendation: OpenPencil

- Repo: <https://github.com/open-pencil/open-pencil> (MIT, about 8.6k stars).
- Interfaces: a headless CLI (inspect, query, export, lint, analyze, script) and an MCP server
  that advertises 100+ tools.
- Design to code: exports JSX + Tailwind, HTML + Tailwind, and design tokens (`analyze`, `variables`).
- Code to design: `@open-pencil/dom-css` imports HTML, CSS and Tailwind as editable layers.
- Formats: reads and writes `.fig` and `.pen` files.
- Why it fits: the CLI works across harnesses, while MCP adds live desktop control.
  Import/export supports handoffs in both directions, not automatic design/code synchronization.
- Risks: the project is young. Several forks have similar names, so install only from
  `open-pencil/open-pencil`. Release cadence and the "100+ tools" claim are unverified.

## Alternatives, ranked

### 2. Anthropic `frontend-design` skill + shadcn/ui MCP

- Repo: <https://github.com/anthropics/skills/tree/main/skills/frontend-design>.
- Model: the code is the design, so there is no handoff step.
- Pros: cheapest and most portable option, and Pi loads the skill natively. The shadcn MCP
  adds a real component registry in OMP, Claude Code and OpenCode.
- Cons: there is no separate design file to review or iterate on apart from the code.

### 3. Penpot MCP

- Repo: <https://github.com/penpot/penpot/tree/develop/mcp> (MPL-2.0).
  The standalone `penpot/penpot-mcp` repo is archived.
- Model: a self-hostable, collaborative Figma alternative. Agents read and write files,
  styles and tokens through the Plugin API.
- Pros: a mature, durable design system with company backing.
- Cons: MCP only, so vanilla Pi needs the adapter. There is no clean React exporter,
  so the agent turns the JSON and tokens into code itself.

## Rejected

| Tool | Reason |
| --- | --- |
| Onlook (Apache-2.0) | Right model (the design is the live React app), but I found no documented CLI or MCP for outside agents. Watch it. |
| tldraw agent-template | The starter is MIT, but the core SDK needs a paid license for production. |
| Excalidraw MCP | Diagrams only, no code export. |
| OpenUI, screenshot-to-code | Standalone apps that agents can't drive. One-way only. |
| Magic MCP (21st.dev) | MCP only, and some catalog content is paid. |
| v0, Google Stitch, Figma MCP | Closed source. |

## Decision tree

- You want an editable design file with code import/export, in every harness: OpenPencil.
- You want speed and don't need a design file: the `frontend-design` skill.
- A team needs a collaborative design system you host yourself: Penpot, run from OMP
  instead of vanilla Pi.

## Open questions

- Is `pi-mcp-adapter` maintained, and is it good enough to use?
- How recently was OpenPencil updated, and does it really expose 100+ tools?
- Does Onlook have a CLI spec?
- Has `superdesign-skill` been tested inside Pi?

## Verified workflow

The portfolio's `just open-design` launches `docs/designs/landing.fig`. Use the globally
Mise-managed `openpencil` directly. File-based edits do not require MCP or an agent-specific
skill. Live desktop control additionally requires the managed MCP package and a working
`openpencil documents --json` connection. Native window capture depends on macOS permissions.

For the Lit portfolio, use strict-font PNG renders, node data, and extracted assets as
implementation references. Build semantic, responsive Lit components rather than copying
the fixed-position HTML export. Import/export does not keep source code and the design in sync.
