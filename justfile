# Show available recipes.
[private]
default:
  @just --list --unsorted

# Idempotently sync OS configuration, apply Brew packages, sync Mise tools, update coding agents.
[group("Management")]
sync: && print-separator brew mise-sync obsidian-sync update-ca hooks
  git pull
  ./scripts/install-dotfiles.sh
  @echo "Finished synchronizing the dotfiles."

# Apply the global Brewfile declaratively: install/upgrade listed, remove unlisted.
[group("Management")]
brew: brew-apply brew-clean && print-separator
  @echo "Finished the Homebrew bundle cycle — apply, clean."

# Install missing and upgrade existing packages from the global Brewfile.
[group("Management")]
[private]
brew-apply:
  brew bundle upgrade --global --quiet

# Clean up anything that's not in the global Brewfile.
[group("Management")]
[private]
brew-clean:
  brew bundle cleanup --global --force

# Dump this machine's installed packages into the global Brewfile (opt-in; commit after).
[group("Management")]
brew-dump:
  brew bundle dump --global --force --no-vscode --no-npm

# Sync Mise tools: install missing, upgrade, and prune tools no longer in config.
[group("Management")]
mise-sync: && print-separator
  mise install --yes
  mise upgrade --yes
  mise prune --yes
  @echo "Finished syncing Mise tools."

# Update coding agents configuration.
[group("Management")]
update-ca: && print-separator
  ./scripts/update-coding-agents/entrypoint.sh
  @echo "Finished updating AI coding agents configuration."

# Install this repo's Git hooks.
[group("Management")]
hooks:
  @hk install --quiet

# Print 80 chars long separator.
[private]
[group("Management")]
print-separator:
  @printf '%*s\n' 80 | tr ' ' '-' && printf "\n"

# Install declared Obsidian tools/plugins and reconcile owned vault settings and snippets.
[group("Management")]
[positional-arguments]
obsidian-setup vault=(env("HOME") / "life"):
  python3 scripts/obsidian.py setup --vault "$1"

# Reconcile the life vault during workstation sync; skip machines without that vault.
[group("Management")]
obsidian-sync:
  python3 scripts/obsidian.py sync

# Check touched notes and all local vault links without changing files or using the network.
[group("Linting")]
[positional-arguments]
obsidian-check +files:
  python3 scripts/obsidian.py check "$@"

# Lint all.
[group("Linting")]
lint: lint-ec lint-md lint-yaml lint-sh

# Use ShellCheck to lint shell scripts.
[group("Linting")]
lint-sh:
  shellcheck scripts/install-dotfiles.sh
  shellcheck scripts/install-os-packages.sh
  shellcheck scripts/configure-markdown-app.sh
  shellcheck -a scripts/configure-touch-id-for-sudo.sh
  shellcheck -a scripts/set-brew-zsh-as-default-shell.sh
  shellcheck -a scripts/update-coding-agents/entrypoint.sh
  shellcheck scripts/update-coding-agents/sync-life-profile.sh
  shellcheck scripts/update-coding-agents/sync-cursor-rule.sh
  shellcheck -a home/.claude/statusline.sh
  shellcheck -a home/.claude/subagent-statusline.sh
  shellcheck home/.agents/skills/shell-scripting/assets/template.sh
  shellcheck home/.agents/skills/shell-scripting/assets/template-linear.sh

# Use markdownlint-cli2 to lint Markdown files.
[group("Linting")]
lint-md:
  markdownlint-cli2 "**/*.md"

# Use editorconfig-checker to lint all files against .editorconfig rules.
[group("Linting")]
lint-ec:
  editorconfig-checker

# Use yamlfmt to lint YAML files.
[group("Linting")]
lint-yaml:
  yamlfmt -lint "**/*.yaml"

# Use committed to lint a commit message file.
[group("Linting")]
lint-commit msg_file:
  committed --commit-file {{msg_file}}

# Open local Pi, Lens and subagents with installed live voice; /reload refreshes extensions.
[group("Development")]
[no-cd]
[positional-arguments]
pi-lens-dev *PI_ARGS:
  @for source_file in \
    "$HOME/projects/open-source/pi/packages/coding-agent/dist/bundle/cli.js" \
    "$HOME/projects/open-source/pi-lens/src/index.ts" \
    "$HOME/projects/open-source/pi-subagents/index.ts" \
    "$HOME/.pi/agent/npm/node_modules/pi-live-codex/index.ts"; do \
    test -f "$source_file" || { \
      printf 'Missing development file: %s\n' "$source_file" >&2; exit 1; \
    }; \
  done
  node "$HOME/projects/open-source/pi/packages/coding-agent/dist/bundle/cli.js" \
    --no-extensions \
    -e "$HOME/projects/open-source/pi-lens/src/index.ts" \
    -e "$HOME/projects/open-source/pi-subagents/index.ts" \
    -e "$HOME/.pi/agent/npm/node_modules/pi-live-codex/index.ts" \
    "$@"

# Open Claude Code with the local Lens working tree; saving a file reloads the plugin.
[group("Development")]
[no-cd]
[positional-arguments]
claude-lens-dev *CLAUDE_ARGS:
  #!/usr/bin/env sh
  set -eu
  plugin_dir="$HOME/projects/open-source/claude-lens"
  test -f "$plugin_dir/.claude-plugin/plugin.json" || {
    printf 'Missing development file: %s\n' "$plugin_dir/.claude-plugin/plugin.json" >&2
    exit 1
  }
  claude plugin disable lens@claude-lens
  trap 'claude plugin enable lens@claude-lens' EXIT
  claude --plugin-dir "$plugin_dir" "$@"

# Run pre-commit hook against all files to verify hook configuration.
[group("Debug")]
check-hooks:
  hk run pre-commit --all
