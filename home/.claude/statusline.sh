#!/usr/bin/env bash
#
# Render Claude Code's status line: model, context usage, cost, duration,
# directory, and git status.

set -euo pipefail

source "${BASH_SOURCE[0]%/*}/statusline-lib.sh"

#######################################
# Build the git branch/status section (staged and modified file counts).
# Globals:
#   COLOR_GREEN, COLOR_YELLOW, COLOR_NC
# Arguments:
#   None
# Outputs:
#   Writes the git section to STDOUT; nothing outside a repo or in detached HEAD.
#######################################
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

#######################################
# Build the current directory section, hyperlinked to the GitHub remote when one exists.
# Arguments:
#   Claude Code's JSON status payload.
# Outputs:
#   Writes the directory section to STDOUT (plain text, or an OSC 8 hyperlink).
#######################################
build_directory_section() {
  local input="$1"
  local dir
  dir=$(echo "$input" | jq -r '.workspace.current_dir')
  local dir_name="${dir##*/}" # Extract just the folder name.
  local remote_url=""

  if git rev-parse --git-dir >/dev/null 2>&1; then
    # No `origin` remote is a normal, non-error case — don't let it trip set -e.
    remote_url=$(git remote get-url origin 2>/dev/null) || true
    remote_url="${remote_url/git@github.com:/https://github.com/}"
    remote_url="${remote_url%.git}"
  fi

  if [[ -n "$remote_url" ]]; then
    # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
    printf '%b' "\e]8;;${remote_url}\a🔗 ${dir_name}\e]8;;\a"
  else
    echo "📁 ${dir_name}"
  fi
}

#######################################
# Build the session duration section.
# Arguments:
#   Claude Code's JSON status payload.
# Outputs:
#   Writes the formatted duration (e.g. "1h 5m") to STDOUT.
#######################################
build_duration_section() {
  local input="$1"
  local duration_ms
  duration_ms=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
  duration_ms="${duration_ms%%.*}" # Integer math below chokes on a float.
  local secs=$((duration_ms / 1000))

  format_elapsed "$secs"
}

#######################################
# Build the session cost section.
# Arguments:
#   Claude Code's JSON status payload.
# Outputs:
#   Writes the formatted cost (e.g. "$0.42") to STDOUT.
#######################################
build_cost_section() {
  local input="$1"
  local cost
  cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')

  printf "💰 \$%.2f" "$cost"
}

#######################################
# Build the context-window usage bar with percentage and token count.
# Arguments:
#   Claude Code's JSON status payload.
# Outputs:
#   Writes the colored usage bar, percentage, and token count to STDOUT.
#######################################
build_bar_section() {
  local input="$1"
  local pct
  pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
  # Input-only tokens currently in the window — same basis as used_percentage.
  local tokens
  tokens=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0' | cut -d. -f1)

  local bar
  bar=$(render_usage_bar "$pct")

  echo "${bar} $(format_usage_text "$pct" "$tokens")"
}

#######################################
# Build the active model name section, including reasoning effort when the
# model supports it.
# Arguments:
#   Claude Code's JSON status payload.
# Outputs:
#   Writes the bracketed, colored model name to STDOUT.
#######################################
build_model_section() {
  local input="$1"
  local model
  model=$(echo "$input" | jq -r '.model.display_name')

  local effort
  effort=$(echo "$input" | jq -r '.effort.level // empty')

  format_model_tag "$model" "$effort"
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
