# Install a global skill like this:
# npx skills add https://github.com/vercel-labs/skills -s find-skills -a opencode -g -y

_get_installed_skill_names() {
  # Returns space-separated list of currently installed global skill names
  # Filters for skills in ~/.agents/skills/ directory using npx skills ls -g --json
  local skills_path="$HOME/.agents/skills/"
  npx skills ls -g --json 2>/dev/null | jq -r --arg path "$skills_path" '.[] | select(.path | startswith($path)) | .name' | sort -u
}

_install_global_skills_from_global_skills_lock_json() {
  local lockfile="$HOME/.agents/.skill-lock.json"

  if [[ ! -f "$lockfile" ]]; then
    echo "Lockfile not found: $lockfile"
    return 1
  fi

  # Get list of currently installed skills
  local installed_skills
  installed_skills=$(_get_installed_skill_names)

  local agent_flags=()
  while IFS= read -r agent; do
    agent_flags+=(-a "$agent")
  done < <(jq -r '.lastSelectedAgents[]' "$lockfile")

  while IFS=$'\t' read -r -u 3 skill_name source_url; do
    # Check if skill is already installed
    if echo "$installed_skills" | grep -qx "$skill_name"; then
      continue
    fi

    local url="${source_url%.git}"
    echo "Installing: $skill_name"
    npx skills add "$url" --skill "$skill_name" "${agent_flags[@]}" -g -y >/dev/null 2>&1
  done 3< <(jq -r '.skills | to_entries[] | "\(.key)\t\(.value.sourceUrl)"' "$lockfile")
}

_ensure_global_skills_are_symlinked_to_opencode() {
  mkdir -p "$OPENCODE_DIR/skills"

  local skills_path="$HOME/.agents/skills/"
  local json
  json=$(npx skills ls -g --json 2>/dev/null)

  # Filter for skills in ~/.agents/skills/ that don't have OpenCode in agents list
  while IFS=$'\t' read -r -u 3 skill_name skill_path; do
    # Check if OpenCode agent is already registered for this skill
    if echo "$json" | jq -e --arg name "$skill_name" --arg agent "OpenCode" '.[] | select(.name == $name) | .agents | index($agent)' >/dev/null 2>&1; then
      continue
    fi

    # Create symlink
    ln -sfn "$skill_path" "$OPENCODE_DIR/skills/$skill_name"
    echo "Linked: $skill_name"
  done 3< <(jq -r --arg path "$skills_path" '.[] | select(.path | startswith($path)) | "\(.name)\t\(.path)"' <<<"$json")
}

_prune_dangling_opencode_skills_symlinks() {
  if [[ -d "$OPENCODE_DIR/skills" ]]; then
    pruned=0
    while IFS= read -r -d '' link; do
      rm -f "$link"
      echo "Pruned OpenCode symlink: $(basename "$link")"
      ((pruned++))
    done < <(find -L "$OPENCODE_DIR/skills" -maxdepth 1 -type l -print0)

    [[ $pruned -eq 0 ]] && echo "No dangling symlinks to prune."
  fi
}

_update_all_skills_to_latest_version() {
  npx skills update
}

sync_global_skills() {
  print_separator "Synchronizing global skills (from ~/.agents/skills)"

  _install_global_skills_from_global_skills_lock_json
  _ensure_global_skills_are_symlinked_to_opencode
  _prune_dangling_opencode_skills_symlinks
  _update_all_skills_to_latest_version

  print_separator "Done synchronizing global skills"
}
