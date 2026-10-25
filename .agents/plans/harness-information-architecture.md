# Harness information architecture

**Outcome:** Assertive communication and maintainability guide a navigable, evolving working
environment.
Current guidance stays separate from historical evidence; each repository and vault owns its shared
language.

**Authority:** The user approved implementation, Markdown refactoring, scoped commits, and pushes in
this session.
The supplied ADR gate is reusable guidance explicitly approved for adaptation; no work repository is
evidence.

## Scope and ownership

| Workspace | Work | Delivery |
| --- | --- | --- |
| Dotfiles | Shared instructions, skills, architecture, model routing, lifecycle guidance, and verification | Existing `origin/main` |
| Family repositories | Local instructions, overview, glossary, maintenance navigation, and stale documentation | Each existing upstream branch |
| Personal portfolio | Public product documentation, glossary, and local decision guidance | Existing `origin/trunk` |
| Life vault | Shared-memory map, glossary, lifecycle, and coordination navigation | Obsidian Sync, never Git |

**Excluded:** Work directories, credentials, private histories, external skill installations,
application behavior, deployment, and package upgrades.
Family means the three discovered repositories: AI Architecture Big Picture, Habit Tracker, and
Money Tracker.
Existing session-owned edits remain part of delivery: `home/.agents/AGENTS.md`,
`docs/agent-instructions.md`,
`docs/agent-skills.md`, `.agents/plans/ai-harness-roadmap.md`, and `.agents/README.md`.
All other repositories began clean; verify each staged diff against its assigned files before
committing.
No private family records or source excerpts enter public portfolio or reusable dotfiles guidance.

## Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| IA1 | Keep a compact global contract with task-triggered references. | Universal authority and privacy constraints must remain visible. |
| IA2 | Put lead orchestration duties in the existing orchestration reference as a lead-only role. | Avoid registering a recursive worker or changing native role discovery. |
| IA3 | Add a commit skill based on the supplied article and existing repository conventions. | Commit procedure loads only for Git delivery. |
| IA4 | Keep one model-and-role selection reference across Pi, Claude Code, and Cursor. | Capabilities and availability differ; model names are not universal rankings. |
| IA5 | Require meaningful root glossaries and scoped lifecycle checks. | Shared terms and current guidance improve future decisions. |

| ID | Decision | Reason |
| --- | --- | --- |
| IA6 | Archive consequential superseded rationale; remove obsolete operational instructions within scope. | Preservation must not keep stale instructions authoritative. |
| IA7 | Apply all three ADR gates before creating an ADR. | Reversible choices and how-to material do not justify permanent decision records. |
| IA8 | Keep knowledge, runtime state, policy, and personal context with separate owners. | Prevent cross-scope leakage and competing sources of truth. |
| IA9 | Use bounded repository workers with explicit OpenAI models. | Independent writing lanes reduce cost without sharing a working tree. |
| IA10 | Verify loading separately from behavior; do not run unapproved behavioral experiments. | Static checks cannot establish reliable recall or model effectiveness. |

## Implementation order

1. Inspect local instructions, branches, clean baselines, and source ownership; check vault Sync
  before edits.
2. Independently review this plan before implementation.
3. Dispatch one writer per family repository and portfolio; retain shared-policy and vault edits in
  the lead.
4. Refactor the global contract, commit skill, lead role, communication, delegation, and
  memory-lifecycle references.
5. Update dotfiles overview, architecture, glossary, maintenance owners, roadmap entry points, and
  delivery tests.
6. Refactor the vault overview and maintenance navigation; preserve personal facts and all safety
  conditions.
7. Audit cross-document ownership, glossary links, retirement rules, privacy, and authorization
  boundaries.
8. Validate each workspace; install only new owned links and rerender Cursor without running full
  sync.
9. Commit each repository separately, push its existing branch, and verify upstream equality.
10. Check vault Sync history and report local, uploaded, and other-device evidence separately.

## Preservation map

- Global communication details move to the existing communication reference; language and safety
  scope remain explicit.
- Global orchestration procedures move to the lead-role reference; all delegation requires reading
  its selection guidance.
- Global commit conventions move to the new commit skill; repository-specific hooks retain
  precedence.
