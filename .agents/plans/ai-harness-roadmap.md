# AI harness roadmap

**Goal:** every session starts with the right rules, skills, roles and tools, and nothing more.
**Harnesses:** **Claude Code** and **Pi**. **Cursor** is planned (see Next). OMP, OpenCode and
Codex are dropped.
**State (2026-10-11):** shared-role Pi portability follow-up implemented and installed;
verification is recorded in the [shared roles plan](/.agents/plans/pi-shared-roles.md).
Personal MCP parity and the session learning loop are tracked in the
[personal MCP plan](/.agents/plans/personal-mcp.md).
The personal/open-source instruction slice is implemented; verification and audit results appear
below. The earlier proposed work/Cursor continuation was superseded by the user's selection of
personal/open-source focus.
The DRY refactor is complete; final verification is recorded below. No sync or work changes.
Tags: **[F]** fact, **[A]** assumption, **[U]** unknown.

## Start here

1. Read **Implemented** and **Session learnings**; review the diffs before anything else.
2. Work details live in the private companion: `<work root>/.agents/plans/ai-harness-work-scope.md`.
   The hub changes live on branch **`chore/ai-harness`**, checked out in the hub's main checkout.
3. Do **Waldo's pending steps**, then pick from **Next**.

## Scope split

**Global** loads in every personal session and harness. **Work** loads only at the work root.
A rule naming a company tool, channel, person or repo is **work-scoped**.

