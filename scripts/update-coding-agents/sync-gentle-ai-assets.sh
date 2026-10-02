# Delivers the four gentle-ai-managed configs into $HOME, then syncs and trims
# the layer `gentle-ai sync` generates from them.
#
# `gentle-ai sync` refuses to write through a symlinked target file, so those
# four configs are copied out of the repo instead of being symlinked by Dotbot —
# which makes the copy step here their only delivery mechanism, and the reason it
# runs whether or not gentle-ai is installed. Everything sync generates is
# machine-local and untracked. See docs/coding-agents.md for the marker map and
# the update procedure.

readonly GENTLE_AI_VERSION_STAMP_FILE="$HOME/.gentle-ai/.dotfiles-last-synced-version"
readonly CLAUDE_SETTINGS_FILE="$HOME/.claude/settings.json"
readonly CLAUDE_MEMORY_FILE="$HOME/.claude/CLAUDE.md"
readonly CLAUDE_AGENTS_DIR="$HOME/.claude/agents"
readonly OPENCODE_MEMORY_FILE="$HOME/.config/opencode/AGENTS.md"
readonly ORCHESTRATOR_AGENT_FILE="$CLAUDE_AGENTS_DIR/gentle-orchestrator.md"
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
# `remote-authorization` is nested inside `agent-routing` in gentle-ai 4.0.
# It reaches the orchestrator agent through extraction and is removed along
# with its outer section when the ambient memory is stripped.
readonly CLAUDE_MEMORY_MARKERS=(
  persona engram-protocol orchestrator agent-routing remote-authorization
)
readonly OPENCODE_MEMORY_MARKERS=(persona engram-protocol)

# Marker sections stripped back out after the orchestrator agent is built.
# CLAUDE.md keeps nothing: it is a one-line `@`-import of AGENTS.md, so anything
# gentle-ai adds there is either a duplicate of AGENTS.md or belongs in the
# sub-agent prompt instead of every session's ambient context.
readonly CLAUDE_STRIPPED_MARKERS=("${CLAUDE_MEMORY_MARKERS[@]}")
readonly OPENCODE_STRIPPED_MARKERS=(persona)

# Frontmatter description of the generated orchestrator agent. Wrapped with line
# continuations only to stay inside the 100-column limit; it is written as a
# single line, which is what Claude Code's agent frontmatter requires.
readonly ORCHESTRATOR_DESCRIPTION="ODD/RDD orchestration - coordinates substantial \
implementation and reviews through delegated workers; handles small bounded work inline. \
Use for ODD workflows, RDD reviews, and multi-agent implementation."

# Mode the managed configs are left with. mktemp creates 0600, so every rewrite
# has to put this back or the files silently drift to owner-only.
readonly MANAGED_CONFIG_MODE=644

# The engram MCP tool prefix gentle-ai generates, and the one it has to become.
# Claude Code namespaces MCP tools after the server key, so the plain user-scope
# registration yields mcp__engram__*. gentle-ai agents instead hardcode the
# mcp__plugin_<plugin>_<server>__ form of a plugin-hosted server, which resolves
# to nothing here. The strings are baked into the gentle-ai binary with no format
# string behind them, so no upstream flag can change what it emits.
readonly UPSTREAM_ENGRAM_TOOL_PREFIX="mcp__plugin_engram_engram__"
readonly REGISTERED_ENGRAM_TOOL_PREFIX="mcp__engram__"

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
  temp_file="$(mktemp)" || return 1
  if ! "$@" >"$temp_file"; then
    rm -f "$temp_file"
    return 1
  fi

  if ! mv "$temp_file" "$file"; then
    rm -f "$temp_file"
    return 1
  fi
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
    END {
      if (inside) {
        print "Unclosed gentle-ai section in " FILENAME > "/dev/stderr"
        exit 1
      }
    }
  ' "$file"
}

