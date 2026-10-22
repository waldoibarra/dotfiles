# Work harness parity

**Goal:** Keep the personal harness and the work harness behaving the same way.
Each behavior has one owner on each side. A duplicate is accepted when this page tracks it.

Read this page before changing a shared rule, hook, or integration on either side.
Apply the same change to the other owner, or record here why the sides differ.

## Shared behaviors

| Behavior | Personal owner | Work owner | Sync |
| --- | --- | --- | --- |
| Communication rules | `home/.agents/AGENTS.md` and `references/communication.md` | The work handbook's communication page | Personal leads; copy rule changes to work |
| Sentence limit lint (17 words) | `home/.config/obsidian/communication.cjs` | A copy of the rule in the work repository's markdownlint config | Byte-equal except rule name; copy on change |
| One MCP definition, native links | `home/.agents/mcp.json`, Dotbot links for Pi and Cursor, Claude adapter | The work `.agents/mcp.json`, linked by the work setup script for all three clients | Same concept; servers differ by scope |
| Developer-local `.agents/` directory | `~/.agents/` as the shared source; `.agents/` ignored by the global Git ignore | `.agents/` at the work root and in each repo, ignored by each repo | Same convention; the work side tracks only its MCP file |
| Skills on the Agent Skills path | `home/.agents/skills/` | Work skills linked to `.claude/skills/` and `.agents/skills/` | Same path for Pi; Cursor discovery pending |
| Markdown lint on agent writes | Not installed | A `PostToolUse` hook on `Write` and `Edit` in the work Claude settings | Candidate for the personal side |
| Reply sentence check | Not installed | Not installed | Candidate: a `Stop` hook in Claude settings, a Pi extension |
| Drafting skills lint their drafts | Not applicable | Work skills that draft standups, timelines, hand-off comments and PR bodies | Work only |

## Differences by design

- **Scope:** Personal servers and preferences never enter the work repository. Work servers never
  enter this one.
- **Claude MCP delivery:** Personal user servers need the registration adapter. The work root uses
  the project file, which Claude Code discovers natively.
- **Records:** Work decisions stay in the work repository. This page names behaviors, never company
  paths or people.

## Pending on the personal side

- Add the Markdown lint hook for agent writes.
- Add the reply sentence check, blocking once with findings.
