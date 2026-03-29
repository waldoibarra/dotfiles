#!/bin/bash

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPTS_DIR

_source_lib_functions() {
  source "$SCRIPTS_DIR/lib/constants.sh"
  source "$SCRIPTS_DIR/lib/shell-helpers.sh"
  source "$SCRIPTS_DIR/lib/ai-gentle-stack.sh"
}

_ensure_development_directory_exists() {
  mkdir -p "$AI_AGENTS_DIR"
}

_update_ai_agents() {
  update_gentleman_ai_ecosystem
}

main() {
  _source_lib_functions
  _ensure_development_directory_exists
  _update_ai_agents

  echo "✅ Done updating. Restart OpenCode if it's open."
}

main
