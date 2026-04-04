# Loaded last, after everything else is set up. It is rarely used today.

readonly _reset="\e[0m"
readonly _cyan="\e[36m"
readonly _bold_magenta="\e[1;35m"

_show_welcome_message() {
  local -r _user="Waldo"
  local -r _greeting="What's your main ${_cyan}focus$_reset today?"

  printf "\n"
  printf "  Welcome, $_bold_magenta$_user$_reset.\n"
  printf "  $_greeting\n"
  printf "\n"
}

_show_welcome_message
