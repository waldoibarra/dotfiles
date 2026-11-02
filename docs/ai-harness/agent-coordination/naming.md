# Name agents, tabs, and workspaces

Back to [agent coordination](README.md).

**Name every agent `<context>-<model>[-<role>]`.** Peers address a name, not a pane ID.
Pane IDs change occupants; a name follows the agent until it exits.

| Context | Source | Examples |
| --- | --- | --- |
| Linear issue | Issue key in the tab label | `roy-92-fable`, `roy-92-astra` |
| Repository without an issue | Directory name, shortened | `melodix-api-fable`, `kh-astra` |
| Learning or personal project | Topic slug | `info-arch-astra`, `life-fable` |
| Same model twice in one context | Add a role suffix | `kh-astra-docs`, `kh-astra-review` |

- Lowercase and hyphens only; Herdr accepts `[a-z][a-z0-9_-]{0,31}`.
- Always keep the model suffix (`fable`, `astra`, `opus`); it tells peers which harness answers.
- Add a role suffix only when context plus model would collide.
- Names are unique per Herdr server, so choose a specific context.

```sh
herdr agent rename <pane-or-name> roy-92-astra
herdr agent list   # the `name` field confirms it
```

## Label your own session

A session renames its own pane and tab on its first reply, and again when it starts coordinating.

| Layer | Label | Example |
| --- | --- | --- |
| Pane and agent | Your name from the convention above | `dotfiles-fable` |
| Tab | The current task in two to four words, never the directory | `Docs restructure` |
| Workspace | Leave it; the operator owns workspaces they created | |

```sh
herdr agent rename "$HERDR_PANE_ID" dotfiles-fable
herdr tab rename <own-tab-id> "Docs restructure"   # tab id from `herdr pane get "$HERDR_PANE_ID"`
```
