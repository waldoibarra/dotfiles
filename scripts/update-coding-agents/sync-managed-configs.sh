# Copies the managed coding agent configs from the repo into $HOME.
#
# These configs are copies, not Dotbot symlinks: the updater resets
# ~/.claude/settings.json on every run, so the machine-specific duplicate hook
# that `herdr integration install claude` writes stays local and is discarded
# instead of leaking into the repo. Dotbot excludes these files from its globs,
# so this copy is their only delivery mechanism. See docs/coding-agents.md.

# Configs copied from the repo, as paths relative to both the repo's home/
# directory and $HOME.
readonly MANAGED_CONFIGS=(
  ".claude/CLAUDE.md"
  ".claude/settings.json"
  ".config/opencode/opencode.json"
)

# Mode the copied configs are left with, regardless of the source's mode.
readonly MANAGED_CONFIG_MODE=644

#######################################
# Print the dotfiles repo root, resolved from the entrypoint's location.
# Globals:
#   ENTRYPOINT_DIR
# Outputs:
#   Writes the repo root to STDOUT, or an error to STDERR when it cannot be found.
# Returns:
#   0 on success, 1 when the entrypoint is not inside a git checkout.
#######################################
resolve_repo_root() {
  if ! git -C "$ENTRYPOINT_DIR" rev-parse --show-toplevel 2>/dev/null; then
    echo "Cannot resolve the dotfiles repo root from $ENTRYPOINT_DIR." >&2
    return 1
  fi
}

#######################################
# Replace the $HOME copy of every managed config with the repo source, dropping
# any leftover Dotbot symlink first.
# Globals:
#   HOME
#   MANAGED_CONFIGS
#   MANAGED_CONFIG_MODE
# Outputs:
#   Writes progress to STDOUT via print_separator, and an error to STDERR when a
#   source is missing.
# Returns:
#   0 on success, 1 when the repo or one of its sources cannot be found.
#######################################
sync_managed_configs() {
  print_separator "Synchronizing managed agent configs"

  local repo_root
  repo_root="$(resolve_repo_root)" || return 1

  local relative_path source_file target_file
  for relative_path in ${MANAGED_CONFIGS[@]+"${MANAGED_CONFIGS[@]}"}; do
    source_file="$repo_root/home/$relative_path"
    target_file="$HOME/$relative_path"

    if [[ ! -f "$source_file" ]]; then
      echo "Missing repo source $source_file; cannot refresh $target_file." >&2
      return 1
    fi

    if [[ -L "$target_file" ]]; then
      rm "$target_file" || return 1
    fi
    mkdir -p "$(dirname "$target_file")" || return 1
    cp "$source_file" "$target_file" || return 1
    chmod "$MANAGED_CONFIG_MODE" "$target_file" || return 1
  done

  echo "Copied ${#MANAGED_CONFIGS[@]} managed agent configs from the repo."
  print_separator "Done synchronizing managed agent configs"
}
