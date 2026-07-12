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
| `just sync` | Full sync: Dotbot + Brew + Mise + coding agents. Safe to re-run anytime. Requires an interactive terminal — it calls `sudo -v` to cache credentials, so an AI agent must ask the user to run it rather than running it itself. |
| `just brew` | Brew bundle: dump, clean up, upgrade. |
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
Homebrew as a bootstrapping step — that is intentional.

## mise

`mise` manages developer tools and CLIs (Node, Python, shell tools, etc.). Global tool
versions are defined in [`home/.config/mise/config.toml`](/home/.config/mise/config.toml).
Project-level overrides live in [`mise.toml`](/mise.toml) at the repo root.

Always prefer `mise` over Homebrew for developer tools and CLIs.

## RTK

RTK (Rust Token Killer) is a transparent CLI proxy that filters and compresses tool output before it
reaches the coding agent, reducing token usage 60–90% on common dev operations.

Installed via Homebrew (`brew "rtk"`). It is wired into Claude Code via a hook in
`~/.claude/settings.json` and into OpenCode via a plugin — both rewrite Bash tool calls
automatically, so `git status` becomes `rtk git status` with no manual invocation needed.

The OpenCode plugin (`~/.config/opencode/plugins/rtk.ts`) is not tracked in dotfiles — it is
managed by RTK itself. `update-coding-agents.sh` runs `rtk init -g --opencode` on every
`just sync` to install or update it idempotently.

See [`home/.claude/RTK.md`](/home/.claude/RTK.md) for the full command reference.

Configuration and filter files live in `home/.config/rtk/` and are symlinked by Dotbot.
