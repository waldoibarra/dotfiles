# Agent skills

Read [Coding agents](coding-agents/README.md) before changing agent files. External skills belong
to their source repositories; repo-authored skills belong in the tracked directories below.

## External skills

[`sync-global-skills-from-lock.sh`](/scripts/update-coding-agents/sync-global-skills-from-lock.sh)
installs missing entries from [`home/.agents/.skill-lock.json`](/home/.agents/.skill-lock.json),
then runs `npx -y skills update -g` for all installed global skills. This updates skills rather
than reinstalling frozen lockfile bytes. A changed tracked lockfile triggers a commit and push.
Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running the updater;
it can publish other unpushed commits on the branch too.

Keep `lastSelectedAgents` set to `pi` and `claude-code`; these become the installer's `-a`
flags. The `pi` target installs into `~/.agents/skills`. Edit external skills in their owning
source repository, not their installed copies.

## Repo-managed skills

Dotbot links these bundles individually; the external lockfile does not manage them.

| Read before… | Tracked source |
| --- | --- |
| Proposing scoped session-improvement packets at handoff | [`session-improvement`](/home/.agents/skills/session-improvement/SKILL.md) |
| Teaching with Socratic questions and checked application | [`socratic-learning`](/home/.agents/skills/socratic-learning/SKILL.md) |
| Starting an empty project without an application stack | [`start-project`](/home/.agents/skills/start-project/SKILL.md) |
| Writing or reviewing shell scripts | [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) |
| Building/debugging/reviewing interfaces with behavior and layout | [`web-app-craft`](/home/.agents/skills/web-app-craft/SKILL.md) |
| Standards-first or frameworkless web work | [`web-standards`](/home/.agents/skills/web-standards/SKILL.md) |
| Isolated layout, intrinsic reflow, spacing, or overflow work | [`css-layout`](/home/.agents/skills/css-layout/SKILL.md) |

The seven `home/.agents/skills/` bundles link to both `~/.agents/skills/` and `~/.claude/skills/`.
Editing an installed symlink edits this checkout; edit the tracked source.

New bundles acquire links on the next Dotbot sync. Source creation alone does not install them.
Check link targets and restart the host before checking discovery; do not run a full machine sync
just to validate a skill. In Pi, use `/skill:<name>` after reload to check discovery.
In Claude Code, start a fresh session and invoke the skill by name. Maintenance scenarios live in
each bundle's `evals/evals.json` where present. Format checks do not establish model or browser
behavior.

The `start-project` skill keeps requirements and POC setup separate from application scaffolding.
It reuses workstation defaults, minimal project docs, and mise/just lint tooling
instead of choosing a stack.

## Learning and session improvement

Use `socratic-learning` for guided learning.
Use `session-improvement` to review how the work could improve.
They share neither learner records nor project curricula.
Projects can require the teaching skill in their own instructions and keep local content separately.

| Task | Pi | Claude Code |
| --- | --- | --- |
| Start guided learning | `/skill:socratic-learning` | `/socratic-learning` |
| Review session improvements | `/skill:session-improvement` | `/session-improvement` |

Natural-language requests can also select these skills through their descriptions.
A closure question requests review, not permission to edit or publish.
The improvement skill proposes scoped changes.
Approved work uses the owning repository's verification and delivery rules.
No shutdown hook runs either skill, and neither reconstructs inaccessible conversation history.

Read [Claude skill loading](https://code.claude.com/docs/en/features-overview)
before changing Claude invocation or discovery expectations.

## Pi discovery

Pi natively scans `~/.agents/skills`; no `~/.pi/agent/skills` copy is needed. A fresh Pi session
or `/reload` refreshes discovery; startup diagnostics and `/skill:<name>` check visibility, not
skill execution. See [Pi and live voice](coding-agents/pi/README.md) for provisioning and the
separate voice-model limitations.