- Global documentation detail moves to the existing documentation skill and a shared lifecycle
  reference.
- Scope, identity selection, privacy, approval, and unavailable-guidance handling remain in the
  global contract.
- Historical roadmap sections retain original claims and verification limits; active navigation
  selects relevant sections.
- Repository docs retain local commands, privacy, prototype boundaries, and product facts.
- The vault retains shared-profile boundaries, Markdown-only edits, Sync checks, and human review.

### Detailed retention contract

**Global sections:** Preserve every requirement unless the following mapping explicitly changes its
ownership.

- Default stance: keep assertive communication and maintainability globally; retain verifiability
  inside maintainability.
- Find the owner: keep missing-guidance handling and canonical ownership; expand task-triggered
  pointers.
- Machine-specific context: preserve all five mandatory startup reads, real-symlink resolution, and
  NDA separation.
- Evidence and decisions: preserve all nine evidence, uncertainty, decision, approval, and readiness
  requirements globally.
- Communication: move all sentence, paragraph, tone, language, source-material, and exception rules
  to `communication-rules.md`.
- Authority: preserve every message approval, write scope, memory approval, privacy, and
  individual-preference boundary globally.
- Orchestration: move all eight rules verbatim into `orchestration.md`; require it before planning
  or any delegation.
- Harness design: retain its reading trigger; existing `harness-design.md` owns all three
  architectural constraints.
- Shell commands: move all four requirements verbatim to new `references/shell.md`; require it
  before shell execution.
- Commits: move all four conventions verbatim to `skills/commit/SKILL.md`; require it before Git
  delivery.
- Learning: keep closure routing globally; `references/memory.md` retains recording, ownership, and
  promotion boundaries.
- Documentation: move every formatting, naming, preservation, and link rule into
  `docs-maintenance/references/conventions.md`.
- RTK: retain the explicit global reading trigger unchanged.

**New paths:** All shared references above live under `home/.agents/`.
Add root `GLOSSARY.md` and `docs/architecture.md` in dotfiles; add root glossaries in the other
approved workspaces.
The lead role remains a section of `references/orchestration.md`, not a new discoverable worker
file.
`references/delegation.md` owns cross-harness model selection; native catalogs remain the source for
actual availability.

**ADR gate:** First require an explicit request or the project's established decision-record
process.
Then require all three: hard to reverse, surprising without context, and a real trade-off between
viable alternatives.
Keep failing content in reference or how-to documentation; do not manufacture ADRs during this
refactor.

**Glossaries:** Define existing domain terms, keep definitions separate from implementation, and
link from local instructions.
Do not invent terminology, copy private facts, or create empty vocabulary scaffolding.

**Retirement:** Mark consequential replacements with successor links; remove stale operational
instructions within authorized scope.
Keep temporary exceptions scoped with an end or recheck condition; unresolved conflicts stay
explicit.
Preserve safety warnings and protected historical snapshots; do not apply one workspace's retention
rules elsewhere.

**Publication gate:** Review staged content, URLs, derived claims, visibility, and audience before
every repository push.
Private family sources and links must not enter public repositories; the approved reusable ADR
excerpt is the exception.
Portfolio Markdown-only paths do not match production workflow filters; recheck this against the
final staged diff.

## Verification

**Dotfiles:** Run `just lint`, explicit skill Markdown checks, authoring validators, and both Python
harness suites.
Use the installed compiled Pi host for fresh-context checks without inference.
Run `python3 scripts/tests/test-agent-harness.py` and `python3 scripts/tests/test-cursor-rule.py`.
Set `PI_PACKAGE_DIR` for compiled-host coverage and run `node
scripts/tests/check-agent-startup.mjs`.
Assert both golden-rule markers, full shared-policy bytes, installed commit-skill discovery, and
deferred specialist bodies.
Extend isolated delivery assertions for `commit/SKILL.md`, its scenarios, and all new shared
reference files.
Run `bash ~/.agents/skills/agent-skills-creator/scripts/validate.sh` against each changed skill
bundle.
Compare the detailed retention contract against every changed global section before accepting the
split.
Verify new links and unchanged-input installation behavior in isolated homes before installing them
locally.

