# Loaded last, after everything else is set up. It is rarely used today.

_show_welcome_message() {
  local -r _username="Waldo"
  local -r _greeting="What's your main \e[36mfocus\e[0m today?"

  printf "\n"
  printf "  Welcome, \e[1;35m$_username\e[0m.\n"
  printf "  $_greeting\n"
  printf "\n"
}

_show_welcome_message
