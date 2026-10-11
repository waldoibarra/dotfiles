#!/usr/bin/env bash
# Configure Markdown documents to open with Cursor when it is installed.

set -euo pipefail

operating_system="$(uname -s)"
if [[ "${operating_system}" != "Darwin" ]]; then
  exit 0
fi

config="${HOME}/.config/duti/markdown.duti"
if [[ ! -s "${config}" ]]; then
  printf 'Missing or empty Markdown association config: %s\n' "${config}" >&2
  exit 1
fi

read -r bundle_id file_extension role extra < "${config}"
if [[ -z "${bundle_id}" || -z "${file_extension}" || -z "${role}" || -n "${extra}" ]]; then
  printf 'Expected one bundle ID, extension, and role in: %s\n' "${config}" >&2
  exit 1
fi

app_available="$(osascript -l JavaScript -e '
  ObjC.import("AppKit");
  function run(args) {
    return !$.NSWorkspace.sharedWorkspace
      .URLForApplicationWithBundleIdentifier(args[0]).isNil();
  }
' "${bundle_id}")"
if [[ "${app_available}" != "true" ]]; then
  printf 'Skipping Markdown association; application %s is unavailable.\n' "${bundle_id}"
  exit 0
fi

if ! command -v duti >/dev/null 2>&1; then
  printf 'Cannot configure Markdown association: install the duti prerequisite.\n' >&2
  exit 1
fi

current_app="$(duti -x "${file_extension#.}")"
if [[ "${current_app##*$'\n'}" == "${bundle_id}" ]]; then
  printf 'Markdown already opens with %s; no change requested.\n' "${bundle_id}"
  exit 0
fi

duti "${config}"
current_app="$(duti -x "${file_extension#.}")"
if [[ "${current_app##*$'\n'}" != "${bundle_id}" ]]; then
  printf 'Markdown handler is not active yet. Approve any macOS prompt before rerunning.\n' >&2
  exit 1
fi
printf 'Verified Markdown documents open with %s.\n' "${bundle_id}"
