# Shell execution

Read before executing shell commands; repository-specific commands remain with their project.

- Run commands directly, never through `bash -c` or `sh -c`; wrappers obstruct inspection and
  trigger permission prompts.
- Use non-interactive flags; never run interactive commands.
- Never name shell variables `path` or `status`; zsh binds them to `PATH` and the exit code.
- Run commands that stash, commit, or trigger hooks one tool call at a time; parallel tool calls
  share one shell, and a hook's stash can swallow the other call's work.

**Scripts:** Read the `shell-scripting` skill before writing or reviewing shell scripts.
Prefer isolated fixtures over workstation mutation when verifying behavior.
