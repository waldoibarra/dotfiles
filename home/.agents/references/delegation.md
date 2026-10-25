# Choose roles and models

**Purpose:** Match one bounded responsibility to an available model without changing the lead's
provider or privileges.
Read before dispatching any worker; the [orchestrator role](orchestration.md) owns coordination and
completion.

## Select the responsibility

| Need | Role | Acceptance |
| --- | --- | --- |
| Review a proposed change | `plan-reviewer` | Evidence, scope, dependencies, and verification are adequate. |
| Implement a bounded slice | `implementer` | Authorized changes and focused checks are complete. |
| Independently inspect finished work | `code-auditor` | Findings cite concrete defects and affected contracts. |
| Exercise browser behavior | `browser-tester` | Real interactions and failure states are checked. |
| Maintain explanations and navigation | `docs-writer` | Facts, links, terminology, and current status agree. |

**Lead:** Orchestration is a main-session responsibility, not another child to launch recursively.
The lead retains decisions, Git writes, shared processes, publication, and user communication.
Role descriptions define responsibilities; they do not prove tools, credentials, or model
availability.

## Choose the host's model

| Host | Authorized model family | Selection guidance |
| --- | --- | --- |
| Pi | OpenAI through the configured provider | Inspect the active registry and worker allowlist; pass an exact eligible provider/model ID. |
| Claude Code | Anthropic | Choose explicit `haiku`, `sonnet`, or `opus`, or an available exact ID. |
| Cursor | Cursor's available catalog | Prefer an available Composer model for bounded work; select an explicit supported ID. |

**Pi:** Configuration is not availability. GPT-5.5 was allowlisted but absent during this refactor.
GPT-6 Sol completed a review; that observation is not a permanent availability or cost guarantee.
Inspect native model discovery before dispatch; do not derive rankings from model names.

**Claude Code:** Haiku is the starting candidate for factual lookups; Sonnet for bounded
implementation.
Use Opus when review depth or risk warrants it and account access permits.
Aliases can resolve differently across providers; verify the actual selected model and supported
effort.

**Cursor:** Its catalog can include Cursor and other providers' models; do not equate host with
provider.
Use the current model selector or authenticated catalog, not copied OpenAI or Anthropic aliases.
Custom subagents support specific model IDs; the native `inherit` default violates our
explicit-selection policy.
No Cursor worker availability, authentication, or execution is established by this guide.

## Match effort to evidence

- For personal/open-source work, choose the least expensive capable eligible model within the
  authorized provider.
- Start lookups and mechanical edits with a smaller available model and bounded context.
- Use stronger reasoning for architecture, security, contradictory evidence, or independent review.
- Consider tools, context, reliability, latency, quota, and observed outcomes; record the selection
  rationale briefly.
- For company work, use the strongest eligible reviewer, mid-tier implementer, and smallest factual
  lookup worker.
- Company routing does not authorize company configuration changes or access to personal plans.
- Effort is separate from model selection; use supported controls and report inherited or
  unavailable settings.

## Preserve control

- Reserve Astra/Fable for main chat, never workers or auxiliary probes. Main-model selection belongs
  to the user.
- Select every worker model explicitly; never inherit the lead or change parent model, billing, or
  privileges.
- Report unavailable models before selecting a replacement; never silently substitute a model or
  provider.
- A quota or timeout failure stops personal/open-source dispatch; ask before launching or resuming
  any model run.
- After two failed acceptance passes, checkpoint and obtain approval before further
  personal/open-source model work.
- Capability recommendations are starting choices, not benchmark results or permission for
  paid-provider fallback.

## Check host contracts

- Read [Claude subagents](https://code.claude.com/docs/en/sub-agents) before changing Claude
  dispatch metadata.
- Read [Claude model configuration](https://code.claude.com/docs/en/model-config) before relying on
  aliases or effort.
- Read [Cursor subagents](https://cursor.com/docs/subagents) before changing Cursor role or model
  configuration.
- Read [Cursor models](https://cursor.com/docs/models-and-pricing) before choosing an ID or
  estimating cost.
- Use the installed Pi runner's model discovery and documentation before changing its selection
  controls.

**Evidence:** Documentation describes supported interfaces; local discovery establishes
availability, and an exercised run establishes execution.
Keep configured, installed, loaded, authenticated, and exercised states separate.
