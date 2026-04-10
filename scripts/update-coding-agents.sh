#!/bin/bash

_ensure_nvm_loaded() {
  # shellcheck disable=SC1091
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
}

_source_dependencies() {
  local -r _scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  source "$_scripts_dir/lib/constants.sh"
  source "$_scripts_dir/lib/shell-helpers.sh"
  source "$_scripts_dir/agents/update-gentleman-ai-ecosystem.sh"
  source "$_scripts_dir/agents/sync-global-skills-from-lock.sh"
  source "$_scripts_dir/agents/register-superpowers-plugin.sh"
}

_update_ai_agents() {
  update_gentleman_ai_ecosystem
  sync_global_skills_from_lock
  register_superpowers_plugin
}

main() {
  _ensure_nvm_loaded
  _source_dependencies
  _update_ai_agents

  echo "✅ Done updating. Restart OpenCode if it's open."
}

main
