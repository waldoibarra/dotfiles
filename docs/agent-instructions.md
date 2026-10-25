# Agent instructions

Shared instructions orient every session; references, skills, and roles supply detail when needed.

Read [Coding agents](/docs/coding-agents/README.md) before editing tracked configuration or choosing
a maintenance guide.

## Policy ownership

[`AGENTS.md`](/home/.agents/AGENTS.md) owns universal boundaries and the task-based reading map.

Its default stance requires assertive communication, a verifiable environment, and maintainability
across codebases.
These defaults apply within task authority and project constraints, not as permission for unrelated
cleanup.
It does not import conditional references or full skill bodies into every session.
Custom skill maintenance has an explicit reading trigger; specialist procedures remain with their
skills.

| Concern | Canonical source |
| --- | --- |
| Communication shapes and formatting | [Communication reference](/home/.agents/references/communication.md) |
| Planning, worker routing, and verification | [Orchestration reference](/home/.agents/references/orchestration.md) |
| Configuration ownership and integration acceptance | [Harness-design reference](/home/.agents/references/harness-design.md) |
| Prompts written for models | [Prompting guide](/docs/prompting.md), installed as `~/.agents/references/prompting.md` |
| Specialist procedures | [Skills](/docs/agent-skills.md) |
| Worker responsibilities | [Shared roles](#shared-role-agents) |

Runtime pointers use installed `~/.agents/` paths, not this checkout's location.

**Prompting guide link:** `prompting.md` stays in `docs/` because people read it too.
`install.conf.yaml` links it into `~/.agents/references/`.
Skills cite that installed path, which is the same on every machine.

Read [harness verification](/docs/coding-agents/personal-workflow.md) before checking instruction
behavior.

## Global loaders

| Agent | Loader |
| --- | --- |
| Claude Code | Dotbot links `~/.claude/CLAUDE.md` to the shared `home/.agents/AGENTS.md` source. |
| Pi | `~/.pi/agent/AGENTS.md` links to the shared source. |
| Codex | Dotbot links `~/.codex/AGENTS.md` to the shared source. |

- Claude's user-level symlink remains separate from project instructions.
- The user confirmed native Claude Code loading with the symlink in place.
  After changing delivery, verify a fresh session with `/context`.
- Desktop Cowork skips symlinked user `CLAUDE.md` files; this trial targets Claude Code.
  Read [Claude memory behavior](https://code.claude.com/docs/en/memory) before extending the trial.
- The shared global source directs configured clients to read the shared vault overview and
  machine-local profile links.
- Pi also loads ancestor context files; remove obsolete home-directory selectors after migration.
- Coding instructions do not replace the live-voice extension's separate prompt.

**Cursor:** The rendered global rule is installed; native instruction loading and the work-ticket
trial remain unverified.
Its project rules and user settings need separate loading verification.

## Harness direction discovery

The global source requires reading installed `~/.agents/references/harness-context.md` at session
start.
This shared reference routes by scope; it contains no personal project plans or current priorities.

Only personal sessions read `~/.agents/harness-roadmap.md` for personal harness prioritization.
Company cross-repository work stays company-scoped and uses its own roadmap.
Dotbot links it to the existing repository roadmap; the overview uses only stable installed paths.
Work sessions follow their project instructions to the company-owned roadmap instead.
Company evidence and credentials never belong in these public personal records.

**Limit:** Discovery instructions guide agents; they do not guarantee compliance or grant backlog
execution authority.

## Personal profile routing

- The shared global instructions require reading `~/life/README.md` at every session start, before
  responding or task work.
- Read `~/life/people/README.md` for shared profile rules before both machine-local profile links at
  session start.
- Personal READMEs own background and priorities; agent identities own individual personas and
  interaction preferences.

| Link | Destination |
| --- | --- |
| `~/.agents/personal-context.md` | `~/life/people/$LIFE_PROFILE/README.md` |
| `~/.agents/agent-identity.md` | `~/life/people/$LIFE_PROFILE/agent-identity.md` |

Set exported `LIFE_PROFILE` in untracked `~/.zprofile.local`; never infer identity from the OS
username.

Read [local shell configuration](zsh-configuration.md#machine-local-configuration)
before selecting a profile.

`dots` and `just update-ca` run
[`sync-life-profile.sh`](/scripts/update-coding-agents/sync-life-profile.sh):

- It validates a lowercase kebab-case profile name and both source files before changing links.
- Correct links remain unchanged; other symlinks are replaced.
- Ordinary files and directories are never overwritten.
- Missing vaults are skipped.
- Missing profile selection warns without changing existing links.
- Invalid profiles, missing source files, and conflicting ordinary files fail before changing either
  link.

For a narrow update without packages or publication, run:

```sh
bash ~/.dotfiles/scripts/update-coding-agents/sync-life-profile.sh
```

- Generated links stay outside Git.
- Generated links select the person while shared dotfiles remain identical across machines.
- Relative profile links resolve against the real vault destination, not the symlink directory.
- The links do not synchronize vault content; Obsidian owns synchronization.

These links replace the earlier untracked `~/AGENTS.md` selector:

- After verifying the links, manually remove that old selector only if it has no unique instructions
  left.
- The updater never deletes it automatically.
- A single-user setup can keep personal context directly in its native agent instructions instead.

Restart configured agents and verify loading; link creation alone does not prove fresh-session
behavior.

## Project discovery

- This repository uses root `AGENTS.md`, without a root `CLAUDE.md` wrapper.
- [Project settings](/.claude/settings.json) exclude the tracked Claude adapter from project
  discovery.
- The exclusion prevents the adapter from loading again as project guidance.

**Pi:** reads context files along the working directory's ancestor path.

- Working inside `home/.agents/` can load the tracked global source twice; do not assume
  deduplication.
- `AGENTS.override.md` replaces the ordinary context file only in its own directory.
- A profile override can therefore replace the linked global policy.

## Shared role agents

[Shared roles](/home/.agents/roles/) state each worker's goal, inputs, constraints, acceptance, and
report.

They contain no provider, model, or effort defaults.

| Role | Responsibility |
| --- | --- |
| `plan-reviewer` | Check feasibility, evidence, decisions, and risks without changing state. |
| `implementer` | Implement one acceptance target; return changes without Git writes. |
| `code-auditor` | Audit the briefed change and evidence without editing. |
| `browser-tester` | Verify reachable behavior; distinguish real integration evidence from simulated states. |
| `docs-writer` | Update owned documentation; leave publication to the orchestrator. |

- The main session owns decisions, Git writes, shared processes, and user communication.
- Role restrictions are policy, not a sandbox; shell-capable reviewers can still mutate files.

Read [Pi delegation](/docs/coding-agents/pi/delegation.md) before changing discovery, inheritance,
or dispatch controls.

- Claude uses linked native agent definitions; dispatch must explicitly select an eligible worker
  model.
- Without delegation, sequential self-review is not independent review.

## Claude response styles

- Claude defaults to `Clear` through [tracked settings](/home/.claude/settings.json).
- `Clear` is a thin adapter to shared communication policy and its installed reference.
- Pi and workers use the same policy without a Claude output style.

Read [Claude's output-style documentation](https://code.claude.com/docs/en/output-styles) before
changing style metadata or activation.

- Keep `keep-coding-instructions: true`; otherwise the style removes software-engineering
  instructions.
- Frontmatter names use lowercase hyphenation; misspelled fields can be ignored silently.
- `/output-style` selects a style; its case-sensitive name must match frontmatter.
- Project-local style settings can override the global default.
- Restart after editing style files; selecting another style applies from the next message.

- `Attention-kind`, `Spartan`, and `Rundown` remain verbatim optional upstream copies, separate from
  the shared policy.
- Read [Attention Span releases](https://github.com/alexgreensh/attention-span/releases) before
  updating them.
- Preserve their attribution and [AGPL-3.0
  license](https://github.com/alexgreensh/attention-span/blob/main/LICENSE).

## Activate and verify

1. Verify the shared source, reference links, role links, and Claude import resolve to the intended
  files.
2. Check profile and project overrides before assuming shared instructions take effect.
3. Restart the agent; inspect its loaded context and skill/role discovery.
4. Exercise the requested behavior before reporting it verified.

- Installed files prove delivery, not loaded instructions or successful behavior.
- Read [file ownership](/docs/coding-agents/README.md#file-ownership) before applying links or
  replacing copied files.
- Read [harness verification](/docs/coding-agents/personal-workflow.md) before spending quota on
  behavioral probes.
