# AI Instructions for dotfiles

## Architecture Overview

Shared dotfiles for macOS (primary) and Debian Linux (partial).

The [`home/`](/home/) directory mirrors `$HOME`. Dotbot manages links according to
[`install.conf.yaml`](/install.conf.yaml); the coding-agent updater copies selected configs
and generates machine-local assets.

## Conventions

### Shared and local configuration

- Edit repo-managed configuration under `home/`, then apply it through the owning installer or
  sync script. Direct edits to installed copies are overwritten; edits through symlinks change
  the shared source.
- Keep identities, signing keys, credentials, nicknames, backups, and session records outside
  the repository. Use the documented local overrides, such as `~/.gitconfig.local`,
  `~/.zprofile.local`, and `~/.zlogin.local`. User-authorized local setup and generated-state
  maintenance may write directly to `$HOME`.
- **Don't hardcode absolute home paths** in tracked files. Use `$HOME`, `~` where the tool
  expands it, or the tool's native home-directory mechanism. Check changed files for
  machine-specific paths before committing; external tools can write them through symlinks.
  Repository URLs and public usernames in URLs are not filesystem paths.

### Decisions and commits

- Ask when a consequential choice remains unresolved, such as destructive scope, publication,
  or a shared default that changes other users' behavior. Proceed with already-authorized work.
- **Atomic commits.** One concern per commit.
- If a change affects documented behavior, update the relevant docs in the same commit,
  including this file when its execution rules change.

## Execution and validation

Run recipes from the repository root. Read [tooling](/docs/tooling.md) before running a
mutating recipe; not requiring sudo does not make a command read-only.

| Command | Purpose and side effects |
| --- | --- |
| `just --list` | List available recipes. |
| `just lint` | Run EditorConfig, Markdown, YAML, and shell checks. |
| `just lint-sh` / `just lint-md` / `just lint-yaml` / `just lint-ec` | Run the relevant check during targeted iteration. |
| `just sync` | Pull changes, apply Dotbot, upgrade/remove packages and tools, update agents, and install hooks. Includes `update-ca` publication behavior below. |
| `just brew` | Install/upgrade listed packages and remove unlisted packages. |
| `just mise-sync` | Install, upgrade, and prune tools. |
| `just update-ca` | Rewrite agent configuration and update global skills; a changed skill lockfile triggers a commit and push. |
| `just hooks` | Install Git hooks for this checkout. |

Agents may run authorized `just sync` and `just brew` workflows with a PTY and the user
available to authenticate. Wait for Touch ID or other configured authentication.
**Obtain publication authorization before running `just update-ca` or `just sync`:**
the updater can commit and push, and a push can publish other unpushed commits on the branch.
Do not use these workflows as read-only validation.

There is no repository-level application build or test recipe. For behavioral changes,
exercise the affected command or generated output in addition to lint. Use an isolated home
for destructive scenarios; a dry run verifies planning, not successful application.

## Reference docs

Each doc is the source of truth for a convention you can't infer from the code alone. Read the
relevant one **before** you touch the area it covers.

| Doc | Read it before… |
| --- | --- |
| [`docs/setup.md`](/docs/setup.md) | bootstrapping a workstation or creating machine-local overrides. |
| [`docs/coding-agents.md`](/docs/coding-agents.md) | editing either global prompt (`home/.claude/CLAUDE.md` or `home/.config/opencode/AGENTS.md`) or any tracked Claude Code / OpenCode / RTK / Herdr / gentle-ai config. Four of those files are copied into `$HOME`, not symlinked — read this before assuming an edit propagates. |
| [`docs/git-configuration.md`](/docs/git-configuration.md) | changing `home/.gitconfig`, or anything touching Git identity, GPG signing, or per-directory overrides. |
| [`docs/tooling.md`](/docs/tooling.md) | adding or changing a tool (Homebrew or mise), editing `hk.pkl` or `committed.toml`, or adding/running `just` recipes. |
| [`docs/zsh-configuration.md`](/docs/zsh-configuration.md) | editing any zsh startup file (`.zshenv`, `.zprofile`, `.zshrc`, `.zlogin`). |
| [`scripts/README.md`](/scripts/README.md) | editing anything under `scripts/`, or changing what runs during `just sync`. |
