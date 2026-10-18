# Agent instructions

Shared instructions orient every session; references, skills, and roles supply detail when needed.
Read [Coding agents](/docs/coding-agents/README.md) before editing tracked configuration or choosing
a maintenance guide.

## Policy ownership

[`AGENTS.md`](/home/.agents/AGENTS.md) owns universal boundaries and the task-based reading map.
It does not import conditional references into every session.

| Concern | Canonical source |
| --- | --- |
| Communication shapes and formatting | [Communication reference](/home/.agents/references/communication.md) |
| Planning, worker routing, and verification | [Orchestration reference](/home/.agents/references/orchestration.md) |
| Configuration ownership and integration acceptance | [Harness-design reference](/home/.agents/references/harness-design.md) |
| Specialist procedures | [Skills](/docs/agent-skills.md) |
| Worker responsibilities | [Shared roles](#shared-role-agents) |

Runtime pointers use installed `~/.agents/` paths, not this checkout's location.
Read [harness verification](/docs/coding-agents/personal-workflow.md) before checking instruction
behavior.

## Global loaders

| Agent | Loader |
| --- | --- |
| Claude Code | Copied `~/.claude/CLAUDE.md` imports `@~/.agents/AGENTS.md`. |
| Pi | `~/.pi/agent/AGENTS.md` links to the shared source. |

Claude's user-level import adapter remains separate from project instructions. The shared global
source directs configured clients to read the untracked, machine-specific `~/AGENTS.md` when present;
that file selects the person's shared profile. Pi also loads ancestor context files, including
`~/AGENTS.md` beneath `$HOME`, so it may receive that context twice. Do not assume deduplication.
Coding instructions do not replace the live-voice extension's separate prompt.

**Cursor:** planned, not configured. Its project rules and user settings need separate loading
verification before implementation.

## Personal profile routing

The dotfiles repository is shared across people; it must not select one person's identity for every
machine. Each person's untracked `~/AGENTS.md` selects their own profile without changing shared
configuration.

| Location | Responsibility |
| --- | --- |
| `~/.agents/AGENTS.md` | Shared policy; asks configured clients to read the local selector. |
| `~/AGENTS.md` | Machine-local selector; points to the current person's vault README. |
| `~/life/people/<person>/README.md` | Personal context and reading triggers, including the person's agent identity file. |
| `~/life/people/<person>/agent-identity.md` | Person-specific agent name and interaction rules. |

Keep the selector outside dotfiles and the shared vault. Do not sync one person's selector onto
another person's machine. Use `~/life/` paths, never a hard-coded home-directory username.

For example, Waldo's selector reads `~/life/people/waldo/README.md`; Lluvia's reads
`~/life/people/lluvia/README.md`. Each README routes to its own `agent-identity.md`.
Do not infer the person from the account name or load both profiles by default.

This indirection supports shared dotfiles and intentionally shared profiles; it is not an agent
requirement. A single-user setup could keep all personal context directly in `~/AGENTS.md`, without
vault profiles or a separate selector. Client loading still needs configuration: do not assume every
coding agent automatically loads a home-directory `AGENTS.md` from every working directory.

Read [Global loaders](#global-loaders) before checking client discovery or troubleshooting profile loading.

## Project discovery

This repository uses root `AGENTS.md`, without a root `CLAUDE.md` wrapper.
[Project settings](/.claude/settings.json) exclude the tracked Claude adapter from project
discovery.
This prevents the adapter from loading again as project guidance.

Pi reads context files along the working directory's ancestor path.
Working inside `home/.agents/` can load the tracked global source twice; do not assume
deduplication.
`AGENTS.override.md` replaces the ordinary context file only in its own directory.
A profile override can therefore replace the linked global policy.

## Shared role agents

[Shared roles](/home/.agents/roles/) define worker responsibilities, acceptance checks, and reports.
They contain no provider, model, or effort defaults.

| Role | Responsibility |
| --- | --- |
| `plan-reviewer` | Check feasibility, evidence, decisions, and risks without changing state. |
| `implementer` | Implement one acceptance target; return changes without Git writes. |
| `code-auditor` | Audit the briefed change and evidence without editing. |
| `browser-tester` | Verify reachable behavior; distinguish real integration evidence from simulated states. |
| `docs-writer` | Update owned documentation; leave publication to the orchestrator. |

The main session owns decisions, Git writes, shared processes, and user communication.
Role restrictions are policy, not a sandbox; shell-capable reviewers can still mutate files.

Read [Pi delegation](/docs/coding-agents/pi/delegation.md) before changing discovery, inheritance,
or dispatch controls.
Claude uses linked native agent definitions; dispatch must explicitly select an eligible worker
model.
Without delegation, sequential self-review is not independent review.

## Claude response styles

Claude defaults to `Clear` through [tracked settings](/home/.claude/settings.json).
`Clear` is a thin adapter to shared communication policy and its installed reference.
Pi and workers use the same policy without a Claude output style.

Read [Claude's output-style documentation](https://code.claude.com/docs/en/output-styles) before
changing style metadata or activation.

- Keep `keep-coding-instructions: true`; otherwise the style removes software-engineering
  instructions.
- Frontmatter names use lowercase hyphenation; misspelled fields can be ignored silently.
- `/output-style` selects a style; its case-sensitive name must match frontmatter.
- Project-local style settings can override the global default.
- Restart after editing style files; selecting another style applies from the next message.

`Attention-kind`, `Spartan`, and `Rundown` remain verbatim optional upstream copies, separate from
the shared policy.
Read [Attention Span releases](https://github.com/alexgreensh/attention-span/releases) before
updating them.
Preserve their attribution and [AGPL-3.0
license](https://github.com/alexgreensh/attention-span/blob/main/LICENSE).

## Activate and verify

1. Verify the shared source, reference links, role links, and Claude import resolve to the intended
  files.
2. Check profile and project overrides before assuming shared instructions take effect.
3. Restart the agent; inspect its loaded context and skill/role discovery.
4. Exercise the requested behavior before reporting it verified.

Installed files prove delivery, not loaded instructions or successful behavior.
Read [file ownership](/docs/coding-agents/README.md#file-ownership) before applying links or
replacing copied files.
Read [harness verification](/docs/coding-agents/personal-workflow.md) before spending quota on
behavioral probes.