#######################################
# Print the body of one gentle-ai marker section, markers excluded.
# Arguments:
#   Path to the file to read.
#   Marker name, e.g. orchestrator.
# Outputs:
#   Writes the section body to STDOUT, or an error to STDERR for invalid extraction.
# Returns:
#   0 for one ordered, nonempty section, 1 otherwise.
#######################################
extract_marker_section() {
  local -r file="$1"
  local -r name="$2"

  awk -v open_marker="<!-- gentle-ai:$name -->" \
    -v close_marker="<!-- /gentle-ai:$name -->" '
    $0 == open_marker {
      if (opened++ || closed) { invalid = 1 }
      inside = 1
      next
    }
    $0 == close_marker {
      if (!inside || closed++) { invalid = 1 }
      inside = 0
      next
    }
    inside {
      print
      if ($0 ~ /[^[:space:]]/ && $0 !~ /^<!-- \/?gentle-ai:/) { nonempty = 1 }
    }
    END {
      if (invalid || inside || opened != 1 || closed != 1 || !nonempty) {
        print "Invalid or empty gentle-ai section " open_marker " in " FILENAME > "/dev/stderr"
        exit 1
      }
    }
  ' "$file"
}

#######################################
# Verify the exact marker inventory, syntax, ordering, nesting and nonempty bodies.
# Only remote-authorization may be nested, directly inside agent-routing.
# Guards every later step: a changed upstream contract must fail loudly before
# building a partial prompt or stripping the wrong ambient context.
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

  if awk -v names="$*" '
    BEGIN {
      count = split(names, expected, " ")
      for (i = 1; i <= count; i++) { allowed[expected[i]] = 1 }
      parent["remote-authorization"] = "agent-routing"
    }
    /gentle-ai:/ {
      if ($0 !~ /^<!-- \/?gentle-ai:[a-z][a-z-]* -->$/) {
        print "Malformed gentle-ai marker at line " NR > "/dev/stderr"
        invalid = 1
        next
      }
      name = $0
      sub(/^<!-- \/?gentle-ai:/, "", name)
      sub(/ -->$/, "", name)
      if (!(name in allowed)) {
        print "Unexpected gentle-ai marker: " name > "/dev/stderr"
        invalid = 1
      }
      if ($0 ~ /^<!-- gentle-ai:/) {
        if (++opened[name] != 1 || stack[depth] != parent[name]) {
          print "Duplicate or wrongly nested gentle-ai marker: " name > "/dev/stderr"
          invalid = 1
        }
        stack[++depth] = name
      } else {
        if (++closed[name] != 1 || depth == 0 || stack[depth] != name) {
          print "Unbalanced gentle-ai marker: " name > "/dev/stderr"
          invalid = 1
          next
        }
        delete stack[depth--]
      }
      next
    }
    /[^[:space:]]/ {
      for (i = 1; i <= depth; i++) { nonempty[stack[i]] = 1 }
    }
    END {
      for (name in allowed) {
        if (opened[name] != 1 || closed[name] != 1 || !nonempty[name]) {
          print "Missing, duplicate or empty gentle-ai section: " name > "/dev/stderr"
          invalid = 1
        }
      }
      if (depth != 0) { invalid = 1 }
      exit invalid ? 1 : 0
    }
  ' "$file"; then
    return 0
  fi

  echo "gentle-ai marker contract changed in $file." >&2
  echo "Follow the update procedure in docs/coding-agents.md, then re-run the sync." >&2
  return 1
}

