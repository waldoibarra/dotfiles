# Tooling

Read [setup](/docs/setup.md) before the first installation. Read this page before syncing the
workstation or changing package and tool management.

## Sync the workstation

Run a full sync in an interactive terminal, or let an agent run it with a pseudo-terminal (PTY)
while you're available to authenticate:

```sh
cd ~/.dotfiles
just sync
```

The `dots` shell alias runs the same workflow from anywhere without changing your shell's directory.
The workflow is designed to be rerun, but it changes the machine: it upgrades tools and can remove
packages. Check local changes and the tracked package lists before running it.

The recipe runs these actions in order:

1. Pull repository changes with `git pull`.
2. Run Dotbot to update links and execute the installation scripts.
3. Apply the global Brewfile: install or upgrade listed packages, then remove unlisted packages.
4. Install, upgrade, and prune Mise tools.
5. Update coding-agent configuration, integrations, and global skills.
6. Install this repository's Git hooks.

Read [Homebrew](#homebrew) before changing the package list and
[coding agents](/docs/coding-agents.md) before editing generated agent configuration.
For narrower updates, use the recipes below instead of running the full workflow.

## just

`just` is the task runner for this repo. Always use `just` recipes instead of running
underlying commands directly.

List all available recipes:

```sh
just
```

Key recipes:

| Recipe | What it does |
| --- | --- |
| `just sync` | Full workstation sync, including package removal. Requires an interactive terminal; see [Sync the workstation](#sync-the-workstation). |
| `just brew` | Apply the global Brewfile declaratively: install/upgrade what's listed, uninstall what isn't. Cask operations can invoke sudo. |
| `just mise-sync` | Sync Mise tools against the tracked configs: install missing, upgrade, prune. |
| `just update-ca` | Update coding agents: OpenCode plugin cache, RTK/Herdr integrations, global skills. |
| `just hooks` | Install this repo's Git hooks via `hk`. |
| `just brew-dump` | Capture this machine's installed packages into the global Brewfile (opt-in; commit after). |
| `just lint-sh` | Lint shell scripts with ShellCheck. |
| `just lint-md` | Lint Markdown files with markdownlint-cli2. |
| `just lint-ec` | Lint all files against `.editorconfig` rules with editorconfig-checker. |
| `just lint-yaml` | Lint YAML files with yamlfmt. |
| `just check-hooks` | Run the pre-commit hook against all files to verify hook configuration. |

### Which recipes may an AI agent run?

Agents may run `dots`, `just sync`, and `just brew` with a PTY while the user is present.
On macOS with Touch ID configured for sudo, the user can approve prompts from agent-launched
commands. Otherwise, use the workstation's configured authentication method.
Wait for authentication; a pending prompt is not a command failure.
`git pull` may also prompt for SSH credentials. Don't assume sudo credentials carry across
separate shell calls.

These commands still upgrade tools and can remove packages. Keep the checks in
[Sync the workstation](#sync-the-workstation); user-present authentication does not make the run
read-only. If the user is unavailable, defer commands that need authentication.

`just update-ca` commits and pushes when the global skill lockfile changes. `just sync`
and `dots` include that step. Obtain publication authorization before running these workflows;
the push can also publish other unpushed commits on the current branch.

Use the narrower recipes when only their domain changed:

- Changed `home/.config/mise/config.toml` or `mise.toml`? Run `just mise-sync`.
- Changed `home/.agents/.skill-lock.json`, or need to refresh the RTK/Herdr integrations or
  OpenCode's plugin cache? Run `just update-ca`.
- Changed `hk.pkl`? Run `just hooks`, then `just check-hooks`.

Anything involving Dotbot (new/renamed tracked files, symlinks) or the Brewfile still needs the
full `just sync`, with the user available to authenticate.

## hk

`hk` manages Git hooks. Hook configuration lives in [`hk.pkl`](/hk.pkl).

The `pre-commit` hook runs `lint-sh`, `lint-md`, `lint-ec`, and `lint-yaml`. The `commit-msg`
hook runs `committed` to enforce commit message format.

After any change to `hk.pkl`, run `just check-hooks` to verify the hook still passes.

## committed

`committed` enforces commit message conventions. Rules are in [`committed.toml`](/committed.toml).

Commit message format: imperative mood, present tense, no trailing period, subject ≤ 50 chars.
Use the body to explain why; use the footer for metadata (e.g. issue references).

Use `github:crate-ci/committed` in [`mise.toml`](/mise.toml) to select the native release.
Aqua's `rosetta2: true` rule selects Intel binaries on Apple Silicon and can cause
`Bad CPU type in executable`. Install it with `mise install github:crate-ci/committed`.
If your shell still uses the old path, run `mise exec -- git commit`; hooks stay enabled.

## Homebrew

Homebrew manages GUI apps and system-level packages. The global Brewfile lives at
[`home/.Brewfile`](/home/.Brewfile) and is symlinked to `~/.Brewfile`.

The committed Brewfile is the **single source of truth**. `just sync` (and `just brew`) apply it
declaratively: `brew bundle upgrade` installs missing packages and upgrades listed ones, then
`brew bundle cleanup` uninstalls anything present on the machine but absent from the Brewfile. This
is how a removal propagates — delete a line, commit, and the next `just sync` on any machine
uninstalls it.

`sync` never runs `brew bundle dump`, so it will not recapture ad-hoc local installs. To **add** a
package, either edit the Brewfile directly, or run `brew install <pkg>` followed by `just brew-dump`
to capture this machine's state; then commit. Dumping is deliberate and opt-in precisely so it can
never clobber a pulled removal.

The Brewfile also declares `mlx-audio` and `voice-mode` as `uv` tools. Mise manages
`uv` itself; the Brewfile manages these packages and `mlx-audio`'s extra dependencies,
including the `en_core_web_sm` 3.8.0 model and `setuptools<81`.

The following casks are macOS-only and have no Linux equivalent managed here yet:

- `docker-desktop`
- `ghostty`
- `obs`
- `obsidian`
- `postman`
- `visual-studio-code`
- `wezterm@nightly`
- `zen`

Never add a tool to Homebrew that Mise can manage. Note: `mise` itself is installed via
Homebrew as a bootstrapping step — that is intentional. A tool may also stay in Homebrew
when Mise's only backend for it is unmaintained, or a different implementation than the
maintained Homebrew formula, or when it belongs to a multi-binary ecosystem that Mise
cannot manage in full — keeping such an ecosystem in one manager beats letting its
versions drift apart (see [The gentle-ai ecosystem](#the-gentle-ai-ecosystem)).

`brew bundle dump` inspects the active `npm`'s globals (`npm ls -g`). mise's isolated
`npm:` tools don't appear there, but packages bundled with node (e.g. `corepack`) always
do, so `npm "corepack"` re-enters the Brewfile on every dump. It's inert (`check` stays
satisfied, `upgrade` ignores npm) — leave it rather than fight the dump cycle.

### The gentle-ai ecosystem

Three formulae come from the third-party tap `gentleman-programming/tap`:

| Formula | What it is |
| --- | --- |
| `engram` | Persistent memory for AI coding agents |
| `gentle-ai` | SDD/RDD ecosystem for AI coding agents |
| `gga` | Provider-agnostic AI code review |

They stay in Homebrew despite being developer CLIs, which normally belong in Mise. `gga` ships no
release binaries, so Mise has no backend that can manage it at all; splitting one ecosystem across
two managers would then let its three versions drift apart. Keeping all three in the Brewfile means
one `just brew` upgrades them together, and the coding-agents sync script notices when `gentle-ai`'s
version changed so its generated layer gets reviewed against the new release — see
[`docs/coding-agents.md`](/docs/coding-agents.md).

Homebrew 6 requires tap trust (`HOMEBREW_REQUIRE_TAP_TRUST` defaults to true), so each of the three
`brew` lines carries `trusted: true`. Trust is declared per formula rather than on the `tap` line:
Homebrew's own guidance is to trust only the items you need, and a per-formula grant is enough
because Homebrew trusts the entry before it loads the formula. `brew bundle cleanup --force` resets
the trust store to exactly what the Brewfile declares, so the Brewfile stays the single source of
truth for trust as well as for packages.

## mise

`mise` manages developer tools and CLIs (Node, Python, shell tools, etc.). Global tool
versions are defined in [`home/.config/mise/config.toml`](/home/.config/mise/config.toml).
Project-level overrides live in [`mise.toml`](/mise.toml) at the repo root.

Always prefer `mise` over Homebrew for developer tools and CLIs.

Like the Brewfile, the mise config is the source of truth. `just sync` (via `just mise-sync`) runs
`mise install` (add missing), `mise upgrade`, then `mise prune` (delete versions no longer
referenced by any tracked config). Removing a tool from the config de-activates it on the next shell
immediately — `mise prune` then reclaims its disk on the next sync. Note `mise prune` spans **all**
tracked configs, not just the global one; use `mise ls --prunable` or `mise prune --dry-run` if you
need to preview on a machine with project-local tool versions.

npm-backed tools whose package ships postinstall/build scripts (e.g.
`@anthropic-ai/claude-code`, whose postinstall copies the native binary) need
`allow_builds = true`. mise's `npm:` backend defaults to `--ignore-scripts=true`;
without it the postinstall is skipped and the tool installs non-functional.

`editorconfig-checker` is declared with an explicit `github:` backend. mise's default `aqua:`
backend resolves it through the aqua registry, whose asset template still expects the pre-4.0
`ec-<os>-<arch>.tar.gz` names; v4.0.0 renamed its release assets to
`editorconfig-checker-<os>-<arch>.tar.gz`, so `mise up` fails with `no asset found`. The `github:`
backend reads the release assets directly and needs no registry entry. v4 also renamed the binary
from `ec` to `editorconfig-checker`, which is what `just lint-ec` invokes.

### OpenPencil

Read this before installing or upgrading the design editor and its automation tools.

- Homebrew owns the desktop app: `cask "openpencil"` in `home/.Brewfile`.
- Global Mise owns `npm:@open-pencil/cli` and `npm:@open-pencil/mcp`, both set to
  `latest`. They upgrade independently of the Homebrew desktop app; no shared version pin
  keeps the three packages aligned.
- Node and Bun are already globally Mise-managed. The published CLI and MCP entry points
  run on Node; no source checkout, Rust build, or ad-hoc global npm install is needed.
- The MCP package exposes `openpencil-mcp` and `openpencil-mcp-http`. The desktop app
  searches Mise's shim directory for the HTTP executable. Restart the app after the first
  MCP install so it can start its local automation server.

Use `just mise-sync` for Mise changes. The portfolio's `just open-design` launches its landing
design. Use `openpencil` directly for file inspection, rendering, and editing; no CLI wrapper.
Passing a design file works headlessly; omitting it requires the running desktop MCP bridge.
Keep the bridge's default authentication enabled.

Read [Agent UI design tools](/docs/agent-ui-design-tools.md) for the tool comparison
and portfolio workflow.

Sources: [installation](https://github.com/open-pencil/open-pencil#installation),
[CLI](https://openpencil.dev/reference/cli),
[MCP](https://openpencil.dev/programmable/mcp-server).

## RTK

RTK (Rust Token Killer) is a transparent CLI proxy that filters and compresses tool output before it
reaches the coding agent, reducing token usage 60–90% on common dev operations.

Installed via Homebrew (`brew "rtk"`). It is wired into Claude Code via a hook in
`~/.claude/settings.json` and into OpenCode via a plugin — both rewrite Bash tool calls
automatically, so `git status` becomes `rtk git status` with no manual invocation needed.

The OpenCode plugin (`~/.config/opencode/plugins/rtk.ts`) is not tracked in dotfiles — it is
managed by RTK itself. `update-coding-agents/entrypoint.sh` runs `rtk init -g --opencode` on every
`just sync` to install or update it idempotently.

See [`home/.claude/RTK.md`](/home/.claude/RTK.md) for the full command reference.

Configuration and filter files live in `home/.config/rtk/` and are symlinked by Dotbot.
