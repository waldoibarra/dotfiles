_ensure_plugin_config() {
  local -r _dependency_spec="superpowers@git+https://github.com/obra/superpowers.git"
  local -r _opencode_json="$OPENCODE_DIR/opencode.json"

  if [[ ! -f "$_opencode_json" ]]; then
    echo "opencode.json not found: $_opencode_json"
    return 1
  fi

  local -r _plugin_exists=$(jq --arg plugin "$_dependency_spec" \
    '[(.plugin // [])[] | select(. == $plugin)] | length > 0' \
    "$_opencode_json")

  if [[ "$_plugin_exists" == "true" ]]; then
    echo "Superpowers plugin already registered"
    return
  fi

  local _tmp_json="$_opencode_json.tmp"

  if jq -e '.plugin' "$_opencode_json" >/dev/null 2>&1; then
    jq --arg plugin "$_dependency_spec" '.plugin += [$plugin]' "$_opencode_json" >"$_tmp_json"
  else
    jq --arg plugin "$_dependency_spec" '. + {plugin: [$plugin]}' "$_opencode_json" >"$_tmp_json"
  fi

  mv "$_tmp_json" "$_opencode_json"
  echo "Added superpowers plugin to opencode.json"
}

register_superpowers_plugin() {
  print_separator "Registering superpowers plugin"

  _ensure_plugin_config

  print_separator "Done registering superpowers plugin"
}
