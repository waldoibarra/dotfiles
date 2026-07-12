[[ -f "$HOME/.zlogin.local" ]] && source "$HOME/.zlogin.local"

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

  print "$_quote"
}

_random_quote() {
  local -r _commands=(nerd funny love inspire metaphysical 'fortune -s')
  local -r _cmd="${_commands[$RANDOM % ${#_commands[@]} + 1]}"
  local _result

  if [[ "$_cmd" == "metaphysical" ]]; then
    _random_metaphysical_quote
    return
  fi

  # ${(z)...} splits the entry into words so multi-word commands like
  # `fortune -s` run with their flags, while bare function names still work.
  _result=$(${(z)_cmd} 2>/dev/null)

  # nerd/funny/love/inspire wrap their quote in ANSI color codes and curly
  # quotes. cowthink sizes its bubble by BYTE length, so the zero-width color
  # escapes and the 3-byte “ ” both over-widen the border. Strip the colors
  # and fold the curly quotes to 1-byte ASCII so byte length matches display
  # width. Scoped to exactly these commands; nothing else needs it.
  if [[ "$_cmd" == (nerd|funny|love|inspire) ]]; then
    _result=$(print -r -- "$_result" | sed $'s/\e\\[[0-9;]*m//g;s/“/"/g;s/”/"/g')
  fi

  if [[ -n "$_result" ]]; then
    print -r -- "$_result"
  else
    _random_metaphysical_quote
  fi
}

_show_welcome_message() {
  local -r _user="${NICKNAME:-$USER}"
  local -r _greeting="What's your main focus today?"
  # Wrap 4 columns short of the terminal: cowthink adds up to 4 columns of
  # bubble border (`( ` … ` )`) on top of the -W text width, so -W $COLUMNS
  # would render past the edge and the terminal would hard-wrap the box.
  local -r _quote="$(_random_quote | cowthink -r -W $((COLUMNS - 4)))"

  [[ -n "$_quote" ]] && printf "\n%s\n" "$_quote" | lolcat
  printf "\n"
  printf "  Welcome, %s.\n" "$_user" | lolcat
  printf "  %s\n" "$_greeting" | lolcat
  printf "\n"
}

_show_welcome_message

unfunction _random_metaphysical_quote _random_quote _show_welcome_message
