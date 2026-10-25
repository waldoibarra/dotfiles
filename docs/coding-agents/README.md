# Coding agents

Pi and Claude Code share policy, skills, and worker roles; client configuration stays native.
Edit tracked sources under `home/`, not installed copies.

## Understand the layers

| Layer | Responsibility |
| --- | --- |
| Global instructions | Universal boundaries and a task-based reading map for every session. |
| Shared references | Conditional communication, orchestration, and integration detail. |
| Skills | Specialist workflows and their bundled references. |
| Roles | Worker responsibilities; the main session retains decisions and Git writes. |
| Native configuration | Client settings, hooks, packages, credentials, and runtime state. |

Read [Agent instructions](/docs/agent-instructions.md) before changing policy ownership or loading
behavior.
These guides own workstation maintenance; runtime instructions never depend on the checkout's
location.

## Choose a task

Read [Write effective AI prompts](/docs/prompting.md) before drafting prompts or refining unhelpful
responses.

| Read before… | Guide |
| --- | --- |
| Changing shared rules, personal instructions or Claude response styles | [Agent instructions](/docs/agent-instructions.md) |
| Understanding Pi provisioning, voice choices, or accepted limitations | [Pi and live voice](pi/README.md) |
| Configuring or verifying personal MCP servers across clients | [Personal MCP servers](mcp.md) |
| Verifying shared instruction behavior and acceptance | [Harness verification](personal-workflow.md) |
| Delegating with a shared role and an explicit model | [Pi delegation](pi/delegation.md) |
| Adding, updating or checking skill discovery | [Agent skills](/docs/agent-skills.md) |
| Diagnosing RTK, Herdr or Moshi hooks and plugins, or the Pi Lens package | [Agent integrations](/docs/agent-integrations.md) |
| Applying tracked config changes | [Copy-managed files](#copy-managed-files), then [Sync the workstation](/docs/tooling.md#sync-the-workstation) |
| Configuring design tools | [UI design tools](/docs/agent-ui-design-tools.md) |
| Changing a behavior the work harness shares | [Work harness parity](work-parity.md) |

**Publication risk:** `just update-ca`, and therefore `just sync`, can commit and push a changed
skill lockfile, publishing other unpushed commits on the branch too. Read
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running either.

## Pi provisioning

Mise installs Pi and keeps its binary on `latest`. Dotbot links shared instructions, roles, Pi
preferences, and runner configuration. The updater installs the latest runner and updates declared
packages, including Git sources, in the normal profile. Changes to linked settings, including Pi UI
edits, change the repository. Per-machine credentials, sessions, package caches, and native installs
remain outside dotfiles. The [Pi guides](pi/README.md) cover file ownership, voice commands, and
accepted limitations.

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
| `.agents/plans/ai-harness-roadmap.md` | Linked to `~/.agents/harness-roadmap.md`; personal priorities, read on demand |
| `home/.agents/mcp.json` | Shared personal MCP definitions; Pi and Cursor links, plus derived Claude user registrations |
| Repo-authored skill directories | Linked individually; [destinations](/docs/agent-skills.md#repo-managed-skills) |
| `home/.pi/agent/settings.json` | Linked; coding defaults, packages, role overrides, compaction preferences |
| `home/.pi/agent/extensions/subagent/config.json` | Linked; minimal Pi runner configuration |
| `home/.pi/agent/models.json` | Linked; model context-window overrides |
| `home/.pi/agent/keybindings.json` | Linked; voice and tree-filter shortcuts |

Pi's `~/.pi/agent/AGENTS.md` links to `home/.agents/AGENTS.md`. The profile directory stays real;
only the named configuration files are linked. See [Pi
configuration](pi/configuration.md#managed-files)
for the settings and their separation from private runtime files.

## Ghostwriter voice

[`home/.config/ghostwriter/soul.md`](/home/.config/ghostwriter/soul.md) owns the initial personal
voice preferences.
Dotbot links only this file into `~/.config/ghostwriter/`; the directory stays real.
Platform profiles, private samples, evaluations, and backups remain local unless explicitly added to
dotfiles.

Edit the repository source when refining the shared baseline. Profile edits through the installed
link also change dotfiles.
Review excerpts and learned preferences before committing; this profile is publishable
configuration, not private storage.
`GHOSTWRITER_HOME` overrides the default directory, bypassing this link unless it names the same
location.

Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before applying the link on an
existing workstation.

## Cursor global instructions

The tracked `home/.cursor/rules/global-instructions.mdc` is a template, not an installed symlink.
Its literal `@~/.agents/AGENTS.md` marker does not currently work as a native Cursor import.
It is our script placeholder, not syntax we expect Cursor to expand.

During `dots` (`just sync`), the coding-agent updater runs
[`sync-cursor-rule.sh`](/scripts/update-coding-agents/sync-cursor-rule.sh).
It replaces that marker with the actual bytes from `~/.agents/AGENTS.md`.
The result is a regular `~/.cursor/rules/global-instructions.mdc` file with its frontmatter preserved.
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

Herdr's machine-specific hook stays in the installed Claude settings copy. Read
[Herdr integration](/docs/agent-integrations.md#herdr) before changing that hook.

Keep shared installation directories real, with links to individual children.
