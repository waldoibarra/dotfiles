# Git configuration

Read this before changing Git identity, signing, aliases or shared defaults.
Dotbot links [home/.gitconfig](/home/.gitconfig) to `~/.gitconfig`; it includes the untracked
`~/.gitconfig.local` first.

Shared defaults use `main`, delta paging, `zdiff3` merge conflicts and fetch pruning.
Identity and signing keys belong in local files, not this repository.

## Setting up `.gitconfig.local`

Create `~/.gitconfig.local` on each machine:

```gitconfig
[user]
    name = Your Name
    email = you@example.com
```

For GPG signing, add your key and enable signing in that same file:

```gitconfig
[user]
    signingkey = YOUR_GPG_KEY_ID
[commit]
    gpgsign = true
```

Find `YOUR_GPG_KEY_ID` with `gpg --list-secret-keys --keyid-format=long`; use the long hexadecimal
ID after `/` on the `sec` line. The Brewfile supplies `gnupg`; the shared config selects `gpg` but
does not enable signing.

For directory-specific identities, put a conditional include **after** the local defaults:

```gitconfig
[includeIf "gitdir:~/projects/work/"]
    path = ~/.gitconfig-work
```

Create `~/.gitconfig-work` with only the overrides, such as `[user]` email and signing key.
Later values win for these settings. The tracked shared file has no conditional includes.

## Branch diff aliases

Each alias fetches first and stops on fetch failure. It compares from the merge base with
`origin/main`, excluding changes made only on main after the branch diverged.

| Command | Output | Compared with |
| --- | --- | --- |
| `git ds` | Short summary | Working tree, including staged and unstaged tracked changes |
| `git dsc` | Short summary | `HEAD` |
| `git db` | Full diff | Working tree, including staged and unstaged tracked changes |
| `git dbc` | Full diff | `HEAD` |

Untracked files are excluded. These aliases require an `origin/main` ref and remote access.

## Branch cleanup aliases

Both commands switch to `main` and fetch with pruning before deleting branches:

- `git cm` deletes merged local branches, excluding names matched by `main`, `master` or `trunk`.
- **`git cg` force-deletes local branches whose upstream is marked gone.** It does not check that
  their commits were merged; inspect and preserve needed work before running it.

## Global ignores

[home/.config/git/ignore](/home/.config/git/ignore) is linked to `~/.config/git/ignore` and selected
by `core.excludesFile`. It ignores the generated `.atl/` skill registry and Claude's local project
settings (`**/.claude/settings.local.json`). Keep project-specific patterns in that project's
`.gitignore`.
