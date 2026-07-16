#!/usr/bin/env bash
#
# Update coding agent tooling: refresh stale entries in OpenCode's plugin
# cache, refresh the RTK OpenCode plugin, and sync globally installed skills
# from the lockfile.

set -euo pipefail

ENTRYPOINT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ENTRYPOINT_DIR
source "${ENTRYPOINT_DIR}/../lib/shell-helpers.sh"
source "${ENTRYPOINT_DIR}/sync-global-skills-from-lock.sh"
source "${ENTRYPOINT_DIR}/refresh-stale-opencode-plugins.sh"

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

main() {
  refresh_stale_opencode_plugins
  install_rtk_opencode_plugin
  sync_global_skills_from_lock

  echo "Done updating. Restart OpenCode if it's open."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
