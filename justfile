# Show available recipes.
[private]
default:
  @just --list --unsorted

# Set up local project tools and Git hooks.
[group("Setup")]
setup: install-local-tools install-git-hooks

# Install local project-level tools (separate from global Mise tools).
[group("Setup")]
[private]
install-local-tools:
  mise trust
  mise install

# Install Git hooks for this repository.
[group("Setup")]
[private]
install-git-hooks:
  hk install

# Idempotently sync OS configuration, sync Brew packages, upgrade Mise tools, update coding agents.
[group("Management")]
sync: && brew mise-up update-ca
  ./scripts/install-dotfiles.sh

# Brew bundle: dump, cleanup, upgrade.
[group("Management")]
brew: brew-dump brew-clean brew-up

# Dump all installed packages into the global Brewfile.
[group("Management")]
[private]
brew-dump:
  brew bundle dump --global --force --describe

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
mise-up:
  mise upgrade

# Update coding agents configuration.
[group("Management")]
update-ca:
  ./scripts/update-coding-agents.sh

# Use ShellCheck to lint shell scripts.
[group("Linting")]
lint-sh:
  shellcheck scripts/install-dotfiles.sh
  shellcheck -a scripts/update-coding-agents.sh

# Run pre-commit hook against all files to verify hook configuration.
[group("Linting")]
check-hooks:
  hk run pre-commit --all
