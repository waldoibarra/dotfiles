# Delivers the four gentle-ai-managed configs into $HOME, then syncs and trims
# the layer `gentle-ai sync` generates from them.
#
# `gentle-ai sync` refuses to write through a symlinked target file, so those
# four configs are copied out of the repo instead of being symlinked by Dotbot —
# which makes the copy step here their only delivery mechanism, and the reason it
# runs whether or not gentle-ai is installed. Everything sync generates is
# machine-local and untracked. See docs/coding-agents.md for the marker map and
# the update procedure.

readonly GENTLE_AI_STATE_FILE="$HOME/.gentle-ai/state.json"
readonly GENTLE_AI_VERSION_STAMP_FILE="$HOME/.gentle-ai/.dotfiles-last-synced-version"
readonly CLAUDE_SETTINGS_FILE="$HOME/.claude/settings.json"
readonly CLAUDE_MEMORY_FILE="$HOME/.claude/CLAUDE.md"
readonly OPENCODE_MEMORY_FILE="$HOME/.config/opencode/AGENTS.md"
readonly ORCHESTRATOR_AGENT_FILE="$HOME/.claude/agents/gentle-orchestrator.md"
readonly OPENCODE_SKILLS_DIR="$HOME/.config/opencode/skills"

# Configs `gentle-ai sync` rewrites in place, as paths relative to both the
# repo's home/ directory and $HOME. Dotbot excludes them from its globs, so the
# copy step below is the only thing that propagates the repo sources.
readonly GENTLE_AI_MANAGED_CONFIGS=(
  ".claude/CLAUDE.md"
  ".claude/settings.json"
  ".config/opencode/AGENTS.md"
  ".config/opencode/opencode.json"
)

# Marker sections `gentle-ai sync` is expected to write into each memory file.
# The assertion below fails the sync when this stops matching reality, because
# every step after it (extract, strip) is written against exactly this set.
readonly CLAUDE_MEMORY_MARKERS=(persona engram-protocol sdd-orchestrator agent-routing)
readonly OPENCODE_MEMORY_MARKERS=(persona engram-protocol)

# Marker sections stripped back out after the orchestrator agent is built.
# CLAUDE.md keeps nothing: it is a one-line `@`-import of AGENTS.md, so anything
# gentle-ai adds there is either a duplicate of AGENTS.md or belongs in the
# sub-agent prompt instead of every session's ambient context.
readonly CLAUDE_STRIPPED_MARKERS=("${CLAUDE_MEMORY_MARKERS[@]}")
readonly OPENCODE_STRIPPED_MARKERS=(persona)

# Per-phase Claude models seeded into gentle-ai's state file on first run only.
# Architect phases get opus, implementation phases sonnet.
readonly SEEDED_CLAUDE_PHASE_ASSIGNMENTS='{
  "sdd-propose": { "model": "opus" },
  "sdd-design": { "model": "opus" },
  "sdd-apply": { "model": "sonnet" },
  "sdd-tasks": { "model": "sonnet" }
}'

# Frontmatter description of the generated orchestrator agent. Wrapped with line
# continuations only to stay inside the 100-column limit; it is written as a
# single line, which is what Claude Code's agent frontmatter requires.
readonly ORCHESTRATOR_DESCRIPTION="SDD/RDD orchestration - coordinates sdd-* and review \
sub-agents; never does work inline. Use for SDD workflows, RDD reviews, and multi-agent \
implementation."

# Floor for the extracted orchestrator prompt. The two sections together are
# ~23 KB; anything much smaller means the extraction silently matched nothing.
readonly MIN_ORCHESTRATOR_PROMPT_BYTES=15000

# Mode the managed configs are left with. mktemp creates 0600, so every rewrite
# has to put this back or the files silently drift to owner-only.
readonly MANAGED_CONFIG_MODE=644

#######################################
# Replace a file with the output of a command. The output is buffered in a temp
# file and only put in place once the command succeeded, so a failing command
# leaves the original untouched. The move is atomic only while $TMPDIR shares a
# filesystem with the target, which is the normal case on both macOS and Linux.
# Globals:
#   MANAGED_CONFIG_MODE
# Arguments:
#   Path to the file to replace.
#   Remaining args: the command to run, which usually reads that same path.
# Returns:
#   0 on success, 1 when the command failed.
#######################################
rewrite_file_with_output() {
  local -r file="$1"
  shift

  local temp_file
  temp_file="$(mktemp)"
  if ! "$@" >"$temp_file"; then
    rm -f "$temp_file"
    return 1
  fi

  mv "$temp_file" "$file"
  chmod "$MANAGED_CONFIG_MODE" "$file"
}