**Repositories:** Use each repository's documented Markdown checks, link checks, and `git diff
--check`.
No prototype execution, package installation, Terraform, deployment, or application changes are
needed.
Read public portfolio CI before pushing to avoid implying deployment approval.

**Vault:** Run `just obsidian-check` for touched Markdown and verify current content in Sync
history.
No other-device receipt claim without evidence from that device.

**Behavioral cases:** Specify stale decisions, temporary exceptions, rejected proposals, and scoped
retrieval without executing model probes.
Independent review uses existing worker routing; at most two failed acceptance rounds before
checkpointing.
Quota or timeout failures stop model dispatch pending approval.

## Recovery

Revert scoped repository commits without overwriting unrelated changes; restore vault notes through
reviewed Sync history.
Remove only newly installed, verified skill or reference links and rerender Cursor after restoring
source.
Reload clients after instruction changes; native Claude and Cursor loading remains separately
verifiable.

## Results

**Implemented:** Split global instructions into golden rules, authority, startup context, and
task-triggered owners.
Added the commit skill, lead-only role, model-selection guide, memory lifecycle, glossary, and
architecture map.
Updated documentation maintenance and project setup with grounded shared language and strict ADR
gates.

**Preservation:** Independent Sol review found no confirmed authority or privacy loss in the global
split.
Family reviews preserved teaching, prototype, financial privacy, and existing decision contracts.
Review corrections repaired glossary navigation, retained-input wording, and stale model examples.
New ignored sources require explicit staging; installation success alone does not establish Git
delivery.

**Checks:** Dotfiles lint, explicit home Markdown checks, and local-link checks pass.
All eleven harness tests and six Cursor tests pass, including compiled-host startup construction.
The commit, documentation maintenance, skill coordinator, and project setup bundles pass their
authoring validators.
New skill/reference links are installed; repeated linking succeeds without forced replacement.
Cursor's generated rule was refreshed without workstation sync or external package updates.

**Shared memory:** All 23 vault Markdown files pass local checks and match their newest Sync history
versions.
CLI and app report completion; another device's receipt remains unverified.
No vault Git workflow, non-Markdown edit, or company-workspace access occurred.

**Model evidence:** GPT-5.5 was configured but unavailable; Sol ran after explicit reporting.
No quota or timeout failure occurred.
No behavioral comparison or new native Claude/Cursor loading probe ran.
Configured, installed, loaded, exercised, committed, and pushed states remain separate.

**Published:** All five repository changes were committed and pushed to their existing upstream
branches.
Remote refs matched local HEAD and all five working trees were clean after delivery.
Dotfiles implementation: `7ea7c15`; family knowledge: `8a1a4a5`; Habit Tracker: `a0cd507`;
Money Tracker: `05f2532`; portfolio: `1ef486a`.
The portfolio commit hook required capitalization; the corrected commit passed without bypassing
hooks.
Obsidian CLI and app report completion; no Git operation ran in the vault.
Portfolio Markdown, EditorConfig, and local-link checks pass; its final prose review was
non-independent.
Strict bold-lead-in coverage remains incomplete in some legacy prose; do not claim universal
formatting compliance.
Two portfolio implementation passes are complete; further model formatting work requires an approval
checkpoint.

## Communication rules follow-through

**Approved:** Preserve the user's `communication-rules.md` rename and strengthen the global
assertive-communication requirement.
The golden rule now requires reading, applying, and checking the rules for every reply or artifact.
It covers lead and worker output, including documentation, code comments, and commit messages.

**Compatibility:** Existing vault pointers still use `communication.md`; its installed alias
resolves to the renamed source.
Both paths share one canonical policy; no vault or external-skill rewrite was needed.
Claude's Clear adapter now references the golden rule instead of the removed Communication section.

**Verified:** The new requirement and alias-migration tests failed before implementation, then
passed.
All twelve harness tests and six Cursor tests pass, including fresh Pi prompt construction.
Repository lint, explicit home Markdown checks, and local links pass.
The renamed link, compatibility alias, and refreshed Cursor rule are installed.
These checks prove delivery and loaded requirements, not universal writing compliance or resolved
legacy formatting.
