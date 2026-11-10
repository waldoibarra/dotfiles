# Skill catalogue and delivery

**Use skills for task-specific procedures, not as a mandatory session checklist.**
Read [session workflow](/docs/ai-harness/session-workflow.md) for human checkpoints and example requests.
Read [the AI harness](/docs/ai-harness/README.md) before changing agent files.
Read [learning skills](/docs/ai-harness/learning.md) for guided learning and the feedback loop.

External skills belong to their source repositories; repo-authored skills belong in the tracked
directories below.

## External skills

[`sync-skills.py`](/scripts/update-coding-agents/sync-skills.py) reconciles the tracked
[`skills-manifest.json`](/home/.agents/skills-manifest.json).
The native `~/.agents/.skill-lock.json` records local resolution state and is not published.
The updater installs missing declarations and repairs client links.
It updates every installed global skill.
Undeclared local skills remain installed and never enter the manifest automatically.
OpenSpec generates local skills before its updater repairs their discovery links.

**Enroll a shared external skill only after approval:**

1. Record its exact skill name and GitHub source URL in `home/.agents/skills-manifest.json`.
    Keep version `1` and all three clients: `pi`, `claude-code`, and `cursor`.
2. Run `just update-ca` after tool bootstrap, or run the existing `dots` alias.
    Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running `dots`.
3. Verify installed content and source metadata in the local lockfile.
    Check Pi, Claude Code, and Cursor discovery in fresh client sessions.
    Invoke the skill harmlessly before claiming it works.
4. Request an authorized commit and push of the manifest to share the declaration.
    The other workstation installs it during its next successful `dots` run.

Install personal experiments locally without changing the manifest.
Removing a declaration does not uninstall an existing skill.
Edit external skills in their owning repository, never their installed copies.
A missing lockfile with existing content requires native source verification before adoption.
Conflicting content or unknown symlinks stop reconciliation without overwriting that installation.
Missing or malformed `SKILL.md` also stops reconciliation, even with matching lock metadata.
Preserve incomplete content and restore the skill manually before retrying.
The installer checks broken repository skill links before Dotbot can clean them.

## Repo-managed skills

Dotbot links these bundles individually; the external manifest does not manage them.

| Read before… | Tracked source |
| --- | --- |
| Preparing atomic commits and authorized pushes | [`commit`](/home/.agents/skills/commit/SKILL.md) |
| Coordinating repository-owned skill creation, refactoring, and delivery | [`custom-skills`](/home/.agents/skills/custom-skills/SKILL.md) |
| Maintaining accurate documentation with concern-based reading paths | [`docs`](/home/.agents/skills/docs/SKILL.md) |
| Assessing outcomes, repeated friction, and approved improvements | [`feedback-loop`](/home/.agents/skills/feedback-loop/SKILL.md) |
| Teaching with Socratic questions and checked application | [`socratic-teaching`](/home/.agents/skills/socratic-teaching/SKILL.md) |
| Adding assigned manual tasks to the shared life list | [`shared-todo`](/home/.agents/skills/shared-todo/SKILL.md) |
| Selecting a disposable prototype or POC and routing its execution | [`prototype-selection`](/home/.agents/skills/prototype-selection/SKILL.md) |
| Starting an empty project without an application stack | [`project-init`](/home/.agents/skills/project-init/SKILL.md) |
| Writing or reviewing shell scripts | [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) |
| Building/debugging/reviewing interfaces with behavior and layout | [`web-interface`](/home/.agents/skills/web-interface/SKILL.md) |
| Standards-first or frameworkless web work | [`web-standards`](/home/.agents/skills/web-standards/SKILL.md) |
| Isolated layout, intrinsic reflow, spacing, or overflow work | [`css-layout`](/home/.agents/skills/css-layout/SKILL.md) |
| Analyzing audiovisual evidence or bounded YouTube live captures | [`video-analysis`](/home/.agents/skills/video-analysis/SKILL.md) |
| Transcribing speech locally with provenance and coverage checks | [`audio-transcription`](/home/.agents/skills/audio-transcription/SKILL.md) |

- The fourteen `home/.agents/skills/` bundles link to `~/.agents/skills/`,
  `~/.claude/skills/`, and `~/.cursor/skills/`.
- Editing an installed symlink edits this checkout; edit the tracked source.

**New bundles:** they acquire links on the next Dotbot sync.

- Source creation alone does not install them.
- Check link targets and restart the host before checking discovery.
- Do not run a full machine sync just to validate a skill.
- In Pi, use `/skill:<name>` after reload to check discovery.
- In Claude Code, start a fresh session and invoke the skill by name.
- Maintenance scenarios live in each bundle's `evals/evals.json` where present.
- Format checks do not establish model or browser behavior.

The `project-init` skill establishes maintained project tooling without choosing an application stack.
Disposable prototypes and POCs use `prototype-selection` instead, without that linting or hook baseline.

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

## Pi discovery

- Pi natively scans `~/.agents/skills`; no `~/.pi/agent/skills` copy is needed.
- A fresh Pi session or `/reload` refreshes discovery.
- Startup diagnostics and `/skill:<name>` check visibility, not skill execution.

Read [Pi and live voice](/docs/ai-harness/pi/README.md) before provisioning Pi or using live voice.
