# Refreshes OpenCode's plugin cache, but only for plugins with a newer
# version available upstream. OpenCode only reinstalls a plugin when its
# cache entry is missing, so this is what triggers an update.

readonly OPENCODE_CACHE_DIR="$HOME/.cache/opencode"
readonly NETWORK_CHECK_TIMEOUT_SECONDS=5

#######################################
# Check whether a git-sourced plugin dependency has new commits upstream.
# Globals:
#   NETWORK_CHECK_TIMEOUT_SECONDS
# Arguments:
#   Plugin name (used in the warning message only).
#   The lockfile's "resolved" field, e.g.
#   "git+ssh://git@github.com/user/repo.git#<commit>".
# Returns:
#   0 if the remote's HEAD commit differs from the cached one, 1 otherwise
#   (including when the remote can't be reached, so a network hiccup
#   doesn't force an unnecessary reinstall).
# Outputs:
#   Writes a warning to STDERR if the remote can't be reached.
#######################################
git_dependency_is_stale() {
  local -r name="$1"
  local -r resolved="$2"
  local repo_url="${resolved#git+}"
  repo_url="${repo_url%%#*}"
  local -r current_commit="${resolved##*#}"

  # `git ls-remote` needs network access; the plugin author's SSH key isn't
  # ours, so talk to GitHub over HTTPS instead of the cached ssh:// remote.
  case "$repo_url" in
    ssh://git@github.com/*) repo_url="https://github.com/${repo_url#ssh://git@github.com/}" ;;
  esac

  local latest_commit
  latest_commit="$(
    timeout "$NETWORK_CHECK_TIMEOUT_SECONDS" git ls-remote "$repo_url" HEAD 2>/dev/null | cut -f1
  )"
  if [[ -z "$latest_commit" ]]; then
    echo "Warning: couldn't reach $repo_url, keeping cached $name." >&2
    return 1
  fi

  [[ "$latest_commit" != "$current_commit" ]]
}

#######################################
# Check whether an npm-sourced plugin dependency has a newer version
# published to the registry.
# Globals:
#   NETWORK_CHECK_TIMEOUT_SECONDS
# Arguments:
#   Plugin (npm package) name.
#   Version pinned in the cached lockfile.
# Returns:
#   0 if the registry's latest version differs from the cached one, 1
#   otherwise (including when the registry can't be reached).
# Outputs:
#   Writes a warning to STDERR if the registry can't be reached.
#######################################
npm_dependency_is_stale() {
  local -r name="$1"
  local -r current_version="$2"

  local latest_version
  latest_version="$(timeout "$NETWORK_CHECK_TIMEOUT_SECONDS" npm view "$name" version 2>/dev/null)"
  if [[ -z "$latest_version" ]]; then
    echo "Warning: couldn't reach the npm registry, keeping cached $name." >&2
    return 1
  fi

  [[ "$latest_version" != "$current_version" ]]
}

#######################################
# Find the package-lock.json OpenCode wrote for one cached plugin install,
# wherever it landed under the plugin's cache directory (git dependencies
# nest it under a cloned-repo path; npm dependencies keep it at the top).
# Arguments:
#   Plugin's top-level cache directory, e.g. one entry under
#   $OPENCODE_CACHE_DIR/packages.
# Outputs:
#   Writes the lockfile path to STDOUT, or nothing if none was found.
#######################################
find_plugin_lockfile() {
  local -r plugin_dir="$1"

  find "$plugin_dir" -name package-lock.json -print -quit
}

#######################################
# Check whether a cached OpenCode plugin has a newer version available
# upstream, dispatching to the git or npm check based on how the lockfile
# says it was resolved.
# Arguments:
#   Path to the cached plugin's package-lock.json.
# Returns:
#   0 if a newer version is available upstream, 1 otherwise.
#######################################
opencode_plugin_is_stale() {
  local -r lockfile="$1"
  local -r package_json="${lockfile%/*}/package.json"

  local name
  name="$(jq -r '.dependencies | keys[0] // empty' "$package_json")"
  [[ -n "$name" ]] || return 1

  local resolved version
  resolved="$(jq -r --arg name "$name" \
    '.packages["node_modules/" + $name].resolved // empty' "$lockfile")"
  version="$(jq -r --arg name "$name" \
    '.packages["node_modules/" + $name].version // empty' "$lockfile")"

  if [[ "$resolved" == git+* ]]; then
    git_dependency_is_stale "$name" "$resolved"
  else
    npm_dependency_is_stale "$name" "$version"
  fi
}

#######################################
# Remove the cache directory of every OpenCode plugin that has a newer
# version available upstream, so OpenCode reinstalls only those on next
# launch. Plugins already up to date are left untouched, since OpenCode only
# reinstalls a plugin when its cache entry is missing.
# Globals:
#   OPENCODE_CACHE_DIR
# Outputs:
#   Writes progress to STDOUT.
#######################################
refresh_stale_opencode_plugins() {
  local -r plugins_dir="$OPENCODE_CACHE_DIR/packages"
  [[ -d "$plugins_dir" ]] || return 0

  local plugin_dir lockfile
  for plugin_dir in "$plugins_dir"/*/; do
    [[ -d "$plugin_dir" ]] || continue

    lockfile="$(find_plugin_lockfile "$plugin_dir")"
    [[ -n "$lockfile" ]] || continue

    if opencode_plugin_is_stale "$lockfile"; then
      echo "OpenCode plugin cache cleared: $(basename "${plugin_dir%/}") (update available)."
      rm -rf "$plugin_dir"
    fi
  done
}
