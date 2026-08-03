#!/usr/bin/env bash
#
# Render Claude Code's sub-agent panel rows: per-agent model, context usage,
# elapsed time, worktree marker, and task label. Reads the agent-panel JSON
# payload on STDIN and writes one {"id", "content"} JSON line per task.

set -euo pipefail

source "${BASH_SOURCE[0]%/*}/statusline-lib.sh"

#######################################
# Map a raw model ID to a display name (e.g. "claude-haiku-4-5-20251001"
# -> "Haiku 4.5"). The task payload carries the model ID only — unlike the
# main status payload, there is no display_name field.
# Arguments:
#   Model ID string.
# Outputs:
#   Writes the display name to STDOUT; the raw ID when it doesn't parse.
#######################################
format_model_name() {
  local model_id="$1"

  # Strip the "claude-" prefix and the trailing release date.
  local trimmed="${model_id#claude-}"
  if [[ "$trimmed" =~ ^(.*)-[0-9]{8}$ ]]; then
    trimmed="${BASH_REMATCH[1]}"
  fi

  # Non-numeric segments form the family name; numeric ones the version.
  local family="" version="" segment
  local -a segments
  IFS='-' read -ra segments <<<"$trimmed"
  for segment in "${segments[@]}"; do
    if [[ "$segment" =~ ^[0-9]+$ ]]; then
      version+="${version:+.}${segment}"
    else
      local capitalized
      capitalized="$(tr '[:lower:]' '[:upper:]' <<<"${segment:0:1}")${segment:1}"
      family+="${family:+ }${capitalized}"
    fi
  done

  if [[ -n "$family" ]]; then
    echo "${family}${version:+ ${version}}"
  else
    echo "$model_id"
  fi
}

