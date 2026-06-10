#!/usr/bin/env bash

set -e

_source_dependencies() {
  local -r _scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  source "$_scripts_dir/lib/shell-helpers.sh"
}

_install_git_hooks() {
  print_separator "Installing Git hooks"

  hk install
  echo "Installed Git hooks. ✅"
}

main() {
  _source_dependencies
  _install_git_hooks
}

main
