# Personal MCP servers

Read [the harness design policy](/home/.agents/references/harness-design.md) before adding integrations.
Personal MCP definitions live in one shared source; work-only servers stay outside this setup.

## Source and scope

[`home/.agents/mcp.json`](/home/.agents/mcp.json) owns the personal server definitions.
Dotbot links it to `~/.agents/mcp.json`, Pi's `~/.pi/agent/mcp.json`, and Cursor's `~/.cursor/mcp.json`.
Pi and Cursor read that file directly; no duplicate definition is required.
Cursor's directory stays real; only its MCP configuration is linked.
Edits through either client's symlink change the tracked source.

Claude Code stores user servers in `~/.claude.json`, alongside private client state.
The [registration adapter](/scripts/update-coding-agents/sync-personal-mcp.py) derives user registrations
through `claude mcp add-json --scope user`. It never replaces that file or imports project servers.

| Server | Launch | Purpose |
| --- | --- | --- |
| `context7` | `npx -y --package=@upstash/context7-mcp@2.2.5 -- context7-mcp` | Resolve library IDs and retrieve public documentation. |
| `fireflies` | `https://api.fireflies.ai/mcp` (HTTP) | Retrieve personal meeting summaries and full transcripts through OAuth. |

Context7's pinned stdio command preserves the existing Claude configuration.
Node/npm and network access are required; `npx` downloads the pinned package if absent.
Context7 accepts unauthenticated requests but may rate-limit them.
No account or API key is provisioned.
Queries reach Context7's external service. Keep private code, company details, and secrets out of
queries.

Use the common `mcpServers` schema. Pi supports stdio and streamable HTTP, not legacy SSE.
Keep client-specific exposure settings out of the shared definition.
Never put credentials in this public repository or replace the entire Claude registry with a
symlink.
Pi commands can follow the config symlink and change tracked bytes.
Review any such changes.

Work roots, project `.mcp.json`, project `.pi/mcp.json`, and unrelated user entries are untouched.
Project servers can shadow user servers.
Verification outside work projects does not establish work parity.
Subagents do not automatically receive every MCP tool. Read [Pi delegation](pi/delegation.md)
before granting a role explicit MCP access.

## Fireflies

The official hosted server uses Streamable HTTP and account OAuth; credentials remain in each
client's native storage.

Read the [official setup](https://docs.fireflies.ai/getting-started/mcp-configuration) before
authenticating.
Read the [tool reference](https://docs.fireflies.ai/mcp-tools/overview) before retrieving meetings.

- In Pi, run `/reload`, then `/mcp login fireflies` to authorize your personal account.
- In Claude Code, restart, then use `/mcp` to authenticate Fireflies.
- Account access and plan limits apply; configuration alone proves neither authentication nor
  successful retrieval.
- Use `fireflies_get_transcripts` to find a meeting, then `fireflies_get_summary` and
  `fireflies_get_transcript` for its content.
- Save returned content explicitly; retain complete transcripts, speaker attribution, and timestamps
  without summarizing them.
- Check full tool-result artifacts when client output is truncated before claiming a complete
  export.
- Keep work recordings and NDA-restricted content outside the shared vault.
- The server also exposes write tools; retrieval approval does not authorize sharing or changing
  meetings.

**Pi verified:** Authenticated meeting discovery, summary retrieval, and transcript retrieval
succeeded in a live session.

**Still unverified:** Claude and Cursor authentication and retrieval;
exporting meeting content to local files.

## Cursor

Restart Cursor after installing the link, then inspect its MCP settings for Context7 and Fireflies.
Authorize Fireflies through Cursor's native OAuth flow; credentials remain client-local.
Verify a Context7 tool call in a fresh chat using the prompt below.
The installed link alone proves neither loading, authentication, nor successful tool calls.
Global instruction rules are separate from MCP setup.
Read [Cursor global instructions](README.md#cursor-global-instructions) before changing their template.

## Apply configuration

Read [sync boundaries](/docs/tooling.md#sync-the-workstation) before running a full workstation
sync.
Dotbot installs links; the existing updater then runs the registration adapter before Pi package
updates.
To reconcile only Claude registrations after the shared source is installed:

```sh
python3 scripts/update-coding-agents/sync-personal-mcp.py
```

The adapter targets normal home configuration, ignoring `CLAUDE_CONFIG_DIR` overrides.
Matching entries cause no writes. Claude's native command adds missing entries.
Conflicts and invalid manifest shapes stop registration.
Unrelated entries are never removed.
A later native-command failure leaves earlier successful additions intact; registration is not a
transaction.

On a conflict, inspect the exact user-scoped entry before replacing it.
After approval, remove only that entry with `claude mcp remove NAME --scope user`, then rerun the
adapter.
Removing a server from the shared manifest does not automatically delete its Claude registration.
Avoid competing changes to the same server during registration; native Claude owns registry writes.

Restart the clients after configuration changes.
In Pi, `/mcp` shows connections and `/reload` refreshes them.

## Verify

Run fixture checks from the repository root; they use disposable homes and a fake Claude executable:

```sh
python3 scripts/tests/test-personal-mcp.py
python3 scripts/tests/test-agent-harness.py
```

To additionally exercise concurrent native Claude registrations inside a disposable home:

```sh
MCP_NATIVE_CHECK=1 python3 scripts/tests/test-personal-mcp.py
```

That test registers inert fixture commands.
It never launches an MCP server or changes your real registry.
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
[personal MCP plan](/docs/plans/personal-mcp.md#progress) before continuing from recorded test
outcomes.

## Client references

- Read [Cursor MCP documentation](https://cursor.com/docs/mcp) before changing its global configuration.

- Read [Pi MCP
  documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/mcp.md)
  before changing its transport or tool exposure.
- Read [Claude MCP documentation](https://code.claude.com/docs/en/mcp) before changing native
  registration.
- Read [Context7 setup](https://context7.com/docs/resources/all-clients)
  before changing authentication or transport.
