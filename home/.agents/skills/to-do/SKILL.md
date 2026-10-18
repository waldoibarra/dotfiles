---
name: to-do
description: >-
  Adds personal manual tasks to the shared life to-do list with an assignee and duplicate checks.
  Use when asked to add a pending task, put something on our shared to-do, or record a personal task.
  Not for coding checklists, issue trackers, scheduled reminders, or performing the recorded task.
---

# Shared to-do

Record requested manual tasks in `~/life/to-do.md`, not in an agent's temporary task list.

## Workflow

1. Read `~/life/AGENTS.md` and its required maintenance guidance before editing the vault.
2. Read `~/life/to-do.md` for its current format and existing tasks.
3. Resolve the assignee from the request; for "my task", use `~/.agents/personal-context.md`.
    Ask only when the task or assignee remains unclear.
4. Check for an equivalent pending task with the same assignee.
    If present, report it instead of adding a duplicate.
5. Add one unchecked item under `## Pending`, following the file's assignee format:

    ```markdown
    - [ ] **Name:** Task description.
    ```

    Remove an empty-list placeholder only when adding the first pending task.
    Preserve existing tasks, identifiers, and supplied context; do not invent deadlines or priorities.
    Follow the vault's content-language rules, independently of the conversation language.
6. Re-read the edited note and confirm the task and assignee were saved correctly.
7. Confirm briefly with the task, assignee, and `~/life/to-do.md` location.
    Distinguish local saving from remote synchronization when Sync status cannot be verified.

## Boundaries

Adding a task does not authorize performing it, spending money, or creating a scheduled reminder.
Keep restricted work content out of the shared vault, following its owning instructions.

## Gotchas

The shared list is a local Markdown note; external task-service discovery is unnecessary for this workflow.

## Maintenance

Read `evals/evals.json` only when changing this skill; scenarios are not executed behavioral evidence.
