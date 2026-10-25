---
name: commit
description: >-
  Prepares atomic, verified Git commits and authorized pushes using repository conventions and readable messages.
  Use when asked to "commit these changes", "push when done", or "write a commit message".
  Message drafting alone never authorizes Git writes.
---

# Commit verified changes

**Outcome:** Commit the authorized changes and verify any separately requested push against the
intended remote branch.
This workflow owns scoped Git delivery, not implementation, unrelated cleanup, automatic
publication, or replacing repository hooks.
A local commit does not prove remote delivery, CI success, or deployment.

## Determine the authorized action

- Drafting a message permits no mutation.
- Commit and push only within the user's granted scope.
- Never change visibility, force-push, discard edits, or bypass hooks to make delivery succeed.
- Keep messages, comments, and posts behind their own publication approvals.

## Inspect the change before staging

1. Read repository instructions, current status, branch, upstream, and commit-message configuration.
2. Identify task-owned files and unrelated edits; inspect the full diff, including untracked files.
3. Verify the intended destination, audience, repository visibility, and any deployment triggered by
    pushing.
4. Check secrets, private evidence, source links, and generated files before staging.
5. Run applicable checks; report unavailable prerequisites or unresolved failures before delivery.

## Write one coherent commit

| Part | Contract |
| --- | --- |
| Scope | One concern, with affected documentation updated alongside behavior |
| Subject | Conventional type, imperative summary, at most 50 characters |
| Body | Optional; wrap at 72 characters and explain intent, constraints, or tradeoffs |
| Separation | Blank line between the subject and optional body |
| Footers | Breaking changes and references |
| Attribution | Never add `Co-Authored-By` or AI attribution |

Match repository-required types and casing; do not introduce a new convention during delivery.
Explain what the diff cannot show rather than repeating obvious file changes.

```text
docs(harness): clarify memory ownership

Separate current guidance from historical evidence. Later sessions can
retrieve decisions without treating superseded steps as active.
```

## Deliver serially and inspect the result

1. Stage named authorized paths; inspect the staged diff and run `git diff --check`.
2. Run each commit or hook-triggering command separately; shared hook stashes can absorb concurrent
    work.
3. Inspect the resulting commit and working tree, preserving unrelated edits.
4. If pushing is authorized, push the explicit intended branch without rewriting remote history.
5. Verify the remote branch matches the intended commit; report remaining local changes.

**Failure:** Stop on rejected pushes or hook failures and diagnose before retrying.
Fetch and reconcile only within authority; never force-push or conceal validation failures.
Report local and remote outcomes separately, without treating Git acceptance as CI or deployment
evidence.

## Source and maintenance

Tim Pope's [A Note About Git Commit
Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)
informs subject/body separation, imperative summaries, and readable wrapping.
The Conventional Commit prefix and strict 50-character subject limit are local conventions.
The article recommends approximately 50 characters; it does not prescribe Conventional Commits.
Editor-specific setup examples are excluded because they are outside Git delivery.

Read `evals/evals.json` when changing this skill; scenarios are specifications, not executed
evidence.
