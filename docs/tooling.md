# Tooling

Read this before changing package lists, running a sync or editing Git hooks.
Read [workstation setup](/docs/setup.md) before first installation.

## Sync the workstation

From an interactive terminal:

```sh
cd ~/.dotfiles
just sync
```

The `dots` alias runs this from any directory. The recipe executes:

1. `git pull`, then [Dotbot bootstrap](/scripts/README.md), installing missing Brew packages
without requesting upgrades.
2. Upgrade Brew-owned Mise, then run remaining Brew upgrades alongside Mise install, upgrade and
  prune.
3. Wait for both updates, then remove packages absent from the global Brewfile.
4. [Obsidian setup](obsidian.md) for an existing life vault: tools, plugins, owned settings, and
ruler.
5. The [coding-agent updater](coding-agents/README.md).
6. Repository Git-hook installation.

**Sync changes the machine and can publish commits.** Review local changes and package lists first.
The agent updater commits and pushes changed skill lockfiles.
That push can include other unpushed commits, which is accepted.

Agents run `dots` only when a change must reach `$HOME` or targets the sync path.
Prefer `just mise-sync`, `just update-ca`, or `just hooks` for narrower changes.
Before running `dots`, tell the user it will run during the work.
Allow time for sudo, Touch ID, or SSH prompts; run it in the background and wait.

### Read package-update output

`just packages-sync` coordinates three phases within `dots`:

1. Upgrade the **Mise executable** through Brew before running Mise-managed tools.
This prevents Brew from replacing Mise during its tool updates.
2. Start remaining Brew upgrades and Mise tool installation, upgrades, and pruning concurrently.
3. Wait for both jobs to succeed, then run Brewfile cleanup.

Only the concurrent jobs receive `[brew]` and `[mise]` prefixes.
The executable update and final cleanup remain unprefixed.
Brew output therefore appears before and after parallel work.

Illustrative output; lines from the two jobs can arrive in either order:

```text
Updating the Mise executable before parallel tool updates.
Syncing Brew and Mise in parallel; cleanup waits for both.
[brew] Starting updates.
[mise] Starting updates.
[brew] brew bundle upgrade --global
[mise] mise install --yes
[mise] mise upgrade --yes
```

Each label includes that job's stdout and stderr, including errors, in one combined stream.
Brew runs without `--quiet`.
Carriage-return progress updates become separate lines instead of overwriting previous output.
Lines appear when tools flush their output; quiet gaps do not prove sequential execution.
`[mise] Finished syncing Mise tools.` means that job finished, not that the entire sync succeeded.

### Sequential mode and recovery

For dependency-sensitive source builds, keep package updates sequential:

```sh
DOTS_SEQUENTIAL=1 just sync
```

Brew can replace libraries or build tools used by Mise backends during parallel updates.
Sequential mode runs the complete Brew cycle before Mise tools.
It does not add output labels.
Missing Brew-owned Mise also selects sequential mode.
The coordinator prints `Syncing Brew and Mise sequentially.`

A failed Brew probe stops the sync; it does not assume Mise is absent.

A preflight failure prevents parallel jobs from starting.
If either parallel job fails, the coordinator waits for the other.
It then fails without running Brewfile cleanup.
Later sync steps do not run. Successful package changes are not rolled back.
Fix the reported error before retrying `just packages-sync` or the full `dots` workflow.
Ctrl+C terminates the coordinator's subprocess groups; it does not undo completed updates.

### Bootstrap versus updates

The installer checks Brewfile packages with `--no-upgrade`.
It uses that flag when installing missing packages too.
Homebrew can still upgrade dependencies required by a missing package.
During `dots`, `DOTS_DEFER_MISE_INSTALL=1` leaves Mise tools for the coordinator
after trusting the configuration.
This variable is scoped to the installer invocation; do not export it for first-time setup.
Standalone installation remains sequential and installs Mise tools, including `just`.
Read [first-time setup](setup.md) before bootstrapping packages.

## Recipes

Run recipes from the repository root. `just --list` lists them; `just` does the same.

| Command | Scope and side effects |
| --- | --- |
| `just sync` | Full workflow above. |
| `just packages-sync` | Coordinate Brew and Mise updates, then remove unlisted Brew packages. |
| `just brew` | Install/upgrade Brewfile packages, then uninstall unlisted packages. |
| `just brew-dump` | Overwrite the global Brewfile from installed packages; exclude VS Code extensions and npm packages. Review before committing. |
| `just mise-sync` | Install, upgrade and prune Mise tools. |
| `just update-ca` | Replace managed agent copies, reconcile Pi packages, refresh integrations and skills; may commit and push. |
| `just hooks` | Install this checkout's hooks with hk. |
| `just obsidian-setup [VAULT]` | Install declared tools/plugins and apply owned settings/ruler; see [Obsidian](obsidian.md). |
| `just obsidian-sync` | Same reconciliation for `~/life/`; skip when the vault is absent. |
| `just obsidian-check FILE...` | Check touched life-vault notes and all local links; no fixes or network requests. |
| `just lint` | Run EditorConfig, Markdown, YAML and shell checks. |
| `just lint-ec`, `just lint-md`, `just lint-yaml`, `just lint-sh` | Run one check. |
| `just lint-commit MESSAGE_FILE` | Validate the message in `MESSAGE_FILE`. |
| `just check-hooks` | Run the pre-commit hook against all files. |
| `just pi-lens-dev [ARGS]` | Open local Pi, Lens and subagents with installed live voice; saves a session unless `--no-session` is passed. |

