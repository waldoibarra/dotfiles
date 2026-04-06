# Loaded last, after everything else is set up.

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Colors                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

readonly _reset="\e[0m"
readonly _cyan="\e[36m"
readonly _bold_magenta="\e[1;35m"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                        Welcome Message                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

_random_quote() {
  local -r _commands=(nerd funny love inspire)
  echo $(${_commands[$RANDOM % ${#_commands[@]} + 1]})
}

_show_welcome_message() {
  local -r _user="Waldo"
  local -r _greeting="What's your main ${_cyan}focus$_reset today?"
  local -r _quote="$(_random_quote)"

  [[ -n "$_quote" ]] && printf "\n  $_quote\n"
  printf "\n"
  printf "  Welcome, $_bold_magenta$_user$_reset.\n"
  printf "  $_greeting\n"
  printf "\n"
}

_show_welcome_message
