# Git Configuration

## Shared vs local config

`home/.gitconfig` is tracked in this repo and symlinked to `~/.gitconfig` by Dotbot.
It contains machine-agnostic settings: aliases, delta pager, merge strategy, and default
branch name.

Identity, signing, and user-specific directory includes live in `~/.gitconfig.local` —
a file that is **not tracked** and must be created manually on each machine.

The shared config loads it via:

```gitconfig
[include]
    path = ~/.gitconfig.local
```

This include is placed before any `[includeIf]` blocks so that directory-specific overrides
(e.g. per-project identities) still take precedence over the local defaults.

## Setting up `.gitconfig.local`

Create `~/.gitconfig.local` on each machine with at minimum a `[user]` block:

```gitconfig
[user]
    name = Your Name
    email = you@example.com
```

### With GPG commit signing (recommended for primary machines)

```gitconfig
[user]
    name = Your Name
    email = you@example.com
    signingkey = YOUR_GPG_KEY_ID

[commit]
    gpgsign = true
```

To find your key ID after importing or generating a key:

```sh
gpg --list-secret-keys --keyid-format=long
```

The key ID is the long hex string after the `/` on the `sec` line.

### With per-directory identity overrides

If you need a different identity for a specific project directory, add an `[includeIf]`
block pointing to a separate config file:

```gitconfig
[includeIf "gitdir:~/projects/royalytics-ai/"]
    path = ~/.gitconfig-royalytics-ai
```

The referenced file (e.g. `~/.gitconfig-royalytics-ai`) should contain only the
overrides for that context:

```gitconfig
[user]
    email = work@example.com
    signingkey = YOUR_WORK_KEY_ID
```

## Note on `gpg`

`gnupg` is installed via `~/.Brewfile` and available on all machines running these
dotfiles. The `[gpg] program = gpg` setting in the shared config is therefore safe to
keep there. Only `gpgsign = true` is local, because not every machine has a key set up.
