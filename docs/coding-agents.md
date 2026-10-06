# Coding agents

Edit tracked sources under `home/`. Dotbot links most files; the coding-agent updater copies
four configs and adds a machine-local generated layer. A configured link is not proof that a
running agent loaded the file.

| Task | Read before acting |
| --- | --- |
| Change a global preference or determine which agent receives it | [Global instructions](#global-instructions) |
| Change Claude's output style | [Response style](#response-style) |
| Apply tracked changes | [Copy-managed files](#copy-managed-files), then [sync the workstation](/docs/tooling.md#sync-the-workstation) |
| Repair generated prompts, agents, or memory tools | [gentle-ai](#gentle-ai) |
| Add or update skills | [Skill ownership](#skill-ownership) |
| Diagnose output filtering or agent-state hooks | [Integrations](#integrations) |
| Configure design tools | [UI design tools](/docs/agent-ui-design-tools.md) |
| Analyze images with a text-only model | [Image recovery skill](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) |

**Publication warning:** `just update-ca`, and therefore `just sync`, can commit and push a
changed skill lockfile. That push can publish other unpushed commits on the branch. Obtain
publication authorization before running either; neither is a read-only validation command.

## File ownership

[`install.conf.yaml`](/install.conf.yaml) defines the links. Paths below are relative to the
repository; their installed equivalents replace `home/` with `~/` unless noted.

| Tracked source | Delivery and owner |
| --- | --- |
| `home/.claude/CLAUDE.md` | Copied; Claude's global import adapter |
| `home/.claude/settings.json` | Copied; hooks, default agent, output style, permissions, status lines |
| `home/.config/opencode/AGENTS.md` | Copied for OpenCode; shared global policy |
| `home/.config/opencode/opencode.json` | Copied; OpenCode providers, plugins, MCP, permissions |
| `home/.claude/output-styles/*.md` | Linked individually; directory also holds generated styles |
| `home/.claude/*statusline*.sh` | Linked; main and subagent status lines |
| `home/.config/opencode/tui.json` | Linked; OpenCode terminal UI settings |
| `home/.claude/RTK.md` | Linked; manually maintained RTK reference |
| `home/.config/rtk/*` | Linked to `~/Library/Application Support/rtk/` on macOS or `~/.config/rtk/` on Linux |
| `home/.agents/.skill-lock.json` | Linked; external skill sources and installer targets |
| Repo-authored skill directories | Linked individually; [ownership and destinations](#repo-managed-skills) |

### Copy-managed files

[`sync-gentle-ai-assets.sh`](/scripts/update-coding-agents/sync-gentle-ai-assets.sh) overwrites
all four copied files from their tracked sources before generating anything. It removes a
leftover target symlink first. This delivery step runs even if `gentle-ai` is absent.

- Edit the repository source, not the installed copy: the next updater run discards local edits.
- Source edits reach copied files on the next updater run, not immediately.
- Keep shared installation directories real, with links to individual children. In particular,
  the updater rejects a symlinked `~/.config/opencode/skills` directory; Dotbot removes that
  legacy link before installing children.
- Do not add a tracked `home/.claude/agents/` directory. The parent glob would link it and send
  generated agent writes into this checkout.

## Global instructions

[`home/.config/opencode/AGENTS.md`](/home/.config/opencode/AGENTS.md) owns global preferences.
Keep it usable in unrelated projects. Repository-specific operating rules belong in the root
[`AGENTS.md`](/AGENTS.md).

| Agent | Global loader | Receives generated Engram protocol? |
| --- | --- | --- |
| Claude Code | Copied `~/.claude/CLAUDE.md` imports `@~/.config/opencode/AGENTS.md` | Yes, through the installed OpenCode copy |
| OpenCode | Copied `~/.config/opencode/AGENTS.md` | Yes |
| Codex | `~/.codex/AGENTS.md` links directly to the tracked source | No |
| Oh My Pi (`omp`) | `~/.omp/agent/AGENTS.md` links to the installed OpenCode copy | Yes |

The Claude adapter is user-level, not a repository wrapper. Keep its one-line import; edit
shared rules only in the source `AGENTS.md`. Leave `~/.codex/AGENTS.override.md` absent unless
you intend to replace Codex's global rules. This updater targets Claude Code and OpenCode;
adding another target requires checking whether it rewrites a currently linked file.

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
The updater restores that value after gentle-ai applies its own style. Project-local style
settings can override the global default.

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

## gentle-ai

The updater runs `gentle-ai sync --agent claude-code,opencode` with
`--opencode-background-subagents=auto`, automatic consent, and self-update disabled. It then
checks generated sections, builds the Claude orchestrator, strips non-ambient sections,
restores the tracked style, and repairs owned agents' Engram tool names.

### Generated files

Generated assets stay machine-local. Inspect them when debugging; change their owning
configuration or generator for a durable fix.

| Location | Owner |
| --- | --- |
| `~/.claude/{agents,commands,skills,output-styles}/` | gentle-ai assets; skills and output styles share directories with tracked links |
| `~/.claude/agents/gentle-orchestrator.md` | This repository's updater |
| `~/.claude/agents/.gentle-ai-native-agent-ownership.json` | gentle-ai ownership ledger; updater records repaired hashes |
| `~/.claude.json` | User configuration merged by gentle-ai, including `mcpServers.engram` |
| `~/.config/opencode/{prompts,commands,plugins,skills}/` | OpenCode generated assets; directories can also contain other integrations |
| `~/.gentle-ai/` | State, backups, and `.dotfiles-last-synced-version` |
| `~/.config/gga/` | Machine-local review configuration |

### Marker map

The script expects this inventory of `<!-- gentle-ai:NAME -->` sections. Missing, unexpected,
empty, duplicate, unbalanced, or misnested sections fail the sync before extraction/stripping.

| File | Section | Policy |
| --- | --- | --- |
| Claude `CLAUDE.md` | `persona` | Strip; retain tracked global policy |
| Claude `CLAUDE.md` | `engram-protocol` | Strip duplicate; import the OpenCode copy |
| Claude `CLAUDE.md` | `orchestrator`, `agent-routing` | Extract into `gentle-orchestrator`, then strip |
| Claude `CLAUDE.md` | `remote-authorization` | Preserve inside extracted `agent-routing`; strip with its parent |
| OpenCode `AGENTS.md` | `persona` | Strip; retain tracked global policy |
| OpenCode `AGENTS.md` | `engram-protocol` | Keep ambient |

Do not copy the generated Engram protocol into the tracked source or edit its installed body
as a permanent fix. The tracked source owns user preferences; gentle-ai owns that protocol.

### Orchestrator and memory tools

`gentle-orchestrator` combines the generated Organic Driven Development (ODD) orchestration
and routing sections, including receipt-driven development (RDD) guidance. The script checks
required role and ODD headings before writing it. It sets `model: fable` and omits a `tools`
key so the agent inherits tools, including delegation. Tracked Claude settings select it as
the default. Use `claude --agent <name>` to select another installed agent at startup;
inspect generated definitions for their models rather than relying on retired SDD profiles.

Claude's plain `engram` MCP server uses `mcp__engram__*`. The updater replaces generated
`mcp__plugin_engram_engram__*` declarations only in regular agent files whose SHA256 matches
the native ownership ledger, directly or after reversing a prior repair. It records the new
hash so upstream still recognizes the file as owned. Unknown, user-edited, and symlinked
agents remain untouched; the local orchestrator is not adopted into upstream ownership.
Remaining `mcp__plugin_*` declarations produce a warning and require inspection.

Restart Claude before checking a repaired agent's available memory tools; agent definitions
are loaded at startup. `claude mcp list` checks server connectivity, not each subagent's tool
allowlist. An `engram:reachable` warning from `gentle-ai doctor` concerns its HTTP probe, not
proof of failure in the MCP stdio setup.

### Update procedure when gentle-ai changes structure

A version notice or marker/prompt assertion failure requires review of the generated shape,
not removal of the assertion.

1. Inspect the installed `gentle-ai sync --help` and upstream changes. Generate scratch assets
    only with authorization, in a disposable home with any config/data overrides also isolated.
    Use the same two agent targets and background-subagent policy as the updater. OpenCode
    detection and any required plugin SDK setup still apply; do not bypass a skipped target.
2. Compare the scratch memory files with `CLAUDE_MEMORY_MARKERS` and
    `OPENCODE_MEMORY_MARKERS` in the script. Review authorization text as well as section names.
3. Update the marker inventories, stripped-marker lists, and extraction/prompt assertions
    together when upstream's contract changes. Preserve the ownership-checked memory repair.
4. Validate against isolated generated files. After publication authorization, run the normal
    updater and inspect loaded instructions, the selected style, and memory tools in new sessions.

A raw `gentle-ai sync` or TUI sync can restore stripped sections and replace the output style
in installed copies. To reapply this repository's policy, use the normal updater only after
accounting for its lockfile commit/push behavior.

### Enable receipt-driven review

Read `gentle-ai review --help` before changing review gates. To opt only the current clone into
RDD, use an explicit scope:

```sh
gentle-ai review mode enable --scope clone --cwd .
gentle-ai skill-registry refresh
gga init
```

The mode command defaults to **global** scope when `--scope` is omitted. RDD gates are CLI
commands, not Git hooks; clone receipts/state are untracked. ODD does not require an SDD scaffold.

The tracked Claude `UserPromptSubmit` hook refreshes the skill registry in every project with
`--quiet --no-gitignore`. It can write `.atl/skill-registry.md` and its cache without adding
ignore rules. This repository and the tracked global Git ignore exclude `.atl/`; see
[Git configuration](/docs/git-configuration.md).

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

New bundles acquire links on the next authorized Dotbot sync; source creation alone does not
install them. Check link targets and restart the host before testing discovery. Do not run a
full machine sync just to validate a skill. Maintenance scenarios live in each bundle's
`evals/evals.json` where present; format checks do not establish model or browser behavior.

## Integrations

### RTK integration

Read [`home/.claude/RTK.md`](/home/.claude/RTK.md) before using or diagnosing RTK. The shared
global instructions point to that file on demand. Claude's tracked Bash hook runs
`rtk hook claude`; the updater refreshes OpenCode's untracked plugin with
`rtk init -g --opencode`, unless its dry run reports `Nothing written`.

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
