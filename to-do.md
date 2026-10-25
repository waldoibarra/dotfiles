# Tooling ideas

**Purpose:** Unapproved improvement candidates, not an execution backlog.
Check current configuration and existing plans before treating an older observation as unresolved.

## Workstation

- Investigate the reported GitHub artifact-attestation rate-limit error during a fresh macOS Mise setup.
- Review the hardcoded AWS profile `waldo` in `.zprofile`.
  An earlier note reports unmanaged AWS credentials; verify the current state before changing it.
  Keep credentials outside tracked configuration.
- Clarify the intended top-screen-bar tool before changing it; its name remains unknown.
- Review [this dotfiles repository](https://github.com/davidarny/dotfiles/tree/main) for useful,
  scoped improvements.

## Agent tools

- [ ] Study [Matt Pocock's skills](https://github.com/mattpocock/skills), starting with the already
  installed workflows and formats.
Assess useful practices, overlap, and compatibility; propose scoped adaptations without updating
  external skills automatically.

- [ ] Compare [OpenWiki](https://github.com/langchain-ai/openwiki) with the manual documentation baseline
  after the [dotfiles pilot](/docs/plans/ai-harness-roadmap.md#documentation-philosophy-pilot).
  Evaluate navigation, factual accuracy, duplication, maintenance effort, and generated changes in one
  approved repository.
  Installation and execution need separate approval; this item records the deferred evaluation.

- Evaluate Hermes installation before running its installer or adding browser dependencies.
  The earlier candidate commands were:

  ```sh
  curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --non-interactive --skip-setup
  npx playwright install
  ```

  Run the second command from the Hermes directory only after installation and execution approval.
- Read [browser investigation](/docs/spikes/browser-access-and-google-oauth.md) before approving
  a browser pilot.
  Implementation remains pending.
- Explore pinned-message support for coding agents and image rendering in Claude Code.
- Investigate sub-agent tool details that cannot expand on click.

## Explorations

- Read [course/media possibilities](/docs/spikes/browser-access-and-google-oauth.md#course-video-and-saved-media-workflow)
  before choosing the first learning source; Clief notes were the initial candidate.
- Compare Higgsfield with alternatives for video creation.
- Evaluate a test influencer profile and monetization without treating the idea as publication approval.
- Explore an agent assisting a group call when explicitly asked questions.
