#!/usr/bin/env bash

set -e

readonly BREW_MAC="/opt/homebrew/bin/brew"
readonly BREW_LINUX="/home/linuxbrew/.linuxbrew/bin/brew"

_get_os_name() {
  uname -s
}

_is_brew_installed() {
  local -r _os=$(_get_os_name)

  if [[ "$_os" == "Darwin" ]]; then
    [[ -x "$BREW_MAC" ]] && return 0
  elif [[ "$_os" == "Linux" ]]; then
    [[ -x "$BREW_LINUX" ]] && return 0
  fi

  if command -v brew >/dev/null 2>&1; then
    return 0
  fi

  return 1
}

_install_brew_deps() {
  local -r _os=$(_get_os_name)

  if [[ "$_os" == "Darwin" ]]; then
    # https://docs.brew.sh/Installation#macos-requirements
    if ! xcode-select -p &>/dev/null; then
      xcode-select --install 2>/dev/null
    fi
  elif [[ "$_os" == "Linux" ]]; then
    # https://docs.brew.sh/Homebrew-on-Linux#requirements
    sudo apt-get install -y build-essential procps curl file git
  fi
}

_run_brew_install_script() {
  local -r _os=$(_get_os_name)

  if [[ "$_os" == "Darwin" ]]; then
    # Prompt for password on MacOS before running the Brew installer as it will throw an error
    # with a warning about `stdin` not being a TTY.
    sudo -v
  fi

  NONINTERACTIVE=1 \
    /bin/bash -c \
    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
}

_add_brew_to_path() {
  local -r _os=$(_get_os_name)

  if [[ "$_os" == "Darwin" ]]; then
    eval "$($BREW_MAC shellenv)"
  elif [[ "$_os" == "Linux" ]]; then
    eval "$($BREW_LINUX shellenv)"
  fi
}

_get_current_shell() {
  if [ -n "$ZSH_VERSION" ]; then
    CURRENT_SHELL="zsh"
  elif [ -n "$BASH_VERSION" ]; then
    CURRENT_SHELL="bash"
  else
    CURRENT_SHELL="${SHELL##*/}"
  fi

  echo "$CURRENT_SHELL"
}

_activate_mise_tools() {
  local -r _current_shell=$(_get_current_shell)

  if [[ "$_current_shell" == "bash" ]]; then
    eval "$(mise activate bash)"
  elif [[ "$_current_shell" == "zsh" ]]; then
    eval "$(mise activate zsh)"
  fi
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

_install_brew() {
  if _is_brew_installed; then
    echo "Homebrew is already installed. ✅"

    if ! command -v brew >/dev/null 2>&1; then
      _add_brew_to_path
    fi
  else
    _install_brew_deps
    _run_brew_install_script
    _add_brew_to_path
    echo "Finished installing Homebrew. ✅"
  fi
}

_install_brew_packages() {
  brew bundle check --global || brew bundle install --global
  echo "Installed Homebrew packages. ✅"
}

_install_mise_tools() {
  mise trust
  mise install
  _activate_mise_tools
  echo "Installed missing Mise-managed tools. ✅"
}

_install_git_hooks() {
  hk install
  echo "Installed Git hooks. ✅"
}

_set_brew_zsh_as_default_shell() {
  local -r _os=$(_get_os_name)
  local -r _brew_zsh="$(_get_brew_zsh_path)"

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
  _install_brew
  _install_brew_packages
  _install_mise_tools
  _install_git_hooks
  _set_brew_zsh_as_default_shell
}

main
