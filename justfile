# Show available recipes.
help:
  @just --list

# Idempotently install configuration on the OS.
install:
  ./scripts/install-dotfiles.sh

# Brew bundle: dump, cleanup, upgrade.
brew: brew-dump brew-cleanup brew-upgrade

# Dump all installed packages into the global Brewfile.
brew-dump:
  brew bundle dump --global --force --describe

# Cleanup anything that's not in the global Brewfile.
brew-cleanup:
  brew bundle cleanup --global --force

# Upgrade all items in the global Brewfile.
brew-upgrade:
  brew bundle upgrade --global

# Use ShellCheck to check for bugs on shell scripts.
check:
  shellcheck scripts/install-dotfiles.sh
  shellcheck -a scripts/update-coding-agents.sh

# Update coding agents.
update-ca:
  ./scripts/update-coding-agents.sh
