# Loaded for every interactive shell. This handles the "look and feel" and tool integrations.
# This is for the interactive experience. It stays snappy because the environment is already set.

# The Complete Load Order
# When you open a new terminal window, Zsh reads configuration files in this specific sequence:
# .zshenv: Always loaded first for every Zsh session (including scripts).
# .zprofile: Loaded only for login shells. On macOS, every new terminal window is treated as a login shell by default.
# .zshrc: Loaded for interactive shells. This is where most of your day-to-day configuration lives.
# .zlogin: Loaded last, but only for login shells.


# Powerlevel10k instant prompt (Must be at the very top)
# ---------------------------------------------------------

# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi


# Oh My Zsh Framework.
# -----------------------

export ZSH="$HOME/.oh-my-zsh"
export ZSH_THEME="powerlevel10k/powerlevel10k"
zstyle ':omz:update' mode auto
zstyle ':omz:plugins:nvm' lazy yes

# https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins
plugins=(
  aws
  # colemak # vi navigation
  # colorize
  command-not-found
  # docker
  # docker-compose
  # dotenv
  # fancy-ctrl-z
  # gh
  # git
  # macos
  nvm
  # ssh
)
# bindkey -v # Enable vi mode.
source $ZSH/oh-my-zsh.sh


# Tool hooks (Required for interactive shell features).
# --------------------------------------------------------

# Load pyenv.
eval "$(pyenv init - zsh)"

# brew upgrade --cask wezterm@nightly --no-quarantine --greedy-latest


# Theme & Plugin Configuration
# -------------------------------

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