| Harness | Rules | Skills | Role agents |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/CLAUDE.md` → `AGENTS.md` | `.claude/skills/` | Shared roles linked into `~/.claude/agents/` |
| Pi | `~/.pi/agent/AGENTS.md` → shared rules | `~/.agents/skills/`; project skills require trust | `pi-subagents` scans `~/.agents/roles/` |
| Cursor (planned) | `AGENTS.md`, `.cursor/rules` **[A]** | not yet | not yet |

## Implemented

**Dotfiles** **[F]**, on `main`; the portability follow-up supersedes Claude-only role ownership:

| File | Change |
| --- | --- |
| `home/.agents/AGENTS.md` | Communication, **Messages**, **Orchestration**, **Shell commands**, **Learning**; 2026-10-11 rules below |
| `home/.agents/roles/*.md` | Five shared roles; model selected per delegation rather than embedded Claude aliases |
| `home/.pi/agent/settings.json`, `extensions/subagent/config.json` | Pinned Pi runner; role/model selection and inherited instructions |
| `install.conf.yaml` | Shared role/reference links and Pi runner config; retired harness configs are no longer linked |
| `docs/agent-instructions.md`, `docs/coding-agents/` | Claude Code and Pi only; Cursor note |
| Retired harness configs, aliases, Mise entries, and obsolete updater helper | Removed from the repository; local app/data removal remains a manual pending step |

**Work knowledge hub** **[F]**, uncommitted on **`chore/ai-harness`** (cut from `origin/main`), in the
hub's main checkout. Switch the hub back to `main` only after committing, or the new skills vanish.

| File | Change |
| --- | --- |
| `.claude/skills/standup`, `demo-feedback-triage`, `ui-state-review` | Skills from the sprint 19 demo week |
| `.claude/skills/issue-handoff` | **New 2026-10-11:** sync descriptions, short review comments, In Review |
| `.claude/skills/staging-deploy` | **New 2026-10-11:** merge order, parser rebaseline, deploy watch, browser test |
| `.claude/skills/{start-issue,create-pr}` | One fallback line each, for harnesses without Linear or sub-agents |
| `scripts/setup.sh`, `STRUCTURE.md` | Each skill links into root `.claude/skills/` (Claude Code) and `.agents/skills/` (Pi) |

**Outside git** **[F]:** root skill links made by hand. Memories `pr-shipping-notes` and
`staging-test-login` gained the 2026-10-11 gotchas.

## Session learnings (2026-10-09 to 10-11)

Patterns from the sprint 19 demo session, and where each now lives:

| Pattern seen | Fix | Where |
| --- | --- | --- |
| Long drafts needed a second pass (Linear comments 400 → 80 words) | Shared context once; omit what the reader has | `AGENTS.md` § Communication; `issue-handoff` |
| Sub-agents invented facts (a Drive folder, "whole plan", a 254px rationale) | Treat sub-agent output as a draft; verify | `AGENTS.md` § Evidence |
| "How do I reset the DB?" read as approval | A question is not approval | `AGENTS.md` § Evidence |
| 174 plan ids in code comments and tests | Ids banned from code, tests, PRs, tickets too | `AGENTS.md` § Orchestration |
| Review rounds kept spawning small fixes | Propose a fix freeze; findings go to next sprint | `AGENTS.md`; `ui-state-review` |
| 28 committed screenshots went stale in a day | Reviewer aids live in the PR, few, captioned | `AGENTS.md` § Documentation; `ui-state-review` |
| Expired session re-logged a fixture user into review tabs | Check the header's user before trusting a shot | `ui-state-review` |
| zsh `path` variable wiped `PATH` | Never name variables `path` or `status` | `AGENTS.md` § Shell |
| Draft PRs skipped CI; API ignores `ready_for_review` | Mark ready; close and reopen the API PR | `staging-deploy`; memory |
| Rebaseline wipes staging Reports for everyone | Warn first; follow the how-to | `staging-deploy` |
| Materialized views missing from `information_schema` | Check columns via `pg_attribute` | `staging-deploy` |

## Verified

- **[F] 2026-10-10:** Claude Code and Pi discover and run all work skills at the work root;
  outputs only in a scratchpad. Pi needs `/trust` or `--approve`.
- **[F] 2026-10-11:** the work root lists 7 skills in `.claude/skills/` and `.agents/skills/`.
- **[U]** `issue-handoff` and `staging-deploy` not yet run as skills; written from this session's
  manual run.
- **[F]** Shared role links now exist in `~/.agents/roles/` and `~/.claude/agents/`.
  Pi discovers five executable roles; runtime checks live in the shared roles plan.
- **[A]** Output styles skip sub-agents; inferred from behavior, not docs.

## Waldo's pending steps

1. **Review work separately:** the earlier hub changes were on **`chore/ai-harness`**;
   their current state was not rechecked. Keep concurrent `pi-lens` work separate from harness commits.
2. **Manual cleanup** (not run). Upgrade OpenUsage first: v0.7.13+ reads Pi's login, not `~/.codex`.

   ```sh
   brew upgrade --cask openusage
   mise uninstall codex opencode github:can1357/oh-my-pi
   rm -rf ~/.omp ~/.config/opencode ~/.cache/opencode ~/.local/share/opencode
   rm -rf ~/.codex   # only after OpenUsage shows the Codex card via Pi
   ```

3. **Pi trust:** run `pi` at the work root, then `/trust` once.
4. **Slack:** `/mcp` in Claude Code to re-authorize.
5. **Sync:** role links and Pi runner were applied with a destination-scoped operation.
   Full `dots`, cleanup, Slack authorization, and work-root trust remain separate pending actions.

## Open decisions

| Id | Question | Default until decided |
| --- | --- | --- |
| D1 | **Pi MCPs:** link `.pi/mcp.json` to the work servers, or keep Slack and Linear Claude-only? | Claude-only; Pi uses skill fallbacks |
| D2 | **Public roadmap:** keep work file names here, or only in the private companion? | Generic names here |
| D4 | **`docs/quotas.md` "OpenCode Go":** a subscription, not the agent. Drop it with the plan? | Kept |
| D3 | **PR images:** `gh` can't upload them. Drag-and-drop by hand, or a non-merged assets ref? | Drag-and-drop by hand |
| D5 | **Unprompted harness writes:** should repeated unanswered proposals permit autonomous edits? | No; propose in-session and retain for handoff until Waldo sets an explicit boundary. |
| D6 | **Personal identities:** should another operator share the current operator's preferences? | No; confirm their environment and consent before sharing personal preferences. |

## Personal and open-source instruction slice

**Intended outcome, not yet observed in ordinary sessions:** notice recurring friction and propose
small evidence-backed improvements at natural handoffs. Canonical policy lives in
[global instructions](/home/.agents/AGENTS.md); read the [personal workflow guide](/docs/coding-agents/personal-workflow.md)
for activation and verification. Company adaptation remains deferred.

### Approved decisions

| Id | Decision | Reason |
| --- | --- | --- |
| H1 | Apply new guidance only to personal and open-source sessions. | Company workflow adaptation remains deferred; harness choice does not establish scope. |
| H2 | Keep one shared instruction source and five provider-neutral roles. | Existing loading and delegation already work; no new runtime mechanism is needed. |
| H3 | Keep Astra leading Pi and Fable leading Claude Code. | Worker selection must not replace the orchestrator. |
| H4 | Select child model and supported effort per task, within the current authorized provider. | Task risk and measured reliability matter more than fixed tiers. |
| H5 | Propose improvements at natural checkpoints; require approval before applying them. | Missed prompts do not establish consent, even for reversible instruction changes. |
| H6 | Keep private evidence and individual preferences separate from public reusable rules. | Open-source reuse must not publish work details or presume individual preferences. |
| H7 | Verify instruction behavior with synthetic, tool-disabled fresh sessions. | Text matching alone cannot demonstrate model behavior; results remain smoke evidence. |

### Historical outcomes

- **[F] Implementation:** Luna high completed instruction changes; Sol medium updated docs. Delegation
  exercised Astra high for review/audit, Luna medium for lookup-review and high for implementation,
  and Sol medium. Terra remains untested.
- **[F] Smoke:** fresh Pi Astra and Claude Fable probes respected eight synthetic scenarios.
  Claude's empty settings-source baseline excluded global instructions; corrected probes retained
  `user` settings, disabled hooks, and disabled Lens.
- **[F] Checks then reported passed:** four provisioning regressions, offline runner discovery and
  invalid-selection checks, `just lint`, shared-file Markdown lint, and scoped whitespace check.
- **[F] Native Claude dispatch:** Fable delegated `plan-reviewer` to Sonnet; metadata recorded
  `claude-fable-5-1` and `claude-sonnet-5-5` on `firstParty`. Parent effort was high; child effort
  was not independently selected or verified.
- **[F] Activation:** shared/Pi links and Claude's global import resolved. New sessions reload
  instructions; not every existing session was refreshed.
- **[F] Independent acceptance audit passed.** Runtime outputs remain private; only sanitized
  summaries are recorded. No enforcement or comparative capability benchmark is claimed.
  Tool-disabled smoke checks show intended decisions only. Ordinary-session proposals remain
  unverified.
- **[F] Boundaries:** no sync, installation, settings, permissions, credentials, or work files
  changed. Concurrent Pi Lens work remains excluded. Cross-provider delegation is untested.

### Refactor verification

- Consolidated repeated policy, candidate assignments, completed recipes, and continuation summaries.
  Shared instructions own policy; the workflow guide owns repeatable checks.
- Astra's independent source audit passed without confirmed or plausible findings.
- Fresh Pi Astra and Claude Fable sessions passed the eight-scenario smoke check after refactoring.
- `just lint`, explicit shared-file Markdown lint, four provisioning tests, offline runner checks,
  and scoped `git diff --check` passed. Concurrent Lens files remained unchanged.
- Broader model-selection scenarios remain a future proposal; no capability ranking is established.

## Lens delivery follow-up

**[F]** Repeated orchestration reminders exposed failures to follow existing delegation rules.
**[F]** Reload instructions preceded further work, causing rejected reloads and queued user input.
**[F]** Partial deliveries left authorized work unfinished. The Pi Lens plan owns its completion list.
**[F]** Laptop previews render. Tokens, attribution, queue controls, and distribution remain unfinished.

**Decision:** retain existing global rules. Use scoped implementers, independent reviews, and verified
completion gates. Pi is the primary coding agent; both Lens packages target the closest supported UX.
Commit verified changes separately, preserving other agents' work. Publication awaits local validation.
This note authorizes no new global policy or company-scope changes.

Read [the Lens display spike](/.agents/spikes/pi-lens-tool-display.md)
before continuing transcript work.
Observe adherence in later personal sessions before proposing additional global wording.

## Next

1. Observe personal/open-source sessions; work adaptation, Cursor support, retired-harness cleanup,
   and autonomous edits remain deferred.
2. **`rfc` skill** (work): company template, tracker mirror, index update, announcement draft.
3. **Frozen review build** (work): serve a build on another port, so hot reload spares review tabs.
4. **Cursor support:** confirm its instruction loading before configuration. Not started.
5. **`setup.sh` links `.claude/agents/`** (work): only once a work-only role agent exists.

**Weekly prune [A]:** shrink absorbed memories, keep `AGENTS.md` near 100 lines, retire unused skills.

## Markdown architecture

```text
~/.dotfiles/                     # public: personal and generic only
├─ home/.agents/AGENTS.md        # global rules, every harness
├─ home/.agents/skills/          # repo-authored generic skills
├─ home/.agents/roles/           # shared role prompts, no provider-specific model defaults
├─ home/.agents/RTK.md           # shared reference; Claude compatibility link retained
├─ home/.pi/agent/               # Pi-specific preferences and runner configuration
├─ docs/                         # how the workstation works
└─ .agents/plans/                # workstation plans, like this one

<work root>/                     # private: company-scoped
├─ CLAUDE.md, .mcp.json, .claude/, .agents/skills/   # links into the knowledge hub
├─ <knowledge hub>/company/      # ADRs, RFCs, handbook, contracts
└─ .agents/plans/                # plans, decisions tables, notes, screenshots
```

Read [Agent instructions](/docs/agent-instructions.md) before changing how either scope loads.
