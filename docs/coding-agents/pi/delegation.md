# Pi delegation

Pi uses pinned `pi-subagents@0.77.0`; no local runner implementation or generated role prompts exist.
Read [shared roles](/docs/agent-instructions.md#shared-role-agents) before editing a role's instructions.

## Choose a role and model

Ask naturally: “Use `code-auditor` with `openai-codex/gpt-6-astra` to review this diff.”
Or launch directly in interactive Pi:

```text
/run code-auditor[model=openai-codex/gpt-6-astra:high] Review the supplied diff without changing files.
```

The model-facing tool accepts independent `agent` and `model` fields:

```json
{
  "agent": "plan-reviewer",
  "model": "openai-codex/gpt-6-luna:medium",
  "task": "Review the supplied plan; report blockers without editing.",
  "async": false,
  "options": { "agentScope": "user" }
}
```

Use `/subagents-models` to inspect available models and effective role mappings.
An explicit model wins; otherwise these roles inherit the parent session's model.
Availability and authentication depend on the provider.
Model selection does not authorize billing changes.

Foreground calls wait for completion. Use `async: true` for background work and inspect its final status.
The configured simplified `tasks` mode applies one top-level model to every child.
For concurrent children using different models, launch separate background calls
with explicit role/model pairs.

## Configuration and boundaries

| Source | Responsibility |
| --- | --- |
| [`home/.agents/roles/`](/home/.agents/roles) | Shared role instructions; Pi scans installed `~/.agents/roles/`. |
| [`settings.json`](/home/.pi/agent/settings.json) | Package pin, role discovery, context inheritance, and Pi tool selection. |
| [`subagent/config.json`](/home/.pi/agent/extensions/subagent/config.json) | Minimal runner feature selection and execution defaults. |

All five roles append their prompt to Pi's base prompt and retain global rules, project instructions,
and the shared skills catalog. Children start with fresh task context unless explicitly requested otherwise.
The caller must supply the goal, files, constraints, and verification criteria.

Pi reviewers receive `read`, `grep`, `find`, `ls`, and `bash`, without `edit` or `write`.
**Bash can mutate files:** the no-mutation rule is policy, not a sandbox.
Other roles receive Pi's normal built-in tools. Nested delegation is not granted by these roles.
Child ambient extensions are disabled; voice and unrelated integrations do not start in each child.
Models provided by extensions need an explicit child extension allowlist.
Browser testing requires available tooling; a role prompt does not install Playwright or an MCP server.

Bundled roles and package skill/prompt resources are disabled. Role management, scripted workflows,
schedules, missions, watchdog, and unused orchestration features are disabled in the runner config.
Use existing shared skills rather than adding a second workflow catalog.

Project role definitions can override names in trusted projects when using `agentScope: "both"`.
Use `agentScope: "user"` when the installed shared definition must win.
Keep company roles, skills, and MCP servers work-scoped; never move them into global configuration.

## Install and verify

Read [installation](/docs/coding-agents/pi/installation.md) before applying configuration.
Pi's `update` skips pinned npm packages, including missing ones.
The updater reads the runner source from settings and explicitly installs that pin before updating packages.

Restart Pi after installation. `/subagents-doctor` checks discovery, not successful child execution.
Run the isolated provisioning checks from the repository root:

```sh
python3 scripts/tests/test-agent-harness.py
```

Check the installed runner without inference, then explicitly enable authenticated live checks:

```sh
node scripts/tests/check-pi-harness.mjs
node scripts/tests/check-pi-harness.mjs --live openai-codex/gpt-6-luna:low openai-codex/gpt-6-astra:low
```

The live check executes all five roles in a disposable workspace.
Private runtime evidence stays outside Git.
It verifies inherited rules/skills and provider model metadata, not model self-reports.
Two background children use different models; a foreground child checks parent-model inheritance.
This checks configuration, not real browser interaction or role performance on production tasks.
The script requires an npm-installed Pi host; `PI_PACKAGE_DIR` can name that host's package directory.

**Headless limitation:** `pi -p '/run …'` returned a stale-context error with this Pi/runner pair.
Use model-issued `subagent` calls or the SDK check for headless execution, not slash-command dispatch.
Recheck these boundaries when updating the pinned runner or Pi.

## Upstream references

- Read [agent definitions](https://github.com/nicobailon/pi-subagents/blob/main/docs/agents.md)
  before changing discovery or inheritance.
- Read [model selection](https://github.com/nicobailon/pi-subagents/blob/main/docs/models.md)
  before changing model routing.
- Read [runner configuration](https://github.com/nicobailon/pi-subagents/blob/main/docs/configuration.md)
  before enabling additional features. Prefer the installed package's docs for the pinned version.
