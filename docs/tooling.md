# Tooling

Read this before changing package lists, running a sync or editing Git hooks.
For first installation, use [setup](/docs/setup.md).

## Sync the workstation

From an interactive terminal:

```sh
cd ~/.dotfiles
just sync
```

The `dots` alias runs this from any directory. The recipe executes:

1. `git pull`, then the [Dotbot installer](/scripts/README.md).
2. Homebrew bundle upgrade, then removal of packages absent from the global Brewfile.
3. Mise install, upgrade and prune.
4. The [coding-agent updater](coding-agents/README.md).
5. Repository Git-hook installation.

**Sync changes the machine and can publish commits.** Review local changes and package lists first.
The agent updater commits and pushes a changed skill lockfile; that push can include other unpushed
commits, which is accepted.

Agents run `dots` when a change must reach `$HOME` or the change targets the sync path itself,
and skip it otherwise. Prefer `just mise-sync`, `just update-ca` or `just hooks` when only
their domain changed. Before running `dots`, tell the user it will run as part of the work so
they can accept sudo, Touch ID or SSH prompts; run it in the background and wait for them.

## Recipes

Run recipes from the repository root. `just --list` lists them; `just` does the same.

| Command | Scope and side effects |
| --- | --- |
| `just sync` | Full workflow above. |
| `just brew` | Install/upgrade Brewfile packages, then uninstall unlisted packages. |
| `just brew-dump` | Overwrite the global Brewfile from installed packages; exclude VS Code extensions and npm packages. Review before committing. |
| `just mise-sync` | Install, upgrade and prune Mise tools. |
| `just update-ca` | Replace managed agent copies, reconcile Pi packages, refresh integrations and skills; may commit and push. |
| `just hooks` | Install this checkout's hooks with hk. |
| `just lint` | Run EditorConfig, Markdown, YAML and shell checks. |
| `just lint-ec`, `just lint-md`, `just lint-yaml`, `just lint-sh` | Run one check. |
| `just lint-commit MESSAGE_FILE` | Validate the message in `MESSAGE_FILE`. |
| `just check-hooks` | Run the pre-commit hook against all files. |
| `just pi-lens-dev [ARGS]` | Open local Pi, Lens and subagents with installed live voice; saves a session unless `--no-session` is passed. |
| `just claude-lens-dev [ARGS]` | Open Claude Code with the local Lens working tree; disables the installed plugin for the session and re-enables it on exit. |

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

Each host has one recipe. Both keep the caller's working directory, forward arguments without
re-parsing them, and never build, install, or change package declarations.

### Pi Lens

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
| Compiled Pi host | `$HOME/projects/personal/pi/packages/coding-agent/dist/bundle/cli.js` |
| Pi Lens | `$HOME/projects/personal/pi-lens/src/index.ts` |
| Subagents | `$HOME/projects/personal/pi-subagents/index.ts` |
| Installed live voice | `$HOME/.pi/agent/npm/node_modules/pi-live-codex/index.ts` |

The recipe checks those files. Prepare missing checkouts and the compiled host separately.
It uses the local compiled host, not Mise's `latest` binary.
Ordinary `pi` and `dots` remain unchanged.

Only the three named extensions load; installed Lens and other auto-discovered extensions remain disabled.
This prevents double rendering. Voice loads without opening the microphone or connecting automatically.
Start voice with `/live spruce` or use Ctrl+L for the default voice.
Read [live voice](coding-agents/pi/live-voice.md) before testing microphone and account access.
Use `--no-session` only for disposable conversations that should not persist after exit.

Sessions launched before voice was included need a new process.
`/reload` retains their original extension paths.
Keep the current conversation open and launch `just pi-lens-dev` in another terminal for voice testing.

Edit Lens or subagent source, finish the active turn, then run `/reload` in the same Pi session.
Reload replaces extensions without restarting the conversation.
Host changes require rebuilding and restarting Pi.
Use ordinary `pi` for the published package configuration.

### Claude Lens

Run `just claude-lens-dev` to load `$HOME/projects/personal/claude-lens` through `--plugin-dir`.
Pass Claude CLI arguments after the recipe name, such as `--continue`.

The recipe disables the installed `lens@claude-lens` plugin first and re-enables it when Claude
exits, so two copies never draw at once. Those are native plugin commands against the installed
settings copy; the tracked source stays enabled. The recipe assumes the normal profile, so it
re-enables the plugin even if it was disabled beforehand.

Saving a Lens file reloads the plugin in place; a save during a turn applies when the turn ends.
Expanded folds and the current view survive the reload. For a loop without a model call, run
`just test` in the Lens checkout; it drives the hooks through Claude Code's engine.
Lens clicks need the tracked `"tui": "fullscreen"` setting.
Read [Claude Lens development](https://github.com/waldoibarra/claude-lens/blob/main/docs/development.md)
before changing its hooks or releasing it.

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
Edit it to add or remove a package. `just brew` runs `brew bundle upgrade --global --quiet`, then
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
macOS may ask permission for the Markdown file type, including `.md` and `.markdown`.
The script requests a change once, then checks the effective handler before reporting success.
If it is not yet active, respond to any existing OS prompt before rerunning; do not queue repeated requests.
A successful duti exit alone does not prove the association changed.

This changes the current user's Markdown association across applications, not just Pi.
It does not change `EDITOR`, `VISUAL`, or Pi's external prompt editor.
Terminal-specific editor overrides and per-file choices can still affect a click; test a real link.

To choose another app or undo this preference, change the mapping's bundle ID and rerun the script.
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
Pi binary installation and upgrades. The `pi-live-codex` extension is a separate Pi-managed package.
Dotbot links Pi's tracked JSON preferences and subagent configuration into `~/.pi/agent`;
Pi UI changes can therefore modify the repository. `just update-ca` installs the configured
subagent pin and updates declared packages. Shared instructions and roles are linked by Dotbot;
Pi discovers shared skills natively. Read [Pi delegation](coding-agents/pi/delegation.md)
before changing the runner or role/model selection.
[Pi and live voice](coding-agents/pi/README.md) documents ownership, shortcuts, and accepted
limitations.

### OpenPencil

Homebrew owns the `openpencil` desktop cask. Mise owns `npm:@open-pencil/cli` and
`npm:@open-pencil/mcp`, both at `latest`. They upgrade independently; there is no shared version pin.

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

Use atomic conventional commits, a subject of at most 50 characters and a body explaining why.

## RTK

Homebrew installs RTK, a CLI output filter. Claude settings reference its Bash rewrite hook,
and the coding-agent updater maintains its Pi extension. Actual rewriting requires those files to
exist, and savings depend on the commands used.

Read the [RTK command reference](/home/.agents/RTK.md) before inspecting RTK, and
[Agent integrations](/docs/agent-integrations.md#rtk) before changing its hooks or plugins.
Dotbot links RTK configuration to `~/Library/Application Support/rtk/` on macOS and
`~/.config/rtk/` on Linux.
