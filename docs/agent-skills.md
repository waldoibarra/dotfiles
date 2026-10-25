# Skill catalogue and delivery

**Use skills for task-specific procedures, not as a mandatory session checklist.**
Read [session workflow](coding-agents/session-workflow.md) for human checkpoints and example
requests.
Read [Coding agents](coding-agents/README.md) before changing agent files.

External skills belong to their source repositories; repo-authored skills belong in the tracked
directories below.

## External skills

[`sync-global-skills-from-lock.sh`](/scripts/update-coding-agents/sync-global-skills-from-lock.sh)
updates external skills:

- It installs missing entries from
  [`home/.agents/.skill-lock.json`](/home/.agents/.skill-lock.json).
- It then runs `npx -y skills update -g` for all installed global skills.
- It updates skills rather than reinstalling frozen lockfile bytes.
- A changed tracked lockfile triggers a commit and push.

**Publishing risk:** the updater can publish other unpushed commits on the branch too.

Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running the updater.

- Keep `lastSelectedAgents` set to `pi` and `claude-code`; these become the installer's `-a` flags.
- The `pi` target installs into `~/.agents/skills`.
- Edit external skills in their owning source repository, not their installed copies.

## Design interviews with documentation

**Use when:** A consequential design has unresolved decisions or terminology worth recording.
Use `grill-with-docs` for the interview; ordinary edits do not need this workflow.

**Discovery:** The external skill sets `disable-model-invocation: true`.
Pi discovers it but omits it from the model's advertised skills.
Invoke it explicitly with `/skill:grill-with-docs` after discovery or reload.

**Portability:** Its body requests a `Skill` tool, which this Pi setup does not provide.
Ask the agent to read these installed files instead of calling that unavailable tool:

- `~/.agents/skills/grilling/SKILL.md`
- `~/.agents/skills/domain-modeling/SKILL.md`

**Boundaries:** Confirm decisions before implementation; record accepted decisions in existing
project documents.
Glossary and ADR creation remain subject to task authority and local documentation rules.
Do not create either merely because the wrapper mentions them.