#######################################
# Repair native-owned agents tool prefixes without adopting user edits. v4 tracks
# ownership by SHA256 of installed bytes, so record the repaired hash too; otherwise
# the next sync mistakes our repair for a user edit and stops updating the agent.
# A previous repair is recoverable only when reversing that exact substitution
# reproduces the recorded hash. Unknown, modified and symlinked files stay untouched.
# Globals:
#   CLAUDE_AGENTS_DIR
#   REGISTERED_ENGRAM_TOOL_PREFIX
#   UPSTREAM_ENGRAM_TOOL_PREFIX
# Outputs:
#   Writes progress to STDOUT.
#######################################
repoint_generated_agent_engram_tools() {
  local -r ownership_file="$CLAUDE_AGENTS_DIR/.gentle-ai-native-agent-ownership.json"
  if [[ ! -f "$ownership_file" || -L "$ownership_file" ]]; then
    echo "No regular native agent ownership ledger; leaving agent files untouched."
    return 0
  fi
  if ! jq -e '.version == 1 and (.files | type == "object") and
    (.files | all(.[]; type == "string" and test("^[0-9a-f]{64}$")))' \
    "$ownership_file" >/dev/null; then
    echo "Unsupported native agent ownership ledger: $ownership_file." >&2
    return 1
  fi

  local agent_file agent_name recorded_hash installed_hash original_hash
  local repointed_count=0
  for agent_file in "$CLAUDE_AGENTS_DIR"/*.md; do
    [[ -f "$agent_file" && ! -L "$agent_file" ]] || continue
    agent_name="${agent_file##*/}"
    # shellcheck disable=SC2016  # $name is a jq variable.
    recorded_hash="$(jq -r --arg name "$agent_name" '.files[$name] // empty' \
      "$ownership_file")" || return 1
    [[ -n "$recorded_hash" ]] || continue
    installed_hash="$(shasum -a 256 "$agent_file")" || return 1
    installed_hash="${installed_hash%% *}"
    if [[ "$installed_hash" != "$recorded_hash" ]]; then
      original_hash="$(sed \
        "s/$REGISTERED_ENGRAM_TOOL_PREFIX/$UPSTREAM_ENGRAM_TOOL_PREFIX/g" "$agent_file" \
        | shasum -a 256)" || return 1
      original_hash="${original_hash%% *}"
      [[ "$original_hash" == "$recorded_hash" ]] || continue
    fi

    if grep -q "$UPSTREAM_ENGRAM_TOOL_PREFIX" "$agent_file"; then
      rewrite_file_with_output "$agent_file" \
        sed "s/$UPSTREAM_ENGRAM_TOOL_PREFIX/$REGISTERED_ENGRAM_TOOL_PREFIX/g" "$agent_file" \
        || return 1
      installed_hash="$(shasum -a 256 "$agent_file")" || return 1
      installed_hash="${installed_hash%% *}"
      repointed_count=$((repointed_count + 1))
    fi
    [[ "$installed_hash" != "$recorded_hash" ]] || continue
    # shellcheck disable=SC2016  # $name and $hash are jq variables.
    rewrite_file_with_output "$ownership_file" \
      jq --arg name "$agent_name" --arg hash "$installed_hash" \
        '.files[$name] = $hash' "$ownership_file" || return 1
  done

  echo "Repointed the engram tool names in $repointed_count generated agents."
}

