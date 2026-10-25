# Work harness parity

**Compare shared behaviors without transferring private configuration or granting cross-workspace authority.**
Each behavior has one owner on each side.
This page records reported duplication and deliberate differences, not verified current work configuration.

Read this page before proposing changes to a behavior shared with the work harness.
Verify the work owner only within an authorized work session.
Personal changes do not authorize company edits; propose corresponding work changes separately.

## Shared behaviors

| Behavior | Personal owner | Reported work owner | Relationship |
| --- | --- | --- | --- |
| Communication rules | `home/.agents/AGENTS.md` and `references/communication-rules.md` | The work handbook's communication page | Personal leads; work adoption requires separate authorization |
| Sentence limit lint (17 words) | `home/.config/obsidian/communication.cjs` | A copy of the rule in the work repository's markdownlint config | Reported byte-equal except rule name; recheck before authorized synchronization |
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

## Unapproved personal candidates

- A Markdown lint hook for agent writes.
- A reply sentence check that blocks once with findings.

Neither candidate is installed or authorized by this record.
Use the [session workflow](session-workflow.md) before proposing implementation.
