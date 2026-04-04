_is_plugin_registered() {
  local -r _opencode_json="$1"
  local -r _plugin_spec="$2"

  jq --arg plugin "$_plugin_spec" \
    '[(.plugin // [])[] | select(. == $plugin)] | length > 0' \
    "$_opencode_json"
}

_add_plugin_to_config() {
  local -r _opencode_json="$1"
  local -r _plugin_spec="$2"
  local _tmp_json="$_opencode_json.tmp"

  if jq -e '.plugin' "$_opencode_json" >/dev/null 2>&1; then
    jq --arg plugin "$_plugin_spec" '.plugin += [$plugin]' "$_opencode_json" >"$_tmp_json"
  else
    jq --arg plugin "$_plugin_spec" '. + {plugin: [$plugin]}' "$_opencode_json" >"$_tmp_json"
  fi

  mv "$_tmp_json" "$_opencode_json"
  echo "Added superpowers plugin to OpenCode."
}

_ensure_opencode_config_exists() {
  local -r _opencode_json="$OPENCODE_DIR/opencode.json"

  if [[ ! -f "$_opencode_json" ]]; then
    echo "❌ OpenCode config not found at: $_opencode_json" >&2
    exit 1
  fi
}

_ensure_plugin_is_registered() {
  local -r _opencode_json="$OPENCODE_DIR/opencode.json"
  local -r _dependency_spec="superpowers@git+https://github.com/obra/superpowers.git"

  local -r _plugin_exists=$(_is_plugin_registered "$_opencode_json" "$_dependency_spec")

  if [[ "$_plugin_exists" == "true" ]]; then
    echo "Superpowers plugin already registered."
    return
  fi

  _add_plugin_to_config "$_opencode_json" "$_dependency_spec"
}

register_superpowers_plugin() {
  print_separator "Registering superpowers plugin"

  _ensure_opencode_config_exists
  _ensure_plugin_is_registered

  print_separator "Done registering superpowers plugin"
}
