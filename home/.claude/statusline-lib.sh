# Shared constants and helpers for the Claude Code status line scripts
# (statusline.sh and subagent-statusline.sh). Sourced, never executed.
# shellcheck shell=bash
# Some constants are consumed only by the sourcing scripts, not in this file.
# shellcheck disable=SC2034

readonly COLOR_MAGENTA="\033[35m"
readonly COLOR_RED="\033[31m"
readonly COLOR_YELLOW="\033[33m"
readonly COLOR_CYAN="\033[36m"
readonly COLOR_GREEN="\033[32m"
readonly COLOR_NC="\033[0m" # No color.

readonly COLOR_CRITICAL="$COLOR_RED"
readonly COLOR_WARNING="$COLOR_YELLOW"
readonly COLOR_HEALTHY="$COLOR_CYAN"

#######################################
# Format a model name (optionally with reasoning effort) into the bracketed,
# colored tag both status lines display.
# Globals:
#   COLOR_MAGENTA, COLOR_NC
# Arguments:
#   Model display name.
#   Reasoning effort level (may be empty).
# Outputs:
#   Writes the bracketed, colored model tag to STDOUT.
#######################################
format_model_tag() {
  local model="$1"
  local effort="$2"

  [[ -n "$effort" ]] && model+=" · ${effort}"

  echo "${COLOR_MAGENTA}[${model}]${COLOR_NC}"
}

#######################################
# Map a percentage to the color for its severity band.
# Globals:
#   COLOR_CRITICAL, COLOR_WARNING, COLOR_HEALTHY
# Arguments:
#   Percentage (0-100).
# Outputs:
#   Writes the matching ANSI color code to STDOUT.
#######################################
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

#######################################
# Draw a colored usage bar for a percentage.
# Globals:
#   COLOR_NC
# Arguments:
#   Percentage (0-100).
# Outputs:
#   Writes the colored ▓/░ bar (without the percentage text) to STDOUT.
#######################################
render_usage_bar() {
  local pct="$1"
  ((pct > 100)) && pct=100
  ((pct < 0)) && pct=0
  local width=10
  local filled=$((pct * width / 100))
  local empty=$((width - filled))
  local fill="" pad=""

  ((filled > 0)) && printf -v fill '%*s' "$filled" ""
  ((empty > 0)) && printf -v pad '%*s' "$empty" ""

  local bar_color
  bar_color=$(get_color_for_bar "$pct")
  local bar="${fill// /▓}${pad// /░}"

  echo "${bar_color}${bar}${COLOR_NC}"
}

#######################################
# Format a token count compactly (e.g. 68231 -> "68.2k").
# Arguments:
#   Token count (integer).
# Outputs:
#   Writes the formatted count to STDOUT.
#######################################
format_token_count() {
  local tokens="$1"

  if ((tokens >= 1000)); then
    printf '%d.%dk' $((tokens / 1000)) $((tokens % 1000 / 100))
  else
    printf '%d' "$tokens"
  fi
}

#######################################
# Format a context-window usage percentage and token count (no bar). Shared
# by the main and subagent status lines, which differ only in whether a bar
# precedes this text.
# Arguments:
#   Percentage (0-100).
#   Token count (integer).
# Outputs:
#   Writes "PCT% · TOKENS" to STDOUT.
#######################################
format_usage_text() {
  local pct="$1"
  local tokens="$2"

  echo "${pct}% · $(format_token_count "$tokens")"
}

#######################################
# Format a duration in seconds as a compact human string (e.g. "1h 5m").
# Arguments:
#   Duration in seconds (integer).
# Outputs:
#   Writes the formatted duration to STDOUT.
#######################################
format_duration() {
  local secs="$1"

  if ((secs >= 3600)); then
    echo "$((secs / 3600))h $((secs % 3600 / 60))m"
  elif ((secs >= 60)); then
    echo "$((secs / 60))m $((secs % 60))s"
  else
    echo "${secs}s"
  fi
}

#######################################
# Format an elapsed-time section (stopwatch emoji + compact duration). Shared
# by the main and subagent status lines.
# Arguments:
#   Duration in seconds (integer).
# Outputs:
#   Writes the formatted elapsed-time section to STDOUT.
#######################################
format_elapsed() {
  echo "⏱️ $(format_duration "$1")"
}

#######################################
# Join non-empty section strings with " | " and print the result.
# Arguments:
#   One or more section strings; empty strings are skipped.
# Outputs:
#   Writes the assembled status line to STDOUT, interpreting \-escapes
#   (e.g. the color codes embedded in each section).
#######################################
print_status_line() {
  local status_line="" separator="" section
  for section in "$@"; do
    [[ -n "$section" ]] || continue
    status_line+="${separator}${section}"
    separator=" | "
  done

  printf '%b\n' "$status_line"
}
