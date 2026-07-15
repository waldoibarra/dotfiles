# Show available recipes.
[private]
default:
  @just --list --unsorted

# Idempotently sync OS configuration, sync Brew packages, upgrade Mise tools, update coding agents.
[group("Management")]
sync: && print-separator brew mise-up update-ca hooks sudo-invalidate
  @echo "Caching password to avoid asking for it later while this runs. " && sudo -v
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

# Install this repo's Git hooks.
[group("Management")]
hooks:
  @hk install --quiet

# Invalidate sudo credentials after sync.
[private]
[group("Management")]
sudo-invalidate:
  @sudo -k

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
  shellcheck -a scripts/configure-sudo-credential-cache.sh
  shellcheck -a scripts/configure-touch-id-for-sudo.sh
  shellcheck -a scripts/set-brew-zsh-as-default-shell.sh
  shellcheck -a scripts/update-coding-agents.sh
  shellcheck home/.claude/statusline.sh
  shellcheck home/.agents/skills/shell-scripting/assets/template.sh
  shellcheck home/.agents/skills/shell-scripting/assets/template-linear.sh
  shellcheck home/.config/opencode/skills/non-vision-image-reader/scripts/recover-pasted-images.sh

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
