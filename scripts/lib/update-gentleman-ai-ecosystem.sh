_copy_file_if_different() {
  local -r _source_file="$1"
  local -r _taget_file="$2"

  if ! cmp -s "$_source_file" "$_taget_file"; then
    cp "$_source_file" "$_taget_file"
  fi
}

_relink_file_if_needed() {
  local -r _source_file="$1"
  local -r _target_file="$2"
  local -r _current_target=$(readlink "$_target_file" 2>/dev/null)

  if [ "$_current_target" != "$_source_file" ]; then
    ln -sf "$_source_file" "$_target_file"
  fi
}

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

_copy_new_opencode_json_and_relink() {
  local -r _dotfiles_opencode="$DOTFILES_DIR/home/.config/opencode/opencode.json"
  local -r _home_opencode="$OPENCODE_DIR/opencode.json"

  _copy_file_if_different "$_home_opencode" "$_dotfiles_opencode"
  _relink_file_if_needed "$_dotfiles_opencode" "$_home_opencode"
}

update_gentleman_ai_ecosystem() {
  local -r _tool_names="gentle-ai, engram, gga"

  print_separator "Updating CLIs: $_tool_names"

  _check_for_new_versions_and_install
  _sync_managed_assets_to_current_version
  _copy_new_opencode_json_and_relink

  print_separator "Done updating CLI: $_tool_names"
}