#######################################
# Print a file with the named gentle-ai marker sections removed.
#
# Removing a section leaves a run of blank lines behind, so runs of blank lines
# are collapsed to a single one — everywhere in the file, not only at the removal
# sites, which is what makes a second run on an already-stripped file
# byte-identical. Leading and trailing blank lines are dropped for the same
# reason. The tracked repo sources must therefore never rely on consecutive blank
# lines surviving; they are Markdown and JSON, where that never matters.
# Arguments:
#   Path to the file to read.
#   Remaining args: marker names to remove, e.g. persona agent-routing.
# Outputs:
#   Writes the stripped file to STDOUT.
#######################################
strip_marker_sections() {
  local -r file="$1"
  shift

  awk -v names="$*" '
    BEGIN {
      count = split(names, name_list, " ")
      for (i = 1; i <= count; i++) {
        open_marker = "<!-- gentle-ai:" name_list[i] " -->"
        close_marker_of[open_marker] = "<!-- /gentle-ai:" name_list[i] " -->"
      }
    }
    inside {
      if ($0 == expected_close_marker) { inside = 0 }
      next
    }
    $0 in close_marker_of {
      inside = 1
      expected_close_marker = close_marker_of[$0]
      next
    }
    /^[[:space:]]*$/ { blank_pending = 1; next }
    {
      if (kept_any && blank_pending) { print "" }
      blank_pending = 0
      kept_any = 1
      print
    }
  ' "$file"
}

#######################################
# Print the body of one gentle-ai marker section, markers excluded.
# Arguments:
#   Path to the file to read.
#   Marker name, e.g. sdd-orchestrator.
# Outputs:
#   Writes the section body to STDOUT, or nothing when the marker is absent.
#######################################
extract_marker_section() {
  local -r file="$1"
  local -r name="$2"

  awk -v open_marker="<!-- gentle-ai:$name -->" \
    -v close_marker="<!-- /gentle-ai:$name -->" '
    $0 == close_marker { inside = 0; next }
    inside { print }
    $0 == open_marker { inside = 1 }
  ' "$file"
}