Use the narrow recipe for the changed domain. Link changes require the Dotbot installer; they do
not inherently require package upgrades or publication. Review its
[side effects](/scripts/README.md) before running it directly.
There is no application build or repository test recipe. Smoke-test changed provisioning in an
isolated environment.

Markdown discovery respects Git ignores, so `just lint-md` skips tracked shared skills under
`home/.agents/`. Check each edited skill document through stdin to bypass file discovery:

```sh
markdownlint-cli2 - < home/.agents/skills/shell-scripting/SKILL.md
```

Verbatim upstream guides and output styles are intentionally exempt from house Markdown rules.
The saved media-spike evidence collection is exempt from EditorConfig checks to preserve output
formatting and manifest checksums. Research Markdown under `.agents/` still receives Markdown and
EditorConfig checks, with variable indentation for numbered-list continuations.

## Develop Lens locally

The recipe keeps the caller's working directory and forwards arguments without re-parsing them.
It never builds, installs, or changes package declarations.

From this checkout, run `just pi-lens-dev` to use the local sources shown below.
The recipe uses Pi's normal session persistence by default.
Pass Pi CLI arguments after the recipe name, including `--continue` or explicit `--no-session`.
`--continue` selects the latest saved session for that directory, including ordinary Pi sessions.
Use `--session` for a specific saved session; previous ephemeral sessions cannot be resumed.

To keep another project's working directory, invoke it there with:

```sh
just --justfile "$HOME/.dotfiles/justfile" pi-lens-dev --continue
```

| Component | Required file |
| --- | --- |
| Compiled Pi host | `$HOME/projects/open-source/pi/packages/coding-agent/dist/bundle/cli.js` |
| Pi Lens | `$HOME/projects/open-source/pi-lens/src/index.ts` |
| Subagents | `$HOME/projects/open-source/pi-subagents/index.ts` |
| Installed live voice | `$HOME/.pi/agent/npm/node_modules/pi-live-codex/index.ts` |

The recipe checks those files. Prepare missing checkouts and the compiled host separately.
It uses the local compiled host, not Mise's `latest` binary.
Ordinary `pi` and `dots` remain unchanged.

Only the three named extensions load; installed Lens and other auto-discovered extensions remain
disabled.
This prevents double rendering. Voice loads without opening the microphone or connecting
automatically.
Start voice with `/live spruce` or use Ctrl+L for the default voice.
Read [live voice](coding-agents/pi/live-voice.md) before testing microphone and account access.
Use `--no-session` only for disposable conversations that should not persist after exit.

Sessions launched before voice was included need a new process.
`/reload` retains their original extension paths.
Keep the current conversation open and launch `just pi-lens-dev` in another terminal for voice
testing.

Edit Lens or subagent source, finish the active turn, then run `/reload` in the same Pi session.
Reload replaces extensions without restarting the conversation.
Host changes require rebuilding and restarting Pi.
Use ordinary `pi` for the published package configuration.

## Editor defaults

[.editorconfig.global](/.editorconfig.global) is linked to `~/.editorconfig` by Dotbot.
It supplies UTF-8, LF, final newlines, trimmed trailing whitespace, two-space indentation,
and a 100-character line-length setting.

EditorConfig-aware tools inherit these defaults for files beneath `$HOME`.
A closer `.editorconfig` can override properties; `root = true` stops ancestor lookup.
Projects outside `$HOME` do not inherit this file. Property support depends on the editor;
`max_line_length` is not universally enforced.

Keep shared defaults here; add project configuration only for exceptions or portable team rules.
This repository retains its own `.editorconfig` for file-specific exceptions.
The global source has a distinct filename so it cannot override those exceptions within `home/`.

## Homebrew

[`home/.Brewfile`](/home/.Brewfile), linked to `~/.Brewfile`, owns system packages and desktop apps.
Edit it to add or remove a package. `just brew` runs `brew bundle upgrade --global`, then
`brew bundle cleanup --global --force`; removing a declaration can uninstall the package.

`just sync` never dumps installed packages back into the file. `just brew-dump` is an explicit
snapshot of this machine, not a merge of shared intent.

Prefer Mise for development CLIs. Homebrew bootstraps Mise and owns system-level tools. The
Moshi tap declares `trusted: true` on its tap entry.

