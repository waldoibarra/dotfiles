#!/bin/bash

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPTS_DIR

_source_lib_functions() {
  source "$SCRIPTS_DIR/lib/constants.sh"
  source "$SCRIPTS_DIR/lib/shell-helpers.sh"
  source "$SCRIPTS_DIR/lib/update-gentleman-ai-ecosystem.sh"
  source "$SCRIPTS_DIR/lib/sync-global-skills-from-lock.sh"
  source "$SCRIPTS_DIR/lib/register-superpowers-plugin.sh"
}

_update_ai_agents() {
  update_gentleman_ai_ecosystem
  sync_global_skills_from_lock
  register_superpowers_plugin
}

main() {
  _source_lib_functions
  _update_ai_agents

  echo "✅ Done updating. Restart OpenCode if it's open."
}

main
