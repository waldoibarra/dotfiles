# Tooling

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
| `just sync` | Full sync: Dotbot + Brew + Mise + coding agents. Safe to re-run anytime. May require an interactive terminal (sudo prompts when scripts need changes), so an AI agent must ask the user to run it rather than running it itself. |
| `just brew` | Apply the global Brewfile declaratively: install/upgrade what's listed, uninstall what isn't. |
| `just brew-dump` | Capture this machine's installed packages into the global Brewfile (opt-in; commit after). |
| `just lint-sh` | Lint shell scripts with ShellCheck. |
| `just lint-md` | Lint Markdown files with markdownlint-cli2. |
| `just lint-ec` | Lint all files against `.editorconfig` rules with editorconfig-checker. |
| `just lint-yaml` | Lint YAML files with yamlfmt. |
| `just check-hooks` | Run the pre-commit hook against all files to verify hook configuration. |

## hk

`hk` manages Git hooks. Hook configuration lives in [`hk.pkl`](/hk.pkl).

The `pre-commit` hook runs `lint-sh`, `lint-md`, `lint-ec`, and `lint-yaml`. The `commit-msg`
hook runs `committed` to enforce commit message format.

After any change to `hk.pkl`, run `just check-hooks` to verify the hook still passes.

## committed

`committed` enforces commit message conventions. Rules are in [`committed.toml`](/committed.toml).

Commit message format: imperative mood, present tense, no trailing period, subject ≤ 50 chars.
Use the body to explain why; use the footer for metadata (e.g. issue references).

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
maintained Homebrew formula.

`brew bundle dump` inspects the active `npm`'s globals (`npm ls -g`). mise's isolated
`npm:` tools don't appear there, but packages bundled with node (e.g. `corepack`) always
do, so `npm "corepack"` re-enters the Brewfile on every dump. It's inert (`check` stays
satisfied, `upgrade` ignores npm) — leave it rather than fight the dump cycle.

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