The cask declarations are macOS-specific and have no Linux guards. Review the Brewfile itself for
its current app list instead of treating Debian support as feature parity.

## Default applications on macOS

Read this before changing which app opens local Markdown links.
[`home/.config/duti/markdown.duti`](/home/.config/duti/markdown.duti) selects Cursor for the
Markdown file type. Dotbot links the single mapping into `~/.config/duti/markdown.duti`.
Homebrew owns `duti`; the installer applies the mapping after OS packages are installed.

The [application script](/scripts/configure-markdown-app.sh) skips non-macOS systems and
unavailable applications. It queries LaunchServices without launching the app.
Missing configuration, missing `duti`, and query/setter errors fail visibly.
If the current handler cannot be queried, the script stops without submitting a change.
The installer supplies the supported Apple Silicon Homebrew PATH for fresh-machine setup.

Apply only this setting from the repository root, then inspect the registered handler:

```sh
PATH="/opt/homebrew/bin:$PATH" ./scripts/configure-markdown-app.sh
duti -x md
```

Expect Cursor's name, application path, and bundle ID.
Already-correct state is a no-op: the script does not submit another change request.

macOS may ask permission for Markdown files, including `.md` and `.markdown`.

The script requests a change once.
It checks the effective handler before reporting success.
If the handler is not active, respond to any existing OS prompt before rerunning.
Do not queue repeated requests.
A successful duti exit alone does not prove the association changed.

This changes the current user's Markdown association across applications, not just Pi.
It does not change `EDITOR`, `VISUAL`, or Pi's external prompt editor.
Terminal-specific editor overrides and per-file choices can still affect a click; test a real link.

To choose another app, change the mapping's bundle ID and rerun the script.
Use the same process to undo this preference.
An OS-only manual change will be overwritten by the next installer run.
Keep the desired mapping in Git; never copy the machine's LaunchServices database into dotfiles.

## Mise

[`home/.config/mise/config.toml`](/home/.config/mise/config.toml) owns global development tools;
[`mise.toml`](/mise.toml) adds this repository's checks. Most versions follow `latest`; Node follows
`lts`, and Python includes both `latest` and `3.12`. This setup is not version-pinned end to end.

`just mise-sync` runs `mise install --yes`, `mise upgrade --yes` and `mise prune --yes`.
Pruning considers Mise's tracked configurations, including other projects. Preview removals with:

```sh
mise prune --dry-run
```

Keep these backend choices unless the underlying constraint changes:

- Claude Code's npm entry sets `allow_builds = true` so its installation scripts can run.
- `editorconfig-checker` uses the explicit GitHub backend and the `editorconfig-checker` binary,
  not the old `ec` name.
- `committed` uses the GitHub backend for native release selection. If a shell retains an old
  incompatible executable path, use `mise exec -- git commit` to run with the managed tools.

### Pi

Mise owns `npm:@earendil-works/pi-coding-agent = "latest"`, so `just mise-sync` and `dots` include
Pi binary installation and upgrades.
The `pi-live-codex` extension is a separate Pi-managed package.
Dotbot links Pi's tracked JSON preferences and subagent configuration into `~/.pi/agent`.
Pi UI changes can therefore modify the repository. `just update-ca` installs the configured
subagent pin and updates declared packages. Shared instructions and roles are linked by Dotbot;
Pi discovers shared skills natively.
Read [Pi delegation](coding-agents/pi/delegation.md) before changing the runner or role/model
selection.
[Pi and live voice](coding-agents/pi/README.md) documents ownership, shortcuts, and accepted
limitations.

### OpenPencil

Homebrew owns the `openpencil` desktop cask. Mise owns `npm:@open-pencil/cli` and
`npm:@open-pencil/mcp`, both at `latest`. They upgrade independently; there is no shared version
pin.

Read [Agent UI design tools](/docs/agent-ui-design-tools.md) before using the CLI or desktop bridge.

## Git hooks

[`hk.pkl`](/hk.pkl) defines pre-commit checks for shell, Markdown, EditorConfig and YAML.
File globs select shell, Markdown and YAML checks; EditorConfig has no file-type filter.
The commit-message hook runs `committed` with [conventional-commit rules](/committed.toml).

After changing hook configuration:

```sh
just hooks
just check-hooks
```

**Owner:** Read the [commit skill](/home/.agents/skills/commit/SKILL.md) before preparing commits or
authorized pushes.
The checked-in [commit rules](/committed.toml) remain the executable message contract.

## RTK

Homebrew installs RTK, a CLI output filter. Claude settings reference its Bash rewrite hook,
and the coding-agent updater maintains its Pi extension. Actual rewriting requires those files to
exist, and savings depend on the commands used.

Read the [RTK command reference](/home/.agents/RTK.md) before inspecting RTK, and
[Agent integrations](/docs/agent-integrations.md#rtk) before changing its hooks or plugins.
Dotbot links RTK configuration to `~/Library/Application Support/rtk/` on macOS and
`~/.config/rtk/` on Linux.
