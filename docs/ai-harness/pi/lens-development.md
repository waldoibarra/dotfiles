# Develop Lens locally

**Run Pi from local Pi, Lens, and voice sources with `just pi-lens-dev`.**
Read [Pi and live voice](README.md) for ownership; read [tooling](/docs/tooling.md#recipes) for the
other recipes.

The recipe keeps the caller's working directory and forwards arguments without re-parsing them.
It never builds, installs, or changes package declarations.

From this checkout, run `just pi-lens-dev` to use the local sources shown below.
The recipe uses Pi's normal session persistence by default.
Pass Pi CLI arguments after the recipe name, including `--continue` or explicit `--no-session`.
`--continue` selects the latest saved session for that directory, including ordinary Pi sessions.
Use `--session` for a specific saved session; previous ephemeral sessions cannot be resumed.

To keep another project's working directory, invoke it there with:

```sh
just --justfile "$HOME/.dotfiles/justfile" pi-lens-dev --continue
```

| Component | Required file |
| --- | --- |
| Compiled Pi host | `$HOME/projects/open-source/pi/packages/coding-agent/dist/bundle/cli.js` |
| Pi Lens | `$HOME/projects/open-source/pi-lens/src/index.ts` |
| Installed live voice | `$HOME/.pi/agent/npm/node_modules/pi-live-codex/index.ts` |

The recipe checks those files. Prepare missing checkouts and the compiled host separately.
It uses the local compiled host, not Mise's `latest` binary.
Ordinary `pi` and `dots` remain unchanged.

Only the two named extensions, Lens and voice, load.
Installed Lens and other auto-discovered extensions remain
disabled.
This prevents double rendering. Voice loads without opening the microphone or connecting
automatically.
Start voice with `/live spruce` or use Ctrl+L for the default voice.
Read [live voice](live-voice.md) before testing microphone and account access.
Use `--no-session` only for disposable conversations that should not persist after exit.

Sessions launched before voice was included need a new process.
`/reload` retains their original extension paths.
Keep the current conversation open and launch `just pi-lens-dev` in another terminal for voice
testing.

Edit Lens source, finish the active turn, then run `/reload` in the same Pi session.
Reload replaces extensions without restarting the conversation.
Host changes require rebuilding and restarting Pi.
Use ordinary `pi` for the published package configuration.
