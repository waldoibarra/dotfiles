#!/bin/bash
# =============================================================================
# Restart Homebrew Service with Custom Plist
# =============================================================================
#
# This script restarts a Homebrew service using a custom plist file from your
# dotfiles repository instead of the default Homebrew-generated plist.
#
# Usage:
#   ./scripts/restart-brew-service-with-custom-plist.sh <formula-name>
#
# Example:
#   ./scripts/restart-brew-service-with-custom-plist.sh ollama
#
# Requirements:
#   - The formula must be installed via Homebrew
#   - A custom plist file must exist in:
#     home/Library/LaunchAgents/homebrew.mxcl.<formula-name>.plist
#
# What this script does:
#   1. Stops the current service (if running)
#   2. Creates a symlink from ~/Library/LaunchAgents/ to your dotfiles plist
#   3. Starts the service using your custom plist
#
# =============================================================================

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_DIR="$(dirname "$SCRIPTS_DIR")"
FORMULA_NAME="${1:-}"

if [[ -z "$FORMULA_NAME" ]]; then
    echo "Usage: $0 <formula-name>"
    exit 1
fi

PLIST_PATH="Library/LaunchAgents/homebrew.mxcl.$FORMULA_NAME.plist"
DOTFILES_PLIST="${DOTFILES_DIR}/home/$PLIST_PATH"
HOME_PLIST="$HOME/$PLIST_PATH"

echo "Restarting $FORMULA_NAME brew service with custom plist."

# This deletes the current $HOME_PLIST.
brew services stop "$FORMULA_NAME" 2>/dev/null || true

ln -sf "$DOTFILES_PLIST" "$HOME_PLIST"

# This deletes the sysmlink, but leaves the contents of $DOTFILES_PLIST.
brew services --file "$HOME_PLIST" start "$FORMULA_NAME"

echo "$FORMULA_NAME brew service started with custom plist."
