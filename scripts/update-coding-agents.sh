#!/usr/bin/env bash
#
# Update coding agent tooling: clear OpenCode's cache, refresh the RTK
# OpenCode plugin, and sync globally installed skills from the lockfile.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPTS_DIR
source "${SCRIPTS_DIR}/lib/constants.sh"
source "${SCRIPTS_DIR}/lib/shell-helpers.sh"
source "${SCRIPTS_DIR}/agents/sync-global-skills-from-lock.sh"

#######################################
# Install or refresh the RTK OpenCode plugin, if RTK is installed.
# https://github.com/rtk-ai/rtk/tree/develop/hooks/opencode
# Outputs:
#   Writes progress to STDOUT.
#######################################
install_rtk_opencode_plugin() {
  if ! command -v rtk >/dev/null 2>&1; then
    echo "rtk not found, skipping OpenCode plugin install."
    return
  fi
  if rtk init -g --opencode --dry-run 2>&1 | grep -q "Nothing written"; then
    echo "RTK OpenCode plugin already up to date."
    return
  fi
  rtk init -g --opencode
  echo "RTK OpenCode plugin installed."
}

#######################################
# Remove OpenCode's cache directory, if present, so it rebuilds from
# scratch on next launch.
# Globals:
#   OPENCODE_CACHE_DIR
# Outputs:
#   Writes progress to STDOUT.
#######################################
clear_opencode_cache() {
  if [[ -d "$OPENCODE_CACHE_DIR" ]]; then
    rm -rf "$OPENCODE_CACHE_DIR"
    echo "OpenCode cache cleared."
  fi
}

main() {
  clear_opencode_cache
  install_rtk_opencode_plugin
  sync_global_skills_from_lock

  echo "Done updating. Restart OpenCode if it's open."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
