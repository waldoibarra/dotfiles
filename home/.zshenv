# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                            Editor                                             ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

export EDITOR="vim"
export VISUAL="vim"

# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                     Non-interactive PATH                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

# SSH command execution (Moshi/mosh pane attach, scp, remote scripts) reads only .zshenv.
# .zprofile re-asserts these for login shells after macOS path_helper reorders PATH.
if [[ "$OSTYPE" == "darwin"* ]]; then
  export BREW_BIN="/opt/homebrew/bin"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  export BREW_BIN="/home/linuxbrew/.linuxbrew/bin"
fi

[[ -f "$BREW_BIN/brew" ]] && eval "$("$BREW_BIN/brew" shellenv)"
command -v mise >/dev/null && eval "$(mise activate zsh --shims)"
export PATH="$HOME/.local/bin:$PATH"
