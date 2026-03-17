# Universal environment variables.
# This file is loaded for every Zsh process, including background scripts. Keep it minimal to avoid breaking automated tasks.
# Use this only for variables that must be available to all scripts (even background ones).

# Set nvim as default editor for OpenCode and other tools.
export EDITOR="nvim"
export VISUAL="nvim"

# Disable all .claude support.
export OPENCODE_DISABLE_CLAUDE_CODE=1

# Mantain Ollama models loaded for 15 minutes, refreshed on use.
export OLLAMA_KEEP_ALIVE="15m"