#######################################
# Build a task's label section, flagging worktree-isolated agents.
# Arguments:
#   A single task's JSON object.
#   The main session's working directory (may be empty).
#   The panel's usable row width in columns.
# Outputs:
#   Writes the (truncated) label to STDOUT; nothing when the task has no
#   label, description, or name.
#######################################
build_task_label_section() {
  local task="$1"
  local session_cwd="$2"
  local columns="$3"

  local label
  label=$(jq -r '.label // .description // .name // empty' <<<"$task")
  [[ -n "$label" ]] || return 0

  # Leave room for the model/bar/duration sections that precede the label.
  local max_label_length=$((columns - 45))
  ((max_label_length < 20)) && max_label_length=20
  ((${#label} > max_label_length)) && label="${label:0:max_label_length - 1}…"

  local task_cwd
  task_cwd=$(jq -r '.cwd // empty' <<<"$task")

  local worktree_marker=""
  if [[ -n "$task_cwd" && -n "$session_cwd" && "$task_cwd" != "$session_cwd" ]]; then
    worktree_marker="🌿 "
  fi

  echo "${worktree_marker}${label}"
}

#######################################
# Build a task's elapsed-time section from its start timestamp.
# Arguments:
#   A single task's JSON object.
# Outputs:
#   Writes the formatted elapsed time to STDOUT; nothing when startTime is
#   absent or unparseable.
#######################################
build_task_duration_section() {
  local task="$1"

  # startTime's format is undocumented — accept epoch seconds, epoch
  # milliseconds, or an ISO 8601 string; give up quietly on anything else.
  local start_secs
  start_secs=$(jq -r '
    .startTime // empty
    | if type == "number" then
        (if . > 1e12 then . / 1000 else . end) | floor
      else
        try (sub("\\.[0-9]+"; "") | fromdateiso8601) catch empty
      end' <<<"$task")
  [[ -n "$start_secs" ]] || return 0

  local now_secs
  now_secs=$(date +%s)
  local elapsed_secs=$((now_secs - start_secs))
  ((elapsed_secs < 0)) && elapsed_secs=0

  echo "⏱️ $(format_duration "$elapsed_secs")"
}

#######################################
# Build a task's context usage section: colored bar, percentage, token count.
# Arguments:
#   A single task's JSON object.
# Outputs:
#   Writes the usage section to STDOUT; only the raw token count when the
#   context window size is unavailable (pre-v2.1.205), nothing without both.
#######################################
build_task_context_section() {
  local task="$1"

  local tokens window_size
  tokens=$(jq -r '.tokenCount // 0' <<<"$task")
  window_size=$(jq -r '.contextWindowSize // 0' <<<"$task")
  tokens="${tokens%%.*}"
  window_size="${window_size%%.*}"

  local formatted_tokens
  formatted_tokens=$(format_token_count "$tokens")

  if ((window_size > 0)); then
    local pct=$((tokens * 100 / window_size))
    ((pct > 100)) && pct=100
    echo "$(render_usage_bar "$pct") ${pct}% · ${formatted_tokens}"
  elif ((tokens > 0)); then
    echo "$formatted_tokens"
  fi
}

#######################################
# Build a task's identity section: model tag (with reasoning effort when
# reported) followed by the agent name when the task has one. Agent-tool
# spawns report name=null — the name only exists for explicitly named agents
# (verified empirically on v2.1.220).
# Globals:
#   COLOR_MAGENTA, COLOR_NC
# Arguments:
#   A single task's JSON object.
# Outputs:
#   Writes the identity section to STDOUT; nothing when both the model
#   (pre-v2.1.205) and the name are absent.
#######################################
build_task_identity_section() {
  local task="$1"

  local model model_tag=""
  model=$(jq -r '.model // empty' <<<"$task")
  if [[ -n "$model" ]]; then
    model=$(format_model_name "$model")
    local effort
    effort=$(jq -r '.effort // empty' <<<"$task")
    [[ -n "$effort" ]] && model+=" · ${effort}"
    model_tag="${COLOR_MAGENTA}[${model}]${COLOR_NC}"
  fi

  local agent_name
  agent_name=$(jq -r '.name // empty' <<<"$task")

  if [[ -n "$model_tag" && -n "$agent_name" ]]; then
    echo "${model_tag} ${agent_name}"
  elif [[ -n "$model_tag" ]]; then
    echo "$model_tag"
  elif [[ -n "$agent_name" ]]; then
    echo "$agent_name"
  fi
}

#######################################
# Assemble one task's sections and emit its {"id", "content"} JSON row.
# Arguments:
#   A single task's JSON object.
#   The main session's working directory (may be empty).
#   The panel's usable row width in columns.
# Outputs:
#   Writes one compact JSON row to STDOUT.
#######################################
build_task_row() {
  local task="$1"
  local session_cwd="$2"
  local columns="$3"

  local identity_section
  identity_section=$(build_task_identity_section "$task")
  local context_section
  context_section=$(build_task_context_section "$task")
  local duration_section
  duration_section=$(build_task_duration_section "$task")
  local label_section
  label_section=$(build_task_label_section "$task" "$session_cwd" "$columns")

  # print_status_line interprets the \-escaped colors into real ANSI bytes;
  # jq then JSON-encodes them so Claude Code renders the row as-is.
  local content
  content=$(print_status_line \
    "$identity_section" \
    "$context_section" \
    "$duration_section" \
    "$label_section")

  local task_id
  task_id=$(jq -r '.id' <<<"$task")

  jq -cn --arg id "$task_id" --arg content "$content" '{id: $id, content: $content}'
}

main() {
  local input
  input=$(cat)

  local session_cwd columns
  session_cwd=$(jq -r '.cwd // empty' <<<"$input")
  columns=$(jq -r '.columns // 80' <<<"$input")

  local task
  while IFS= read -r task; do
    [[ -n "$task" ]] || continue
    build_task_row "$task" "$session_cwd" "$columns"
  done < <(jq -c '.tasks[]?' <<<"$input")
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
