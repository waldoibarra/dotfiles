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
| H3 | Superseded: fixed Astra/Fable leads. | The user now chooses the main model per session. |
| H4 | Superseded: unrestricted task-specific child selection. | Astra/Fable are now excluded from every worker role. |
| H5 | Propose improvements at natural checkpoints; require approval before applying them. | Missed prompts do not establish consent, even for reversible instruction changes. |
| H6 | Keep private evidence and individual preferences separate from public reusable rules. | Open-source reuse must not publish work details or presume individual preferences. |
| H7 | Verify instruction behavior with synthetic, tool-disabled fresh sessions. | Text matching alone cannot demonstrate model behavior; results remain smoke evidence. |
| H8 | Reserve Astra/Fable for the main chat; require explicit non-lead workers. | User correction after excessive quota consumption. |
| H9 | Keep main-model selection user-owned, including weaker research models. | Session requirements determine the main model. |
| H10 | Enforce Pi worker selection through its existing strict model scope. | Block expensive lead inheritance without another plugin. |
| H11 | Checkpoint after repeated failures; require approval after quota or timeout failures. | Prevent unattended retry and review loops. |
| H12 | Use native all-message steering at the next tool-batch boundary. | Closer queued-message behavior without another package. |

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
**[F]** Partial deliveries left authorized work unfinished.
The dotfiles Lens delivery plan owns its completion list.
**[F]** Laptop previews render. Tokens, attribution, queue controls, and distribution remain unfinished.

**Earlier decision, superseded by H8–H12:** retain existing global rules.
Use scoped implementers, independent reviews, and verified
completion gates. Pi is the primary coding agent; both Lens packages target the closest supported UX.
Commit verified changes separately, preserving other agents' work.
Package publication awaits local validation.
The user separately authorized public GitHub source for Pi Lens.
This note authorizes no new global policy or company-scope changes.

Read [the Lens display spike](/.agents/spikes/pi-lens-tool-display.md)
before continuing transcript work.
Observe adherence in later personal sessions before proposing additional global wording.

### Session-improvement skill

