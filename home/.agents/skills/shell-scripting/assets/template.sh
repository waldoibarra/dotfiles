#!/usr/bin/env bash
#
# <One-line description of what this script does.>

set -euo pipefail

readonly SCRIPT_NAME="${0##*/}"

#######################################
# Print a timestamped message to STDERR (errors and warnings).
# Globals:
#   SCRIPT_NAME
# Arguments:
#   Message to print.
# Outputs:
#   Writes the message to STDERR.
#######################################
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: ${SCRIPT_NAME}: $*" >&2
}

#######################################
# Build and print a greeting for a name.
# Arguments:
#   Name to greet.
# Outputs:
#   Writes the greeting to STDOUT.
#######################################
greet() {
  local name="$1"

  local greeting
  greeting="$(printf 'Hello, %s!' "${name}")"

  printf '%s\n' "${greeting}"
}

main() {
  greet "world"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
