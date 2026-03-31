# Loaded once per login session. This is the ideal place for Homebrew, pyenv, and your global $PATH.
# This runs once at login. It is the best place for heavy initializations like Brew, NVM, and Pyenv paths.

export PATH="$PATH:$HOME/.opencode/bin"
export PATH="/opt/homebrew/opt/make/libexec/gnubin:$PATH"

# Homebrew initialization
export BREW_BIN="/opt/homebrew/bin"
if [[ -n "$BREW_BIN" && -f "$BREW_BIN/brew" ]]; then
    eval "$($BREW_BIN/brew shellenv)"
fi

# Pyenv path setup.
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PATH:$PYENV_ROOT/bin"

# NVM path setup.
export NVM_DIR="$HOME/.nvm"
