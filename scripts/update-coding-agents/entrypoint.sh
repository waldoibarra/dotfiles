#!/usr/bin/env bash
#
# Update coding agent tooling: copy the managed agent configs, refresh
# stale entries in OpenCode's plugin cache, refresh the RTK OpenCode plugin
# and the Herdr agent integrations, and sync globally installed skills from
# the lockfile.

set -euo pipefail

ENTRYPOINT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ENTRYPOINT_DIR
# shellcheck source=../lib/shell-helpers.sh
source "${ENTRYPOINT_DIR}/../lib/shell-helpers.sh"
# shellcheck source=sync-managed-configs.sh
source "${ENTRYPOINT_DIR}/sync-managed-configs.sh"
# shellcheck source=sync-global-skills-from-lock.sh
source "${ENTRYPOINT_DIR}/sync-global-skills-from-lock.sh"
# shellcheck source=refresh-stale-opencode-plugins.sh
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
# machine-specific absolute-path hook entry to ~/.claude/settings.json (it
# detects its hook by exact command string, so the tracked $HOME form looks
# missing to it). That entry used to land in the repo, back when the settings
# file was a symlink to it; it is a copy now, so the duplicate stays local and
# sync_managed_configs clobbers it from the repo on the next run.
# Outputs:
#   Writes progress to STDOUT.
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

  herdr integration install claude
  echo "Herdr Claude hook installed."
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
# Install or refresh an RTK agent integration, if RTK is installed.
# `rtk init --dry-run` always prints "Nothing written"; pending changes show
# up as "[dry-run] would ..." lines instead. Failures only warn, so the
# remaining updater steps still run.
# https://github.com/rtk-ai/rtk/tree/develop/hooks
# Arguments:
#   Integration label for progress messages (e.g. OpenCode).
#   `rtk init` arguments selecting the integration (e.g. -g --opencode).
# Outputs:
#   Writes progress to STDOUT and warnings to STDERR.
#######################################
install_rtk_integration() {
  local label="$1"
  shift
  if ! command -v rtk >/dev/null 2>&1; then
    echo "rtk not found, skipping RTK ${label} install."
    return
  fi
  # Capture first: piping rtk into grep -q makes grep's early exit SIGPIPE
  # rtk, which pipefail then reports as a pipeline failure.
  local dry_run_output rc=0
  dry_run_output="$(rtk init "$@" --dry-run </dev/null 2>&1)" || rc=$?
  if ((rc != 0)); then
    echo "Warning: RTK ${label} dry run failed, skipping." >&2
    return
  fi
  if ! grep -q '^\[dry-run\] would ' <<<"${dry_run_output}"; then
    echo "RTK ${label} integration already up to date."
    return
  fi
  if ! rtk init "$@" </dev/null; then
    echo "Warning: RTK ${label} install failed." >&2
    return
  fi
  echo "RTK ${label} integration installed."
}

main() {
  # First: it resets ~/.claude/settings.json to the tracked bytes, which would
  # otherwise discard whatever the Herdr steps below write into that file.
  sync_managed_configs
  refresh_stale_opencode_plugins
  install_rtk_integration OpenCode -g --opencode
  install_herdr_opencode_plugin
  install_herdr_claude_hook
  sync_global_skills_from_lock

  echo "Done updating. Restart OpenCode if it's open."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
