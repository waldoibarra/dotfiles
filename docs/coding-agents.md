# Coding agents

Edit tracked sources under `home/`, not installed copies. Dotbot links most files; the coding-agent
updater copies three configs. A configured link does not prove that a running agent loaded the file.

## Choose a task

| Read before… | Guide |
| --- | --- |
| Changing shared rules, personal instructions or Claude response styles | [Agent instructions](/docs/agent-instructions.md) |
| Diagnosing differences between OMP text and live voice | [OMP live voice](/docs/omp-live-voice.md) |
| Adding, updating or checking skill discovery | [Agent skills](/docs/agent-skills.md) |
| Diagnosing RTK, Herdr or Moshi hooks and plugins | [Agent integrations](/docs/agent-integrations.md) |
| Applying tracked config changes | [Copy-managed files](#copy-managed-files), then [Sync the workstation](/docs/tooling.md#sync-the-workstation) |
| Configuring design tools | [UI design tools](/docs/agent-ui-design-tools.md) |
| Analyzing images with a text-only model | [Image recovery skill](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) |

**Publication risk:** `just update-ca`, and therefore `just sync`, can commit and push a changed
skill lockfile, publishing other unpushed commits on the branch too. Read
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running either.

## File ownership

[`install.conf.yaml`](/install.conf.yaml) defines the links. Paths below are repository-relative;
installed paths replace `home/` with `~/` unless noted.

| Tracked source | Delivery and purpose |
| --- | --- |
| `home/.claude/CLAUDE.md` | Copied; Claude's global import adapter |
| `home/.claude/settings.json` | Copied; hooks, output style, permissions, status lines |
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

## Copy-managed files

[`sync-managed-configs.sh`](/scripts/update-coding-agents/sync-managed-configs.sh) overwrites the
three copied configs from tracked sources, removing leftover target symlinks first. Source edits
reach these copies on the next updater run; local edits to installed copies are discarded.

Herdr's machine-specific hook stays in the installed Claude settings copy. Read
[Herdr integration](/docs/agent-integrations.md#herdr) before changing that hook.

Keep shared installation directories real, with links to individual children. Existing OpenCode
installations must already use this layout for `~/.config/opencode/skills` before syncing.
