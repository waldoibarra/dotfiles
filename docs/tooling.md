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
| `just update-ca` | Replace managed agent copies, reconcile Pi's voice package, refresh integrations and skills; may commit and push. |
| `just hooks` | Install this checkout's hooks with hk. |
| `just lint` | Run EditorConfig, Markdown, YAML and shell checks. |
| `just lint-ec`, `just lint-md`, `just lint-yaml`, `just lint-sh` | Run one check. |
| `just lint-commit MESSAGE_FILE` | Validate the message in `MESSAGE_FILE`. |
| `just check-hooks` | Run the pre-commit hook against all files. |

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
Dotbot links the three tracked JSON settings files into `~/.pi/agent`; Pi UI changes can therefore
modify the repository. `just update-ca` uses a targeted Pi package update to install or upgrade
`pi-live-codex`. Shared instructions are linked by Dotbot; Pi discovers shared skills natively.
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
the coding-agent updater maintains its OpenCode plugin and OMP extension, and Dotbot links
Codex's hook. Actual rewriting requires those files to exist, and savings depend on the
commands used.

Read the [RTK command reference](/home/.claude/RTK.md) before inspecting RTK, and
[Agent integrations](/docs/agent-integrations.md#rtk) before changing its hooks or plugins.
Dotbot links RTK configuration to `~/Library/Application Support/rtk/` on macOS and
`~/.config/rtk/` on Linux.
