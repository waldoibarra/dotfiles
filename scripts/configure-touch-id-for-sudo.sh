#!/usr/bin/env bash
#
# Ensure /etc/pam.d/sudo_local enables Touch ID (pam_tid.so) for sudo, so the
# terminal authenticates via Touch ID instead of a password prompt. Built from
# Apple's /etc/pam.d/sudo_local.template (uncommented). The sudo_local file
# survives system updates: /etc/pam.d/sudo includes it on macOS Sonoma and
# later, and Apple does not overwrite it (unlike /etc/pam.d/sudo itself).

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPTS_DIR
source "${SCRIPTS_DIR}/lib/shell-helpers.sh"

readonly PAM_FILE="/etc/pam.d/sudo_local"
readonly PAM_TEMPLATE="/etc/pam.d/sudo_local.template"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Not on macOS; skipping Touch ID for sudo."
  exit 0
fi

print_separator "Configuring Touch ID for sudo"

if [[ -f "${PAM_FILE}" ]] && grep -Eq '^[^#]*pam_tid\.so' "${PAM_FILE}"; then
  echo "Touch ID for sudo is already enabled."
  exit 0
fi

if [[ ! -f "${PAM_TEMPLATE}" ]]; then
  echo "PAM template ${PAM_TEMPLATE} not found; cannot configure Touch ID." >&2
  exit 1
fi

echo "Writing ${PAM_FILE} from ${PAM_TEMPLATE} to enable Touch ID for sudo."
sed '/pam_tid\.so/s/^[[:space:]]*#//' "${PAM_TEMPLATE}" | sudo tee "${PAM_FILE}" >/dev/null
sudo chmod 444 "${PAM_FILE}"
echo "Enabled Touch ID for sudo."
