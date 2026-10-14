# AI harness roadmap

**Next:** Validate shared roles in ordinary Pi and Claude Code sessions.

**Scope:** Personal and open-source workflows. Company adaptation and Cursor support remain
deferred.

## Do next

### ASAP: validate shared roles

**State:** Shared roles are installed. Historical probes passed; everyday use remains unverified.

- Choose a real task for each harness.
- Confirm invocation, explicit model selection, and actual effort settings.
- Inspect inherited instructions and available tools.
- Verify approval boundaries and useful outcomes, not merely successful dispatch.
- Record observed results and remaining limits in the shared roles plan.

**Done when:** Both harnesses complete real delegated work with verified boundaries and useful
outcomes.

- Read [shared roles](/.agents/plans/pi-shared-roles.md) before reviewing historical discovery and
  dispatch evidence.
- Read [delegation](/docs/coding-agents/pi/delegation.md) before selecting Pi roles and models.
- Read [harness verification](/docs/coding-agents/personal-workflow.md) before defining acceptance
  or approving behavioral probes.

### Pending workstation steps

1. **Restart:** Restart Pi and Claude Code after the completed `dots` integration updates.
2. **Pi trust:** At the work root, run `pi`, then `/trust` once if still required.
3. **Slack:** Use `/mcp` in Claude Code to re-authorize if still required.
4. **Cleanup:** Remove retired applications and data only after reviewing the prerequisites below.

**Unverified:** Restart, work-root trust, Slack authorization, and retired-harness cleanup have not
been confirmed complete.

```text
Upgrade OpenUsage first: v0.7.13+ reads Pi's login, not `~/.codex`.
```

```sh
rm -rf ~/.codex   # only after OpenUsage shows the Codex card via Pi
```