#######################################
# Warn when plugin-style MCP tool names survive in the generated agents. The
# repoint above only knows the one prefix gentle-ai ships today; a renamed or
# newly added plugin-style name would be dropped from those agents just as
# silently as the engram one was, and this is the only thing that would say so.
# Warns instead of failing: the names are inert, so the agent still runs, and a
# cosmetic upstream rename should not block the whole sync.
# Globals:
#   CLAUDE_AGENTS_DIR
# Outputs:
#   Writes the surviving prefixes, and a pointer to the update procedure, to
#   STDERR.
#######################################
warn_on_unresolvable_agent_mcp_tools() {
  [[ -d "$CLAUDE_AGENTS_DIR" ]] || return 0

  # Include user-owned files left untouched by the repair: unresolved names in
  # those need manual attention too. An unmatched glob stays literal.
  local agent_files=("$CLAUDE_AGENTS_DIR"/*.md)
  [[ -f "${agent_files[0]}" ]] || return 0

  # No plugin is installed, so any mcp__plugin_* name resolves to nothing. grep
  # exits 1 when there are none, which is the healthy case.
  local surviving_names
  surviving_names="$(grep -ho 'mcp__plugin_[a-z0-9_]*' "${agent_files[@]}" | sort -u || true)"
  [[ -n "$surviving_names" ]] || return 0

  echo "Plugin-style MCP tool names are still declared in $CLAUDE_AGENTS_DIR, and" \
    "Claude Code drops them silently: $(tr '\n' ' ' <<<"$surviving_names")." \
    "Follow the update procedure in docs/coding-agents.md." >&2
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
  current_version="$(gentle-ai version | awk '{ print $NF }')" || return 1

  local recorded_version=""
  if [[ -f "$GENTLE_AI_VERSION_STAMP_FILE" ]]; then
    recorded_version="$(cat "$GENTLE_AI_VERSION_STAMP_FILE")" || return 1
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

  mkdir -p "$(dirname "$GENTLE_AI_VERSION_STAMP_FILE")" || return 1
  echo "$current_version" >"$GENTLE_AI_VERSION_STAMP_FILE"
}

#######################################
# Print the dotfiles repo root, resolved from the entrypoint's location.
# Globals:
#   ENTRYPOINT_DIR
# Outputs:
#   Writes the repo root to STDOUT, or an error to STDERR when it cannot be found.
# Returns:
#   0 on success, 1 when the entrypoint is not inside a git checkout.
#######################################
resolve_repo_root() {
  if ! git -C "$ENTRYPOINT_DIR" rev-parse --show-toplevel 2>/dev/null; then
    echo "Cannot resolve the dotfiles repo root from $ENTRYPOINT_DIR." >&2
    return 1
  fi
}

#######################################
# Re-apply the tracked output style to Claude Code's settings. `gentle-ai sync`
# forces its own `outputStyle` into the $HOME copy; this sets the key back to the
# value the tracked source carries, or deletes it when the source has none, so
# the copy stays equivalent to the repo source either way.
# Globals:
#   CLAUDE_SETTINGS_FILE
# Returns:
#   0 on success, 1 when the repo root cannot be found or jq failed.
#######################################
restore_claude_output_style() {
  local repo_root
  repo_root="$(resolve_repo_root)" || return 1
  local -r tracked_settings_file="$repo_root/home/.claude/settings.json"

  # shellcheck disable=SC2016  # $tracked is a jq variable, not a shell one.
  rewrite_file_with_output "$CLAUDE_SETTINGS_FILE" \
    jq --slurpfile tracked "$tracked_settings_file" \
      'if ($tracked[0] | has("outputStyle")) then .outputStyle = $tracked[0].outputStyle
        else del(.outputStyle) end' "$CLAUDE_SETTINGS_FILE"
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
    ${CLAUDE_STRIPPED_MARKERS[@]+"${CLAUDE_STRIPPED_MARKERS[@]}"} || return 1
  rewrite_file_with_output "$OPENCODE_MEMORY_FILE" \
    strip_marker_sections "$OPENCODE_MEMORY_FILE" \
    ${OPENCODE_STRIPPED_MARKERS[@]+"${OPENCODE_STRIPPED_MARKERS[@]}"} || return 1

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
# generated native agents) would land in the working tree.
# Globals:
#   CLAUDE_MEMORY_FILE
#   ORCHESTRATOR_AGENT_FILE
#   ORCHESTRATOR_DESCRIPTION
# Outputs:
#   Writes progress to STDOUT and an error to STDERR for an invalid prompt.
# Returns:
#   0 on success, 1 when either section lacks its required v4 structure.
#######################################
build_orchestrator_agent() {
  local orchestrator_section routing_section
  orchestrator_section="$(extract_marker_section "$CLAUDE_MEMORY_FILE" orchestrator)" || return 1
  routing_section="$(extract_marker_section "$CLAUDE_MEMORY_FILE" agent-routing)" || return 1

  # Validate the roles of both extracted sections instead of using a byte floor:
  # prompt length changes across releases without implying lost instructions.
  local heading
  for heading in "## Agent Teams Orchestrator" "### Core Role" "### Delegation Rules"; do
    if ! grep -qxF "$heading" <<<"$orchestrator_section"; then
      echo "Extracted orchestrator is missing '$heading' in $CLAUDE_MEMORY_FILE." >&2
      return 1
    fi
  done
  if ! grep -qxF "## Implementation Routing" <<<"$routing_section" \
    || ! grep -qxF "### ODD protocol (MANDATORY, in this order, on every request)" \
      <<<"$routing_section"; then
    echo "Extracted agent-routing lacks the ODD protocol in $CLAUDE_MEMORY_FILE." >&2
    return 1
  fi

  local prompt_body prompt_bytes
  prompt_body="$(printf '%s\n\n%s\n' "$orchestrator_section" "$routing_section")"
  prompt_bytes="$(printf '%s' "$prompt_body" | wc -c | tr -d '[:space:]')"

  mkdir -p "$(dirname "$ORCHESTRATOR_AGENT_FILE")" || return 1
  cat >"$ORCHESTRATOR_AGENT_FILE" <<EOF || return 1
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
    ${CLAUDE_MEMORY_MARKERS[@]+"${CLAUDE_MEMORY_MARKERS[@]}"} || return 1
  assert_marker_inventory "$OPENCODE_MEMORY_FILE" \
    ${OPENCODE_MEMORY_MARKERS[@]+"${OPENCODE_MEMORY_MARKERS[@]}"}
}

#######################################
# Run `gentle-ai sync` non-interactively for both agents. v4 installs ODD
# orchestration without SDD modes or per-phase profiles. Explicit `auto` keeps an
# unsupported or unknown OpenCode runtime in foreground mode instead of failing.
# Outputs:
#   Writes gentle-ai's own output to STDOUT/STDERR.
# Returns:
#   gentle-ai's exit status.
#######################################
run_gentle_ai_sync() {
  GENTLE_AI_YES=1 GENTLE_AI_NO_SELF_UPDATE=1 gentle-ai sync \
    --agent claude-code,opencode \
    --opencode-background-subagents=auto
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
# section back out, re-apply the tracked output style sync overrides, and repair
# the engram tool names sync bakes into the generated agents.
# Outputs:
#   Writes progress to STDOUT.
# Returns:
#   0 on success, non-zero when sync failed or the layer changed shape.
#######################################
sync_gentle_ai_generated_layer() {
  assert_opencode_skills_dir_is_real || return 1
  run_gentle_ai_sync || return 1
  assert_marker_inventories || return 1
  build_orchestrator_agent || return 1
  strip_ambient_marker_sections || return 1
  restore_claude_output_style || return 1
  repoint_generated_agent_engram_tools || return 1
  warn_on_unresolvable_agent_mcp_tools || return 1
  notify_on_gentle_ai_version_change
}

#######################################
# Replace the $HOME copy of every gentle-ai-managed config with the repo source,
# dropping any leftover Dotbot symlink first. Dotbot does not link these, so this
# is their only delivery mechanism — and it doubles as the garbage collector for
# the generated layer: sync only ever adds marker sections, never prunes them, so
# every run has to start from the tracked bytes.
# Globals:
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
  repo_root="$(resolve_repo_root)" || return 1

  local relative_path source_file target_file
  for relative_path in ${GENTLE_AI_MANAGED_CONFIGS[@]+"${GENTLE_AI_MANAGED_CONFIGS[@]}"}; do
    source_file="$repo_root/home/$relative_path"
    target_file="$HOME/$relative_path"

    if [[ ! -f "$source_file" ]]; then
      echo "Missing repo source $source_file; cannot refresh $target_file." >&2
      return 1
    fi

    if [[ -L "$target_file" ]]; then
      rm "$target_file" || return 1
    fi
    mkdir -p "$(dirname "$target_file")" || return 1
    cp "$source_file" "$target_file" || return 1
    chmod "$MANAGED_CONFIG_MODE" "$target_file" || return 1
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

  copy_managed_configs_from_repo || return 1
  if command -v gentle-ai >/dev/null 2>&1; then
    sync_gentle_ai_generated_layer || return 1
  else
    echo "gentle-ai not found, skipping its generated layer;" \
      "the configs copied above are still up to date."
  fi

  print_separator "Done synchronizing gentle-ai assets"
}