#######################################
# Verify a file carries exactly the expected gentle-ai marker sections, each
# exactly once. Guards every later step: the extract and strip lists are written
# against this inventory, so a renamed, added, or dropped upstream section has
# to fail loudly instead of silently leaving content behind.
# Arguments:
#   Path to the file to check.
#   Remaining args: expected marker names.
# Outputs:
#   Writes the offending marker names, and a pointer to the update procedure,
#   to STDERR on mismatch.
# Returns:
#   0 when the inventory matches, 1 otherwise.
#######################################
assert_marker_inventory() {
  local -r file="$1"
  shift

  if [[ ! -f "$file" ]]; then
    echo "gentle-ai sync produced no $file." >&2
    echo "Follow the update procedure in docs/coding-agents.md, then re-run the sync." >&2
    return 1
  fi

  # A file with no markers at all is itself one of the mismatches to report, but
  # it also makes grep exit 1 — capture first so pipefail cannot abort the script
  # before the diagnostic below gets printed.
  local marker_matches
  marker_matches="$(grep -o 'gentle-ai:[a-z-]*' "$file" || true)"
  local present_names
  present_names="$(sort -u <<<"${marker_matches//gentle-ai:/}")"

  local mismatches="" name

  local unexpected_names=""
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    if ! printf '%s\n' "$@" | grep -qxF "$name"; then
      unexpected_names+="$name "
    fi
  done <<<"$present_names"
  if [[ -n "$unexpected_names" ]]; then
    mismatches+=" unexpected: $unexpected_names"
  fi

  local missing_names=""
  for name in "$@"; do
    if ! grep -qxF "$name" <<<"$present_names"; then
      missing_names+="$name "
    fi
  done
  if [[ -n "$missing_names" ]]; then
    mismatches+=" missing: $missing_names"
  fi

  local open_count close_count
  for name in "$@"; do
    open_count="$(grep -c "^<!-- gentle-ai:$name -->\$" "$file" || true)"
    close_count="$(grep -c "^<!-- /gentle-ai:$name -->\$" "$file" || true)"
    if [[ "$open_count" != 1 || "$close_count" != 1 ]]; then
      mismatches+=" not exactly once: $name (open x$open_count, close x$close_count)"
    fi
  done

  if [[ -z "$mismatches" ]]; then
    return 0
  fi

  echo "gentle-ai marker inventory changed in $file —$mismatches." >&2
  echo "Follow the update procedure in docs/coding-agents.md, then re-run the sync." >&2
  return 1
}

#######################################
# Report gentle-ai's own health check. Never fatal: engram and gga are separate
# formulae that may still be installing, or intentionally not running.
# Outputs:
#   Writes the doctor report to STDOUT and a warning to STDERR when unhealthy.
#######################################
run_gentle_ai_doctor() {
  if ! gentle-ai doctor; then
    echo "Warning: 'gentle-ai doctor' reports problems (see its output above)." >&2
  fi
}

#######################################
# Announce a gentle-ai version change so the generated layer gets reviewed
# against the new release, and record the version that was synced.
# Globals:
#   GENTLE_AI_VERSION_STAMP_FILE
# Outputs:
#   Writes a review notice to STDOUT on the first run and after every upgrade.
#######################################
notify_on_gentle_ai_version_change() {
  # `gentle-ai version` prints "gentle-ai <semver>"; keep only the number.
  local current_version
  current_version="$(gentle-ai version | awk '{ print $NF }')"

  local recorded_version=""
  if [[ -f "$GENTLE_AI_VERSION_STAMP_FILE" ]]; then
    recorded_version="$(cat "$GENTLE_AI_VERSION_STAMP_FILE")"
  fi
  if [[ "$current_version" == "$recorded_version" ]]; then
    return 0
  fi

  echo
  echo "**************************************************************************"
  echo "gentle-ai changed: ${recorded_version:-<none>} -> $current_version"
  echo "Review its upstream changes against docs/coding-agents.md — the marker map,"
  echo "the generated gentle-orchestrator agent and the settings.json hook are all"
  echo "pinned to a specific upstream shape."
  echo "**************************************************************************"
  echo

  mkdir -p "$(dirname "$GENTLE_AI_VERSION_STAMP_FILE")"
  echo "$current_version" >"$GENTLE_AI_VERSION_STAMP_FILE"
}

#######################################
# Drop the output style `gentle-ai sync` forces into Claude Code's settings. It
# is the one settings key sync writes that the tracked source does not already
# carry, so removing it keeps the copy equivalent to the repo source.
# Globals:
#   CLAUDE_SETTINGS_FILE
#######################################
remove_claude_output_style() {
  rewrite_file_with_output "$CLAUDE_SETTINGS_FILE" \
    jq 'del(.outputStyle)' "$CLAUDE_SETTINGS_FILE"
}

#######################################
# Strip the gentle-ai sections that should not be ambient context out of both
# memory files. CLAUDE.md keeps nothing at all; AGENTS.md keeps the engram
# protocol and loses only the persona, which conflicts with the tracked one.
# Globals:
#   CLAUDE_MEMORY_FILE
#   CLAUDE_STRIPPED_MARKERS
#   OPENCODE_MEMORY_FILE
#   OPENCODE_STRIPPED_MARKERS
# Outputs:
#   Writes progress to STDOUT.
#######################################
strip_ambient_marker_sections() {
  rewrite_file_with_output "$CLAUDE_MEMORY_FILE" \
    strip_marker_sections "$CLAUDE_MEMORY_FILE" \
    ${CLAUDE_STRIPPED_MARKERS[@]+"${CLAUDE_STRIPPED_MARKERS[@]}"}
  rewrite_file_with_output "$OPENCODE_MEMORY_FILE" \
    strip_marker_sections "$OPENCODE_MEMORY_FILE" \
    ${OPENCODE_STRIPPED_MARKERS[@]+"${OPENCODE_STRIPPED_MARKERS[@]}"}

  echo "Stripped the non-ambient gentle-ai sections from CLAUDE.md and AGENTS.md."
}

#######################################
# Regenerate the gentle-orchestrator sub-agent from the two orchestration
# sections gentle-ai writes into CLAUDE.md. Must run before those sections are
# stripped. Deliberately declares no `tools` key, so the agent inherits every
# tool — including Agent, without which it could not delegate at all.
# This writes into ~/.claude/agents/ assuming it is a real, machine-local
# directory. Never track a home/.claude/agents/ directory in this repo: the
# Dotbot home/.claude/* glob would symlink it, and this write (plus gentle-ai's
# ~20 generated agents) would land in the working tree.
# Globals:
#   CLAUDE_MEMORY_FILE
#   MIN_ORCHESTRATOR_PROMPT_BYTES
#   ORCHESTRATOR_AGENT_FILE
#   ORCHESTRATOR_DESCRIPTION
# Outputs:
#   Writes progress to STDOUT and an error to STDERR when the prompt is short.
# Returns:
#   0 on success, 1 when the extracted prompt is implausibly small.
#######################################
build_orchestrator_agent() {
  local orchestrator_section routing_section
  orchestrator_section="$(extract_marker_section "$CLAUDE_MEMORY_FILE" sdd-orchestrator)"
  routing_section="$(extract_marker_section "$CLAUDE_MEMORY_FILE" agent-routing)"

  local prompt_body prompt_bytes
  prompt_body="$(printf '%s\n\n%s\n' "$orchestrator_section" "$routing_section")"
  prompt_bytes="$(printf '%s' "$prompt_body" | wc -c | tr -d '[:space:]')"
  if ((prompt_bytes < MIN_ORCHESTRATOR_PROMPT_BYTES)); then
    echo "Extracted only $prompt_bytes bytes of orchestrator prompt from" \
      "$CLAUDE_MEMORY_FILE, expected at least $MIN_ORCHESTRATOR_PROMPT_BYTES." \
      "Follow the update procedure in docs/coding-agents.md." >&2
    return 1
  fi

  mkdir -p "$(dirname "$ORCHESTRATOR_AGENT_FILE")"
  cat >"$ORCHESTRATOR_AGENT_FILE" <<EOF
---
name: gentle-orchestrator
description: $ORCHESTRATOR_DESCRIPTION
model: fable
---
$prompt_body
EOF

  echo "Built $ORCHESTRATOR_AGENT_FILE ($prompt_bytes bytes of prompt)."
}

#######################################
# Verify both memory files carry exactly the marker inventory the later steps
# are written against.
# Globals:
#   CLAUDE_MEMORY_FILE
#   CLAUDE_MEMORY_MARKERS
#   OPENCODE_MEMORY_FILE
#   OPENCODE_MEMORY_MARKERS
# Returns:
#   0 when both inventories match, 1 otherwise.
#######################################
assert_marker_inventories() {
  assert_marker_inventory "$CLAUDE_MEMORY_FILE" \
    ${CLAUDE_MEMORY_MARKERS[@]+"${CLAUDE_MEMORY_MARKERS[@]}"}
  assert_marker_inventory "$OPENCODE_MEMORY_FILE" \
    ${OPENCODE_MEMORY_MARKERS[@]+"${OPENCODE_MEMORY_MARKERS[@]}"}
}

#######################################
# Run `gentle-ai sync` non-interactively for both agents, in multi-agent SDD
# mode with generated per-phase OpenCode profiles.
# Outputs:
#   Writes gentle-ai's own output to STDOUT/STDERR.
# Returns:
#   gentle-ai's exit status.
#######################################
run_gentle_ai_sync() {
  GENTLE_AI_YES=1 GENTLE_AI_NO_SELF_UPDATE=1 gentle-ai sync \
    --agent claude-code,opencode \
    --sdd-mode multi \
    --sdd-profile-strategy generated-multi
}

#######################################
# Seed the per-phase Claude model assignments gentle-ai reads when it writes the
# `model:` frontmatter of the generated sdd-* agents. Written only when the key
# is absent, so a later change made through gentle-ai's TUI survives every sync.
# Globals:
#   GENTLE_AI_STATE_FILE
#   SEEDED_CLAUDE_PHASE_ASSIGNMENTS
# Outputs:
#   Writes progress to STDOUT.
#######################################
seed_claude_phase_assignments() {
  mkdir -p "$(dirname "$GENTLE_AI_STATE_FILE")"
  if [[ ! -f "$GENTLE_AI_STATE_FILE" || ! -s "$GENTLE_AI_STATE_FILE" ]]; then
    echo '{}' >"$GENTLE_AI_STATE_FILE"
  fi
  # A whitespace-only or otherwise non-object file (crash artifact) would make
  # the seeding jq below emit nothing and "succeed", truncating the state file.
  if ! jq -e 'type == "object"' "$GENTLE_AI_STATE_FILE" >/dev/null; then
    echo "${GENTLE_AI_STATE_FILE} is not a JSON object; refusing to seed the" \
      "model assignments. Inspect or delete it, then re-run the sync." >&2
    return 1
  fi
  if jq -e 'has("claude_phase_assignments")' "$GENTLE_AI_STATE_FILE" >/dev/null; then
    return 0
  fi

  # shellcheck disable=SC2016  # $assignments is a jq variable, not a shell one.
  rewrite_file_with_output "$GENTLE_AI_STATE_FILE" \
    jq --argjson assignments "$SEEDED_CLAUDE_PHASE_ASSIGNMENTS" \
    '.claude_phase_assignments = $assignments' "$GENTLE_AI_STATE_FILE"

  echo "Seeded the gentle-ai per-phase Claude model assignments."
}

#######################################
# Refuse to sync while the OpenCode skills directory is still the old Dotbot
# directory symlink. `gentle-ai sync` writes ~20 skill directories in there and
# happily follows a symlinked parent, so it would commit them into this repo.
# Dotbot owns the migration off that symlink; this only refuses to run before it.
# Globals:
#   OPENCODE_SKILLS_DIR
# Outputs:
#   Writes an error to STDERR when the directory is still a symlink.
# Returns:
#   0 when it is safe to sync, 1 otherwise.
#######################################
assert_opencode_skills_dir_is_real() {
  if [[ ! -L "$OPENCODE_SKILLS_DIR" ]]; then
    return 0
  fi

  echo "$OPENCODE_SKILLS_DIR is still a symlink into this repo, and" \
    "'gentle-ai sync' would write its generated skills through it." \
    "Run 'just sync' first so Dotbot replaces it with a real directory." >&2
  return 1
}

#######################################
# Run `gentle-ai sync` and reduce what it generated to what should stay ambient:
# harvest the two orchestration sections into a sub-agent, strip every injected
# section back out, and undo the one settings key sync adds.
# Outputs:
#   Writes progress to STDOUT.
# Returns:
#   0 on success, non-zero when sync failed or the layer changed shape.
#######################################
sync_gentle_ai_generated_layer() {
  assert_opencode_skills_dir_is_real
  seed_claude_phase_assignments
  run_gentle_ai_sync
  assert_marker_inventories
  build_orchestrator_agent
  strip_ambient_marker_sections
  remove_claude_output_style
  notify_on_gentle_ai_version_change
  run_gentle_ai_doctor
}

#######################################
# Replace the $HOME copy of every gentle-ai-managed config with the repo source,
# dropping any leftover Dotbot symlink first. Dotbot does not link these, so this
# is their only delivery mechanism — and it doubles as the garbage collector for
# the generated layer: sync only ever adds marker sections, never prunes them, so
# every run has to start from the tracked bytes.
# Globals:
#   ENTRYPOINT_DIR
#   GENTLE_AI_MANAGED_CONFIGS
#   HOME
#   MANAGED_CONFIG_MODE
# Outputs:
#   Writes progress to STDOUT, and an error to STDERR when a source is missing.
# Returns:
#   0 on success, 1 when the repo or one of its sources cannot be found.
#######################################
copy_managed_configs_from_repo() {
  local repo_root
  if ! repo_root="$(git -C "$ENTRYPOINT_DIR" rev-parse --show-toplevel 2>/dev/null)"; then
    echo "Cannot resolve the dotfiles repo root from $ENTRYPOINT_DIR;" \
      "the gentle-ai-managed configs cannot be refreshed." >&2
    return 1
  fi

  local relative_path source_file target_file
  for relative_path in ${GENTLE_AI_MANAGED_CONFIGS[@]+"${GENTLE_AI_MANAGED_CONFIGS[@]}"}; do
    source_file="$repo_root/home/$relative_path"
    target_file="$HOME/$relative_path"

    if [[ ! -f "$source_file" ]]; then
      echo "Missing repo source $source_file; cannot refresh $target_file." >&2
      return 1
    fi

    if [[ -L "$target_file" ]]; then
      rm "$target_file"
    fi
    mkdir -p "$(dirname "$target_file")"
    cp "$source_file" "$target_file"
    chmod "$MANAGED_CONFIG_MODE" "$target_file"
  done

  echo "Copied ${#GENTLE_AI_MANAGED_CONFIGS[@]} gentle-ai-managed configs from the repo."
}

#######################################
# Deliver the gentle-ai-managed configs, then sync gentle-ai's generated layer on
# top of them. The copy runs unconditionally because Dotbot no longer links those
# files; only the generated layer needs the gentle-ai binary.
# Outputs:
#   Writes progress to STDOUT via print_separator.
# Returns:
#   0 on success, non-zero when a step failed.
#######################################
sync_gentle_ai_assets() {
  print_separator "Synchronizing gentle-ai assets"

  copy_managed_configs_from_repo
  if command -v gentle-ai >/dev/null 2>&1; then
    sync_gentle_ai_generated_layer
  else
    echo "gentle-ai not found, skipping its generated layer;" \
      "the configs copied above are still up to date."
  fi

  print_separator "Done synchronizing gentle-ai assets"
}
