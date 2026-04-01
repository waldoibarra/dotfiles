_check_for_new_versions_and_install() {
  brew update
  brew upgrade gentle-ai
  brew upgrade engram
  brew upgrade gga
}

_refresh_managed_assets_to_current_version() {
  gentle-ai install --agent opencode --persona neutral --preset full-gentleman
  # gentle-ai sync --agent opencode --include-permissions
}

_copy_new_opencode_json_and_relink() {
  local -r _dotfiles_opencode="$DOTFILES_DIR/home/.config/opencode/opencode.json"
  local -r _home_opencode="$OPENCODE_DIR/opencode.json"

  cp "$_home_opencode" "$_dotfiles_opencode"
  ln -sf "$_dotfiles_opencode" "$_home_opencode"
}

update_gentleman_ai_ecosystem() {
  local -r _tool_names="gentle-ai, engram, gga"

  print_separator "Updating CLIs: $_tool_names"

  _check_for_new_versions_and_install
  _refresh_managed_assets_to_current_version
  _copy_new_opencode_json_and_relink

  print_separator "Done updating CLI: $_tool_names"
}
