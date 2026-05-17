#!/usr/bin/env bash

_get_os_name() {
  uname -s
}

_install_brew_deps() {
  local -r _os=$(_get_os_name)

  if [[ "$_os" == "Darwin" ]]; then
    # https://docs.brew.sh/Installation#macos-requirements
    xcode-select --install 2>/dev/null
  elif [[ "$_os" == "Linux" ]]; then
    # https://docs.brew.sh/Homebrew-on-Linux#requirements
    sudo apt-get install -y build-essential procps curl file git
  fi
}

_run_brew_install_script() {
  NONINTERACTIVE=1 \
    /bin/bash -c \
    "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
}

_add_brew_to_path() {
  local -r _os=$(_get_os_name)

  if [[ "$_os" == "Darwin" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ "$_os" == "Linux" ]]; then
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
  fi
}

_install_brew() {
  if command -v brew >/dev/null 2>&1; then
    echo "Homebrew is already installed. ✅"
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
  mise install
  echo "Installed missing Mise-managed tools. ✅"
}

main() {
  _install_brew
  _install_brew_packages
  _install_mise_tools
}

main
