# Coding agents

Edit tracked sources under `home/`, not installed copies. Dotbot links most files; the coding-agent
updater copies three configs. A configured link does not prove that a running agent loaded the file.

## Choose a task

| Read before… | Guide |
| --- | --- |
| Changing shared rules, personal instructions or Claude response styles | [Agent instructions](/docs/agent-instructions.md) |
| Diagnosing differences between OMP text and live voice | [OMP live voice](/docs/omp-live-voice.md) |
| Understanding Pi provisioning, voice choices, or accepted limitations | [Pi and live voice](pi/README.md) |
| Adding, updating or checking skill discovery | [Agent skills](/docs/agent-skills.md) |
| Diagnosing RTK, Herdr or Moshi hooks and plugins, or the Lens plugin | [Agent integrations](/docs/agent-integrations.md) |
| Applying tracked config changes | [Copy-managed files](#copy-managed-files), then [Sync the workstation](/docs/tooling.md#sync-the-workstation) |
| Configuring design tools | [UI design tools](/docs/agent-ui-design-tools.md) |
| Analyzing images with a text-only model | [Image recovery skill](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) |

**Publication risk:** `just update-ca`, and therefore `just sync`, can commit and push a changed
skill lockfile, publishing other unpushed commits on the branch too. Read
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running either.

## Pi provisioning

Mise installs Pi. Dotbot links shared instructions and Pi's three JSON preference files. The updater
reconciles `pi-live-codex` in the normal profile. Changes to linked settings, including Pi UI edits,
change the repository. OMP remains available; no credentials migrate between agents.
The [Pi guides](pi/README.md) cover file ownership, voice commands, and accepted limitations.

## File ownership

[`install.conf.yaml`](/install.conf.yaml) defines the links. Paths below are repository-relative;
installed paths replace `home/` with `~/` unless noted.

| Tracked source | Delivery and purpose |
| --- | --- |
| `home/.claude/CLAUDE.md` | Copied; Claude's global import adapter |
| `home/.claude/settings.json` | Copied; hooks, output style, permissions, plugins, status lines |
| `home/.config/opencode/opencode.json` | Copied; OpenCode providers, plugins, MCP, permissions |
| `home/.claude/output-styles/*.md` | Linked individually; the directory stays real |
| `home/.claude/*statusline*.sh` | Linked; main and subagent status lines |
| `home/.claude/.shellcheckrc` | Repository-only; ShellCheck configuration for the status-line scripts |
| `home/.config/opencode/tui.json` | Linked; OpenCode terminal UI settings |
| `home/.claude/RTK.md` | Linked; manually maintained RTK reference |
| `home/.config/rtk/*` | Linked to `~/Library/Application Support/rtk/` on macOS or `~/.config/rtk/` on Linux |
| `home/.agents/.skill-lock.json` | Linked; external skill sources and installer targets |
| `home/.agents/AGENTS.md` | Linked to `~/.agents/AGENTS.md`; shared global policy |
| Repo-authored skill directories | Linked individually; [destinations](/docs/agent-skills.md#repo-managed-skills) |
| `home/.pi/agent/settings.json` | Linked; coding defaults, voice package, compaction preferences |
| `home/.pi/agent/models.json` | Linked; model context-window overrides |
| `home/.pi/agent/keybindings.json` | Linked; voice and tree-filter shortcuts |

Pi's `~/.pi/agent/AGENTS.md` links to `home/.agents/AGENTS.md`. The profile directory stays real;
only the named configuration files are linked. See [Pi configuration](pi/configuration.md#managed-files)
for the settings and their separation from private runtime files.

## Copy-managed files

[`sync-managed-configs.sh`](/scripts/update-coding-agents/sync-managed-configs.sh) overwrites the
three copied configs from tracked sources, removing leftover target symlinks first. Source edits
reach these copies on the next updater run; local edits to installed copies are discarded.

Herdr's machine-specific hook stays in the installed Claude settings copy. Read
[Herdr integration](/docs/agent-integrations.md#herdr) before changing that hook.

Keep shared installation directories real, with links to individual children. Existing OpenCode
installations must already use this layout for `~/.config/opencode/skills` before syncing.
