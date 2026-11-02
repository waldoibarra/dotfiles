# Progressive disclosure for the docs and the global contract

**Status:** Approved and implemented on 2026-11-01; review findings applied. Read [results](#results).
Read [decisions](#decisions) for the structure. Read [verification](#verification) for the checks.
Read [open decisions](#open-decisions) for what only the operator can settle.

## Outcome

Each entrypoint below reaches its representative tasks in at most two link hops.
A heading jump inside the landing page counts as a hop. Each page serves one reader need.
Each fact has one owner. The global contract carries rules and reading triggers only.

| Entrypoint | Representative task | Route after the change |
| --- | --- | --- |
| `README.md` | Sync the workstation | README → tooling.md#sync-the-workstation |
| `docs/README.md` | Spawn a worker | docs map → agent-coordination/spawning.md |
| `docs/README.md` | Change Claude's model defaults | docs map → ai-harness/configuration.md#claude-model-defaults |
| `docs/ai-harness/README.md` | List the live agents | harness map → agent-coordination/listing.md |
| `docs/ai-harness/README.md` | Install an external skill | harness map → ai-harness/skills.md#external-skills |
| `home/.agents/AGENTS.md` | Brief a worker | contract trigger → agent-coordination/briefing.md |
| `home/.agents/AGENTS.md` | Choose a prototype route | contract trigger → session-workflow.md#prototype |
| `docs/ai-harness/pi/README.md` | Develop Lens locally | Pi map → pi/lens-development.md |

## Evidence

- `docs/` has no index. The repo README routes nine guides; the harness README routes fifteen.
- Four harness guides sit at the docs root. The rest of the harness lives in `ai-harness/`.
- `tooling.md` (371 lines) holds twelve sections across workstation, Pi, and harness concerns.
- `agent-skills.md` (251 lines) holds nine sections across installation, routing, and learning.
- `ai-harness/agent-coordination.md` (175 lines) holds five reader needs on one page.
- `home/.agents/AGENTS.md` is 1,426 words and explains rationale inline.
- `quotas.md` lists five providers' reset windows, three usable links, and personal ratings.

## Decisions

| Id | Decision | Reason |
| --- | --- | --- |
| D1 | Add `docs/README.md`: purpose, the three reading layers, and a task table. | The repo README stays the human pitch. The docs need their own orientation. |
| D2 | Move the four root harness guides into `docs/ai-harness/` without the `agent-` prefix. | One directory per concern. Names describe purpose, not audience. |
| D3 | Split `agent-coordination.md` into a directory: `README.md`, `naming.md`, `listing.md`, `spawning.md`, `briefing.md`. | Five reader needs, each one hop from the index. |
| D4 | Split `tooling.md` by the [section map](#section-maps). | Workstation readers never need Lens internals or audio. |
| D5 | Split `agent-skills.md` by the [section map](#section-maps). | Installation, task routing, and learning change on different lifecycles. |
| D6 | Regroup the harness README table into Start, Configure, Coordinate, Verify, Maintain. | Fifteen flat rows hide the layers. |
| D7 | Keep `quotas.md`; move it to `ai-harness/quotas.md`, retitle it "Provider usage limits", and mark ratings as personal and unverified. Placeholder links become listed open items. | The reviewer showed the page holds real reset windows and links. |
| D8 | Rewrite `home/.agents/AGENTS.md` to about 900 words by the [rule map](#rule-preservation-map). Rationale moves to `ai-harness/instructions.md`. | Always-loaded text costs every session. Triggers scale; prose does not. |
| D9 | Add three contract rules, each conditional on running inside Herdr (`HERDR_ENV=1`): rename own pane and tab on the first reply and again when coordinating; write every first message to an agent with the prompting guide; close containers this session created once their deliverable is verified, unless the operator asked to keep them. | Operator request on 2026-11-01, with the reviewer's ownership and confirmation conditions. |
| D10 | The `docs` skill's "Verify and hand off" list becomes the independent-review brief. Add one sentence there: hand the list to an independent reviewer before delivery of structural work. | The list already covers coherence, routes, and sentence checks. No duplicate checklist. |
| D11 | Keep `prompting.md` at `docs/prompting.md`. | Its installed symlink and the glossary link it. |
| D12 | Plans, spikes, and history change only where a link breaks. | They are evidence, not guidance. |
| D13 | Commit the existing uncommitted work first as the baseline, then four dependent commits in order. Recovery reverts in reverse order. See [commits](#commits). | Later commits reference paths earlier commits create. |

## Section maps

**`tooling.md` after D4.** Eight sections stay: sync, recipes, raw source material, editor
defaults, Homebrew, Mise, Git hooks, and RTK. Three move. "Develop Lens locally" goes to
`ai-harness/pi/lens-development.md`. "Local audio transcription" merges into
`audio-transcription.md`. "Default applications on macOS" becomes `macos-defaults.md`.
Each moved section leaves a one-line pointer at its old position.

**`agent-skills.md` after D5.** Five sections become `ai-harness/skills.md`: external skills,
repo-managed skills, custom skill maintenance, names and migration, and Pi discovery.
"Learning and session improvement" becomes `ai-harness/learning.md`. Three sections are task
routes: design interviews, prototype selection, and documentation maintenance. They join the
session workflow's skill-selection table as rows. Their detail stays on the skills they route to.

## Rule preservation map

| `AGENTS.md` section today | Retained inline | Moved behind a trigger |
| --- | --- | --- |
| Golden rules | The six bold rules and the 17-word limit | Examples and rationale to `ai-harness/instructions.md` |
| Start with the right context | The startup read list and the NDA boundary | None |
| Read the owning guidance | One merged trigger table | The ownership prose, kept in `documentation.md` |
| Establish evidence | All five rules, shortened | None |
| Make decisions actionable | Planning gate, prototype gate, approval rules | Explanations of why to `session-workflow.md` |
| Preserve authority and privacy | Every rule, verbatim where it names a boundary | None |
| Close the loop | The feedback-loop trigger and record rule | Rationale to `ai-harness/learning.md` |

Three installed routes need checking after the rewrite. `~/.agents/AGENTS.md`,
`~/.pi/agent/AGENTS.md`, and `~/.claude/CLAUDE.md` must resolve to the same tracked file.

## Commits

| Order | Commit | Depends on |
| --- | --- | --- |
| 0 | Baseline: Pi subagents removal, coordination manual, script, alias, glossary | existing work |
| 1 | Docs map and coordination directory | 0 |
| 2 | Harness guides moved; tooling and skills split; quotas retitled | 1 |
| 3 | Global contract rewrite with the three rules | 2 |
| 4 | `docs` skill review handoff | 3 |

## Verification

1. Content inventory per touched page, accounting for every section, link, and command.
2. `just lint-md`, `just lint-ec`, and a link check over every touched page.
3. Skill files through stdin lint, because normal discovery skips `home/.agents/`.
4. The structure reference's six route questions, answered for each entrypoint above.
5. Sentence check: no authored sentence over 17 words in touched prose.
6. Installed routes resolved from a fresh shell after `dots`.
7. Fresh sessions in disposable Herdr workspaces, one Claude Code and one Pi. Each must rename
   its pane and tab on its first reply. Each must run `agents` on request. Each must spawn a
   worker by the manual with an AIM first message. Record the transcript lines as evidence here.
8. Independent review of the implementation with the `docs` verify list as its brief.

## Rollback

Commit 0 is the baseline. Any later commit reverts alone in reverse order.
Before commit 0, no reset or clean is permitted; the tree holds approved uncommitted work.

## Open decisions

1. The orchestration reference reserves Astra and Fable for main chat, never workers. The operator
   asked for Astra reviewers twice today. One option amends the delegation reference to allow
   Astra for independent review on explicit request. The other picks a worker model. This plan
   assumes the amendment.

## Results

Implemented on 2026-11-01 in commits `3b02310` through `d352d57`, plus the fixes below.

- Independent plan review (Astra): rework. All findings folded into the decisions above.
- Fresh Claude Code session under Herdr: renamed its pane to `dotfiles-fable` and its tab on the
  first reply; listed agents with the script. Tab label was the directory, not the task.
- Fresh Pi session under Herdr: renamed its pane to `roster-astra` and its tab to "Live agents"
  on the first reply; built its own table instead of running the script.
- Fixes from the tests: the contract gained a listing trigger, and the naming page gained a rule
  for a session's own tab label.
- Independent implementation review (Astra): ship with fixes. Eight findings, all applied in the
  follow-up commit: two missing direct routes, `/docs` path resolution in the contract, label rules
  moved to one owner, stale Lens claims, two long sentences, the audio pointer, and this index entry.
- Not independently rerun by the reviewer: lint recipes and fresh-session behavior; both ran here.
