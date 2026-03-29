cd_or_exit() {
  cd "$1" || { echo "❌ Failed to cd into $1"; exit 1; }
}

print_separator() {
  local -r _separator="🔷"

  printf "\n%s %s %s\n\n" "$_separator" "$1" "$_separator"
}
