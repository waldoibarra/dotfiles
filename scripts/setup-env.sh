#!/usr/bin/env bash

set -e

_source_dependencies() {
  local -r _scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  source "$_scripts_dir/lib/shell-helpers.sh"
}

_get_os_name() {
  uname -s
}

_get_brew_zsh_path() {
  echo "$(brew --prefix)/bin/zsh"
}

_add_to_allowed_shells() {
  local -r _brew_zsh="$(_get_brew_zsh_path)"

  if grep -qx "$_brew_zsh" /etc/shells; then
    echo "Zsh is already in /etc/shells: $_brew_zsh"
    return
  fi

  echo "Adding $_brew_zsh to /etc/shells"
  echo "$_brew_zsh" | sudo tee -a /etc/shells >/dev/null
}

_set_default_shell() {
  local -r _os=$(_get_os_name)
  local -r _brew_zsh="$(_get_brew_zsh_path)"

  echo "Setting default shell to $_brew_zsh."

  if [[ "$_os" == "Darwin" ]]; then
    chsh -s "$_brew_zsh"
  elif [[ "$_os" == "Linux" ]]; then
    sudo chsh -s "$_brew_zsh" "$USER"
  fi
}

_set_brew_zsh_as_default_shell() {
  local -r _os=$(_get_os_name)
  local -r _brew_zsh="$(_get_brew_zsh_path)"

  print_separator "Setting Zsh as default shell"

  if [ "$SHELL" = "$_brew_zsh" ]; then
    echo "Default shell is already $_brew_zsh. ✅"
    return
  fi

  _add_to_allowed_shells
  _set_default_shell
  echo "Changed default shell to $_brew_zsh. ✅"

  if [[ "$_os" == "Darwin" ]]; then
    echo "Open a new terminal session. ❤️"
  elif [[ "$_os" == "Linux" ]]; then
    echo "Log out and log back in. ❤️"
  fi
}

main() {
  _source_dependencies
  _set_brew_zsh_as_default_shell
}

main
