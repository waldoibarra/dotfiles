# Show available recipes.
[private]
default:
  @just --list --unsorted

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

# Use ShellCheck to check for bugs on shell scripts.
[group("Linting")]
check:
  shellcheck scripts/install-dotfiles.sh
  shellcheck -a scripts/update-coding-agents.sh
