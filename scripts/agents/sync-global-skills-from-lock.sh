# Syncs global skills from ~/.agents/.skills-lock.json, creates symlinks to OpenCode.
#
# Install a global skill like this:
# npx skills add https://github.com/vercel-labs/skills -s find-skills -a opencode -g -y

_get_global_skills_json() {
  npx -y skills ls -g --json 2>/dev/null
}

_get_skills_in_agents_dir() {
  local -r _skills_json=$(_get_global_skills_json)

  jq -r --arg path "$_agents_path" '.[] | select(.path | startswith($path)) | .name' <<<"$_skills_json" | sort -u
}

_install_skill() {
  local -r _skill_name="$1"
  local -r _source_url="$2"
  local -r _agent_flags=("$@")
  local -r _url="${_source_url%.git}"

  echo "Installing: $_skill_name"
  npx -y skills add "$_url" --skill "$_skill_name" "${_agent_flags[@]}" -g -y >/dev/null 2>&1
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

_update_all_skills() {
  npx -y skills update -g
}

sync_global_skills_from_lock() {
  local -r _agents_path="$HOME/.agents/skills/"
  local -r _opencode_skills_dir="$OPENCODE_DIR/skills"

  print_separator "Synchronizing global skills (from ~/.agents/.skills-lock.json)"

  _install_skills_from_lockfile
  _update_all_skills

  print_separator "Done synchronizing global skills"
}
