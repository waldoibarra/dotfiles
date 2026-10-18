#!/usr/bin/env bash
#
# Update coding agent tooling: copy managed configs, reconcile Pi packages,
# refresh RTK, Herdr and Moshi integrations, and sync globally installed skills.

set -euo pipefail

ENTRYPOINT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly ENTRYPOINT_DIR
# shellcheck source=../lib/shell-helpers.sh
source "${ENTRYPOINT_DIR}/../lib/shell-helpers.sh"
# shellcheck source=sync-managed-configs.sh
source "${ENTRYPOINT_DIR}/sync-managed-configs.sh"
# shellcheck source=sync-global-skills-from-lock.sh
source "${ENTRYPOINT_DIR}/sync-global-skills-from-lock.sh"

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
# Install a missing or outdated native Herdr integration.
# Claude's installer may add a machine-local hook to its copied settings;
# Pi's installer writes only an extension and requires the directory to exist.
# Arguments:
#   Integration target: claude or pi.
# Outputs:
#   Writes progress to STDOUT and installation failures to STDERR.
#######################################
install_herdr_integration() {
  local agent="$1"
  if ! command -v herdr >/dev/null 2>&1; then
    echo "Herdr not found, skipping ${agent} integration."
    return
  fi
  case "${agent}" in
    pi)
      if ! command -v "${agent}" >/dev/null 2>&1; then
        echo "${agent} not found, skipping Herdr integration."
        return
      fi
      ;;
  esac
  if herdr_integration_is_current "${agent}"; then
    echo "Herdr ${agent} integration already up to date."
    return
  fi
  case "${agent}" in
    pi) mkdir -p "${HOME}/.${agent}/agent/extensions" || return 1 ;;
  esac
  herdr integration install "${agent}" || return 1
  echo "Herdr ${agent} integration installed."
}

#######################################
# Install or refresh an RTK agent integration, if RTK is installed.
# `rtk init --dry-run` always prints "Nothing written"; pending changes show
# up as "[dry-run] would ..." lines instead. Failures only warn, so the
# remaining updater steps still run.
# https://github.com/rtk-ai/rtk/tree/develop/hooks
# Arguments:
#   Integration label for progress messages (e.g. pi).
#   `rtk init` arguments selecting the integration (e.g. -g --agent pi).
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

#######################################
# Install the native RTK extension when the selected agent binary exists.
# Arguments:
#   Agent target, e.g. pi.
# Outputs:
#   Writes progress to STDOUT and warnings to STDERR.
#######################################
install_rtk_agent_extension() {
  local agent="$1"
  if ! command -v "${agent}" >/dev/null 2>&1; then
    echo "${agent} not found, skipping RTK install."
    return
  fi
  install_rtk_integration "${agent}" -g --agent "${agent}"
}

#######################################
# Install the native Moshi extension when Moshi and the agent binary exist.
# Arguments:
#   Agent target, e.g. pi.
# Outputs:
#   Writes installer progress to STDOUT and failures to STDERR.
#######################################
install_moshi_agent_extension() {
  local agent="$1"
  if ! command -v moshi-hook >/dev/null 2>&1 || ! command -v "${agent}" >/dev/null 2>&1; then
    echo "Moshi or ${agent} not found, skipping Moshi integration."
    return
  fi
  # Hook sync must not prompt for or save machine-local first-run preferences.
  moshi-hook install --target "${agent}" </dev/null
}

#######################################
# Reconcile packages declared in Pi's linked settings using the normal profile.
# Globals:
#   HOME
# Outputs:
#   Writes package progress to STDOUT and failures to STDERR.
#######################################
install_pi_packages() (
  if ! command -v pi >/dev/null 2>&1; then
    echo "Pi is required; run the Mise installation before updating agents." >&2
    return 1
  fi
  cd "${HOME}" || return 1
  export PI_CODING_AGENT_DIR="${HOME}/.pi/agent"
  unset OPENAI_API_KEY
  # Pi update skips pinned npm packages, including missing installations.
  local subagent_source
  subagent_source="$(node -e '
    const settings = require(process.argv[1]);
    const source = settings.packages.map(p => typeof p === "string" ? p : p.source)
      .find(p => p.startsWith("npm:pi-subagents@"));
    if (!source) throw new Error("Missing pinned pi-subagents package declaration");
    console.log(source);
  ' "${PI_CODING_AGENT_DIR}/settings.json")" || return 1
  pi install "${subagent_source}" --no-approve || return 1
  pi update --extensions --no-approve
)

main() {
  bash "${ENTRYPOINT_DIR}/sync-life-profile.sh"
  # First: it resets ~/.claude/settings.json to the tracked bytes, which would
  # otherwise discard whatever the Herdr steps below write into that file.
  sync_managed_configs
  python3 "${ENTRYPOINT_DIR}/sync-personal-mcp.py"
  install_pi_packages
  install_rtk_agent_extension pi
  install_herdr_integration claude
  install_herdr_integration pi
  install_moshi_agent_extension pi
  sync_global_skills_from_lock

  echo "Done updating. Restart Claude Code and Pi if they are open."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
