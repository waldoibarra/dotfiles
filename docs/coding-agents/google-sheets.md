# Connect personal Google Sheets

Use the local, MIT-licensed [mcp-google-sheets](https://github.com/xing5/mcp-google-sheets) server
with Pi or Claude Code. No hosted connector subscription or monthly tool allowance applies.
[Google API quotas](https://developers.google.com/workspace/sheets/api/limits) still apply.

## Before you start

The shared [MCP manifest](/home/.agents/mcp.json) launches
[`google-sheets-personal-mcp`](/home/.local/bin/google-sheets-personal-mcp).
Both agents use the same personal OAuth files; ambient Google credentials are ignored.
Read [MCP installation](/docs/coding-agents/mcp.md#apply-configuration)
before provisioning a new machine.

The launcher requires Python 3 and `uvx` on `PATH`.
It runs `mcp-google-sheets==0.6.3` with Python 3.12 and `mcp==1.30.0` over stdio.
The SDK pin prevents the import failure caused by MCP 2.x removing FastMCP.
Other transitive dependencies are not locked; run the package check before changing versions.

**Google OAuth setup is required once.** This local server opens its own browser sign-in.
Pi's `/mcp` shows connection status; native remote `/mcp login` does not authenticate this stdio server.
There is no Pipedream or Composio dependency.

## Configure Google OAuth

1. Create or select a personal project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **Google Sheets API** and **Google Drive API**.
3. Configure Google Auth Platform for **External** users.
4. Add your personal Google account as a **test user** while the app is in Testing.
5. Create an OAuth client of type **Desktop app** and download its JSON.
6. Create the private destination if it does not exist:

    ```sh
    mkdir -p ~/.config/mcp-google-sheets/personal
    chmod 700 ~/.config/mcp-google-sheets/personal
    ```

7. Move the downloaded JSON to `~/.config/mcp-google-sheets/personal/client.json`, then restrict it:

    ```sh
    chmod 600 ~/.config/mcp-google-sheets/personal/client.json
    ```

Never paste this file into chat or commit it.
A missing or malformed file stops the launcher before it starts the server.

## Sign in and verify editing

1. Start Pi in a personal directory outside `~/projects/work`.
2. Open `/mcp` and inspect `google-sheets-personal`; reconnect if it previously failed.
3. Complete the server's Google consent flow in your browser using your personal account.
4. Reconnect if the client times out during consent.
5. Ask the agent to read a small range from a disposable spreadsheet you own.
6. Explicitly authorize one cell change; confirm its value in Google Sheets.

Start Claude Code only after the first login finishes if you also want to test it.
Its existing user registration uses the same launcher and personal token.
Charting and other Google services are outside this setup task.

Treat these as separate checks:

| State | Evidence |
| --- | --- |
| Configured | The client resolves the local launcher from the shared manifest. |
| Authenticated | Google consent succeeds and the server exposes its tools. |
| Editing verified | An authorized write succeeds and its value is read back. |

Offline checks do not establish authenticated Google access or successful editing.

## Protect account access

The server requests full Sheets and Drive OAuth scopes. Its tool allowlist does not narrow those grants.
Tools expose data, formulas, tabs, writes, creation, copying, and raw batch updates.
Raw batch updates can delete data. Sharing tools are omitted; approve each requested operation's scope.
An authenticated session can access spreadsheets available to the signed-in account.

The launcher clears ambient service-account settings and prevents Application Default Credentials fallback.
It rejects startup under resolved `~/projects/work` paths, including symlinks.
This is a startup guard, not a sandbox; other work roots are unguarded.
Existing connections survive directory changes. Keep personal and work sessions separate.

Tokens live at `~/.local/state/mcp-google-sheets/personal/token.json` with private permissions.
Upstream token writes are unsynchronized; simultaneous refresh from both agents remains unverified.
External apps in Testing receive seven-day refresh tokens, except those requesting only basic identity.
Read [Google's token-expiration rules](https://developers.google.com/identity/protocols/oauth2#expiration)
before diagnosing repeated sign-in requests.

Local execution avoids an additional hosted connector processor.
Spreadsheet content returned to an agent can still reach its model provider.

## Troubleshoot

| Symptom | Action |
| --- | --- |
| Missing or invalid Desktop OAuth client configuration | Check the path printed in the error and the downloaded client type. |
| `uvx` cannot execute | Check `uvx` is installed and available on the agent's `PATH`. |
| Refusing to start under `~/projects/work` | Start a separate session in a personal directory. |
| Connection timeout during consent | Finish browser consent, then reconnect from `/mcp`. |
| Access blocked by Google | Check the consent screen, test-user list, and selected account. |
| API disabled | Enable Sheets and Drive APIs in the OAuth client's project. |
| Quota error | Reduce request frequency or follow Google's quota guidance. |

## Check or remove the integration

Run offline fixtures without authenticating:

```sh
python3 scripts/tests/test-personal-google-sheets.py
python3 scripts/tests/test-personal-mcp.py
```

The package check downloads dependencies but neither starts OAuth nor calls Google:

```sh
MCP_SHEETS_PACKAGE_CHECK=1 python3 scripts/tests/test-personal-google-sheets.py
```

To remove access, revoke the application's grant in your Google account and stop connected agent sessions.
Remove the shared manifest entry and inspect/remove its exact Claude user registration.
Removing the manifest entry alone does not remove Claude's registration.
Remove the launcher link and Dotbot declaration only when uninstalling the integration.
Delete unused private OAuth files yourself. This does not revoke Google's grant.
