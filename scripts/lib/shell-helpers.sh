print_separator() {
  local -r _separator="🔷"

  printf "\n%s %s %s\n\n" "$_separator" "$1" "$_separator"
}
