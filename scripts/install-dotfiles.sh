#!/usr/bin/env bash
#
# Script copied from dotbot's repository, as indicated in their documentation.
# Updated $BASEDIR to point to the project root, as we copied to scripts/ dir.
# cp dotbot/tools/git-submodule/install scripts/install-dotfiles.sh

# Bash 3.2 treats empty "$@" as unbound under nounset; preserve argument forwarding.
set -eo pipefail

# Git and Python are prerequisites: neither can be installed by Dotbot itself.
if ! git --version >/dev/null 2>&1; then
  echo "Git is required. Follow docs/setup.md before installing dotfiles." >&2
  exit 1
fi
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 7))' >/dev/null 2>&1; then
  echo "Python 3.7+ is required by Dotbot. Follow docs/setup.md." >&2
  exit 1
fi

# Child installers cannot export PATH back to Dotbot or its subsequent shell steps.
# Include the supported prefix even before Homebrew exists there.
case "$(uname -s)" in
  Darwin) export PATH="${PATH}:/opt/homebrew/bin:/opt/homebrew/sbin" ;;
  Linux) export PATH="${PATH}:/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin" ;;
esac

CONFIG="install.conf.yaml"
DOTBOT_DIR="dotbot"

DOTBOT_BIN="bin/dotbot"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASEDIR="$(dirname "${SCRIPTS_DIR}")"

cd "${BASEDIR}"
git -C "${DOTBOT_DIR}" submodule sync --quiet --recursive
git submodule update --init --recursive "${DOTBOT_DIR}"

"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "${CONFIG}" "${@}"
