# TO DO

There are some MacOS specific Brew packages, need to figure out how to install them on Linux (Debian).

- [ ] docker-desktop
- [ ] ghostty
- [ ] obs
- [ ] obsidian
- [ ] postman
- [ ] visual-studio-code
- [ ] wezterm@nightly
- [ ] zen

Might be better to manage them with something different, like Nix.

## Improvements

- [ ] Mise threw an error about GitHub API rate limit for artifact attestations, this on a fresh
  MacOS machine.
- [ ] Git global config has hardcoded values for `name`, `email`, and `signingkey`.
- [ ] AWS profile is hardcoded to `waldo` on `.zprofile`.
- [ ] AWS credentials are not managed.
- [x] `just sync` should do a `git pull`.
- [x] npm "corepack" on Brewfile was missing due to locally installed Node version.
