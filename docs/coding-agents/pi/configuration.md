# Pi configuration

Tracked preferences live under [`home/.pi/agent`](../../../home/.pi/agent). Dotbot links each JSON
file into the normal profile. The profile directory stays real; credentials and runtime data do
not enter the repository.

## Managed files

| Path | Purpose and current state |
| --- | --- |
| `~/.pi/agent/settings.json` | Linked to [settings.json](../../../home/.pi/agent/settings.json): coding defaults, voice package, compaction and reserves. |
| `~/.pi/agent/models.json` | Linked to [models.json](../../../home/.pi/agent/models.json): per-model context-window overrides. |
| `~/.pi/agent/keybindings.json` | Linked to [keybindings.json](../../../home/.pi/agent/keybindings.json): Ctrl+L for voice, Option+L for the tree filter. |
| `~/.pi/agent/AGENTS.md` | Dotbot link to [shared agent instructions](../../../home/.agents/AGENTS.md). |
| `~/.pi/agent/npm/node_modules/pi-live-codex` | Pi-managed extension code and dependencies. Local edits would be overwritten by updates. |
| `~/.pi/agent/auth.json` | Private authentication state; never tracked or copied between agents. |
| `~/.pi/agent/models-store.json` | Generated model cache, not the configuration source. |
| `~/.pi/pi-live-codex.lock` | Shared microphone-ownership lock, outside the agent directory. |

The relevant top-level settings are `defaultProvider: "openai-codex"`,
`defaultModel: "gpt-6-astra"`, `packages: ["npm:pi-live-codex"]`, and `compaction.enabled: true`.
Edit the tracked sources for persistent preferences and package declarations. Pi's settings writer
follows the symlink, so changes through Pi's UI or package commands can also change the repository.
Review those diffs before committing. Keep secrets and machine-specific values out of linked files.
There is no Pi merge layer or managed-copy step. Dotbot's normal backup behavior applies when it
replaces existing local files with links.

Authentication, sessions, caches, native binaries, and voice locks are separate and stay outside
Git. They are not linked, copied, or removed by this configuration step. Package updates target
only `npm:pi-live-codex`. [Installation and sync](installation.md) describes the updater sequence.

## Extended context and compaction

`models.json` sets `providers.openai-codex.modelOverrides[MODEL_ID].contextWindow` to **1,050,000**
for each of these exact model IDs. In `settings.json`, the corresponding
`compaction.modelOverrides["openai-codex/MODEL_ID"].reserveTokens` is **128,000**.

| Model ID | Total context | Response reserve |
| --- | --- | --- |
| `gpt-5.5` | 1,050,000 | 128,000 |
| `gpt-5.6-luna` | 1,050,000 | 128,000 |
| `gpt-5.6-sol` | 1,050,000 | 128,000 |
| `gpt-5.6-terra` | 1,050,000 | 128,000 |
| `gpt-6-astra` | 1,050,000 | 128,000 |
| `gpt-6-luna` | 1,050,000 | 128,000 |
| `gpt-6-sol` | 1,050,000 | 128,000 |
| `gpt-6.1-sol` | 1,050,000 | 128,000 |

`gpt-5.3-codex-spark` retains its catalog window of **128,000**, without an override. The expanded
models leave 922,000 tokens before the response reserve. The reserve also affects compaction
summary limits; it is not only a trigger threshold.

Pi loaded these settings and displayed Astra as `1.1M (auto)`, rounding the total window.
Requests beyond the previous 272,000-token catalog limit were not tested against the subscription
backend. Client metadata and published model capacities do not prove backend acceptance at the
maximum window.

Pi 1.0.4 had no equivalent of OMP's extended-context toggle. OMP's existing setting was left alone.
The integration retains the tested overrides. Recheck native Pi support and current model
specifications when changing them. New model IDs do not inherit these values automatically.

## Keybindings

The local `keybindings.json` contains:

```json
{
  "app.model.select": [],
  "app.tree.filter.labeledOnly": "alt+l"
}
```

Both original bindings conflicted with the extension's Ctrl+L shortcut. `/model` still opens the
model selector, and Option+L selects the tree's labeled-only filter. A fresh Pi session and
`/hotkeys` confirmed Ctrl+L was registered for live voice without conflicts. No extension patch
was needed. [Live voice](live-voice.md) lists the voice controls and commands.

## Instructions and skills

Pi natively discovers `~/.agents/skills`; there is no second skill copy or new Skills CLI target.
Its global `AGENTS.md` supplies shared policy, and ancestor context discovery loads personal
`~/AGENTS.md` for projects under `$HOME`. Projects elsewhere need their own personal-context
arrangement. Coding context does not replace the extension's separate hardcoded voice prompt.

`AGENTS.override.md` is an upstream Pi convention, not a file created by these dotfiles. If present,
it takes precedence over an ordinary context file in the same directory. A profile override can
therefore replace the linked global instructions; a project override affects that directory's
context. This integration neither creates nor requires an override file.

## Upstream references

- [Pi configuration and context discovery](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md).
- [Pi model configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md)
  and [compaction settings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md#per-model-overrides).
- [Pi keybindings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/keybindings.md).
- Model capacity references inspected during the trial:
  [GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5),
  [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna),
  [Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol),
  [Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra),
  [GPT-6 Astra](https://developers.openai.com/api/docs/models/gpt-6-astra),
  [Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
  [Sol](https://developers.openai.com/api/docs/models/gpt-6-sol),
  [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), and
  [Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/).
