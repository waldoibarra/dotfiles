# Shared roles for Pi and Claude Code

## Outcome

Shared rules, skills, references, and role prompts live under `~/.agents/`.
Pi delegates with an independently selected role and model, preserving global and project rules.
Use existing package capabilities; do not build a runner, generator, or role abstraction.

Read this plan before resuming the shared-role migration.
Read [the roadmap](/.agents/plans/ai-harness-roadmap.md) for the broader work and private scope.

## Decisions

| Id | Decision | Reason |
| --- | --- | --- |
| P1 | Use pinned `pi-subagents@0.77.0`. | Published runner supports per-call `agent` and `model`; no local runner maintenance. |
| P2 | Move the five roles into `home/.agents/roles/`. | One Markdown prompt per role; retain only portable name/description frontmatter. |
| P3 | Link shared roles individually into `~/.claude/agents/`; configure Pi's scan directory. | Native adapters avoid copied prompts; Claude inherits tools and uses policy-only reviewer restrictions. |
| P4 | Choose models per delegation; otherwise inherit the parent model. | Avoid provider-specific defaults in generic role definitions. |
| P5 | Configure Pi context inheritance and tools through role overrides. | Package defaults strip global rules; Pi-specific fields belong in Pi settings. |
| P6 | Disable bundled roles, prompts, skills, schedules, missions, and scripted workflows. | Single/parallel calls suffice; different parallel models require separate single-agent launches. |
| P7 | Retain Bash for reviewers, with a no-mutation instruction. | Git inspection needs Bash; this is policy, not a sandbox. |
| P8 | Keep Pi runtime/configuration under `~/.pi/agent/`. | Credentials, sessions, and runtime extensions are not portable shared content. |
| P9 | Move RTK reference into `~/.agents/`; retain a compatibility link. | Shared instructions must not depend on Claude's directory layout. |
| P10 | Explicitly install the configured runner pin before package updates. | Pi 1.1.0 skips pinned npm packages during updates, even when missing. |

Waldo requested DRY/YAGNI, explicit role/model selection, tests, and commits.
Workstation sync is authorized.
The existing five roles are retained; no new roles are introduced.

## Implementation

1. Review this plan independently using a read-only Pi process before editing runtime configuration.
2. Add isolated checks for role discovery, inheritance, installer links, and package reconciliation.
3. Move roles/reference; update Dotbot links, shared rules, Pi settings, and package updater.
4. Apply links without unrelated package upgrades; reconcile the pinned runner and test fresh sessions.
5. Audit the scoped changes independently; fix confirmed issues and run lint.
6. Update maintained guides and roadmap with observed results; commit only scoped changes.

## Verification

- Isolated Dotbot `create`/`link` run: both harnesses resolve identical role bytes; repeat remains valid.
- Package discovery: exactly five global roles; no bundled roles or accidental skills-as-roles.
- Child prompt: global rules, project rules, shared skills, and selected role are present.
- Child execution: two explicit authenticated model selections succeed; omitted model inherits the parent.
- Invalid role/model: explicit failure, never silent substitution.
- Pi reviewer tools omit `write` and `edit`; Bash remains mutation-capable.
  Claude reviewers use policy-only restrictions.
- Foreground and background delegation: final output and selected model recorded in runtime evidence.
- Updater fixture: normal profile, no project approval, declared packages reconciled; failures propagate.
- `just lint`, plus explicit Markdown checks for ignored shared files.

## Boundaries and recovery

- Do not alter work repositories, company MCP servers, credentials, or unrelated pending changes.
- Browser-role execution is tested with a canary, not a live app; no browser task was supplied.
- No full `dots` run solely for validation: it upgrades/prunes unrelated tools and can publish commits.
  Use a temporary minimal Dotbot config containing only changed destinations, then reconcile Pi packages.
- Revert scoped configuration and links to remove the runner; retain runtime evidence outside Git.
- Pin updates require rerunning integration checks; installed Pi is currently 1.1.0.

## Progress

- Repository and installed Pi/package documentation inspected.
- Independent plan review completed with `openai-codex/gpt-6-astra` (read-only Pi process).
- Review fixes: scoped installation, honest Claude restrictions, separate launches for mixed models.
- Four isolated tests failed before implementation: missing links, runner config, and updater behavior.
- Implementation delegated to `openai-codex/gpt-6-luna`; main session verified and corrected configuration.
- Runtime checks caught two issues: missing pinned-package installation and string-valued tool overrides.
  Both were fixed; role override tools use arrays as required by the installed runner.
- Four isolated provisioning tests pass, including repeat linking and both package failure paths.
- Installed SDK checks pass: five executable roles; invalid role/model selections fail explicitly.
- All five roles ran successfully in a disposable workspace on Pi 1.1.0 with runner 0.77.0.
  Foreground tests selected Luna/Astra explicitly and inherited the parent model for `docs-writer`.
  Concurrent background tests selected different models for `implementer` and `browser-tester`.
- Child sessions contain global rules, project fixture instructions, shared skills, and role bodies.
  Provider response metadata confirms the selected models; no model self-report was used as proof.
- A fresh CLI session enabled subagents and delegated to Astra through the model-issued tool successfully.
- `pi -p '/run …'` failed with stale context; the maintained guide documents this headless limitation.
  Interactive TUI slash behavior was not exercised; no upstream patch was introduced.
- Claude Code accepted `--agent plan-reviewer` and quoted the shared role's no-editing rule.
  The canary disabled tools and MCP servers; it did not test reviewer task performance.
- Independent audit through `code-auditor` on Astra returned **pass** with no confirmed actionable issues.
- `just lint`, explicit shared-file Markdown lint, `git diff --check`, and offline runtime checks pass.
- All four isolated tests also pass against an exported staged tree, independent of unstaged cleanup.
- Only changed agent links and the pinned package were installed; no full `dots` or publication ran.
- Runtime evidence remains in temporary directories, outside Git. Work skills/MCPs remain unverified.
- Commit scope includes shared-role provisioning and its required skill/config ownership updates.
  Separate cleanup and concurrent Lens notes are excluded.
