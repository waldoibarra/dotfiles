---
name: shared-todo
description: >-
  Records assigned personal manual tasks in the shared life to-do list, checking for duplicates.
  Use when asked to add a pending task, record a personal task, or update the shared to-do.
  Excludes coding checklists, issue trackers, scheduled reminders, and performing the recorded task.
---

# Record a shared personal task

**Outcome:** Save one requested task with its assignee in `~/life/to-do.md`, without performing it.
The shared list is a local Markdown note, not an agent checklist or external task service.

## Confirm the destination and assignee

1. Read `~/life/AGENTS.md` and its required maintenance guidance before editing the vault.
2. Read `~/life/to-do.md` for the current format and existing tasks.
3. Resolve the assignee from the request; for “my task,” use `~/.agents/personal-context.md`.
4. Ask only when the task or assignee remains unclear.

Keep restricted work content out of the shared vault, following its owning instructions.
Do not infer deadlines or priorities.

## Save without duplication

1. Check for an equivalent pending task with the same assignee.
2. If one exists, report it instead of adding another.
3. Otherwise, add one unchecked item under `## Pending` using the existing assignee format:

    ```markdown
    - [ ] **Name:** Task description.
    ```

4. Remove an empty-list placeholder only when adding the first pending task.
5. Preserve existing tasks, identifiers, and supplied context.
6. Follow the vault's content-language rules, independently of the conversation language.

Adding a task does not authorize performing it, spending money, or creating a scheduled reminder.
External task-service discovery is unnecessary for this workflow.

## Verify and confirm

Re-read the edited note and confirm the task and assignee were saved correctly.
Report the task, assignee, and `~/life/to-do.md` location briefly.
Distinguish local saving from remote synchronization when Sync status cannot be verified.

**Maintenance:** Read `evals/evals.json` only when changing this skill; scenarios are not executed
behavioral evidence.
