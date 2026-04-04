_check_for_new_versions_and_install() {
  brew update
  brew upgrade --quiet gentle-ai
  brew upgrade --quiet engram
  brew upgrade --quiet gga
}

_sync_managed_assets_to_current_version() {
  # gentle-ai install --agent opencode --persona neutral --preset full-gentleman
  gentle-ai sync --agent opencode --include-permissions
}

update_gentleman_ai_ecosystem() {
  local -r _tool_names="gentle-ai, engram, gga"

  print_separator "Updating CLIs: $_tool_names"

  _check_for_new_versions_and_install
  _sync_managed_assets_to_current_version

  print_separator "Done updating CLI: $_tool_names"
}
