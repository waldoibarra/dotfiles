#!/usr/bin/env bash
#
# Ensure /etc/sudoers.d/timestamp_type sets timestamp_type=global so sudo
# credentials are cached per-user (shared across TTYs) rather than per-TTY.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPTS_DIR
source "${SCRIPTS_DIR}/lib/shell-helpers.sh"

readonly SUDOERS_FILE="/etc/sudoers.d/timestamp_type"
readonly SUDOERS_DIRECTIVE="Defaults timestamp_type=global"

print_separator "Configuring sudo timestamp type"

if [[ -f "${SUDOERS_FILE}" ]] && grep -qx "${SUDOERS_DIRECTIVE}" "${SUDOERS_FILE}"; then
  echo "Sudo timestamp type is already global. ✅"
  exit 0
fi

echo "Writing ${SUDOERS_FILE} to set timestamp_type=global."
echo "${SUDOERS_DIRECTIVE}" | sudo tee "${SUDOERS_FILE}" >/dev/null
sudo chmod 444 "${SUDOERS_FILE}"
echo "Set sudo timestamp type to global. ✅"
