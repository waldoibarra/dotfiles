# Shared shell helper functions for the scripts/ directory.

#######################################
# Print a visually distinct separator line around a title.
# Arguments:
#   Title text to print between the separator markers.
# Outputs:
#   Writes the separator and title to STDOUT.
#######################################
print_separator() {
  local -r separator="🔷"

  printf "\n%s %s %s\n\n" "$separator" "$1" "$separator"
}
