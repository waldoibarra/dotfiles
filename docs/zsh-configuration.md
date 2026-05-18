# Zsh Configuration

## Startup file load order

Zsh reads startup files in this order. Not all files are read in every context.

| File | Login shell | Interactive shell | Scripts |
| --- | --- | --- | --- |
| `.zshenv` | yes | yes | yes |
| `.zprofile` | yes | — | — |
| `.zshrc` | — | yes | — |
| `.zlogin` | yes | — | — |

> A terminal emulator (Ghostty, WezTerm, etc.) typically starts a login interactive shell,
> so all four files are read in that case.

## Files

### [`.zshenv`](/home/.zshenv)

Read for every Zsh process — interactive shells, login shells, and background scripts alike.
Because of this, it must stay minimal and side-effect free. Commands that produce output,
assume a TTY, or modify the prompt do not belong here.

**Currently:** `EDITOR` and `VISUAL`.

### [`.zprofile`](/home/.zprofile)

Read once at the start of a login session, before `.zshrc`. The right place for environment
setup that is expensive or only needs to happen once: `PATH` modifications, tool initializations
(Homebrew, mise shims), and session-wide environment variables.

**Currently:** Homebrew, mise shims, AWS profile, Ollama config.

### [`.zshrc`](/home/.zshrc)

Read for every interactive shell. This is where the user-facing shell experience lives:
plugins, themes, aliases, key bindings, completion, and anything that only makes sense
when a human is at the keyboard. Environment variables that are only needed interactively
(e.g. a prompt theme setting) can live here, but variables needed by scripts belong in
`.zshenv` or `.zprofile`.

**Currently:** Antigen bootstrap, oh-my-zsh plugins, random theme, mise activation, aliases.

### [`.zlogin`](/home/.zlogin)

Read at the end of a login shell's startup, after `.zshrc`. Runs after the full environment
is set up, making it the right place for one-time login tasks like printing a welcome message.

**Currently:** Welcome message with a random quote and greeting.

## Machine-local configuration

`.zlogin` sources `~/.zlogin.local` if it exists. It is the only startup file with a `.local`
override — `.zprofile`, `.zshrc`, and `.zshenv` have no equivalent.

`~/.zlogin.local` is intentionally **not** tracked by this repo. It must be created directly
in `$HOME` on each machine. Do not add it to `install.conf.yaml` and do not create it under
`home/` or symlink it.

### Customizing the welcome message name

By default the welcome message uses `$USER` (your OS username). To display a different name,
create `~/.zlogin.local` directly in `$HOME` with:

```sh
export NICKNAME="Waldo"
```
