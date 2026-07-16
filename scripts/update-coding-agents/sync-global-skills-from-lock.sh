# Syncs global skills from ~/.agents/.skill-lock.json.
#
# Install a global skill like this:
# npx skills add https://github.com/vercel-labs/skills \
#   -s find-skills -a opencode -a claude-code -g -y

#######################################
# Print the currently installed global skills, as reported by the skills CLI.
# Outputs:
#   Writes the raw `skills ls -g --json` output to STDOUT.
#######################################
get_global_skills_json() {
  npx -y skills ls -g --json 2>/dev/null
}

#######################################
# Install a single skill for the given agents, unless it's already installed.
# Arguments:
#   Skill name.
#   Skill source repository URL.
#   Remaining args: agent flags to pass through, e.g. -a opencode -a claude-code.
# Outputs:
#   Writes progress to STDOUT.
#######################################
install_skill() {
  local -r skill_name="$1"
  local -r source_url="$2"
  local -r agent_flags=("${@:3}")
  local -r url="${source_url%.git}"

  echo "Installing: $skill_name"
  npx -y skills add "$url" --skill "$skill_name" "${agent_flags[@]}" -g -y >/dev/null 2>&1
}

#######################################
# Print the names of installed global skills whose path starts with the
# given prefix.
# Arguments:
#   Path prefix to match installed skill paths against.
# Outputs:
#   Writes one skill name per line to STDOUT, sorted and deduplicated.
#######################################
get_skills_in_dir() {
  local -r path_prefix="$1"
  local skills_json
  skills_json="$(get_global_skills_json)"

  jq -r --arg path "$path_prefix" \
    '.[] | select(.path | startswith($path)) | .name' <<<"$skills_json" | sort -u
}

#######################################
# Commit and push the global skill lockfile, if the update above changed it.
# Resolves the repo root via Git so this works regardless of the caller's
# current working directory.
# Outputs:
#   Writes Git's own commit/push output to STDOUT/STDERR.
#######################################
commit_and_push_skills_lockfile() {
  local repo_root
  repo_root="$(git rev-parse --show-toplevel)"
  local -r lockfile_relpath="home/.agents/.skill-lock.json"

  # The lockfile only changes when a skill actually published a new version.
  git -C "$repo_root" diff --quiet -- "$lockfile_relpath" && return 0

  git -C "$repo_root" commit -m "$(
    cat <<'EOF'
chore(agents): update skill lock file

Skills were updated via `npx skills update -g`.
EOF
  )" -- "$lockfile_relpath"
  git -C "$repo_root" push
}

#######################################
# Update every installed global skill to its latest published version.
# Outputs:
#   Writes the skills CLI's own output to STDOUT.
#######################################
update_all_skills() {
  npx -y skills update -g
}

#######################################
# Install every skill listed in the global lockfile that isn't already
# installed under $HOME/.agents/skills.
# Globals:
#   HOME
# Outputs:
#   Writes progress to STDOUT; writes an error to STDOUT and returns 1 if
#   the lockfile is missing.
#######################################
install_skills_from_lockfile() {
  local -r lockfile="$HOME/.agents/.skill-lock.json"

  if [[ ! -f "$lockfile" ]]; then
    echo "Lockfile not found: $lockfile" >&2
    return 1
  fi

  local installed_skills
  installed_skills="$(get_skills_in_dir "$HOME/.agents/skills/")"
  local agent_flags=()

  while IFS= read -r agent; do
    agent_flags+=(-a "$agent")
  done < <(jq -r '.lastSelectedAgents[]' "$lockfile")

  while IFS=$'\t' read -r -u 3 skill_name source_url; do
    if grep -qx "$skill_name" <<<"$installed_skills"; then
      continue
    fi

    install_skill "$skill_name" "$source_url" "${agent_flags[@]}"
  done 3< <(jq -r '.skills | to_entries[] | "\(.key)\t\(.value.sourceUrl)"' "$lockfile")
}

#######################################
# Install missing global skills from the lockfile, update all of them, and
# push the lockfile if it changed.
# Outputs:
#   Writes progress to STDOUT via print_separator.
#######################################
sync_global_skills_from_lock() {
  print_separator "Synchronizing global skills (from ~/.agents/.skill-lock.json)"

  install_skills_from_lockfile
  update_all_skills
  commit_and_push_skills_lockfile

  print_separator "Done synchronizing global skills"
}