**Ownership:** Keep the external installation unchanged; upstream owns its metadata and
tool-specific wording.
Read [external skill maintenance](#external-skills) before proposing a source fix or updating it.
Loader checks establish discovery and explicit command expansion, not interview quality or
automatic selection.

## Repo-managed skills

Dotbot links these bundles individually; the external lockfile does not manage them.

| Read before… | Tracked source |
| --- | --- |
| Preparing atomic commits and authorized pushes | [`commit`](/home/.agents/skills/commit/SKILL.md) |
| Coordinating repository-owned skill creation, refactoring, and delivery | [`custom-skills`](/home/.agents/skills/custom-skills/SKILL.md) |
| Maintaining accurate documentation with concern-based reading paths | [`docs`](/home/.agents/skills/docs/SKILL.md) |
| Assessing outcomes, repeated friction, and approved improvements | [`feedback-loop`](/home/.agents/skills/feedback-loop/SKILL.md) |
| Teaching with Socratic questions and checked application | [`socratic-teaching`](/home/.agents/skills/socratic-teaching/SKILL.md) |
| Adding assigned manual tasks to the shared life list | [`shared-todo`](/home/.agents/skills/shared-todo/SKILL.md) |
| Starting an empty project without an application stack | [`project-init`](/home/.agents/skills/project-init/SKILL.md) |
| Writing or reviewing shell scripts | [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) |
| Building/debugging/reviewing interfaces with behavior and layout | [`web-interface`](/home/.agents/skills/web-interface/SKILL.md) |
| Standards-first or frameworkless web work | [`web-standards`](/home/.agents/skills/web-standards/SKILL.md) |
| Isolated layout, intrinsic reflow, spacing, or overflow work | [`css-layout`](/home/.agents/skills/css-layout/SKILL.md) |

- The eleven `home/.agents/skills/` bundles link to both `~/.agents/skills/` and
  `~/.claude/skills/`.
- Editing an installed symlink edits this checkout; edit the tracked source.

**New bundles:** they acquire links on the next Dotbot sync.

- Source creation alone does not install them.
- Check link targets and restart the host before checking discovery.
- Do not run a full machine sync just to validate a skill.
- In Pi, use `/skill:<name>` after reload to check discovery.
- In Claude Code, start a fresh session and invoke the skill by name.
- Maintenance scenarios live in each bundle's `evals/evals.json` where present.
- Format checks do not establish model or browser behavior.

The `project-init` skill keeps requirements and POC setup separate from application scaffolding.

It reuses workstation defaults, minimal project docs, and mise/just lint tooling instead of choosing
a stack.

## Custom skill maintenance

Read [`custom-skills`](/home/.agents/skills/custom-skills/SKILL.md) before maintaining
repository-owned custom skills as an integrated workflow.
It coordinates local ownership and delivery; `agent-skills-creator` owns the authoring procedures.
Generic skill-authoring requests still use that external specialist directly.
`feedback-loop` remains proposal-only and routes approved custom-skill work to the
coordinator.

- Start with the user's outcome, protected behavior, and existing owners; avoid another generic
  checklist.
- Read [shared language and lifecycle
  conventions](/home/.agents/skills/docs/references/conventions.md)
  before changing glossary, naming, or retention behavior.
- Check authored skill prose and output requirements against the shared communication rules through
  `custom-skills`.
- Apply `docs` information architecture and preservation criteria; `agent-skills-creator` owns skill
  authoring.
- Keep domain vocabulary consistent; load `domain-modeling` only for unresolved meanings.
- Prefer executable feedback and isolated checks over additional instructions for unobservable
  failures.
- Reuse `skill-creator` utilities only after checking their interfaces and active execution
  permissions.
- Do not inherit its model selection, unrestricted parallel launch, or retry defaults.

**Checks:** Run the installed authoring validator against each changed bundle:

```sh
bash ~/.agents/skills/agent-skills-creator/scripts/validate.sh home/.agents/skills/custom-skills
markdownlint-cli2 - < home/.agents/skills/custom-skills/SKILL.md
python3 scripts/tests/test-agent-harness.py
```

**Boundaries:** The delivery test uses temporary homes and checks bundled bytes and unchanged-link
timestamps.
It does not exercise model routing or skill effectiveness.
The JSON scenarios and routing examples remain specifications until adapted to an approved runner
and executed.
Missing authoring dependencies block dependent checks; do not install or update external skills
implicitly.

**Rollback:** Restore scoped source changes and remove only verified new links when installed.
Reload each host before checking discovery; a source rollback alone does not prove runtime recovery.

## Documentation maintenance

**Purpose:** `docs` maintains accurate Markdown and concern-based reading paths within the active
task.
Its [structure reference](/home/.agents/skills/docs/references/structure.md) owns documentation
information architecture, including Diátaxis and progressive disclosure.
Shared instructions and worker roles route documentation work through the same skill.

**Use:** Read [documentation maintenance](/docs/documentation.md) for ownership, local checks, and
invocation.
The skill owns editing authority and preservation; instruction files and skill definitions retain
their specialist workflows.
`ghostwriter` handles prose under house conventions; `feedback-loop` remains proposal-only at
closure.

**Limits:** Discovery and model-followed routing are not file watchers or guaranteed execution
hooks.
The reference requires no generator; OpenWiki evaluation remains deferred in [tooling
ideas](/to-do.md#agent-tools).

## Current names and migration

Names describe each skill's job; clear existing names remain unchanged.
Historical records may use prior names; use these current names for invocation and installed paths.

| Previous name | Current name | Intent |
| --- | --- | --- |
| `docs-maintenance` | `docs` | Maintain documentation |
| `skill-maintenance` | `custom-skills` | Coordinate repository-owned skill maintenance |
| `session-improvement`, `session-review` | `feedback-loop` | Compare outcomes with intent and propose improvements without applying them |
| `socratic-learning` | `socratic-teaching` | Teach without learner tracking |
| `start-project` | `project-init` | Initialize an empty, stack-free project |
| `to-do` | `shared-todo` | Record assigned tasks in the shared personal list |
| `web-app-craft` | `web-interface` | Coordinate interface behavior and layout |

No legacy aliases are installed; update external references before invoking retired names.
Dotbot removes obsolete managed links; unmanaged files remain untouched.
Reload the client after migration and verify discovery separately from actual task behavior.

## Learning and session improvement

- Use `socratic-teaching` for guided learning.
- Use `feedback-loop` to compare intended and observed outcomes, including follow-up evidence after
  approved changes.
- They share neither learner records nor project curricula.
- Projects can require the teaching skill in their own instructions and keep local content
  separately.

| Task | Pi | Claude Code |
| --- | --- | --- |
| Start guided learning | `/skill:socratic-teaching` | `/socratic-teaching` |
| Review session improvements | `/skill:feedback-loop` | `/feedback-loop` |

- Natural-language requests can also select these skills through their descriptions.
- A closure question requests review, not permission to edit or publish.
- `feedback-loop` assesses evidence first, then loads its placement reference only for
  warranted proposals.

**Touched docs:** `feedback-loop` uses `docs` for read-only review of session-edited Markdown.
It skips unrelated Git changes and read-only sources; any proposed corrections still require
execution authority.

**Voice feedback:** `feedback-loop` reads Ghostwriter and relevant profiles when the
session supplies writing feedback.
It proposes evidence-backed profile changes, checking whose voice and which co-users are affected.
Explicit preferences can justify proposals without repeated corrections; profile changes still
require approval.

**Follow-up:** The skill assesses correction effort, repeated context, review burden, and decision
clarity from available evidence.
It diagnoses intent and audience mismatches through the canonical communication rules.
Without comparable evidence, report improvement as unverified; static checks and installation do not
prove reduced human effort.
No monitoring, observation logs, automatic learning, or model experiments follow from invoking the
skill.

**Approved edits:** Use the owning specialist workflow and repository delivery rules.

`ghostwriter` owns prose; it replaces the former `docs-writing` name.

No shutdown hook runs `socratic-teaching` or `feedback-loop`; neither reconstructs
inaccessible
conversation history.

Read [Claude skill loading](https://code.claude.com/docs/en/features-overview)
before changing Claude invocation or discovery expectations.

## Pi discovery

- Pi natively scans `~/.agents/skills`; no `~/.pi/agent/skills` copy is needed.
- A fresh Pi session or `/reload` refreshes discovery.
- Startup diagnostics and `/skill:<name>` check visibility, not skill execution.

Read [Pi and live voice](coding-agents/pi/README.md) before provisioning Pi or using live voice.
