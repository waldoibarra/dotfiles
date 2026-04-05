# Loaded once per login session. This is the ideal place for Homebrew, pyenv, and your global $PATH.
# This runs once at login. It is the best place for heavy initializations like Brew, NVM, and Pyenv paths.

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                          Homebrew                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

export BREW_BIN="/opt/homebrew/bin"
[[ -f "$BREW_BIN/brew" ]] && eval "$($BREW_BIN/brew shellenv)"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                             PATH                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

export PATH="$HOMEBREW_PREFIX/opt/make/libexec/gnubin:$PATH"
export PYENV_ROOT="$HOME/.pyenv"
[[ -d "$PYENV_ROOT/bin" ]] && export PATH="$PYENV_ROOT/bin:$PATH"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Tools                                              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

export NVM_DIR="$HOME/.nvm"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                         Brew Services                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

launchctl setenv OLLAMA_KEEP_ALIVE "15m"
