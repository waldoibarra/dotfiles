# Loaded for every interactive shell. This handles the "look and feel" and tool integrations.
# This is for the interactive experience. It stays snappy because the environment is already set.

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                          Bootstrap                                            ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

source $HOMEBREW_PREFIX/share/antigen/antigen.zsh
antigen use oh-my-zsh

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                           Bundles                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

# Bundles from the default repo (robbyrussell's oh-my-zsh).
antigen bundle aws
antigen bundle command-not-found
antigen bundle fancy-ctrl-z

# Generate random Quotes and Facts(nerd, funny, love, inspire, facts).
antigen bundle vkolagotla/zsh-random-quotes

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
# ║                                            Tools                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

eval "$(mise activate zsh)"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                           Aliases                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

alias lso="eza -aal --octal-permissions"
