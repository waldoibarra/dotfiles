#!/usr/bin/env bash

set -euo pipefail

readonly COLOR_MAGENTA="\033[35m"
readonly COLOR_RED="\033[31m"
readonly COLOR_YELLOW="\033[33m"
readonly COLOR_CYAN="\033[36m"
readonly COLOR_GREEN="\033[32m"
readonly COLOR_NC="\033[0m" # No color.

readonly COLOR_CRITICAL="$COLOR_RED"
readonly COLOR_WARNING="$COLOR_YELLOW"
readonly COLOR_HEALTHY="$COLOR_CYAN"

main() {
  local -r _input=$(cat)

  local -r _model_section=$(_build_model_section "$_input")
  local -r _bar_section=$(_build_bar_section "$_input")
  local -r _cost_section=$(_build_cost_section "$_input")
  local -r _duration_section=$(_build_duration_section "$_input")
  local -r _directory_section=$(_build_directory_section "$_input")
  local -r _git_section=$(_build_git_section)

  # Edit order here to rearrange the status line.
  local -a _sections=(
    "$_model_section"
    "$_bar_section"
    "$_cost_section"
    "$_duration_section"
    "$_directory_section"
    "$_git_section"
  )

  _print_status_line "${_sections[@]}"
}

_print_status_line() {
  local _status_line="" _separator="" _section
  for _section in "$@"; do
    [[ -n "$_section" ]] || continue
    _status_line+="${_separator}${_section}"
    _separator=" | "
  done

  printf '%b\n' "$_status_line"
}

_build_model_section() {
  local -r _input="$1"
  local -r _model=$(echo "$_input" | jq -r '.model.display_name')

  echo "${COLOR_MAGENTA}[$_model]${COLOR_NC}"
}

_build_bar_section() {
  local -r _input="$1"
  local -r _pct=$(echo "$_input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
  local -r _width=10
  local -r _filled=$((_pct * _width / 100))
  local -r _empty=$((_width - _filled))
  local _fill="" _pad=""

  ((_filled > 0)) && printf -v _fill '%*s' "$_filled" ""
  ((_empty > 0)) && printf -v _pad '%*s' "$_empty" ""

  local -r _bar_color=$(_get_color_for_bar "$_pct")
  local -r _bar="${_fill// /▓}${_pad// /░}"

  echo "${_bar_color}${_bar}${COLOR_NC} ${_pct}%"
}

_build_cost_section() {
  local -r _input="$1"
  local -r _cost=$(echo "$_input" | jq -r '.cost.total_cost_usd // 0')

  printf "💰 $%.2f" "$_cost"
}

_build_duration_section() {
  local -r _input="$1"
  local -r _duration_ms=$(echo "$_input" | jq -r '.cost.total_duration_ms // 0')
  local -r _secs=$((_duration_ms / 1000))
  local -r _icon="⏱️"

  if ((_secs >= 3600)); then
    echo "$_icon $((_secs / 3600))h $((_secs % 3600 / 60))m"
  elif ((_secs >= 60)); then
    echo "$_icon $((_secs / 60))m $((_secs % 60))s"
  else
    echo "$_icon ${_secs}s"
  fi
}

_build_directory_section() {
  local -r _input="$1"
  local -r _dir=$(echo "$_input" | jq -r '.workspace.current_dir')
  local -r _dir_name="${_dir##*/}" # Extract just the folder name.
  local -r _remote_url=$(git remote get-url origin 2>/dev/null | \
    sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

  if [[ -n "$_remote_url" ]]; then
    # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
    printf '%b' "\e]8;;${_remote_url}\a🔗 ${_dir_name}\e]8;;\a"
  else
    echo "📁 ${_dir_name}"
  fi
}

_build_git_section() {
  local -r _branch=$(git branch --show-current 2>/dev/null)
  local -r _staged=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
  local -r _modified=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

  local _status=""
  ((_staged > 0)) && _status+=" ${COLOR_GREEN}+${_staged}${COLOR_NC}"
  ((_modified > 0)) && _status+=" ${COLOR_YELLOW}~${_modified}${COLOR_NC}"

  if [[ -n "$_branch" ]]; then
    echo "🌳${_status} ${_branch}"
  fi
}

_get_color_for_bar() {
  local -r _pct="$1"

  if ((_pct >= 90)); then
    echo "$COLOR_CRITICAL"
  elif ((_pct >= 70)); then
    echo "$COLOR_WARNING"
  else
    echo "$COLOR_HEALTHY"
  fi
}

main
