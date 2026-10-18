# Zsh configuration

Read this before editing shell startup files or adding local environment overrides.

## Startup order

Zsh reads these files in order when their conditions apply:

| File | Loaded for | Repository behavior |
| --- | --- | --- |
| [.zshenv](/home/.zshenv) | Every Zsh process | Set Vim as editor; add Homebrew, Mise shims and `~/.local/bin` to PATH. |
| [.zprofile](/home/.zprofile) | Login shells | Reapply PATH, set Ollama keep-alive, then load local overrides. |
| [.zshrc](/home/.zshrc) | Interactive shells | Load Antigen/oh-my-zsh, random theme, Mise activation, pager settings and aliases. |
| [.zlogin](/home/.zlogin) | Login shells, after `.zshrc` | In interactive shells, load the local welcome name, print a quote and greeting, then remove helper functions. |

A login interactive terminal loads all four. A non-login, non-interactive command loads only
`.zshenv`; keep it quiet and free of prompt or terminal-dependent work.

`.zprofile` repeats PATH setup because macOS `/etc/zprofile` runs `path_helper` after `.zshenv`
and can reorder it. Homebrew paths are fixed to `/opt/homebrew` on macOS and
`/home/linuxbrew/.linuxbrew` on Linux; Intel macOS is not handled.

## Shared defaults

- Ollama keep-alive is `15m`: macOS sets it through `launchctl setenv`; Linux exports it.
- `.zshrc` assumes Homebrew Antigen is installed and activates oh-my-zsh bundles.
- `lso` runs `eza -aal --octal-permissions`; `dots` runs the
  [full sync](/docs/tooling.md#sync-the-workstation) without changing the current directory.
- On macOS, `claude` and `pi` aliases run under `caffeinate -i`.
- `.zlogin` returns immediately in non-interactive shells, before loading `~/.zlogin.local` or
  defining welcome helpers. Automated login-shell commands do not run the greeting setup.

## Machine-local configuration

Create these directly in `$HOME`; do not track or symlink them through Dotbot:

| File | Use |
| --- | --- |
| `~/.zprofile.local` | Override login-session environment values, including account-specific settings. |
| `~/.zlogin.local` | Set `NICKNAME` for the greeting; otherwise it uses `$USER`. |

Set the shared-vault profile in your untracked `~/.zprofile.local`:

```sh
export LIFE_PROFILE="waldo" # Use "lluvia" on Lluvia's machine.
```

The value names your directory under `~/life/people/`; never infer it from the operating-system username.
Open a new login terminal, then verify with `printenv LIFE_PROFILE`.

`dots` and `just update-ca` warn during agent updates if `~/life/` exists but this variable is
empty or unset. The warning does not stop updates. The updater does not source `.zprofile.local`;
it inherits exported values from the calling shell.

Agent updates use `LIFE_PROFILE` to provision two local links into your vault profile.
Read [profile routing](agent-instructions.md#personal-profile-routing) before provisioning or
changing them.

For a custom greeting name:

```sh
# ~/.zlogin.local
export NICKNAME="Waldo"
```

`.zshenv` and `.zshrc` have no local counterpart. Variables in `.zprofile.local` are not loaded by a
fresh non-login shell; scripts receive them only if inherited from a login session or set elsewhere.
Keep secrets outside this repository.

## Docker Desktop PATH changes

Docker Desktop can reinsert a `~/.docker/bin` block into `.zprofile`, even when CLI installation
uses System mode. Check the actual CLI location before removing a redundant block; removal does
not prevent reinsertion. Track the upstream reports
[#662](https://github.com/docker/desktop-feedback/issues/662) and
[#647](https://github.com/docker/desktop-feedback/issues/647) before adopting a workaround.
