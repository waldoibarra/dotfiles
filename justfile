# Show available recipes.
[private]
default:
  @just --list --unsorted

# Idempotently sync OS configuration, sync Brew packages, upgrade Mise tools, update coding agents.
[group("Management")]
sync: && print-separator brew mise-up update-ca
  git pull
  ./scripts/install-dotfiles.sh
  @echo "🌧️ Finished synchronizing the dotfiles. 🕉️"

# Brew bundle: dump, cleanup, upgrade.
[group("Management")]
brew: brew-dump brew-clean brew-up && print-separator
  @echo "🌧️ Finished the Homebrew bundle cycle — dump, clean, ugrade. 🕉️"

# Dump all installed packages into the global Brewfile.
[group("Management")]
[private]
brew-dump:
  brew bundle dump --global --force --no-vscode

# Clean up anything that's not in the global Brewfile.
[group("Management")]
[private]
brew-clean:
  brew bundle cleanup --global --force

# Upgrade all items in the global Brewfile.
[group("Management")]
[private]
brew-up:
  brew bundle upgrade --global --quiet

# Upgrade outdated (Mise managed) tools to their latests versions.
[group("Management")]
mise-up: && print-separator
  mise upgrade
  @echo "🌧️ Finished upgrading Mise tools. 🕉️"

# Update coding agents configuration.
[group("Management")]
update-ca: && print-separator
  ./scripts/update-coding-agents.sh
  @echo "🌧️ Finished updating AI coding agents configuration. 🕉️"

# Print 80 chars long separator.
[private]
[group("Management")]
print-separator:
  @printf '%*s\n' 80 | tr ' ' '-' && printf "\n"

# Use ShellCheck to lint shell scripts.
[group("Linting")]
lint-sh:
  shellcheck scripts/install-dotfiles.sh
  shellcheck scripts/install-os-packages.sh
  shellcheck -a scripts/setup-env.sh
  shellcheck -a scripts/setup-repo.sh
  shellcheck -a scripts/update-coding-agents.sh
  shellcheck home/.claude/statusline.sh

# Use markdownlint-cli2 to lint Markdown files.
[group("Linting")]
lint-md:
  markdownlint-cli2 "**/*.md"

# Use editorconfig-checker to lint all files against .editorconfig rules.
[group("Linting")]
lint-ec:
  ec

# Use yamlfmt to lint YAML files.
[group("Linting")]
lint-yaml:
  yamlfmt -lint "**/*.yaml"

# Use committed to lint a commit message file.
[group("Linting")]
lint-commit msg_file:
  committed --commit-file {{msg_file}}

# Run pre-commit hook against all files to verify hook configuration.
[group("Debug")]
check-hooks:
  hk run pre-commit --all
