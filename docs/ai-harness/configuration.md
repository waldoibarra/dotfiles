# Harness configuration and delivery

**Edit tracked sources, not installed copies or generated files.**
Dotbot links most configuration; the updater copies Claude settings and renders Cursor instructions.
Credentials, identities, signing keys, sessions, and machine-local overrides stay outside this
repository.

Read [workstation sync](/docs/tooling.md#sync-the-workstation) before applying changes to `$HOME`.
Read [Pi configuration](pi/configuration.md) for Pi-specific settings and runtime files.
Read [personal MCP servers](mcp.md) for shared definitions and Claude registration.

## File ownership

[`install.conf.yaml`](/install.conf.yaml) defines the links. Paths below are repository-relative;
installed paths replace `home/` with `~/` unless noted.

| Tracked source | Delivery and purpose |
| --- | --- |
| `home/.cursor/rules/global-instructions.mdc` | Template; updater renders a regular Cursor rule file |
| `home/.claude/settings.json` | Copied; hooks, output style, permissions, plugins, status lines |
| `home/.agents/roles/*.md` | Linked individually to `~/.agents/roles/` and `~/.claude/agents/`; [shared roles](/docs/agent-instructions.md#shared-role-agents) |
| `home/.claude/output-styles/*.md` | Linked individually; the directory stays real |
| `home/.claude/*statusline*.sh` | Linked; main and subagent status lines |
| `home/.claude/.shellcheckrc` | Repository-only; ShellCheck configuration for the status-line scripts |
| `home/.agents/RTK.md` | Linked to `~/.agents/RTK.md` and `~/.claude/RTK.md`; shared RTK reference |
| `home/.config/rtk/*` | Linked to `~/Library/Application Support/rtk/` on macOS or `~/.config/rtk/` on Linux |
| `home/.agents/.skill-lock.json` | Linked; external skill sources and installer targets |
| `home/.agents/AGENTS.md` | Linked to `~/.agents/AGENTS.md`, `~/.claude/CLAUDE.md`, `~/.pi/agent/AGENTS.md`, and `~/.codex/AGENTS.md`; global policy and reading map |
| `home/.agents/references/*.md` | Linked individually to `~/.agents/references/`; shared on-demand detail |
| `home/.config/openspec/config.json` | Linked native skills-only preferences; [OpenSpec integration](openspec.md) |
| `.agents/skills/openspec-*/` | Upstream-generated skills linked into shared discovery roots for Pi, Claude Code, and Cursor |
| `openspec/schemas/session-workflow/` | Linked native user-level schema; [workflow contract](session-workflow.md#choose-the-work-route) |
| `docs/ai-harness/session-workflow.md` | Linked to `~/.agents/references/session-workflow.md` for portable schema instructions |
| `home/.agents/mcp.json` | Shared personal MCP definitions; Pi and Cursor links, plus derived Claude user registrations |
| Repo-authored skill directories | Linked individually; [destinations](/docs/agent-skills.md#repo-managed-skills) |
| `home/.pi/agent/` configuration files | Individually linked; [Pi managed files](pi/configuration.md#managed-files) owns the complete inventory |

Keep shared installation directories real, with links to individual children.
Pi's [managed-file reference](pi/configuration.md#managed-files) separates linked preferences from
private runtime files.

## Cursor global instructions

The tracked `home/.cursor/rules/global-instructions.mdc` is a template, not an installed symlink.
Its literal `@~/.agents/AGENTS.md` marker is a renderer placeholder, not a native import.

During `dots` (`just sync`), the coding-agent updater runs
[`sync-cursor-rule.sh`](/scripts/update-coding-agents/sync-cursor-rule.sh).
It replaces that marker with the actual bytes from `~/.agents/AGENTS.md`.
The result is a regular `~/.cursor/rules/global-instructions.mdc` file with its frontmatter
preserved.
Only this exact marker is expanded; references inside the instructions are not recursively included.

The renderer atomically replaces old symlinks without modifying their targets.
Matching bytes and permissions leave the installed file untouched; generated files use mode `0644`.
Missing inputs or an invalid marker count fail before replacing the installed rule.
Edit the tracked template or shared instructions; installed rule edits are overwritten on sync.
Instruction edits reach Cursor on the next render, not immediately through a symlink.

To refresh only this rule without package updates or publication:

```sh
bash scripts/update-coding-agents/sync-cursor-rule.sh
```

Restart Cursor afterward. File generation does not verify fresh-session instruction loading.
Run `python3 scripts/tests/test-cursor-rule.py` for isolated rendering and migration checks.

## Claude model defaults

The tracked `home/.claude/settings.json` selects the `opus` alias and `medium` default effort.
`effortLevel` applies when the model has no saved effort setting.
Per-model settings, higher-precedence configuration, and explicit session overrides can change the
effective effort.
Read [Claude effort settings](https://code.claude.com/docs/en/settings-reference#effortlevel)
before changing these defaults.
The managed-config sync below delivers the tracked settings to the installed user copy.

## Copy-managed files

[`sync-managed-configs.sh`](/scripts/update-coding-agents/sync-managed-configs.sh) overwrites the
Claude settings from the tracked source, removing a leftover settings symlink first.
Source edits reach this copy on the next updater run; local settings edits are discarded.
Dotbot owns Claude's global instruction symlink; the updater does not replace it.

Herdr's installer can add a machine-specific hook after the managed copy is refreshed.
The next refresh discards that local addition before integration reconciliation.
Read [Herdr integration](/docs/agent-integrations.md#herdr) before changing that hook.