The generic session-improvement workflow now lives in
[`home/.agents/skills/session-improvement/SKILL.md`](/home/.agents/skills/session-improvement/SKILL.md),
with routing scenarios in its `evals/evals.json`.
The shared `Learning` rule only routes closure and repeated-correction cases to that skill; policy
remains in one place and approved edits still require scoped consent.
Dotbot's existing skill-directory globs are the intended installation mechanism for Pi and Claude Code.
No hook, daemon, settings schema, dependency, or updater path was added.
Read [skill activation verification](#skill-activation-verification) for current installation
and test
status.
Rollback: revert the skill directory, the single Learning routing clause, and the related
docs/plan notes.

### Fixture-safety outcome

A delegated warning-test prototype left an unbounded context log, filling approximately 65 GiB.
A second prototype retained approximately 911 MiB.
The resulting `ENOSPC` stopped a later implementation worker.
The lead found no surviving prototype process and removed only those two disposable logs.
Available space recovered to 67 GiB; repository changes were preserved.

The warning fixture now caps provider calls, logged context, terminal output, and elapsed time.
Its cleanup terminates the owned process group. Both terminal modes passed afterward.

Applied under the user's subsequent request to improve the harness using this session's evidence.
The shared rule now requires bounded fixtures and cleanup of owned processes.
The resource-control fixture passed before this instruction change; no inference probe was rerun.
Rollback: revert the added rule; retain the independently verified fixture safeguards.

### Usage correction and verification

Read [the Lens delivery plan](/.agents/plans/pi-lens-delivery.md)
before resuming the measured usage review or cross-repository delivery.
These personal records stay in dotfiles; public product repositories must not copy or link them.
The audit found 33 recorded Astra child dispatches, including 13 implementation and 17 audit runs.
Repeated review loops and large parent/worker contexts compounded the routing mistake.
Local telemetry is not the provider's quota ledger; exact subscription-limit consumption remains unknown.

Canonical policy now reserves Astra/Fable for the main chat and leaves main-model choice to the user.
Pi's strict allowlist rejects Astra selection and inherited Astra before inference.
Claude receives the same shared policy; no native Claude runtime model block is claimed.
Roles remain provider-neutral. Parent model, billing, privileges, and context capacities were not changed.

Six provisioning tests and the actual installed runner's offline rejection checks passed.
The fresh offline session also loaded all-message steering.
No new model calls or behavioral probes ran.
Instruction edits were self-reviewed, not independently reviewed. No `dots` or publication ran.
Rollback uses the scoped configuration/instruction diff; no credentials or unrelated work were touched.

## Approved Lens-session instruction refinements

The user explicitly requested harness updates based on this session's repeated friction.
Changes stay in `home/.agents/AGENTS.md`, the shared canonical source.
No new instruction files were added.

| Id | Decision | Evidence and reason |
| --- | --- | --- |
| H13 | Reconcile current decisions and carry settled approvals forward | Repeated release/version/installation questions fragmented already-authorized delivery |
| H14 | Distinguish configured, installed, loaded, authenticated, and exercised states | Published Lens source was repeatedly confused with laptop readiness; a host-version guard blocked activation |
| H15 | Verify cleanup on every exit and concurrent input across awaits | Passing audits missed live-fixture deletion and editor-clearing data-loss paths |
| H16 | Add a portable `session-improvement` skill, not a hook or daemon | Native Pi and Claude skill discovery already fits closure-time proposals with approval boundaries. |
| H17 | Keep session-improvement evidence limited to accessible current context | Avoid raw history mining while still allowing exact user-reported observations and repo evidence. |

These replace three existing rule passages rather than duplicating their policy.
Question-versus-execution boundaries and necessary-decision waits remain intact.
Quota stops and two-failed-pass limits are unchanged.
Independent wording review used the AGENTS.md quick checklist; project-command checks were inapplicable.
Lead retained explicit waiting before dependent work, which the draft wording had omitted.

Static review scenarios:

- A settled release/version choice is reused; genuinely missing approvals are grouped.
- A question about resetting data remains a question, not permission to reset it.
- A package declaration or publication alone is not reported as an active installation.
- A known runtime mismatch blocks readiness even when source checks pass.
- Async teardown stops owned work before deleting artifacts after assertions, cancellation, or timeout.
- Draft edits during an awaited operation must survive acceptance and recovery.

These scenarios were reviewed against wording, not run as fresh model probes.
Ordinary-session behavioral improvement remains unmeasured. Existing loader wiring is unchanged.
Rollback: revert only the three shared-instruction replacements.
Retain factual release and verification records.

## Next

1. Observe personal/open-source sessions; work adaptation, Cursor support, retired-harness cleanup,
   and autonomous edits remain deferred.
2. **`rfc` skill** (work): company template, tracker mirror, index update, announcement draft.
3. **Frozen review build** (work): serve a build on another port, so hot reload spares review tabs.
4. **Cursor support:** confirm its instruction loading before configuration. Not started.
5. **`setup.sh` links `.claude/agents/`** (work): only once a work-only role agent exists.
6. **Communication lint (idea, 2026-10-13):** a script that checks Markdown against the shared
   Communication rules (words per bullet and paragraph at most 17, fenced blocks skipped), run
   warn-only through `hk` pre-commit here, then as a Claude Code `Stop` hook on the last reply and
   as a Pi extension. Deferred: layer 1 (instructions, `Clear` style, Pi `APPEND_SYSTEM.md`) first;
   layer 2 (role pointers to the Communication section) before any lint.

**Weekly prune [A]:** shrink absorbed memories, keep `AGENTS.md` near 100 lines, retire unused skills.

## Socratic-learning skill

The reusable teaching method now lives in
[`home/.agents/skills/socratic-learning/SKILL.md`](/home/.agents/skills/socratic-learning/SKILL.md),
with routing scenarios in its `evals/evals.json`.
Education-project files now adapt that global skill instead of copying the teaching loop.
Dotbot's existing skill-directory globs are the intended installation mechanism for Pi and
Claude Code. No teacher role, hook, daemon, installer change, or curriculum was added.
Read [skill activation verification](#skill-activation-verification) for current installation
and test
status.

### Socratic-learning decisions

| Id | Decision | Reason |
| --- | --- | --- |
| S1 | Use a portable `socratic-learning` skill, not a teacher role. | Skill discovery already fits on-demand teaching without always-loaded role cost. |
| S2 | Keep project curricula and persistence rules in education repositories. | Global instructions must not carry project-specific story, learner records, or private links. |
| S3 | Treat orientation, learning, and maintenance as separate modes. | Orientation maps territory; learning verifies understanding; maintenance updates durable knowledge. |
| S4 | Require fresh prerequisites, open reasoning, concise synthesis, and independent application. | Short answers alone do not prove understanding; present understanding must be checked. |
| S5 | Permit curiosity-led factual domain expansion when local scope already approves it. | Avoid repeated permission questions while preserving approval for behavior and cross-repo changes. |
| S6 | Report missing `socratic-learning` availability as a teaching blocker in adapters. | Education teaching now depends on the canonical global method. |
| S7 | Route approved reusable improvements through specialist workflows. | The session-improvement skill proposes and routes; it does not execute changes alone. |
| S8 | Superseded: implement a shared teacher role. | The approved incremental plan chose a global skill instead. |

### Skill activation verification

The parent verified Pi 1.2.0 and Claude Code 2.1.296 on this workstation.
Selected Dotbot links were applied twice in a disposable home, then twice in the normal home.
Both skills resolve to the tracked sources through the existing Pi/shared and Claude skill directories.
No full sync, package install, microphone test, or Claude model call ran.

Pi's native `DefaultResourceLoader` discovered both skills and the project's required teaching
instruction
offline.
The probe disabled extensions and packages through in-memory settings; it made no model request.
A lower-level `loadSkills` probe missed shared discovery; the full resource loader check
corrected that
test.
Claude filesystem installation is verified; fresh Claude discovery and behavioral execution remain unverified.
Existing running chats may still need reload or restart.
The education repository now has a one-line Claude import of its canonical `AGENTS.md`.

Both skill validators, nine agent-harness tests, dotfiles lint, explicit shared Markdown lint,
and education lint passed. `skills-ref` is unavailable; no validator package was installed.
A GPT-5.5 medium synthetic smoke covered six authored scenarios and two extra approval boundaries.
It preserved no-write/no-push limits, fresh questioning, and independent application without
recording learner
progress.
It unnecessarily asked the learner to choose a topic folder; the skill now assigns ownership
resolution to the
teacher.
That focused clarification is statically checked, not behaviorally retested.
One proposal lacked an exact path because the fixture supplied no repository; actionable
packets still require
paths.
No comparative benchmark, automatic routing test, Claude model probe, or live teaching
effectiveness claim is
made.
Final independent review found two stale status passages; both now link to this canonical
verification
section.
Rollback: revert the scoped source changes and remove only the two new links from each skill directory.
Do not remove shared directories or unrelated skills.

## Teacher role idea

**Status:** superseded by `socratic-learning`; no role is implemented, installed or activated.
Historical notes remain below for context.

Candidate teaching behavior:

- Check understanding afresh each session and agree on one small objective.
- Ask one question or propose one action, then wait without solving the learner's practice.
- Connect concepts through a progressive narrative; explain why each connection matters.
- Ask for an accurate explanation in the learner's own words, using at most 17 words.
- If that criterion fails, change the explanation or example and iterate.
  Do not merely shorten the learner's text.
- Check application separately; a short answer alone does not prove understanding.
- Keep topic content and teaching procedures separate; load detail only when needed.
- Evaluate the learner's actual answers; editorial rewriting cannot supply evidence of understanding.
- Expand topic knowledge through questions and deeper exploration, not a prefilled course.
- Do not keep learner tracking, scores, review queues or session logs.

A future shared role would keep reusable teaching behavior only.
Project curricula stay in their owning projects rather than being embedded in the shared role.
Provider, model, language and effort would be selected for the session, not embedded in the role.

**Next:** no teacher-role implementation is planned. Improve the `socratic-learning` skill only
through scoped approval, validation, and host-specific discovery checks.

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
