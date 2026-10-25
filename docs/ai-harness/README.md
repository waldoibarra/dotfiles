# AI harness

Pi, Claude Code, and Cursor share policy and skills; client configuration stays native.
Worker-role support remains client-specific.
Edit tracked sources under `home/`, not installed copies.

Read [the architecture](/docs/architecture.md) before changing how configuration, project knowledge,
and shared memory connect.
Read [model and role selection](/home/.agents/references/delegation.md) before delegating in Pi,
Claude Code, or Cursor.

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
| Starting, directing, or closing an everyday agent session | [Session workflow](session-workflow.md) |
| Changing shared rules, personal instructions or Claude response styles | [Agent instructions](/docs/agent-instructions.md) |
| Understanding Pi provisioning, voice choices, or accepted limitations | [Pi and live voice](pi/README.md) |
| Configuring or verifying personal MCP servers across clients | [Personal MCP servers](mcp.md) |
| Verifying shared instruction behavior and acceptance | [Harness verification](harness-verification.md) |
| Delegating with a shared role and an explicit model | [Pi delegation](pi/delegation.md) |
| Adding, updating or checking skill discovery | [Agent skills](/docs/agent-skills.md) |
| Planning and delivering a native OpenSpec change | [OpenSpec integration](openspec.md) |
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
| `home/.config/openspec/config.json` | Linked native skills-only preferences; [OpenSpec integration](openspec.md) |
| `.agents/skills/openspec-*/` | Upstream-generated skills linked into shared discovery roots for Pi, Claude Code, and Cursor |
| `openspec/schemas/session-workflow/` | Linked native user-level schema; [workflow contract](session-workflow.md#choose-the-work-route) |
| `docs/ai-harness/session-workflow.md` | Linked to `~/.agents/references/session-workflow.md` for portable schema instructions |
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

[`home/.config/ghostwriter/soul.md`](/home/.config/ghostwriter/soul.md) owns shared writing defaults
and routes drafting by audience and purpose, not app.
Dotbot links these four files individually into `~/.config/ghostwriter/`; the directory stays real.

| Source | Scope |
| --- | --- |
| [soul.md](/home/.config/ghostwriter/soul.md) | Shared style defaults and profile selection |
| [professional.md](/home/.config/ghostwriter/professional.md) | Work communication outside DMs and social content; client-facing documents |
| [personal.md](/home/.config/ghostwriter/personal.md) | Every DM, including work-related messages, plus personal correspondence |
| [social-media.md](/home/.config/ghostwriter/social-media.md) | Social content outside DMs: bios, stories, reels, posts, captions, comments, and replies |

These audience-based names adapt Ghostwriter's surface-based convention through explicit routing
in `soul.md`.
Every DM uses `personal.md`, regardless of app or professional environment; this routing takes
precedence.
Social-media scope includes Instagram, LinkedIn, X, and other social platforms, excluding DMs.
A Slack work DM uses `personal.md`; a LinkedIn post uses `social-media.md`.
These files contain generic defaults, not learned voices for Waldo or Lluvia.
Personal examples and measured habits are excluded; the current writer's stated preferences
guide individual voice.
Person-specific profile selection remains deferred.

Private samples, evaluations, backups, and other unlisted profiles remain local.
Dotbot cleans broken Ghostwriter links pointing into this checkout.
This removes retired `bumble.md`, `slack.md`, `whatsapp.md`, and `discord.md` links without
deleting unrelated local files.
Edit repository sources; changes through installed links also change dotfiles.
Keep individual samples and learned preferences outside these shared defaults.
These profiles are publishable configuration, not private storage.
`GHOSTWRITER_HOME` overrides the default directory, bypassing these links unless it names the same
location.

Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before applying links on an
existing workstation.

## Cursor global instructions

The tracked `home/.cursor/rules/global-instructions.mdc` is a template, not an installed symlink.
Its literal `@~/.agents/AGENTS.md` marker does not currently work as a native Cursor import.
It is our script placeholder, not syntax we expect Cursor to expand.

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

Herdr's machine-specific hook stays in the installed Claude settings copy. Read
[Herdr integration](/docs/agent-integrations.md#herdr) before changing that hook.

Keep shared installation directories real, with links to individual children.
