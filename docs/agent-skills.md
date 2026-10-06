# Agent skills

Read [Coding agents](/docs/coding-agents.md) before changing agent files. External skills belong
to their source repositories; repo-authored skills belong in the tracked directories below.

## External skills

[`sync-global-skills-from-lock.sh`](/scripts/update-coding-agents/sync-global-skills-from-lock.sh)
installs missing entries from [`home/.agents/.skill-lock.json`](/home/.agents/.skill-lock.json),
then runs `npx -y skills update -g` for all installed global skills. This updates skills rather
than reinstalling frozen lockfile bytes. A changed tracked lockfile triggers a commit and push.
Read [Sync the workstation](/docs/tooling.md#sync-the-workstation) before running the updater;
it can publish other unpushed commits on the branch too.

Keep `lastSelectedAgents` set to `opencode` and `claude-code`; these become the installer's `-a`
flags. Edit external skills in their owning source repository, not their installed copies.

## Repo-managed skills

Dotbot links these bundles individually; the external lockfile does not manage them.

| Read before… | Tracked source |
| --- | --- |
| Writing or reviewing shell scripts | [`shell-scripting`](/home/.agents/skills/shell-scripting/SKILL.md) |
| Building/debugging/reviewing interfaces with behavior and layout | [`web-app-craft`](/home/.agents/skills/web-app-craft/SKILL.md) |
| Standards-first or frameworkless web work | [`web-standards`](/home/.agents/skills/web-standards/SKILL.md) |
| Isolated layout, intrinsic reflow, spacing, or overflow work | [`css-layout`](/home/.agents/skills/css-layout/SKILL.md) |
| Interpreting images with a text-only model and an available vision MCP | [`non-vision-image-reader`](/home/.config/opencode/skills/non-vision-image-reader/SKILL.md) |

The four `home/.agents/skills/` bundles link to both `~/.agents/skills/` and `~/.claude/skills/`.
[OpenCode also discovers those locations](https://opencode.ai/docs/skills). The image skill links
under `~/.config/opencode/skills/` and includes its OpenCode-specific recovery script.
Editing an installed symlink edits this checkout; edit the tracked source.

New bundles acquire links on the next Dotbot sync. Source creation alone does not install them.
Check link targets and restart the host before checking discovery; do not run a full machine sync
just to validate a skill. Maintenance scenarios live in each bundle's `evals/evals.json` where
present. Format checks do not establish model or browser behavior.

## OMP discovery

**Oh My Pi (`omp`) and Pi (`pi`) are different agents.** The Skills CLI's `pi` target installs
under `~/.pi/agent/skills`; adding it does not configure OMP.

OMP can discover shared `~/.agents/skills` without another copy, subject to enabled providers,
`skills.enableAgentsUser` and skill filters. Read the
[OMP discovery docs](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md) before changing
providers; foreign user-level providers require opt-in through `enabledProviders`.

Installed, discovered and advertised are different states. In a fresh OMP session, resolve
`skill://<name>` to check access. `disable-model-invocation: true` hides a discovered skill from
the automatic listing without disabling direct access or enabled `/skill:<name>` commands.
Resolving a skill does not exercise its workflow or external dependencies.
