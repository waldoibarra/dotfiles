# Loaded once per login session. This is the ideal place for Homebrew, pyenv, and your global $PATH.
# This runs once at login. It is the best place for heavy initializations like Brew, NVM, and Pyenv paths.

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                          Homebrew                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

export BREW_BIN="/opt/homebrew/bin"
[[ -f "$BREW_BIN/brew" ]] && eval "$($BREW_BIN/brew shellenv)"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                         Brew Services                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

launchctl setenv OLLAMA_KEEP_ALIVE "15m"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Mise                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

# Shims for non-interactive shells.
eval "$(mise activate zsh --shims)"
