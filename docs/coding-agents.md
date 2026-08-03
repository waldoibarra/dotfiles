# Coding Agents

This is a dotfiles repo — its primary purpose is managing configuration files for the current
machine. The global configuration files for Claude Code and OpenCode are tracked here and symlinked
into `$HOME` via DotBot, the same way every other dotfile is — except for the four **copied** files
noted below, which gentle-ai rewrites in place (see [gentle-ai](#gentle-ai)).

## Tracked files

| Tool | Repo path | `$HOME` path |
| --- | --- | --- |
| Claude Code | `home/.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` (copied, not symlinked) |
| Claude Code | `home/.claude/settings.json` | `~/.claude/settings.json` (copied, not symlinked) |
| Claude Code | `home/.claude/statusline-lib.sh` | `~/.claude/statusline-lib.sh` |
| Claude Code | `home/.claude/statusline.sh` | `~/.claude/statusline.sh` |
| Claude Code | `home/.claude/subagent-statusline.sh` | `~/.claude/subagent-statusline.sh` |
| OpenCode | `home/.config/opencode/AGENTS.md` | `~/.config/opencode/AGENTS.md` (copied, not symlinked) |
| OpenCode | `home/.config/opencode/opencode.json` | `~/.config/opencode/opencode.json` (copied, not symlinked) |
| OpenCode | `home/.config/opencode/tui.json` | `~/.config/opencode/tui.json` |
| RTK | `home/.claude/RTK.md` | `~/.claude/RTK.md` |
| RTK | `home/.config/rtk/config.toml` | `~/Library/Application Support/rtk/config.toml` (macOS), `~/.config/rtk/config.toml` (Linux) |
| RTK | `home/.config/rtk/filters.toml` | same pattern as `config.toml` |

## RTK integration

`RTK.md` is placed in `~/.claude/` by `rtk init -g` because RTK injects context only into Claude
Code. Both `CLAUDE.md` and `AGENTS.md` reference `~/.claude/RTK.md` directly, so OpenCode also
benefits from the same file without duplicating it.

`RTK.md` is maintained manually — its content may diverge from what `rtk init -g` generates by
default.

The OpenCode plugin (`~/.config/opencode/plugins/rtk.ts`) is intentionally not tracked in the
table above. RTK embeds the plugin at compile time and is the authoritative source for the correct
version. It is installed and kept current by `rtk init -g --opencode`, which runs automatically
via `update-coding-agents/entrypoint.sh` on every `just sync`.

## Herdr integration

Herdr (terminal workspace manager) shows per-agent state through integrations installed by
`herdr integration install <name>`. Two are in use:

- **OpenCode** — a plugin at `~/.config/opencode/plugins/herdr-agent-state.js`. Intentionally
  untracked, like the RTK plugin: the herdr binary embeds it and is the authoritative source for
  the correct version. `update-coding-agents/entrypoint.sh` installs or refreshes it on every
  `just sync`, skipping when `herdr integration status` reports it current.
- **Claude Code** — a `SessionStart` hook entry in the tracked
  [`home/.claude/settings.json`](/home/.claude/settings.json) plus an untracked script at
  `~/.claude/hooks/herdr-agent-state.sh`. The hook command is kept in portable `$HOME` form;
  `herdr integration status` versions only the script file, so it reports `current` with the
  portable entry in place, and `update-coding-agents/entrypoint.sh` only reinstalls when it does
  not. Because `herdr integration install claude` detects its hook by exact absolute-path command
  string, an install re-adds a machine-specific duplicate hook entry. That used to land in this
  repo, since `~/.claude/settings.json` was a symlink to the tracked file — hence the old
  dirty-check-and-`git restore` dance, now removed. `~/.claude/settings.json` is a copy since
  gentle-ai landed (see [gentle-ai](#gentle-ai)), so the duplicate only ever reaches that copy and
  the next `dots` run clobbers it back to the tracked form. Caveat: if a Herdr release ever changes
  the hook **command** (not just the script), the tracked entry goes stale silently — reinstall
  manually and port the new command into `$HOME` form here.

## gentle-ai

[gentle-ai](https://github.com/Gentleman-Programming/gentle-ai) is an SDD/RDD ecosystem for coding
agents, installed from Homebrew together with `engram` and `gga` — see
[`docs/tooling.md`](/docs/tooling.md). `gentle-ai sync` generates agents, commands, skills and
prompts for both Claude Code and OpenCode. `scripts/update-coding-agents/sync-gentle-ai-assets.sh`
runs it on every `just sync` and then reduces what it produced to what this machine actually wants.

### Copy-managed files

`gentle-ai sync` **aborts** when a target file is a symlink, and it rewrites all four of these:

- `home/.claude/CLAUDE.md`
- `home/.claude/settings.json`
- `home/.config/opencode/AGENTS.md`
- `home/.config/opencode/opencode.json`

So Dotbot no longer links them (they are `exclude`d from its globs in
[`install.conf.yaml`](/install.conf.yaml)); the sync script copies the repo source over the `$HOME`
target instead, dropping any leftover symlink first. That copy is also the **garbage collector**:
`gentle-ai sync` only ever adds marker sections, it never prunes them, so every run has to start
from the tracked bytes.

Consequences:

- Editing a repo source still propagates — on the next `dots` run, not instantly.
- **Never edit those four files under `$HOME`.** The next sync clobbers them without asking.
- `~/.config/opencode/skills` is a real directory now, with one symlink per repo skill. gentle-ai
  writes ~20 generated skill directories in there; as a directory symlink it would have written
  them straight into this repo. The sync script refuses to run while it is still a symlink.
- The Herdr Claude hook step can no longer dirty the repo's `settings.json`, because `$HOME`'s copy
  is a different file now. Any absolute-path duplicate hook Herdr adds lives in that copy until the
  next `dots` run clobbers it — see [Herdr integration](#herdr-integration).

### The machine-local generated layer

Everything below is written by `gentle-ai sync` and **not tracked** — it is regenerated from the
installed `gentle-ai` version on every sync, so there is nothing to commit and nothing to review:

| Path | Contents |
| --- | --- |
| `~/.claude/{agents,commands,skills,output-styles,mcp}/` | `sdd-*`, `review-*`, `jd-*` agents, slash commands, skills, the engram MCP entry |
| `~/.claude/agents/gentle-orchestrator.md` | Built by the sync script, see below |
| `~/.claude.json` | Merged, not replaced |
| `~/.config/opencode/{prompts,commands,plugins,skills}/` | The OpenCode half of the same layer |
| `~/.config/gga/` | `gga` review configuration |
| `~/.gentle-ai/` | `state.json`, backups, and the version stamp the sync script keeps |

### Marker map

`gentle-ai sync` injects `<!-- gentle-ai:NAME --> … <!-- /gentle-ai:NAME -->` blocks into the two
global memory files. The sync script asserts this exact inventory, then strips most of it back out:

| File | Section | Kept? | Why |
| --- | --- | --- | --- |
| `~/.claude/CLAUDE.md` | `persona` | stripped | Conflicts with the tracked persona in `AGENTS.md` |
| `~/.claude/CLAUDE.md` | `engram-protocol` | stripped | Already reaches Claude Code through the `@`-import of `AGENTS.md` |
| `~/.claude/CLAUDE.md` | `sdd-orchestrator` | stripped | Moved into the `gentle-orchestrator` agent, so it arrives as that agent's prompt instead of as global memory |
| `~/.claude/CLAUDE.md` | `agent-routing` | stripped | Same |
| `~/.config/opencode/AGENTS.md` | `persona` | stripped | Conflicts with the tracked persona directly above it |
| `~/.config/opencode/AGENTS.md` | `engram-protocol` | **kept** | The one section that has to be ambient: it governs when to write memory |

`CLAUDE.md` therefore ends up as just its one-line `@`-import again, and `AGENTS.md` keeps only the
engram protocol. What that costs depends on which agent the session starts as:

| Session | Ambient cost | Made of |
| --- | --- | --- |
| Stock gentle-ai, no stripping | ~10,950 tokens | persona + engram + orchestrator + routing, with engram and persona duplicated across both files |
| Default session here (`gentle-orchestrator`) | ~7,500 tokens | the orchestrator prompt (~5,800) + engram (~1,700), each exactly once |
| Session on any other agent | ~1,700 tokens | engram only |

So the orchestrator prompt is **not** free in a default session — `gentle-orchestrator` is the
global default (see below), so every default session carries it. The win is that nothing is
duplicated and nothing is loaded twice: ~30% below stock even in the most expensive case, and
~85% below it whenever a session runs on another agent or a sub-agent.

### The gentle-orchestrator agent

`~/.claude/agents/gentle-orchestrator.md` is **regenerated on every sync** from the
`sdd-orchestrator` and `agent-routing` sections, before they are stripped. It is a plain sub-agent
definition: `model: fable`, and deliberately **no `tools` key**, so it inherits every tool including
`Agent` — without which it could not delegate at all.

It is the global default agent, via `"agent": "gentle-orchestrator"` in
[`home/.claude/settings.json`](/home/.claude/settings.json), so every default session starts on
Fable in orchestration mode. To opt out of a session, start with `claude --agent <other>`; to switch
models inside a session, use `/model`.

### Model assignments

`gentle-ai` reads `claude_phase_assignments` from `~/.gentle-ai/state.json` to set the `model:`
frontmatter of the generated `~/.claude/agents/sdd-*.md`. The sync script seeds it **only when the
key is absent**, so anything changed later through gentle-ai's TUI survives every sync:

| Phase | Model | Why |
| --- | --- | --- |
| `sdd-propose`, `sdd-design` | `opus` | Architect phases — the decisions are expensive to get wrong |
| `sdd-apply`, `sdd-tasks` | `sonnet` | Implementation phases — volume work against a settled design |

Valid models are `fable`, `opus`, `sonnet` and `haiku`, with an optional `"effort"` of `low`,
`medium`, `high`, `xhigh` or `max`. OpenCode's generated agents carry no model of their own: they
inherit whatever model is selected in OpenCode (GLM at the moment). Per-phase OpenCode splits are
possible later through `gentle-ai sync --profile` / `--profile-phase`.

### Update procedure when gentle-ai changes structure

Everything above is pinned to one upstream shape. Two things make a change visible instead of
silent:

- The **marker assertion** fails the sync, naming the unexpected or missing section.
- The **version stamp** (`~/.gentle-ai/.dotfiles-last-synced-version`) prints a prominent notice the
  first time a new `gentle-ai` version is synced, even when the markers still match.

When either fires:

1. Sync a scratch `$HOME` so the real one is not touched, and keep using that same `$HOME` for
    step 2 — the real `~/.claude/CLAUDE.md` is the already-stripped 30-byte file and would show
    nothing:

    ```sh
    export GA_CHECK=/tmp/ga-check && mkdir -p "$GA_CHECK"
    HOME="$GA_CHECK" gentle-ai sync --agent claude-code,opencode \
      --sdd-mode multi --sdd-profile-strategy generated-multi
    ```

2. List the section names it wrote — one line per section, per file:

    ```sh
    grep -oh 'gentle-ai:[a-z-]*' "$GA_CHECK"/.claude/CLAUDE.md \
      "$GA_CHECK"/.config/opencode/AGENTS.md | sort -u
    ```

3. Compare against `CLAUDE_MEMORY_MARKERS` and `OPENCODE_MEMORY_MARKERS` in
    [`sync-gentle-ai-assets.sh`](/scripts/update-coding-agents/sync-gentle-ai-assets.sh).
4. Update those lists, then the `*_STRIPPED_MARKERS` lists and the two
    `extract_marker_section` calls in `build_orchestrator_agent` that feed the agent prompt.
5. Re-run `just update-ca` and confirm the assertion passes.

### RDD is machine-local

Receipt-driven development installs **no Git hooks**. The gates are `gentle-ai review …` CLI
commands, and their receipts and state live in the repo's `.git` common directory — untracked,
per-clone, and invisible to anyone who does not run them.

Per-repo one-time setup, in the repo you want it in:

```sh
gentle-ai review mode enable --cwd .   # opt this clone into RDD
gentle-ai skill-registry refresh       # write .atl/skill-registry.md
gga init                               # provider-agnostic review config
```

Then `/sdd-init` inside Claude Code to scaffold the SDD artifacts. `skill-registry refresh` also
runs automatically on every prompt, via the `UserPromptSubmit` hook in
[`home/.claude/settings.json`](/home/.claude/settings.json) — that hook is exactly what
`gentle-ai sync` would otherwise add itself, so keeping it tracked makes sync's `settings.json`
write a no-op.

That hook runs in **every** repo, and `--no-gitignore` (required for the settings no-op) means it
writes `.atl/skill-registry.md` and `.atl/.skill-registry.cache.json` without ignoring them itself.
`.atl/` is therefore ignored in two places: this repo's own
[`.gitignore`](/.gitignore), and the tracked global ignore file
[`home/.config/git/ignore`](/home/.config/git/ignore) which covers every other repo — see
[`docs/git-configuration.md`](/docs/git-configuration.md).

### Rollback

1. Delete the four `gentleman-programming/tap` lines from [`home/.Brewfile`](/home/.Brewfile).
2. Delete `scripts/update-coding-agents/sync-gentle-ai-assets.sh` and its `source` line and
    `main()` call in `entrypoint.sh`.
3. Drop the `exclude:` lists and the `~/.config/opencode/skills/` link entry from
    [`install.conf.yaml`](/install.conf.yaml), and the shell step that removes the old symlink.
4. Remove `"agent": "gentle-orchestrator"` and the `UserPromptSubmit` hook from
    [`home/.claude/settings.json`](/home/.claude/settings.json).
5. Delete the four `$HOME` copies and run `just sync`; Dotbot re-links them, `brew bundle cleanup`
    uninstalls the three formulae, and `rm -rf ~/.gentle-ai ~/.config/gga` clears the rest.

## Global skills lockfile

`scripts/update-coding-agents/sync-global-skills-from-lock.sh` keeps globally installed Claude Code
/ OpenCode skills in sync with [`home/.agents/.skill-lock.json`](/home/.agents/.skill-lock.json): it
installs any skill listed there that isn't already present, runs `npx skills update -g` to update
all of them, then **commits and pushes the lockfile to the repo's remote** if the update changed its
content. It runs automatically via `update-coding-agents/entrypoint.sh` on every `just sync`.

## Repo-managed skills

Most global skills are installed and pinned by the lockfile (see [Global skills
lockfile](#global-skills-lockfile)). Two skills are instead **authored as source**
in the repo and edited here directly — never installed, never in the lockfile:

| Skill | Repo source | Symlinked to |
| --- | --- | --- |
| [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) | `home/.agents/skills/shell-scripting` | `~/.agents/skills/` **and** `~/.claude/skills/` (shared source via two Dotbot globs) |
| [`non-vision-image-reader`](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) | `home/.config/opencode/skills/non-vision-image-reader` | `~/.config/opencode/skills/` (opencode global skills) |

Dotbot relinks these on every `just sync`, so edits in the repo are picked up
once the tool reloads its config (restart opencode / Claude Code). Because they
are symlink targets, **never edit them under `~/.agents/skills/`,
`~/.claude/skills/`, or `~/.config/opencode/skills/`** — always edit the repo
source under `home/`.

## Global instructions

[`AGENTS.md`](/home/.config/opencode/AGENTS.md) is the single source of truth for global
instructions. [`CLAUDE.md`](/home/.claude/CLAUDE.md) is a one-line `@`-import of it:

```md
@~/.config/opencode/AGENTS.md
```

This is the [pattern Claude Code recommends](https://code.claude.com/docs/en/memory.md#import-additional-files)
for repos that keep instructions in `AGENTS.md`. Edit `AGENTS.md` only — `CLAUDE.md` auto-imports
it, so there is nothing to mirror.

## Local project instructions

Like any other repo, this dotfiles repo has its own local agent instruction files:

- [`AGENTS.md`](/AGENTS.md) — the source of truth for both tools, committed to the repo.
- [`CLAUDE.md`](/CLAUDE.md) — a committed file that uses Claude Code's `@`-include syntax (`@AGENTS.md`)
  to pull in the full content of `AGENTS.md` at load time.

Claude Code picks up `CLAUDE.md` (which includes `AGENTS.md` via `@`).
OpenCode picks up `AGENTS.md` directly. `AGENTS.md` remains the single source of truth.

## Preventing double-injection of global instruction files

The global instruction files tracked in this repo —
[`home/.claude/CLAUDE.md`](/home/.claude/CLAUDE.md) and
[`home/.config/opencode/AGENTS.md`](/home/.config/opencode/AGENTS.md) — live
inside the project tree. Without exclusion, both tools load them **twice**: once
as the global instruction file (via the symlink to `$HOME`) and again as a
project-level file discovered by traversing the repo.

### Claude Code

Claude Code solves this with `claudeMdExcludes` in the project-level
[`.claude/settings.json`](/.claude/settings.json):

```json
{
  "claudeMdExcludes": [
    "**/home/.claude/CLAUDE.md"
  ]
}
```

This prevents the global `CLAUDE.md` source file from being injected as a
project-level instruction when working in this repo.

### OpenCode

OpenCode has **no equivalent** of `claudeMdExcludes`. The `instructions` field in
`opencode.json` is additive only — it cannot suppress the default `AGENTS.md`
discovery. Feature requests have been filed repeatedly and consistently closed as
"not planned" ([#17990](https://github.com/anomalyco/opencode/issues/17990),
[#31697](https://github.com/anomalyco/opencode/issues/31697)); community PRs to
implement exclusion
([#17980](https://github.com/anomalyco/opencode/pull/17980),
[#20784](https://github.com/anomalyco/opencode/pull/20784)) were abandoned.

Until an exclusion mechanism lands upstream, `home/.config/opencode/AGENTS.md`
will be double-injected when working in this repo. A potential workaround would
be a plugin using the `experimental.chat.system.transform` hook to strip the
duplicate at runtime, but this has not been implemented.

## How symlinks are managed

Dotbot uses glob patterns in `install.conf.yaml` to symlink every file inside each directory:

```yaml
~/.claude/:
  glob: true
  path: home/.claude/*
  exclude:
    - home/.claude/CLAUDE.md
    - home/.claude/settings.json
~/.config/opencode/:
  glob: true
  path: home/.config/opencode/*
  exclude:
    - home/.config/opencode/AGENTS.md
    - home/.config/opencode/opencode.json
    - home/.config/opencode/skills
~/.config/opencode/skills/:
  glob: true
  path: home/.config/opencode/skills/*
```

Any new file added to `home/.claude/` or `home/.config/opencode/` will be automatically symlinked
on the next `just sync`. The excluded entries are the gentle-ai-managed ones — they are copied by
the sync script instead, see [gentle-ai](#gentle-ai).
