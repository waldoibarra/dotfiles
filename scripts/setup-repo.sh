#!/usr/bin/env bash

set -e

_source_dependencies() {
  local -r _scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  source "$_scripts_dir/lib/shell-helpers.sh"
}

_get_repo_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd
}

_install_git_hooks() {
  print_separator "Installing Git hooks"

  hk install
  echo "Installed Git hooks. ✅"
}

_create_claude_symlink() {
  local -r _repo_root="$(_get_repo_root)"
  local -r _claude_md="$_repo_root/CLAUDE.md"

  print_separator "Setting up local CLAUDE.md symlink"

  if [[ -L "$_claude_md" && "$(readlink "$_claude_md")" == "AGENTS.md" ]]; then
    echo "CLAUDE.md symlink already exists. ✅"
    return
  fi

  ln -sf AGENTS.md "$_claude_md"
  echo "Created symlink: CLAUDE.md → AGENTS.md ✅"
}

main() {
  _source_dependencies
  _install_git_hooks
  _create_claude_symlink
}

main
