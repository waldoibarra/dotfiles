#!/usr/bin/env bash
#
# Script copied from dotbot's repository, as indicated in their documentation.
# Updated $BASEDIR to point to the project root, as we copied to scripts/ dir.
# cp dotbot/tools/git-submodule/install scripts/install-dotfiles.sh
#
# Deliberately kept at `set -e` only (not -u/pipefail), matching upstream: this
# script has no pipelines and no optionally-unset variables for -u to guard.

set -e

CONFIG="install.conf.yaml"
DOTBOT_DIR="dotbot"

DOTBOT_BIN="bin/dotbot"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASEDIR="$(dirname "${SCRIPTS_DIR}")"

cd "${BASEDIR}"
git -C "${DOTBOT_DIR}" submodule sync --quiet --recursive
git submodule update --init --recursive "${DOTBOT_DIR}"

"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "${CONFIG}" "${@}"
