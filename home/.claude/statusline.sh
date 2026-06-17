#!/usr/bin/env bash
set -euo pipefail

_parse_input() {
  local -r _input="$1"
  echo "$_input" | jq -r '[
    .model.display_name // "claude",
    (.context_window.used_percentage // 0 | round),
    (.cost.total_cost_usd // 0),
    (.cost.total_duration_ms // 0),
    (.workspace.current_dir // "")
  ] | @tsv'
}

_build_context_bar() {
  local -r _pct="$1"
  local -r _width=10
  local -r _filled=$((_pct * _width / 100))
  local -r _empty=$((_width - _filled))
  local _fill="" _pad=""

  ((_filled > 0)) && printf -v _fill '%*s' "$_filled" ""
  ((_empty > 0)) && printf -v _pad '%*s' "$_empty" ""

  echo "${_fill// /▓}${_pad// /░}"
}

_color_for_pct() {
  local -r _pct="$1"

  if ((_pct >= 90)); then
    printf "%s" "\033[31m" # red: critical
  elif ((_pct >= 70)); then
    printf "%s" "\033[33m" # yellow: warning
  else
    printf "%s" "\033[36m" # cyan: healthy
  fi
}

_format_duration() {
  local -r _ms="$1"
  local -r _s=$((_ms / 1000))

  if ((_s >= 3600)); then
    echo "$((_s / 3600))h $((_s % 3600 / 60))m"
  elif ((_s >= 60)); then
    echo "$((_s / 60))m $((_s % 60))s"
  else
    echo "${_s}s"
  fi
}

_format_cost() {
  local -r _usd="$1"
  printf '$%.2f' "$_usd"
}

_resolve_git() {
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    return
  fi

  local _remote="" _branch _staged _modified

  _remote=$(git remote get-url origin 2>/dev/null |
    sed -E 's/git@github\.com:/https:\/\/github.com\//; s/\.git$//' 2>/dev/null) || true
  _branch=$(git branch --show-current 2>/dev/null)
  _staged=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
  _modified=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

  echo "${_remote}|${_branch}|${_staged}|${_modified}"
}

_format_dir() {
  local -r _dir="$1"
  local -r _remote="$2"
  local -r _dirname="${_dir##*/}"

  if [[ -n "$_remote" ]]; then
    printf '%b' "🔗 \e]8;;${_remote}\a${_dirname}\e]8;;\a"
  else
    printf '%s' "📁 ${_dirname}"
  fi
}

_format_git_status() {
  local -r _branch="$1"
  local -r _staged="$2"
  local -r _modified="$3"
  local -r _green="\033[32m"
  local -r _yellow="\033[33m"
  local -r _reset="\033[0m"

  local _status="🌳 $_branch"
  ((_staged > 0)) && _status+=" ${_green}+${_staged}${_reset}"
  ((_modified > 0)) && _status+=" ${_yellow}~${_modified}${_reset}"

  printf '%s' "$_status"
}

main() {
  local _input
  _input=$(cat)

  local _model _pct _cost_raw _duration_ms _dir
  IFS=$'\t' read -r _model _pct _cost_raw _duration_ms _dir < <(_parse_input "$_input")

  local -r _bar=$(_build_context_bar "$_pct")
  local -r _color=$(_color_for_pct "$_pct")
  local -r _reset="\033[0m"
  local -r _magenta="\033[35m"
  local -r _duration=$(_format_duration "$_duration_ms")
  local -r _cost=$(_format_cost "$_cost_raw")

  local _remote="" _branch="" _staged="0" _modified="0"
  local _git_raw
  _git_raw=$(_resolve_git)
  [[ -n "$_git_raw" ]] && IFS='|' read -r _remote _branch _staged _modified <<<"$_git_raw"

  local -r _dir_display=$(_format_dir "$_dir" "$_remote")
  local _git_status=""
  [[ -n "$_branch" ]] && _git_status=$(_format_git_status "$_branch" "$_staged" "$_modified")

  # Edit order here to rearrange the status line.
  local -a _parts=(
    "${_magenta}[$_model]${_reset}"
    "${_color}${_bar} ${_pct}%${_reset}"
    "💰 $_cost"
    "⏱️ $_duration"
    "$_dir_display"
    "$_git_status"
  )

  local _line="" _sep="" _part
  for _part in "${_parts[@]}"; do
    [[ -n "$_part" ]] || continue
    _line+="${_sep}${_part}"
    _sep=" | "
  done

  printf '%b\n' "$_line"
}

main
