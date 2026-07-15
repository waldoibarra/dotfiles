# TO DO

## Improvements

- [ ] Mise threw an error about GitHub API rate limit for artifact attestations, this on a fresh
  MacOS machine.
- [x] Git global config has hardcoded values for `name`, `email`, and `signingkey`.
- [ ] AWS profile is hardcoded to `waldo` on `.zprofile`.
- [ ] AWS credentials are not managed.
- [x] `just sync` should do a `git pull`.
- [x] npm "corepack" on Brewfile was missing due to locally installed Node version.
- [ ] Pimp the top screen bar (can't remember the tool name, but I think it's on the git history).
- [ ] Add Hermes installation?
  `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --non-interactive --skip-setup`,
  then `npx playwright install` on the hermes dir.
