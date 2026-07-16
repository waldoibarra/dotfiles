# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                          Bootstrap                                            ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

source $HOMEBREW_PREFIX/share/antigen/antigen.zsh
antigen use oh-my-zsh

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                           Bundles                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

local _bundles=(
  # Bundles from the default repo (robbyrussell's oh-my-zsh).
  command-not-found
  emoji
  emotty
  fancy-ctrl-z

  # Generate random Quotes and Facts(nerd, funny, love, inspire, facts).
  vkolagotla/zsh-random-quotes
)

for bundle in $_bundles; do
  antigen bundle $bundle
done

unset _bundles

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Theme                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

antigen theme random
export ZSH_THEME_RANDOM_QUIET=true

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Apply                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

antigen apply

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                          Environment                                          ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

# Let less handle mouse wheel scrolling natively (oh-my-zsh sets LESS=-R above).
# Otherwise the terminal falls back to translating wheel scroll into arrow key
# presses while less/delta hold the alternate screen, which can get stuck and
# leak into the shell as bogus history navigation after the pager exits.
export LESS="${LESS} --mouse --wheel-lines=3"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Tools                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

eval "$(mise activate zsh)"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                           Aliases                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

alias lso="eza -aal --octal-permissions"
alias dots='just --justfile ~/.dotfiles/justfile --working-directory ~/.dotfiles sync'

if [[ "$OSTYPE" == "darwin"* ]]; then
  alias claude="caffeinate -i claude"
  alias opencode="caffeinate -i opencode"
fi