**Prerequisites:** Read [cleanup
history](/.agents/plans/history/ai-harness-roadmap-2026-10-13.md#waldos-pending-steps) before
removing retired applications or credentials.

### Work follow-up

**Status:** Earlier work-hub changes used `chore/ai-harness`; current branch and commit state remain
unverified.

- Inspect the private companion before resuming work changes.
- Confirm saved changes before switching branches.
- Keep company configuration and evidence in the work workspace.
- Verify `issue-handoff` and `staging-deploy` through actual use; earlier reports did not establish
  execution.

**Private companion:** `<work root>/.agents/plans/ai-harness-work-scope.md` owns company-specific
continuation.

## Completed and verified

### Ghostwriter setup

- Initial personal profile committed and pushed in `27a4388`.
- `dots` completed; `~/.config/ghostwriter/soul.md` links to its tracked source.
- Communication-rule audit, Markdown, YAML, and EditorConfig checks passed.
- Preferences come from the setup conversation; representative platform samples remain unmeasured.
- Refinement through real drafts is optional, not an ASAP setup task.

**Owner:** Read [Ghostwriter voice](/docs/coding-agents/README.md#ghostwriter-voice) before changing
profile ownership or delivery.

### Shared harness foundation

- Claude Code and Pi share policy, references, skills, and five provider-neutral roles.
- Role contracts, reference delivery, and the personal improvement workflow were implemented and
  checked.
- Retired harness configuration was removed from dotfiles; local application and data cleanup
  remains separate.
- Historical synthetic probes establish intended responses, not everyday reliability or comparative
  model capability.
- Later instruction refactors still need fresh-session loading and behavioral verification.

**Owner:** Read [agent instructions](/docs/agent-instructions.md) before changing policy ownership,
loading, or shared roles.

### Learning skills

- `session-improvement` owns evidence-backed improvement proposals and routes approved execution.
- `socratic-learning` owns reusable teaching; the teacher-role proposal is superseded.
- Both skills were linked and discovered through Pi's resource loader.
- Claude filesystem installation was verified; fresh Claude discovery and behavioral execution
  remain unverified.
- Synthetic teaching smoke passed; the subsequent ownership clarification received static checks
  only.
- Live teaching effectiveness and comparative skill performance remain unmeasured.

**Owner:** Read [learning skills](/docs/agent-skills.md#learning-and-session-improvement) before
changing either skill's responsibilities.

### Separate delivery records

- Read [Lens status](/.agents/plans/pi-lens-delivery.md) before continuing Lens work or claiming
  installation readiness.
- Read [Lens verification](/.agents/plans/pi-lens-verification.md) before repeating acceptance
  checks.
- Read [personal MCP](/.agents/plans/personal-mcp.md) before continuing personal integrations or
  authentication setup.

**Boundary:** Those records own current status; older observations in this roadmap's archive are
historical evidence.

## Decisions still open

| ID | Question | Current default |
| --- | --- | --- |
| D1 | Extend work MCPs to Pi? | Claude-only; Pi uses skill fallbacks. |
| D2 | Where should company-specific roadmap details live? | Private companion; public notes remain generic. |
| D3 | How should PR images be attached? | Manual upload; automation remains unresolved. |
| D4 | Remove the `docs/quotas.md` OpenCode Go reference? | Keep it; the subscription differs from the retired agent. |

**Scope:** D1, D3, and D4 require work-context review; this document authorizes no company changes.

## Settled boundaries

| ID | Decision | Reason |
| --- | --- | --- |
| D5 | Unanswered proposals never authorize edits. | Silence is not approval. |
| D6 | Keep individual preferences separate. | Another operator has not consented to inherit them. |

**Approval:** Company adaptation, runtime changes, and publication require their own approval.

**Policy:** Read [global instructions](/home/.agents/AGENTS.md) before changing shared behavioral
boundaries.

**History:** Read [approved decisions](/.agents/plans/history/ai-harness-roadmap-2026-10-13.md)
before revisiting H1–H17, G1–G12, or S1–S8.

## Deferred ideas

**Status:** These are retained proposals, not approved implementation work.

### Personal workflow

- Observe ordinary sessions before proposing more global instructions.
- Consider broader model-selection scenarios; no capability ranking is established.
- Review absorbed memories and unused skills; the earlier 100-line instruction target remains an
  unvalidated heuristic.

### Communication lint

- Consider a warning-only Markdown check for the 17-word paragraph and list-item limit.
- Skip fenced blocks; never shorten safety content to satisfy the limit.
- Align shared instructions, Clear, and Pi guidance before adding automation.
- Review role references next; only then consider `hk`, Claude hooks, or a Pi extension.

### Pi output styles

- Explore switchable styles without duplicating the shared communication source.
- Candidates: `pi-custom-system-prompt` and `pi-system-prompt`; compatibility with this fork remains
  unverified.
- Check maintenance, licensing, loading behavior, and shared-source support before selecting an
  integration.

### Cursor and company work

- Verify Cursor instruction loading before configuration; support has not started.
- Defer company workflow adaptation until separately approved.
- Consider a work `rfc` skill covering templates, tracker mirrors, indexing, and announcement
  drafts.
- Consider a separate review server so development reloads do not interrupt review.
- Add work setup links for role agents only after a work-only role exists.

## Evidence and maintenance

**Archive:** The [historical roadmap](/.agents/plans/history/ai-harness-roadmap-2026-10-13.md)
preserves the full source from `7b3ecb8`, unchanged.

- Historical decisions, measurements, incidents, rollback instructions, and superseded proposals
  remain available there.
- Archive statuses describe their original sessions; they are neither current readiness claims nor
  new authorization.
- Work details were already tracked; this rewrite adds no private workspace evidence.
- Update active milestones when verification changes; keep implementation procedures in their owning
  guides.

**Rewrite verified:** Archive bytes, decision rows, local links, prose limits, Markdown, and
EditorConfig checks passed.

**Review:** Independent plan review completed; final edits were self-reviewed.
