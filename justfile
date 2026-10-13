# Show available recipes.
[private]
default:
  @just --list --unsorted

# Idempotently sync OS configuration, apply Brew packages, sync Mise tools, update coding agents.
[group("Management")]
sync: && print-separator brew mise-sync update-ca hooks
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

# Open the local Pi build with Lens and subagents sources; /reload refreshes both extensions.
[group("Development")]
[no-cd]
pi-lens-dev:
  @for source_file in \
    "$HOME/projects/personal/pi/packages/coding-agent/dist/bundle/cli.js" \
    "$HOME/projects/personal/pi-lens/src/index.ts" \
    "$HOME/projects/personal/pi-subagents/index.ts"; do \
    test -f "$source_file" || { \
      printf 'Missing development file: %s\n' "$source_file" >&2; exit 1; \
    }; \
  done
  node "$HOME/projects/personal/pi/packages/coding-agent/dist/bundle/cli.js" \
    --no-session --no-extensions \
    -e "$HOME/projects/personal/pi-lens/src/index.ts" \
    -e "$HOME/projects/personal/pi-subagents/index.ts"

# Run pre-commit hook against all files to verify hook configuration.
[group("Debug")]
check-hooks:
  hk run pre-commit --all
