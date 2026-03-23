# Universal environment variables.
# This file is loaded for every Zsh process, including background scripts. Keep it minimal to avoid breaking automated tasks.
# Use this only for variables that must be available to all scripts (even background ones).

# Set vim as default editor for OpenCode and other tools.
export EDITOR="vim"
export VISUAL="vim"

# Disable all OpenCode ~/.claude support.
export OPENCODE_DISABLE_CLAUDE_CODE=1
