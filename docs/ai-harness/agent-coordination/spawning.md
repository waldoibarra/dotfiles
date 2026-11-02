# Spawn and close a worker

Back to [agent coordination](README.md). Write the [brief](briefing.md) first.

Use this when the operator asks to spawn a worker, an independent reviewer, or a peer agent.
Say "spawn a worker" or "spawn an independent reviewer"; add "with Astra" or "with Claude" to pick
the harness. Without a harness, use Pi, because a different model gives a more independent read.

**Each worker gets a disposable workspace holding one tab with one pane.** This mirrors
firstmate's one-task container, so adopting it later changes nothing. Split the lead's tab only
when the operator says "split", "beside me", or "in this tab".

Each layer answers one question, so the sidebar identifies the work without opening it:

| Layer | Question | Label | Example |
| --- | --- | --- | --- |
| Workspace | What task? | Task in two to four words, Title case | `Glossary proposal` |
| Tab | What role? | The glossary role, plus the deliverable when several | `Independent reviewer` |
| Agent and pane | Who? | The [agent name](naming.md) | `harness-glossary-astra` |

1. Resolve the lead's own pane and name with `herdr agent list`.
2. Write the [brief](briefing.md) to a file before starting the worker.
3. Create the workspace without taking focus, passing the worker's directory and the task label.
  The result's `root_pane.pane_id` and `tab.tab_id` are the new pane and tab.
4. Rename the tab to the role and the pane to the worker's name.
5. Start the worker under that name. Use `--kind claude` for Claude Code. Native agent flags go
  after `--`.
6. Wait for idle once, after start. Then send the first message, written with the
  [AIM template](/docs/prompting.md#prompt-template); a bare "read the brief at a path" is not a
  prompt. Never add `--wait`.
7. Do not wait again. The reply arrives as a prompt in the lead's session; a second wait blocks
  the lead while that message is already queued. Verify the reply's claims against files.
8. Close the worker's workspace once its deliverable is verified, unless the operator asked to
  keep it. Close only containers this lead created. Closing ends the agent; say so in the reply.

```sh
herdr workspace create --cwd <dir> --label "<Task label>" --no-focus                 # step 3
herdr tab rename <new-tab-id> "<Role>"                                               # step 4
herdr pane rename <new-pane-id> <name>
herdr agent start <name> --kind pi --pane <new-pane-id> --timeout 60000              # step 5
herdr agent wait <name> --until idle --timeout 60000                                 # step 6
herdr agent prompt <name> "$(cat <first-message-file>)"                              # step 6
herdr workspace close <new-workspace-id>                                             # step 8
```

On request, replace steps 3 and 4 with a split of the lead's pane; `pane.pane_id` is the new pane:

```sh
herdr pane split <lead-pane-id> --direction right --ratio 0.5 --cwd <dir> --no-focus
herdr pane close <new-pane-id>   # when finished
```

Workspace, tab, and pane creation, renames, and closes were exercised on 2026-11-01.
Starting an agent and sending prompts keep their usual approval boundaries.
