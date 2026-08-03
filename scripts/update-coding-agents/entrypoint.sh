#!/usr/bin/env bash
#
# Update coding agent tooling: refresh stale entries in OpenCode's plugin
# cache, refresh the RTK OpenCode plugin and the Herdr agent integrations,
# and sync globally installed skills from the lockfile.

set -euo pipefail

ENTRYPOINT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ENTRYPOINT_DIR
# shellcheck source=scripts/lib/shell-helpers.sh
source "${ENTRYPOINT_DIR}/../lib/shell-helpers.sh"
# shellcheck source=scripts/update-coding-agents/sync-global-skills-from-lock.sh
source "${ENTRYPOINT_DIR}/sync-global-skills-from-lock.sh"
# shellcheck source=scripts/update-coding-agents/refresh-stale-opencode-plugins.sh
source "${ENTRYPOINT_DIR}/refresh-stale-opencode-plugins.sh"

#######################################
# Check whether a Herdr agent integration is installed and current.
# Arguments:
#   Integration name as reported by `herdr integration status` (e.g. claude).
# Returns:
#   0 if the integration is current, non-zero otherwise.
#######################################
herdr_integration_is_current() {
  # Capture first: piping herdr into grep -q makes grep's early exit SIGPIPE
  # herdr, which pipefail then reports as a pipeline failure.
  local integration_status
  integration_status="$(herdr integration status 2>/dev/null || true)"
  grep -q "^$1: current" <<<"${integration_status}"
}

#######################################
# Install or refresh the Herdr Claude Code hook, if Herdr is installed.
# `herdr integration install claude` writes the hook script AND re-adds a
# machine-specific absolute-path hook entry to the tracked settings.json
# (it detects its hook by exact command string, so the tracked $HOME form
# looks missing to it). The settings file is restored to its committed form
# afterwards — only safe when it has no uncommitted changes, so the update
# is skipped with a warning otherwise.
# Globals:
#   ENTRYPOINT_DIR
# Outputs:
#   Writes progress to STDOUT and warnings to STDERR.
#######################################
install_herdr_claude_hook() {
  if ! command -v herdr >/dev/null 2>&1; then
    echo "Herdr not found, skipping Claude hook install."
    return
  fi
  if herdr_integration_is_current claude; then
    echo "Herdr Claude hook already up to date."
    return
  fi

  local settings_file
  settings_file="$(git -C "${ENTRYPOINT_DIR}" rev-parse --show-toplevel)/home/.claude/settings.json"
  if [[ -n "$(git -C "${ENTRYPOINT_DIR}" status --porcelain -- "${settings_file}")" ]]; then
    echo "Herdr Claude hook is outdated, but home/.claude/settings.json has uncommitted changes;" \
      "skipping. Run 'herdr integration install claude' manually (see docs/coding-agents.md)." >&2
    return
  fi
  herdr integration install claude
  git -C "${ENTRYPOINT_DIR}" restore -- "${settings_file}"
  echo "Herdr Claude hook installed; settings.json restored to its tracked form."
}

#######################################
# Install or refresh the Herdr OpenCode plugin, if Herdr is installed.
# `herdr integration status` validates the installed plugin's version against
# the herdr binary, so it doubles as the up-to-date check.
# https://herdr.dev/docs/agents
# Outputs:
#   Writes progress to STDOUT.
#######################################
install_herdr_opencode_plugin() {
  if ! command -v herdr >/dev/null 2>&1; then
    echo "Herdr not found, skipping OpenCode plugin install."
    return
  fi
  if herdr_integration_is_current opencode; then
    echo "Herdr OpenCode plugin already up to date."
    return
  fi
  herdr integration install opencode
  echo "Herdr OpenCode plugin installed."
}

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
  # Capture first: piping rtk into grep -q makes grep's early exit SIGPIPE
  # rtk, which pipefail then reports as a pipeline failure.
  local dry_run_output
  dry_run_output="$(rtk init -g --opencode --dry-run 2>&1 || true)"
  if grep -q "Nothing written" <<<"${dry_run_output}"; then
    echo "RTK OpenCode plugin already up to date."
    return
  fi
  rtk init -g --opencode
  echo "RTK OpenCode plugin installed."
}

main() {
  refresh_stale_opencode_plugins
  install_rtk_opencode_plugin
  install_herdr_opencode_plugin
  install_herdr_claude_hook
  sync_global_skills_from_lock

  echo "Done updating. Restart OpenCode if it's open."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
