# Obsidian

**Purpose:** Cmd+S formats human edits; agents check touched notes and vault links. Everything runs
without subscriptions or model calls.

## Setup

**Existing vault:** Open the existing `~/life/` folder as a vault in Obsidian.
No vault recreation is needed.

**Manual once:** Connect the vault to Obsidian Sync and wait until the app reports **Fully synced**.
Enable community plugins.
Enable the CLI under **Settings → General → Advanced → Command line interface**.
Read [workstation setup](setup.md) only when dotfiles or Obsidian are missing.

**Security:** Community plugins execute code with Obsidian's permissions. Review upstream before
installation or upgrades.

```sh
cd ~/.dotfiles
just obsidian-setup
```

- Installs declared tools and missing plugins; enables Markdownlint, Custom Note Width, and the
  Source-mode ruler.
- Updates owned settings, backs up replacements under `~/.local/state/obsidian-setup/backups/`, and
  preserves unrelated configuration.
- Requires the correct open vault, completed Sync, and the default `.obsidian` directory.

**Routine:** `dots` / `just sync` includes setup. Missing vaults are skipped; other setup failures
stop visibly.

**Repeat safely:** Unchanged configuration retains its bytes and timestamps.
Existing plugins are not reinstalled or unnecessarily reloaded.

**Other vault:** Use `just obsidian-setup "$HOME/other-vault"`.

## Humans and agents

**Humans:** Press **Cmd+S**, or **Ctrl+S** elsewhere. Background autosave does not format; unfixable
issues remain warnings.
Test with `#  Example`; saving should produce `# Example`.

**Ruler:** Source mode uses uniform monospace typography and a 120-column guide. Live Preview and
Reading view stay unchanged.
Tabs and wide Unicode glyphs differ from character counts; linting remains authoritative.

**Agents:** Read `~/life/coordination/collaboration.md` and `~/life/coordination/maintenance.md`
before editing.
Improve touched notes while preserving intent, facts, qualifications, safety conditions, and
unrelated changes. Then run:

```sh
cd ~/.dotfiles
just obsidian-check README.md coordination/maintenance.md
```

**Checks:** Named notes receive shared Markdown rules, a 120-character line limit, and 17 words per
sentence.
Local file links and anchors are checked vault-wide, without network requests or automatic fixes.
Verify wikilinks and block references separately. Fix touched-note defects; report unrelated
findings and unverified links.

Never shorten safety content to satisfy a word budget.
Explain preserved safety text, then put `<!-- markdownlint-disable-next-line LIFE001 -->`
immediately before its block.
Do not use exemptions to bypass ordinary prose cleanup.

**Public links:** Review URLs first, then pass selected links through Markdown stdin.
Positional URL inputs inspect fetched pages.

```sh
printf '%s\n' '<https://obsidian.md/help/cli>' |
  lychee --no-progress --exclude-all-private --max-retries 1 --timeout 15 -
```

- Never feed private, signed, authentication, unsubscribe, or action-triggering URLs into automatic
  network checks.
- Redirect destinations also need review; private-IP filtering is not a complete privacy boundary.
- Authentication, rate limits, JavaScript-only anchors, and outages can prevent verification without
  proving a broken link.
- Report checked, failed, excluded, and unverified links separately. Never claim all links work from
  an offline pass.

## Maintain

| Read before changing… | Owner |
| --- | --- |
| Tool versions | [Global Mise configuration](/home/.config/mise/config.toml) |
| Plugins or ruler activation | [Vault manifest](/home/.config/obsidian/vault.json) |
| Formatting or sentence counting | [Shared rules](/home/.config/obsidian/markdownlint.json), [sentence rule](/home/.config/obsidian/communication.cjs) |
| GUI settings | [Formatter settings](/home/.config/obsidian/markdownlint-plugin.json) |
| Provisioning, backups, or checks | [Setup script](/scripts/obsidian.py) |

- Provision each computer separately: Obsidian Sync excludes `.markdownlint.json`.
- Never track the whole `.obsidian` directory, workspace layouts, credentials, Sync state, or
  recent-file history.
- Existing plugin versions remain unchanged; review updates manually in Obsidian and retest Cmd+S.
- Removing declarations does not uninstall plugins. Remove unwanted declarations, then disable or
  uninstall components in Obsidian.
- Roll back by stopping reconciliation, restoring local backups, and reloading affected plugins.

**Verify:** Run `python3 scripts/tests/test-obsidian.py` before provisioning changed rules on both
computers.
Local setup and fixtures passed; Waldo confirmed formatting and the ruler.
Lluvia's setup passed: tools, plugins, formatter settings, and ruler activation were verified.
Cmd+S formatting and the ruler's appearance remain unverified on Lluvia's machine.
Agent requirements are instructions, not unavoidable hooks or watchers.
