---
name: commit
description: >-
  Prepares atomic, verified Git commits and authorized pushes using repository conventions and
  readable messages. Use when asked to "commit these changes", "push when done", or
  "write a commit message". Message drafting alone never authorizes Git writes.
---

# Commit and deliver

- **IS:** scoped Git delivery and readable commit messages after implementation is ready.
- **IS NOT:** implementation, unrelated cleanup, automatic publication, or a replacement for
  repository hooks.

**Done:** Authorized changes are committed; requested pushes are verified against the intended
remote branch.
Report local and remote outcomes separately; a commit is not proof of a successful push.

## Establish scope

1. Read repository instructions, current status, branch, upstream, and commit-message configuration.
2. Identify authorized files and existing unrelated edits; inspect the full diff, including
  untracked files.
3. Verify the intended destination, audience, repository visibility, and any deployment triggered by
  pushing.
4. Check secrets, private evidence, source links, and generated files before staging.
5. Run the applicable checks; report unavailable prerequisites or unresolved failures before
  delivery.

**Authority:** Drafting a message permits no mutation. Commit and push only within the user's
granted scope.
Never change visibility, force-push, discard edits, or bypass hooks to make delivery succeed.
Keep messages, comments, and posts behind their own publication approvals.

## Shape the commit

- Never add `Co-Authored-By` or AI attribution.
- Use atomic conventional commits: one concern, typed subject, at most 50 characters.
- Wrap optional bodies at 72 characters; explain why. Put breaking changes and references in
  footers.
- Update affected documentation in the same commit as behavior changes.
- Use an imperative summary; separate it from an optional body with a blank line.
- Explain intent, constraints, and trade-offs when the diff cannot explain them.
- Match repository-required types and casing; do not introduce a new convention during delivery.

```text
docs(harness): clarify memory ownership

Separate current guidance from historical evidence so later sessions
can retrieve decisions without treating superseded steps as active.
```

## Deliver serially

1. Stage the named authorized paths; inspect the staged diff and run `git diff --check`.
2. Run each commit or hook-triggering command separately; shared hook stashes can absorb concurrent
  work.
3. Inspect the resulting commit and working tree; preserve unrelated edits.
4. If pushing is authorized, push the explicit intended branch without rewriting remote history.
5. Verify the remote branch matches the intended commit; report any remaining local changes.

**Failure:** Stop on rejected pushes or hook failures; diagnose before retrying.
Fetch and reconcile within authority; never force-push or conceal validation failures.
Do not claim remote CI or deployment passed merely because Git accepted the push.

## Sources

**Adaptation:** Tim Pope's [A Note About Git Commit
Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) supplies
subject/body separation,
imperative summaries, and readable wrapping.
Our existing Conventional Commit prefix and strict 50-character subject limit remain local
conventions.
The article recommends approximately 50 characters; it does not prescribe Conventional Commits.
Editor-specific setup examples are excluded because they are not part of Git delivery.

**Maintenance:** Read `evals/evals.json` when changing this skill; scenarios are specifications, not
executed evidence.
