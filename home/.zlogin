[[ -f "$HOME/.zlogin.local" ]] && source "$HOME/.zlogin.local"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Colors                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

typeset +r _reset="\e[0m"
typeset +r _cyan="\e[36m"
typeset +r _bold_magenta="\e[1;35m"
typeset +r _green="\033[0;32m"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                        Welcome Message                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

_random_metaphysical_quote() {
  local -r _metaphysical_quotes=(
    "The observer and the observed are one."
    "Time is the mind of space."
    "Consciousness is the universe experiencing itself."
    "What is, always will have been."
    "The map is not the territory."
    "To be is to be perceived."
    "Existence precedes essence."
    "The present moment always will have been."
    "You are not in the universe, you are the universe."
    "Silence is the language of the absolute."
  )

  local -r _quote="${_metaphysical_quotes[$RANDOM % ${#_metaphysical_quotes[@]} + 1]}"

  echo "$_green$_quote$_reset"
}

_random_quote() {
  local -r _commands=(nerd funny love inspire metaphysical)
  local _cmd="${_commands[$RANDOM % ${#_commands[@]} + 1]}"
  local _result

  if [[ "$_cmd" == "metaphysical" ]]; then
    _random_metaphysical_quote
    return
  fi

  _result=$("$_cmd" 2>/dev/null)

  if [[ -n "$_result" ]]; then
    echo "$_result$_reset"
  else
    _random_metaphysical_quote
  fi
}

_show_welcome_message() {
  local -r _user="${NICKNAME:-$USER}"
  local -r _greeting="What's your main ${_cyan}focus$_reset today?"
  local -r _quote="$(_random_quote | cowsay -r --think -W $COLUMNS)"

  [[ -n "$_quote" ]] && printf "\n  %s\n" "$_quote"
  printf "\n"
  printf "  Welcome, $_bold_magenta$_user$_reset.\n"
  printf "  $_greeting\n"
  printf "\n"
}

_show_welcome_message

unset _reset _cyan _bold_magenta
unfunction _random_metaphysical_quote _random_quote _show_welcome_message
