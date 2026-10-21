#!/usr/bin/env bash
# Render the Cursor template without treating its marker as a native import.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
template_file="${repo_root}/home/.cursor/rules/global-instructions.mdc"
instructions_file="${HOME}/.agents/AGENTS.md"
target_file="${HOME}/.cursor/rules/global-instructions.mdc"
marker='@~/.agents/AGENTS.md'

# Sentinels preserve trailing newlines normally stripped by command substitution.
template="$(cat "${template_file}" && printf '.')"
template="${template%.}"
if [[ "${template}" != *"${marker}"* ]]; then
  echo "Expected exactly one ${marker} marker in ${template_file}" >&2
  exit 1
fi
prefix="${template%%"${marker}"*}"
suffix="${template#*"${marker}"}"
if [[ "${suffix}" == *"${marker}"* ]]; then
  echo "Expected exactly one ${marker} marker in ${template_file}" >&2
  exit 1
fi
instructions="$(cat "${instructions_file}" && printf '.')"
instructions="${instructions%.}"

mkdir -p "$(dirname "${target_file}")"
staging="$(mktemp "${target_file}.tmp.XXXXXX")"
trap 'rm -f "${staging}"' EXIT
printf '%s%s%s' "${prefix}" "${instructions}" "${suffix}" >"${staging}"
chmod 644 "${staging}"

if [[ ! -L "${target_file}" && -f "${target_file}" ]] && cmp -s "${staging}" "${target_file}"; then
  # Portable across BSD and GNU stat; avoid chmod when the desired mode already matches.
  if [[ "$(find "${target_file}" -prune -perm 0644 -print)" != "${target_file}" ]]; then
    chmod 644 "${target_file}"
  fi
else
  if [[ -d "${target_file}" ]]; then
    echo "Refusing to replace directory ${target_file}" >&2
    exit 1
  fi
  mv -f "${staging}" "${target_file}"
fi
printf '%s\n' 'Cursor global instructions synchronized as a regular file.'
