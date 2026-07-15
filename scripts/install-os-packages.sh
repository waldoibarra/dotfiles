#!/usr/bin/env bash
#
# Install Homebrew (and its packages) and Mise (and its tools), plus the
# WezTerm terminfo entry on macOS.

set -euo pipefail

# Apple Silicon only — Intel Macs install Homebrew to /usr/local instead.
readonly BREW_MAC="/opt/homebrew/bin/brew"
readonly BREW_LINUX="/home/linuxbrew/.linuxbrew/bin/brew"

#######################################
# Detects the shell running this script, so activate_mise_tools knows which
# `mise activate` snippet to eval.
# Globals:
#   ZSH_VERSION
#   BASH_VERSION
#   SHELL
# Arguments:
#   None
# Outputs:
#   Writes the shell name (zsh, bash, or basename of $SHELL) to stdout.
#######################################
get_current_shell() {
  if [[ -n "${ZSH_VERSION:-}" ]]; then
    echo "zsh"
  elif [[ -n "${BASH_VERSION:-}" ]]; then
    echo "bash"
  else
    echo "${SHELL##*/}"
  fi
}

#######################################
# Prints the current OS's kernel name (Darwin, Linux).
# Arguments:
#   None
# Outputs:
#   Writes the OS name to stdout.
#######################################
get_os_name() {
  uname -s
}

#######################################
# Evals the mise shell hook for whichever shell is running this script.
# Arguments:
#   None
#######################################
activate_mise_tools() {
  local current_shell
  current_shell=$(get_current_shell)

  if [[ "$current_shell" == "bash" ]]; then
    eval "$(mise activate bash)"
  elif [[ "$current_shell" == "zsh" ]]; then
    eval "$(mise activate zsh)"
  fi
}

#######################################
# Downloads and runs Homebrew's official installer non-interactively.
# Arguments:
#   None
#######################################
run_brew_install_script() {
  local os
  os=$(get_os_name)

  if [[ "$os" == "Darwin" ]]; then
    # Prompt for password on MacOS before running the Brew installer as it will throw an error
    # with a warning about `stdin` not being a TTY.
    sudo -v
  fi

  local install_script
  install_script="$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  NONINTERACTIVE=1 /bin/bash -c "$install_script"
}

#######################################
# Installs the OS-level prerequisites Homebrew's installer needs before it
# can run.
# Arguments:
#   None
#######################################
install_brew_deps() {
  local os
  os=$(get_os_name)

  if [[ "$os" == "Darwin" ]]; then
    # https://docs.brew.sh/Installation#macos-requirements
    if ! xcode-select -p &>/dev/null; then
      xcode-select --install 2>/dev/null
    fi
  elif [[ "$os" == "Linux" ]]; then
    # https://docs.brew.sh/Homebrew-on-Linux#requirements
    sudo apt-get install -y build-essential procps curl file git
  fi
}

#######################################
# Evals Homebrew's shellenv so `brew` and its shims are on PATH for the rest
# of this script's process.
# Globals:
#   BREW_MAC
#   BREW_LINUX
# Arguments:
#   None
#######################################
add_brew_to_path() {
  local os
  os=$(get_os_name)

  if [[ "$os" == "Darwin" ]]; then
    eval "$($BREW_MAC shellenv)"
  elif [[ "$os" == "Linux" ]]; then
    eval "$($BREW_LINUX shellenv)"
  fi
}

#######################################
# Checks the well-known Homebrew install paths for the current OS first, since
# a freshly installed brew may not be on PATH yet in this shell.
# Globals:
#   BREW_MAC
#   BREW_LINUX
# Arguments:
#   None
# Returns:
#   0 if Homebrew is installed, 1 otherwise.
#######################################
is_brew_installed() {
  local os
  os=$(get_os_name)

  if [[ "$os" == "Darwin" ]]; then
    [[ -x "$BREW_MAC" ]] && return 0
  elif [[ "$os" == "Linux" ]]; then
    [[ -x "$BREW_LINUX" ]] && return 0
  fi

  if command -v brew >/dev/null 2>&1; then
    return 0
  fi

  return 1
}

#######################################
# Installs the WezTerm terminfo entry on macOS so wezterm is a recognized TERM
# value for tools like tic/infocmp that don't ship it by default.
# Arguments:
#   None
#######################################
install_wezterm_terminfo() {
  if [[ "$(get_os_name)" != "Darwin" ]]; then return; fi
  if ! command -v wezterm >/dev/null 2>&1; then return; fi

  if infocmp wezterm >/dev/null 2>&1; then
    echo "WezTerm terminfo already installed."
    return
  fi

  local tmpfile
  tmpfile=$(mktemp)
  trap 'rm -f "$tmpfile"' RETURN

  curl -fsSL -o "$tmpfile" \
    "https://raw.githubusercontent.com/wezterm/wezterm/master/termwiz/data/wezterm.terminfo"
  tic -x -o ~/.terminfo "$tmpfile"
  echo "Installed WezTerm terminfo."
}

#######################################
# Trusts this repo's mise config, installs its pinned tools, and activates
# them for the rest of this script's process.
# Arguments:
#   None
#######################################
install_mise_tools() {
  mise trust --quiet
  mise install
  activate_mise_tools
  echo "Installed missing Mise-managed tools."
}

#######################################
# Installs the Homebrew packages declared in the global Brewfile, if they
# aren't already satisfied.
# Arguments:
#   None
#######################################
install_brew_packages() {
  brew bundle check --global || brew bundle install --global
  echo "Installed Homebrew packages."
}

#######################################
# Installs Homebrew if it's missing, or otherwise makes sure it's on PATH.
# Arguments:
#   None
#######################################
install_brew() {
  if is_brew_installed; then
    echo "Homebrew is already installed."

    if ! command -v brew >/dev/null 2>&1; then
      add_brew_to_path
    fi
  else
    install_brew_deps
    run_brew_install_script
    add_brew_to_path
    echo "Finished installing Homebrew."
  fi
}

main() {
  install_brew
  install_brew_packages
  install_mise_tools
  install_wezterm_terminfo
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
