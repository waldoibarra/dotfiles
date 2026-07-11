#!/usr/bin/env bash

set -e

_source_dependencies() {
  local -r _scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  source "$_scripts_dir/lib/shell-helpers.sh"
}

_configure_global_sudo_credential_cache() {
  local -r _sudoers_file="/etc/sudoers.d/timestamp_type"
  local -r _content="Defaults timestamp_type=global"

  print_separator "Configuring sudo timestamp type"

  if [[ -f "$_sudoers_file" ]] && grep -qx "$_content" "$_sudoers_file"; then
    echo "Sudo timestamp type is already global. ✅"
    return
  fi

  echo "Writing $_sudoers_file to set timestamp_type=global."
  echo "$_content" | sudo tee "$_sudoers_file" >/dev/null
  sudo chmod 444 "$_sudoers_file"
  echo "Set sudo timestamp type to global. ✅"
}

main() {
  _source_dependencies
  _configure_global_sudo_credential_cache
}

main
