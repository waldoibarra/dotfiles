# Agent skills

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

## Repo-managed skills

Dotbot links these bundles individually; the external lockfile does not manage them.

| Read before… | Tracked source |
| --- | --- |
| Maintaining touched Markdown documentation without losing information | [`docs-maintenance`](/home/.agents/skills/docs-maintenance/SKILL.md) |
| Proposing scoped session-improvement packets at handoff | [`session-improvement`](/home/.agents/skills/session-improvement/SKILL.md) |
| Teaching with Socratic questions and checked application | [`socratic-learning`](/home/.agents/skills/socratic-learning/SKILL.md) |
| Adding assigned manual tasks to the shared life list | [`to-do`](/home/.agents/skills/to-do/SKILL.md) |
| Starting an empty project without an application stack | [`start-project`](/home/.agents/skills/start-project/SKILL.md) |
| Writing or reviewing shell scripts | [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) |
| Building/debugging/reviewing interfaces with behavior and layout | [`web-app-craft`](/home/.agents/skills/web-app-craft/SKILL.md) |
| Standards-first or frameworkless web work | [`web-standards`](/home/.agents/skills/web-standards/SKILL.md) |
| Isolated layout, intrinsic reflow, spacing, or overflow work | [`css-layout`](/home/.agents/skills/css-layout/SKILL.md) |

- The nine `home/.agents/skills/` bundles link to both `~/.agents/skills/` and `~/.claude/skills/`.
- Editing an installed symlink edits this checkout; edit the tracked source.

**New bundles:** they acquire links on the next Dotbot sync.

- Source creation alone does not install them.
- Check link targets and restart the host before checking discovery.
- Do not run a full machine sync just to validate a skill.
- In Pi, use `/skill:<name>` after reload to check discovery.
- In Claude Code, start a fresh session and invoke the skill by name.
- Maintenance scenarios live in each bundle's `evals/evals.json` where present.
- Format checks do not establish model or browser behavior.

The `start-project` skill keeps requirements and POC setup separate from application scaffolding.

It reuses workstation defaults, minimal project docs, and mise/just lint tooling instead of choosing
a stack.

## Documentation maintenance

**Purpose:** `docs-maintenance` checks information preservation, factual accuracy, and concern-based
structure in touched Markdown documentation.

**Routing:** Shared instructions require reading it before creating, editing, or reviewing Markdown
documentation.

**Limit:** This is model-followed routing, not a file watcher or guaranteed execution hook.

- Authorized in-place improvements need no separate cosmetic approval.
- Structural moves, splits, deletion, and substantial rewrites require approval unless already
  covered by the task.
- Unrelated documents, other contributors' changes, and frozen historical records remain outside
  automatic editing scope.
- `ghostwriter` owns prose; instruction and skill definitions retain their specialist workflows.
- `session-improvement` remains the separate, proposal-only closure workflow.

**Guide:** Read [documentation maintenance](/docs/documentation.md) before using the workflow or
checking its activation limits.

## Learning and session improvement

- Use `socratic-learning` for guided learning.
- Use `session-improvement` to review how the work could improve.
- They share neither learner records nor project curricula.
- Projects can require the teaching skill in their own instructions and keep local content
  separately.

| Task | Pi | Claude Code |
| --- | --- | --- |
| Start guided learning | `/skill:socratic-learning` | `/socratic-learning` |
| Review session improvements | `/skill:session-improvement` | `/session-improvement` |

- Natural-language requests can also select these skills through their descriptions.
- A closure question requests review, not permission to edit or publish.
- `session-improvement` assesses evidence first, then loads its placement reference only for
  warranted proposals.

**Touched docs:** `session-improvement` reads `docs-maintenance` for a scoped, read-only review of
session-edited Markdown documentation.

- Skip this review when no documentation was edited.
- Exclude unrelated Git changes; documentation improvements remain proposals, not permission to
  rewrite or create directories.

**Approved edits:** Use the owning specialist workflow and repository delivery rules.

`ghostwriter` owns prose; it replaces the former `docs-writing` name.

No shutdown hook runs `socratic-learning` or `session-improvement`; neither reconstructs inaccessible
conversation history.

Read [Claude skill loading](https://code.claude.com/docs/en/features-overview)
before changing Claude invocation or discovery expectations.

## Pi discovery

- Pi natively scans `~/.agents/skills`; no `~/.pi/agent/skills` copy is needed.
- A fresh Pi session or `/reload` refreshes discovery.
- Startup diagnostics and `/skill:<name>` check visibility, not skill execution.

Read [Pi and live voice](coding-agents/pi/README.md) before provisioning Pi or using live voice.
