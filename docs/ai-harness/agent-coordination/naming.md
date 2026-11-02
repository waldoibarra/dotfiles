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
