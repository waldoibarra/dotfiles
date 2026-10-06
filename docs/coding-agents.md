# Coding agents

Edit tracked sources under `home/`. Dotbot links most files; the coding-agent updater copies
four configs. A configured link is not proof that a running agent loaded the file.

| Task | Read before acting |
| --- | --- |
| Change a global preference or determine which agent receives it | [Global instructions](#global-instructions) |
| Change Claude's output style | [Response style](#response-style) |
| Apply tracked changes | [Copy-managed files](#copy-managed-files), then [sync the workstation](/docs/tooling.md#sync-the-workstation) |
| Add or update skills | [Skill ownership](#skill-ownership) |
| Diagnose output filtering or agent-state hooks | [Integrations](#integrations) |
| Configure design tools | [UI design tools](/docs/agent-ui-design-tools.md) |
| Analyze images with a text-only model | [Image recovery skill](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) |

**Publication note:** `just update-ca`, and therefore `just sync`, can commit and push a
changed skill lockfile, publishing other unpushed commits on the branch too. Read
[Sync the workstation](/docs/tooling.md#sync-the-workstation) before running either.

## File ownership

[`install.conf.yaml`](/install.conf.yaml) defines the links. Paths below are relative to the
repository; their installed equivalents replace `home/` with `~/` unless noted.

| Tracked source | Delivery and owner |
| --- | --- |
| `home/.claude/CLAUDE.md` | Copied; Claude's global import adapter |
| `home/.claude/settings.json` | Copied; hooks, output style, permissions, status lines |
| `home/.config/opencode/AGENTS.md` | Copied for OpenCode; shared global policy |
| `home/.config/opencode/opencode.json` | Copied; OpenCode providers, plugins, MCP, permissions |
| `home/.claude/output-styles/*.md` | Linked individually; the directory stays real |
| `home/.claude/*statusline*.sh` | Linked; main and subagent status lines |
| `home/.config/opencode/tui.json` | Linked; OpenCode terminal UI settings |
| `home/.claude/RTK.md` | Linked; manually maintained RTK reference |
| `home/.config/rtk/*` | Linked to `~/Library/Application Support/rtk/` on macOS or `~/.config/rtk/` on Linux |
| `home/.agents/.skill-lock.json` | Linked; external skill sources and installer targets |
| Repo-authored skill directories | Linked individually; [ownership and destinations](#repo-managed-skills) |

### Copy-managed files

[`sync-managed-configs.sh`](/scripts/update-coding-agents/sync-managed-configs.sh) overwrites
all four copied files from their tracked sources, removing a leftover target symlink first.
They are copies, not links, so the machine-specific hook Herdr adds to the installed Claude
settings stays local; see [Herdr integration](#herdr-integration).

- Edit the repository source, not the installed copy: the next updater run discards local edits.
- Source edits reach copied files on the next updater run, not immediately.
- Keep shared installation directories real, with links to individual children. Dotbot removes
  the legacy `~/.config/opencode/skills` directory symlink before installing children.

## Global instructions

[`home/.config/opencode/AGENTS.md`](/home/.config/opencode/AGENTS.md) owns global preferences.
Keep it usable in unrelated projects. Repository-specific operating rules belong in the root
[`AGENTS.md`](/AGENTS.md).

| Agent | Global loader |
| --- | --- |
| Claude Code | Copied `~/.claude/CLAUDE.md` imports `@~/.config/opencode/AGENTS.md` |
| OpenCode | Copied `~/.config/opencode/AGENTS.md` |
| Codex | `~/.codex/AGENTS.md` links directly to the tracked source |
| Oh My Pi (`omp`) | `~/.omp/agent/AGENTS.md` links to the installed OpenCode copy |

The Claude adapter is user-level, not a repository wrapper. Keep its one-line import; edit
shared rules only in the source `AGENTS.md`. Leave `~/.codex/AGENTS.override.md` absent unless
you intend to replace Codex's global rules.

Codex is installed only to sign in to the OpenAI subscription so OpenUsage can read its auth
token. It is not used for coding; its `AGENTS.md` link exists for consistency, and its RTK hook
(see [RTK integration](#rtk-integration)) is pre-installed only in case that changes. Skills
are not configured for it.

For the default OMP profile, `~/.omp/agent/APPEND_SYSTEM.md` also links to `~/AGENTS.md`.
That personal file is machine-local and must already exist. A project append file or
`--append-system-prompt` can override it. Restart agents after changing loaded instructions;
check the active session's context rather than inferring loading from the filesystem.

### Project loading

This repository uses root `AGENTS.md` without a root `CLAUDE.md` wrapper. The user-level Claude
import above remains separate. [`.claude/settings.json`](/.claude/settings.json) excludes
`**/home/.claude/CLAUDE.md` from project discovery so the tracked global adapter is not loaded
again as local guidance.

Codex reads project instructions along the path to its working directory, so working inside
`home/.config/opencode/` can load the tracked global source again. OpenCode's `instructions`
setting is additive; no exclusion is configured here for that source. Check loaded context
when working in these directories instead of assuming all hosts deduplicate instructions.

## Response style

Claude Code defaults to `Spartan` through
[`home/.claude/settings.json`](/home/.claude/settings.json). `/output-style` selects a style;
change the tracked `outputStyle` to make a global default survive the next updater run.
Project-local style settings can override the global default.

The three tracked styles are verbatim
[Attention Span](https://github.com/alexgreensh/attention-span) copies:

| Style | Format |
| --- | --- |
| `Attention-kind` | Plain English, front-loaded, warm |
| `Spartan` | Blunt, compact arrow points |
| `Rundown` | TL;DR and status checklists |

Each retains `keep-coding-instructions: true` and upstream attribution. Compare its version
comment with [upstream releases](https://github.com/alexgreensh/attention-span/releases)
before replacing a vendored file. Preserve the
[AGPL-3.0 license](https://github.com/alexgreensh/attention-span/blob/main/LICENSE); this
repository does not relicense the copies. These selectable Claude styles are separate from
the shared global instruction source.

## Skill ownership

### Global skills lockfile

[`sync-global-skills-from-lock.sh`](/scripts/update-coding-agents/sync-global-skills-from-lock.sh)
installs missing entries from [`home/.agents/.skill-lock.json`](/home/.agents/.skill-lock.json),
then runs `npx -y skills update -g` for all installed global skills. This is an update workflow,
not a frozen reinstall of locked bytes. A changed tracked lockfile triggers a commit and push.

Keep `lastSelectedAgents` set to `opencode` and `claude-code`; these become the installer's
`-a` flags. Edit external skills in their owning source repository, not their installed copies.

**Oh My Pi (`omp`) and Pi (`pi`) are different agents.** The Skills CLI's `pi` target installs
under `~/.pi/agent/skills`; adding it does not configure OMP. OMP can discover shared
`~/.agents/skills` without another copy, subject to enabled providers, `skills.enableAgentsUser`,
and skill filters. Current [OMP discovery docs](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md)
require opting into foreign user-level providers through `enabledProviders`.

Installed, discovered, and advertised are different states. In a fresh OMP session, resolve a
skill with `skill://<name>` to check access. `disable-model-invocation: true` hides a discovered
skill from the automatic listing without disabling direct access or enabled `/skill:<name>`
commands. Resolving a skill does not exercise its workflow or external dependencies.

### Repo-managed skills

These are authored here and linked by Dotbot, not managed by the external lockfile:

| Read before… | Source |
| --- | --- |
| Writing or reviewing shell scripts | [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) |
| Building/debugging/reviewing interfaces with both behavior and layout | [`web-app-craft`](/home/.agents/skills/web-app-craft/SKILL.md) |
| Standards-first or frameworkless web work | [`web-standards`](/home/.agents/skills/web-standards/SKILL.md) |
| Isolated layout, intrinsic reflow, spacing, or overflow work | [`css-layout`](/home/.agents/skills/css-layout/SKILL.md) |
| Interpreting images with a text-only model and an available vision MCP | [`non-vision-image-reader`](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) |

The four `home/.agents/skills/` bundles link to both `~/.agents/skills/` and `~/.claude/skills/`.
[OpenCode also discovers those locations](https://opencode.ai/docs/skills). The image skill
links under `~/.config/opencode/skills/` and includes its OpenCode-specific recovery script.
Edit the tracked source: editing an installed symlink edits this checkout.

New bundles acquire links on the next Dotbot sync; source creation alone does not
install them. Check link targets and restart the host before testing discovery. Do not run a
full machine sync just to validate a skill. Maintenance scenarios live in each bundle's
`evals/evals.json` where present; format checks do not establish model or browser behavior.

## Integrations

### RTK integration

Read [`home/.claude/RTK.md`](/home/.claude/RTK.md) before using or diagnosing RTK. The shared
global instructions point to that file on demand. Claude's tracked Bash hook runs
`rtk hook claude`. The updater refreshes two untracked, RTK-generated files when their dry
run lists pending `[dry-run] would …` changes: OpenCode's plugin with `rtk init -g --opencode`,
and, when the `omp` binary exists, OMP's `~/.omp/agent/extensions/rtk.ts` with
`rtk init -g --agent omp`. Pi (`pi`) is not configured. Dry runs
always print `Nothing written`, so that line does not mean the integration is current. A failed
RTK step warns and lets the remaining updater steps run.

Codex's hook is tracked instead:
[`home/.codex/hooks.json`](/home/.codex/hooks.json) runs `rtk hook codex` and Dotbot links it
to `~/.codex/hooks.json`. Do not run `rtk init -g --codex`: it also appends an `@RTK.md`
reference to `~/.codex/AGENTS.md`, which is a link to the shared global instructions. Codex runs
a non-managed hook only after its definition is trusted through `/hooks`, once per machine and
again after any edit changes the hook's hash. Codex 0.160.1 loads the symlinked file; until it
is trusted, commands run without RTK.

The tracked RTK config enables usage tracking and telemetry, and keeps tee output for failures.
`filters.toml` contains a commented example, not an active custom filter. Neither a configured
hook nor a supported rewrite proves a live session used it.

### Herdr integration

The updater checks `herdr integration status` and installs stale/missing Claude and OpenCode
integrations when Herdr is available. The binary owns the untracked scripts/plugins. Claude's
tracked `SessionStart` hook uses `$HOME/.claude/hooks/herdr-agent-state.sh`.

Herdr installation can add an absolute-path duplicate hook to the installed settings copy.
The next updater run resets it from the tracked source. If Herdr changes the hook command,
review the installed entry and port it into the tracked `$HOME` form.

### Moshi integration

Tracked Claude settings call `'/opt/homebrew/bin/moshi-hook' claude-hook`; that command assumes
Homebrew's Apple Silicon prefix. Moshi's OpenCode plugin and daemon/LaunchAgent are machine-local,
not installed by the coding-agent updater. `moshi-hook install --target opencode` owns its plugin.
For daemon failures, inspect the actual service environment: launchd does not inherit the
interactive shell's mise PATH. Keep machine-local service configuration out of this repository.
