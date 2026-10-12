# Personal MCP servers

Read [the harness design policy](/home/.agents/AGENTS.md#harness-design) before adding integrations.
Personal MCP definitions live in one shared source; work-only servers stay outside this setup.

## Source and scope

[`home/.agents/mcp.json`](/home/.agents/mcp.json) owns the personal server definitions.
Dotbot links it to `~/.agents/mcp.json` and Pi's native `~/.pi/agent/mcp.json`.
Pi reads that file directly; no MCP extension or duplicate definition is required.

Claude Code stores user servers in `~/.claude.json`, alongside private client state.
The [registration adapter](/scripts/update-coding-agents/sync-personal-mcp.py) derives user registrations
through `claude mcp add-json --scope user`. It never replaces that file or imports project servers.

| Server | Launch | Purpose |
| --- | --- | --- |
| `context7` | `npx -y --package=@upstash/context7-mcp@2.2.5 -- context7-mcp` | Resolve library IDs and retrieve public documentation. |
| `google-sheets-personal` | `google-sheets-personal-mcp` | Personal Sheets access through isolated Desktop OAuth. |

Context7's pinned stdio command preserves the existing Claude configuration.
Node/npm and network access are required; `npx` downloads the pinned package if absent.
Context7 accepts unauthenticated requests but may rate-limit them; no account or API key is provisioned.
Queries reach Context7's external service. Keep private code, company details, and secrets out of queries.

Use the common `mcpServers` schema. Pi supports stdio and streamable HTTP, not legacy SSE.
Keep client-specific exposure settings out of the shared definition.
Never put credentials in this public repository or replace the entire Claude registry with a symlink.
Pi commands can follow the config symlink and change tracked bytes; review any such changes.

Work roots, project `.mcp.json`, project `.pi/mcp.json`, and unrelated user entries are untouched.
Project servers can shadow user servers.
Verification outside work projects does not establish work parity.
Subagents do not automatically receive every MCP tool. Read [Pi delegation](pi/delegation.md)
before granting a role explicit MCP access.

## Google Sheets

The personal Sheets server runs locally through the shared launcher.
Read [Connect personal Google Sheets](/docs/coding-agents/google-sheets.md)
before creating OAuth credentials, signing in, or testing spreadsheet edits.
That guide owns runtime versions, access boundaries, troubleshooting, and removal.

## Apply configuration

Read [sync boundaries](/docs/tooling.md#sync-the-workstation) before running a full workstation sync.
Dotbot installs links; the existing updater then runs the registration adapter before Pi package updates.
To reconcile only Claude registrations after the shared source is installed:

```sh
python3 scripts/update-coding-agents/sync-personal-mcp.py
```

The adapter targets the normal home configuration, ignoring `CLAUDE_CONFIG_DIR` overrides.
Matching entries cause no writes. Missing entries are added through Claude's native command.
Detected conflicts and invalid manifest shapes fail before registration.
Unrelated entries are never removed.
A later native-command failure leaves earlier successful additions intact; registration is not a transaction.

On a conflict, inspect the exact user-scoped entry before replacing it.
After approval, remove only that entry with `claude mcp remove NAME --scope user`, then rerun the adapter.
Removing a server from the shared manifest does not automatically delete its Claude registration.
Avoid competing changes to the same server during registration; native Claude owns registry writes.

Restart the clients after configuration changes.
In Pi, `/mcp` shows connections and `/reload` refreshes them.

## Verify

Run fixture checks from the repository root; they use disposable homes and a fake Claude executable:

```sh
python3 scripts/tests/test-personal-mcp.py
python3 scripts/tests/test-personal-google-sheets.py
python3 scripts/tests/test-agent-harness.py
```

To additionally exercise concurrent native Claude registrations inside a disposable home:

```sh
MCP_NATIVE_CHECK=1 python3 scripts/tests/test-personal-mcp.py
```

That test registers inert fixture commands; it never launches an MCP server or changes your real registry.
It demonstrates observed native behavior, not a guarantee against every competing writer.

These commands connect servers and may start browser consent.
Run them yourself from a personal directory after completing setup.
Use isolated profiles for unattended connection checks:

```sh
claude mcp get context7
pi mcp list --json
```

Expect Context7 connected and Pi reporting `resolve-library-id` and `query-docs` without errors.
Connection checks do not prove successful API calls. In each fresh client session, request:

> Use Context7 to resolve React, then fetch a basic useState example using the returned library ID.
> Report failures rather than answering from memory. Do not send local files or work details.

Inspect tool results, not only the final response. Read the
[personal MCP plan](/.agents/plans/personal-mcp.md#progress) before continuing from recorded test outcomes.

## Client references

- Read [Pi MCP documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/mcp.md)
  before changing its transport or tool exposure.
- Read [Claude MCP documentation](https://code.claude.com/docs/en/mcp) before changing native registration.
- Read [Context7 setup](https://context7.com/docs/resources/all-clients)
  before changing authentication or transport.
