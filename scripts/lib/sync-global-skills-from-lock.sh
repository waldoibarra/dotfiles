# Syncs global skills from ~/.agents/.skills-lock.json, creates symlinks to OpenCode.
#
# Install a global skill like this:
# npx skills add https://github.com/vercel-labs/skills -s find-skills -a opencode -g -y

_get_global_skills_json() {
  npx skills ls -g --json 2>/dev/null
}

_get_skills_in_agents_dir() {
  local -r _skills_json=$(_get_global_skills_json)

  jq -r --arg path "$_agents_path" '.[] | select(.path | startswith($path)) | .name' <<<"$_skills_json" | sort -u
}

_skill_is_registered_with_opencode() {
  local -r _skills_json="$1"
  local -r _skill_name="$2"

  jq -e --arg name "$_skill_name" --arg agent "OpenCode" '.[] | select(.name == $name) | .agents | index($agent)' <<<"$_skills_json" >/dev/null 2>&1
}

_install_skill() {
  local -r _skill_name="$1"
  local -r _source_url="$2"
  local -r _agent_flags=("$@")
  local -r _url="${_source_url%.git}"

  echo "Installing: $_skill_name"
  npx skills add "$_url" --skill "$_skill_name" "${_agent_flags[@]}" -g -y >/dev/null 2>&1
}

_install_skills_from_lockfile() {
  local -r _lockfile="$HOME/.agents/.skill-lock.json"

  if [[ ! -f "$_lockfile" ]]; then
    echo "Lockfile not found: $_lockfile"
    return 1
  fi

  local -r _installed_skills=$(_get_skills_in_agents_dir)
  local _agent_flags=()

  while IFS= read -r agent; do
    _agent_flags+=(-a "$agent")
  done < <(jq -r '.lastSelectedAgents[]' "$_lockfile")

  while IFS=$'\t' read -r -u 3 skill_name source_url; do
    if echo "$_installed_skills" | grep -qx "$skill_name"; then
      continue
    fi

    _install_skill "$skill_name" "$source_url" "${_agent_flags[@]}"
  done 3< <(jq -r '.skills | to_entries[] | "\(.key)\t\(.value.sourceUrl)"' "$_lockfile")
}

_link_skill_to_opencode() {
  local -r _skill_name="$1"
  local -r _skill_path="$2"

  ln -sfn "$_skill_path" "$_opencode_skills_dir/$_skill_name"
  echo "Linked: $_skill_name"
}

_ensure_opencode_skills_symlinks() {
  mkdir -p "$_opencode_skills_dir"

  local -r _skills_json=$(_get_global_skills_json)

  while IFS=$'\t' read -r -u 3 skill_name skill_path; do
    if ! _skill_is_registered_with_opencode "$_skills_json" "$skill_name"; then
      _link_skill_to_opencode "$skill_name" "$skill_path"
    fi
  done 3< <(jq -r --arg path "$_agents_path" '.[] | select(.path | startswith($path)) | "\(.name)\t\(.path)"' <<<"$_skills_json")
}

_prune_invalid_opencode_symlinks() {
  if [[ ! -d "$_opencode_skills_dir" ]]; then
    return
  fi

  local _pruned=0

  while IFS= read -r -d '' link; do
    rm -f "$link"
    echo "Pruned OpenCode symlink: $(basename "$link")"
    ((_pruned++))
  done < <(find -L "$_opencode_skills_dir" -maxdepth 1 -type l -print0)

  [[ $_pruned -eq 0 ]] && echo "No dangling symlinks to prune."
}

_update_all_skills() {
  npx skills update
}

sync_global_skills_from_lock() {
  local -r _agents_path="$HOME/.agents/skills/"
  local -r _opencode_skills_dir="$OPENCODE_DIR/skills"

  print_separator "Synchronizing global skills (from ~/.agents/.skills-lock.json)"

  _install_skills_from_lockfile
  _ensure_opencode_skills_symlinks
  _prune_invalid_opencode_symlinks
  _update_all_skills

  print_separator "Done synchronizing global skills"
}
