#!/usr/bin/env bash
# Provision machine-local profile links without modifying the shared vault.
set -euo pipefail

if [[ ! -d "${HOME}/life" ]]; then
  exit 0
fi
if [[ -z "${LIFE_PROFILE:-}" ]]; then
  echo 'Warning: ~/life exists but LIFE_PROFILE is empty or unset.' >&2
  echo 'Set export LIFE_PROFILE="<person>" in ~/.zprofile.local; open a new login terminal.' >&2
  exit 0
fi
if [[ ! "${LIFE_PROFILE}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo 'Invalid LIFE_PROFILE: expected a lowercase kebab-case directory name.' >&2
  exit 1
fi

profile_dir="${HOME}/life/people/${LIFE_PROFILE}"
link_names=(personal-context.md agent-identity.md)
source_names=(README.md agent-identity.md)
# Preflight both destinations before changing either link.
for index in 0 1; do
  source_file="${profile_dir}/${source_names[index]}"
  target_file="${HOME}/.agents/${link_names[index]}"
  if [[ ! -f "${source_file}" ]]; then
    echo "Missing profile file: ${source_file}; links unchanged." >&2
    exit 1
  fi
  if [[ -e "${target_file}" && ! -L "${target_file}" ]]; then
    echo "Refusing to overwrite non-symlink: ${target_file}." >&2
    exit 1
  fi
done

mkdir -p "${HOME}/.agents"
for index in 0 1; do
  source_file="${profile_dir}/${source_names[index]}"
  target_file="${HOME}/.agents/${link_names[index]}"
  if [[ -L "${target_file}" && "$(readlink "${target_file}")" == "${source_file}" ]]; then
    continue
  fi
  # -n replaces a symlink to a directory rather than writing inside that directory.
  ln -sfn "${source_file}" "${target_file}"
  echo "Linked ${target_file} to ${source_file}."
done
