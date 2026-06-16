#!/usr/bin/env bash

_source_dependencies() {
  local -r _scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  source "$_scripts_dir/lib/constants.sh"
  source "$_scripts_dir/lib/shell-helpers.sh"
  source "$_scripts_dir/agents/sync-global-skills-from-lock.sh"
}

_clear_opencode_cache() {
  if [[ -d "$OPENCODE_CACHE_DIR" ]]; then
    rm -rf "$OPENCODE_CACHE_DIR"
    printf "\nOpenCode cache cleared. 🗑️\n"
  fi
}

_install_rtk_opencode_plugin() {
  # https://github.com/rtk-ai/rtk/tree/develop/hooks/opencode
  if ! command -v rtk >/dev/null 2>&1; then
    echo "rtk not found, skipping OpenCode plugin install."
    return
  fi
  rtk init -g --opencode
  echo "RTK OpenCode plugin up to date. ✅"
}

main() {
  _source_dependencies
  _clear_opencode_cache
  _install_rtk_opencode_plugin
  sync_global_skills_from_lock

  echo "✅ Done updating. Restart OpenCode if it's open."
}

main
