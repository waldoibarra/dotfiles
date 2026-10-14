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

| Read before… | Guide |
| --- | --- |
| Changing shared rules, personal instructions or Claude response styles | [Agent instructions](/docs/agent-instructions.md) |
| Understanding Pi provisioning, voice choices, or accepted limitations | [Pi and live voice](pi/README.md) |
| Configuring or verifying personal MCP servers across clients | [Personal MCP servers](mcp.md) |
| Connecting personal Sheets or troubleshooting Google sign-in | [Google Sheets setup](google-sheets.md) |
| Verifying shared instruction behavior and acceptance | [Harness verification](personal-workflow.md) |
| Delegating with a shared role and an explicit model | [Pi delegation](pi/delegation.md) |
| Adding, updating or checking skill discovery | [Agent skills](/docs/agent-skills.md) |
| Diagnosing RTK, Herdr or Moshi hooks and plugins, or the Lens plugin | [Agent integrations](/docs/agent-integrations.md) |
| Applying tracked config changes | [Copy-managed files](#copy-managed-files), then [Sync the workstation](/docs/tooling.md#sync-the-workstation) |
| Configuring design tools | [UI design tools](/docs/agent-ui-design-tools.md) |

**Publication risk:** `just update-ca`, and therefore `just sync`, can commit and push a changed
skill lockfile, publishing other unpushed commits on the branch too. Read
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running either.

## Pi provisioning

Mise installs Pi and keeps its binary on `latest`. Dotbot links shared instructions, roles, Pi
preferences, and runner configuration. The updater installs the pinned runner and updates declared
packages, including Git sources, in the normal profile. Changes to linked settings, including Pi UI
edits, change the repository. Per-machine credentials, sessions, package caches, and native installs
remain outside dotfiles. The [Pi guides](pi/README.md) cover file ownership, voice commands, and
accepted limitations.

## File ownership

[`install.conf.yaml`](/install.conf.yaml) defines the links. Paths below are repository-relative;
installed paths replace `home/` with `~/` unless noted.

| Tracked source | Delivery and purpose |
| --- | --- |
| `home/.claude/CLAUDE.md` | Copied; Claude's global import adapter |
| `home/.claude/settings.json` | Copied; hooks, output style, permissions, plugins, status lines |
| `home/.agents/roles/*.md` | Linked individually to `~/.agents/roles/` and `~/.claude/agents/`; [shared roles](/docs/agent-instructions.md#shared-role-agents) |
| `home/.claude/output-styles/*.md` | Linked individually; the directory stays real |
| `home/.claude/*statusline*.sh` | Linked; main and subagent status lines |
| `home/.claude/.shellcheckrc` | Repository-only; ShellCheck configuration for the status-line scripts |
| `home/.agents/RTK.md` | Linked to `~/.agents/RTK.md` and `~/.claude/RTK.md`; shared RTK reference |
| `home/.config/rtk/*` | Linked to `~/Library/Application Support/rtk/` on macOS or `~/.config/rtk/` on Linux |
| `home/.agents/.skill-lock.json` | Linked; external skill sources and installer targets |
| `home/.agents/AGENTS.md` | Linked to `~/.agents/AGENTS.md`; global policy and reading map |
| `home/.agents/references/*.md` | Linked individually to `~/.agents/references/`; shared on-demand detail |
| `home/.agents/mcp.json` | Shared personal MCP definitions; Pi link and derived Claude user registrations |
| Repo-authored skill directories | Linked individually; [destinations](/docs/agent-skills.md#repo-managed-skills) |
| `home/.pi/agent/settings.json` | Linked; coding defaults, packages, role overrides, compaction preferences |
| `home/.pi/agent/extensions/subagent/config.json` | Linked; minimal Pi runner configuration |
| `home/.pi/agent/models.json` | Linked; model context-window overrides |
| `home/.pi/agent/keybindings.json` | Linked; voice and tree-filter shortcuts |

Pi's `~/.pi/agent/AGENTS.md` links to `home/.agents/AGENTS.md`. The profile directory stays real;
only the named configuration files are linked. See [Pi
configuration](pi/configuration.md#managed-files)
for the settings and their separation from private runtime files.

## Copy-managed files

[`sync-managed-configs.sh`](/scripts/update-coding-agents/sync-managed-configs.sh) overwrites the
two copied configs from tracked sources, removing leftover target symlinks first. Source edits
reach these copies on the next updater run; local edits to installed copies are discarded.

Herdr's machine-specific hook stays in the installed Claude settings copy. Read
[Herdr integration](/docs/agent-integrations.md#herdr) before changing that hook.

Keep shared installation directories real, with links to individual children.
