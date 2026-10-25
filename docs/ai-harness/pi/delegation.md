# Pi delegation

Pi declares `pi-subagents@latest`; updates follow the current npm release.
Shared roles remain provider-neutral; private runtime evidence stays outside this repository.
Read [shared roles](/docs/agent-instructions.md#shared-role-agents) before editing a role's
instructions.

## Choose a role and model

Read [cross-harness selection](/home/.agents/references/delegation.md) before choosing a
responsibility, model, or effort.
The examples below require active registry availability; configured entries do not prove access.

Ask naturally: “Use `code-auditor` with `openai-codex/gpt-6-sol` to review this diff.”
Or launch directly in interactive Pi:

```text
/run code-auditor[model=openai-codex/gpt-6-sol:medium] Review the supplied diff without changing files.
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
Pass an explicit non-lead model. The strict worker allowlist rejects Astra, including inherited
selection.
Choose model and supported effort separately under the shared routing policy.
The [shared selection policy](/home/.agents/references/delegation.md) owns model and effort recommendations.
Use observed acceptance results; no effort level guarantees correctness.
The allowlist is in tracked settings; it does not rank models or prove provider availability.
Trusted project settings can replace the user scope;
shared instructions still prohibit leader-model children.
Availability and authentication depend on the provider.
Model selection does not authorize billing changes.

Foreground calls wait for completion. Use `async: true` for background work and inspect its final
status.
The configured simplified `tasks` mode applies one top-level model to every child.
For concurrent children using different models, launch separate background calls
with explicit role/model pairs.

## Configuration and boundaries

| Source | Responsibility |
| --- | --- |
| [`home/.agents/roles/`](/home/.agents/roles) | Shared role instructions; Pi scans installed `~/.agents/roles/`. |
| [`settings.json`](/home/.pi/agent/settings.json) | Package source, role discovery, context inheritance, and Pi tool selection. |
| [`subagent/config.json`](/home/.pi/agent/extensions/subagent/config.json) | Minimal runner feature selection and execution defaults. |

All five roles append their prompt to Pi's base prompt.
They retain global rules, project instructions, and the shared skills catalog. Children start with
fresh task context unless explicitly requested
otherwise.
The caller must supply the goal, files, constraints, and verification criteria.

### Bind repository work before dispatch

Set the tool's native `cwd` to the intended repository root for every repository-bound invocation:

```json
{
  "agent": "code-auditor",
  "model": "openai-codex/gpt-5.5:medium",
  "cwd": "/absolute/repository",
  "task": "Verify the expected Git root, then audit only this repository's diff.",
  "async": true
}
```

Keep each chain or parallel workflow inside one repository. Use separate invocations for different
roots.
The native cwd starts the child correctly; task prose names the expected root as a second check.
Before source inspection, set `EXPECTED_REPO_ROOT` to that absolute, resolved Git root and run:

```sh
actual_root=$(git rev-parse --show-toplevel) || exit 1
if [ "$actual_root" != "$EXPECTED_REPO_ROOT" ]; then
  printf 'Repository mismatch: expected %s, got %s\n' "$EXPECTED_REPO_ROOT" "$actual_root" >&2
  exit 1
fi
```

Report the verified root with findings. Stop on mismatch;
do not audit whichever repository happens to be open.
This is a checked dispatch procedure, not a runner-enforced sandbox.

### Child tool boundaries

Pi reviewers receive `read`, `grep`, `find`, `ls`, and `bash`, without `edit` or `write`.
**Bash can mutate files:** the no-mutation rule is policy, not a sandbox.
Other roles receive Pi's normal built-in tools. Nested delegation is not granted by these roles.
Child ambient extensions are disabled; voice and unrelated integrations do not start in each child.
Models provided by extensions need an explicit child extension allowlist.
Browser testing requires available tooling; a role prompt does not install Playwright or an MCP
server.

Bundled roles and package skill/prompt resources are disabled. Role management, scripted workflows,
schedules, missions, watchdog, and unused orchestration features are disabled in the runner config.
Use existing shared skills rather than adding a second workflow catalog.

Project role definitions can override names in trusted projects when using `agentScope: "both"`.
Use `agentScope: "user"` when the installed shared definition must win.
Keep company roles, skills, and MCP servers work-scoped; never move them into global configuration.

## Install and verify

Read [installation](/docs/ai-harness/pi/installation.md) before applying configuration.
The updater reads the runner source from settings and explicitly installs it before updating
packages.
This resolves `latest` and covers missing installations without duplicating the source in scripts.

Restart Pi after installation. `/subagents-doctor` checks discovery, not successful child execution.
Run the isolated provisioning checks from the repository root:

```sh
python3 scripts/tests/test-agent-harness.py
```

Check the installed runner without inference:

```sh
node scripts/tests/check-pi-harness.mjs
```

**Optional live check:** Obtain execution approval and select two eligible IDs from the active
registry first.
Replace both placeholders below; they are not model names or claims of availability.

```sh
node scripts/tests/check-pi-harness.mjs --live '<first-provider/model:effort>' '<second-provider/model:effort>'
```

The live check executes all five roles in a disposable workspace.
Private runtime evidence stays outside Git.
It verifies inherited rules/skills and provider model metadata, not model self-reports.
Two background children use different models. Every live child uses an explicit eligible worker
model.
Offline checks reject Astra selection, including inheritance when Astra is the main model.
This checks configuration, not real browser interaction or role performance on production tasks.
The script requires an npm-installed Pi host; `PI_PACKAGE_DIR` can name that host's package
directory.

**Historical headless limitation:** An earlier `pi -p '/run …'` check returned a stale-context error.
That result does not establish behavior for every later Pi/runner pair.
Use model-issued `subagent` calls or the SDK check for headless verification.
Recheck these boundaries when updating the runner or Pi.

## Upstream references

- Read [agent definitions](https://github.com/nicobailon/pi-subagents/blob/main/docs/agents.md)
  before changing discovery or inheritance.
- Read [model selection](https://github.com/nicobailon/pi-subagents/blob/main/docs/models.md)
  before changing model routing.
- Read [runner
  configuration](https://github.com/nicobailon/pi-subagents/blob/main/docs/configuration.md)
  before enabling additional features. Prefer the installed package's docs for the installed
  version.
