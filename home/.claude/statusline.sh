#!/usr/bin/env bash
#
# Render Claude Code's status line: model, context usage, cost, duration,
# directory, and git status.

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

get_color_for_bar() {
  local pct="$1"

  if ((pct >= 90)); then
    echo "$COLOR_CRITICAL"
  elif ((pct >= 70)); then
    echo "$COLOR_WARNING"
  else
    echo "$COLOR_HEALTHY"
  fi
}

print_status_line() {
  local status_line="" separator="" section
  for section in "$@"; do
    [[ -n "$section" ]] || continue
    status_line+="${separator}${section}"
    separator=" | "
  done

  printf '%b\n' "$status_line"
}

build_git_section() {
  # Outside a git repo these all fail loudly (128/129) and, with pipefail,
  # that propagates through the trailing wc/tr stages — bail out early
  # instead of letting `set -e` kill the whole status line.
  git rev-parse --git-dir >/dev/null 2>&1 || return 0

  local branch
  branch=$(git branch --show-current 2>/dev/null)
  [[ -n "$branch" ]] || return 0

  local staged modified
  staged=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
  modified=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

  local status=""
  ((staged > 0)) && status+=" ${COLOR_GREEN}+${staged}${COLOR_NC}"
  ((modified > 0)) && status+=" ${COLOR_YELLOW}~${modified}${COLOR_NC}"

  echo "🌳${status} ${branch}"
}

build_directory_section() {
  local input="$1"
  local dir
  dir=$(echo "$input" | jq -r '.workspace.current_dir')
  local dir_name="${dir##*/}" # Extract just the folder name.
  local remote_url=""

  if git rev-parse --git-dir >/dev/null 2>&1; then
    # No `origin` remote is a normal, non-error case — don't let it trip set -e.
    remote_url=$(git remote get-url origin 2>/dev/null | \
      sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//') || true
  fi

  if [[ -n "$remote_url" ]]; then
    # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
    printf '%b' "\e]8;;${remote_url}\a🔗 ${dir_name}\e]8;;\a"
  else
    echo "📁 ${dir_name}"
  fi
}

build_duration_section() {
  local input="$1"
  local duration_ms
  duration_ms=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
  local secs=$((duration_ms / 1000))
  local icon="⏱️"

  if ((secs >= 3600)); then
    echo "$icon $((secs / 3600))h $((secs % 3600 / 60))m"
  elif ((secs >= 60)); then
    echo "$icon $((secs / 60))m $((secs % 60))s"
  else
    echo "$icon ${secs}s"
  fi
}

build_cost_section() {
  local input="$1"
  local cost
  cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')

  printf "💰 \$%.2f" "$cost"
}

build_bar_section() {
  local input="$1"
  local pct
  pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
  local width=10
  local filled=$((pct * width / 100))
  local empty=$((width - filled))
  local fill="" pad=""

  ((filled > 0)) && printf -v fill '%*s' "$filled" ""
  ((empty > 0)) && printf -v pad '%*s' "$empty" ""

  local bar_color
  bar_color=$(get_color_for_bar "$pct")
  local bar="${fill// /▓}${pad// /░}"

  echo "${bar_color}${bar}${COLOR_NC} ${pct}%"
}

build_model_section() {
  local input="$1"
  local model
  model=$(echo "$input" | jq -r '.model.display_name')

  echo "${COLOR_MAGENTA}[$model]${COLOR_NC}"
}

main() {
  local input
  input=$(cat)

  local model_section
  model_section=$(build_model_section "$input")
  local bar_section
  bar_section=$(build_bar_section "$input")
  local cost_section
  cost_section=$(build_cost_section "$input")
  local duration_section
  duration_section=$(build_duration_section "$input")
  local directory_section
  directory_section=$(build_directory_section "$input")
  local git_section
  git_section=$(build_git_section)

  # Edit order here to rearrange the status line.
  local -a sections=(
    "$model_section"
    "$bar_section"
    "$cost_section"
    "$duration_section"
    "$directory_section"
    "$git_section"
  )

  print_status_line "${sections[@]}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
