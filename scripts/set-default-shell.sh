#!/usr/bin/env bash
# Sets Homebrew's zsh as the default shell.
# Idempotent: skips each step if already done.
# May prompt for a password to write to /etc/shells and to run chsh.

set -euo pipefail

_brew_zsh() {
  echo "$(brew --prefix)/bin/zsh"
}

_add_to_allowed_shells() {
  local -r _brew_zsh="$(_brew_zsh)"

  if grep -qx "$_brew_zsh" /etc/shells; then
    echo "Already in /etc/shells: $_brew_zsh"
    return
  fi

  echo "Adding $_brew_zsh to /etc/shells (requires sudo) —"
  echo "$_brew_zsh" | sudo tee -a /etc/shells >/dev/null
}

_set_default_shell() {
  local -r _brew_zsh="$(_brew_zsh)"

  if [ "$SHELL" = "$_brew_zsh" ]; then
    echo "Default shell is already $_brew_zsh"
    return
  fi

  echo "Setting default shell to $_brew_zsh (requires password) —"
  chsh -s "$_brew_zsh"
}

main() {
  _add_to_allowed_shells
  _set_default_shell
}

main
