#!/usr/bin/env bash
#
# Set the Homebrew-installed Zsh as the default login shell.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPTS_DIR
source "${SCRIPTS_DIR}/lib/shell-helpers.sh"

#######################################
# Print the current OS's kernel name (Darwin, Linux, ...).
# Arguments:
#   None
#######################################
get_os_name() {
  uname -s
}

#######################################
# Print the path to the Homebrew-installed Zsh binary.
# Arguments:
#   None
#######################################
get_brew_zsh_path() {
  local brew_prefix
  brew_prefix="$(brew --prefix)"
  echo "${brew_prefix}/bin/zsh"
}

#######################################
# Set the platform's default login shell to the given Zsh binary.
# On Linux, `chsh` requires `sudo` and an explicit username; on macOS it
# doesn't, since it authenticates the caller directly.
# Arguments:
#   None
#######################################
set_default_shell() {
  local os brew_zsh
  os="$(get_os_name)"
  brew_zsh="$(get_brew_zsh_path)"

  echo "Setting default shell to ${brew_zsh}."

  if [[ "${os}" == "Darwin" ]]; then
    chsh -s "${brew_zsh}"
  elif [[ "${os}" == "Linux" ]]; then
    sudo chsh -s "${brew_zsh}" "${USER}"
  fi
}

#######################################
# Register the given shell in /etc/shells so `chsh` will accept it as a
# default shell. Required because a Homebrew-installed Zsh isn't a system
# shell macOS/Linux trust by default.
# Arguments:
#   None
#######################################
add_to_allowed_shells() {
  local brew_zsh
  brew_zsh="$(get_brew_zsh_path)"

  if grep -qx "${brew_zsh}" /etc/shells; then
    echo "Zsh is already in /etc/shells: ${brew_zsh}"
    return
  fi

  echo "Adding ${brew_zsh} to /etc/shells"
  echo "${brew_zsh}" | sudo tee -a /etc/shells >/dev/null
}

main() {
  local os brew_zsh
  os="$(get_os_name)"
  brew_zsh="$(get_brew_zsh_path)"

  print_separator "Setting Zsh as default shell"

  if [[ "${SHELL}" == "${brew_zsh}" ]]; then
    echo "Default shell is already ${brew_zsh}. ✅"
    return
  fi

  add_to_allowed_shells
  set_default_shell
  echo "Changed default shell to ${brew_zsh}. ✅"

  if [[ "${os}" == "Darwin" ]]; then
    echo "Open a new terminal session. ❤️"
  elif [[ "${os}" == "Linux" ]]; then
    echo "Log out and log back in. ❤️"
  fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
