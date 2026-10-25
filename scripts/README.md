# Scripts

Read this before changing installer or sync behavior. These scripts modify the workstation;
use [tooling](/docs/tooling.md) to choose the narrowest operation.

## Idempotency

Read [repository guardrails](/AGENTS.md#guardrails) before changing script behavior.

- Test initial setup, repeated runs, and retry after partial failure in isolated fixtures.
- Verify unchanged file contents, timestamps, permissions, and unrelated settings.
- Avoid duplicate installs, entries, backups, or reloads.
- Hold external inputs fixed when testing updaters; a successful exit alone does not prove
  idempotency.
- Prefer atomic writes and state checks. Fail safely when the current state cannot be determined.

## Installation

[`install-dotfiles.sh`](/scripts/install-dotfiles.sh) initializes the Dotbot submodule and runs
[install.conf.yaml](/install.conf.yaml) from the repository root. It forwards arguments to Dotbot.
The wrapper checks Git and Python 3.7+ before invoking Dotbot.
It exposes the supported Homebrew prefix to every Dotbot subprocess, even before Brew exists there.
The configuration updates submodules from their remotes, manages links and runs these scripts:

| Script | Behavior |
| --- | --- |
| [configure-touch-id-for-sudo.sh](/scripts/configure-touch-id-for-sudo.sh) | On macOS, build `/etc/pam.d/sudo_local` from Apple's template if Touch ID is not enabled; set mode `444`. Skip other systems; fail if the template is missing. |
| [install-os-packages.sh](/scripts/install-os-packages.sh) | Install Homebrew if needed, check/install its global bundle with `--no-upgrade`, trust/install Mise tools, and install missing WezTerm terminfo on macOS when WezTerm is available. |
| [configure-markdown-app.sh](/scripts/configure-markdown-app.sh) | After package installation, apply the user-wide Markdown handler with duti. Skip non-macOS or an unavailable app. |
| [set-brew-zsh-as-default-shell.sh](/scripts/set-brew-zsh-as-default-shell.sh) | Register Homebrew Zsh in `/etc/shells` and select it with `chsh`, unless `$SHELL` already matches. |

Read [default applications](/docs/tooling.md#default-applications-on-macos) before changing file
associations or responding to OS approval prompts. Already-correct handlers are not changed again.
The Markdown step receives Homebrew's Apple Silicon PATH explicitly;
package subprocesses cannot update its parent.

Installation does not run the coding-agent updater, prune tools or install this checkout's hooks.
`just sync` sets `DOTS_DEFER_MISE_INSTALL=1` for the installer,
deferring Mise tools to the package coordinator.
Standalone installation installs Mise tools sequentially and needs neither Mise nor `just`
beforehand.
Brew's `--no-upgrade` avoids routine upgrades but permits dependency upgrades required by missing
packages.

Run `python3 scripts/tests/test-package-bootstrap.py` for isolated bootstrap, repeat-run, failure,
prerequisite, and PATH checks.

## Package updates

[`sync-packages.py`](/scripts/sync-packages.py) coordinates Brew and Mise through `just packages-sync`.
Read [package-update output](/docs/tooling.md#read-package-update-output)
before interpreting interleaved logs.
Read [sequential mode and recovery](/docs/tooling.md#sequential-mode-and-recovery)
before retrying failed updates or running source builds.
Python owns subprocess groups, waits for both update results, and terminates children on
interruption.
The Mise exclusion applies only to Brew upgrades, never the later Brewfile cleanup.

Each parallel job has a reader thread that drains its merged stdout and stderr pipe.
A shared output lock keeps labeled lines intact. Readers finish before cleanup starts.
The coordinator forwards lines as they arrive, without waiting for job completion.

Run these isolated checks after changing bootstrap, coordination, or output handling:

```sh
python3 scripts/tests/test-package-bootstrap.py
python3 scripts/tests/test-sync-packages.py
```

The coordinator checks cover concurrency, sequential fallback, failure propagation, retries,
and interruption cleanup.
Output checks cover both streams, carriage-return progress,
and visible output while both jobs remain running.
Fixtures use fake package managers; they never update the workstation.

## Coding-agent updates

[`update-coding-agents/entrypoint.sh`](/scripts/update-coding-agents/entrypoint.sh) runs these steps
in order through `just update-ca` and `just sync`:

Before these steps,
[sync-life-profile.sh](update-coding-agents/sync-life-profile.sh)
provisions personal-context and agent-identity symlinks using exported `LIFE_PROFILE`.
Set the variable in `~/.zprofile.local` and open a new login terminal.
If the vault exists without a profile, it warns without changing links or blocking updates.
Invalid selections, missing source files, or ordinary files at link destinations stop updates.
Run `python3 scripts/tests/test-life-profile.py` for isolated linking and preservation checks.

1. Copy managed Claude settings and render Cursor's global instruction template.
  Dotbot links `~/.claude/CLAUDE.md` to shared instructions; the updater leaves that link intact.
  Claude's global instructions need no import adapter.
  The Cursor renderer expands `@~/.agents/AGENTS.md` into a regular file.
  Read [Cursor global instructions](../docs/coding-agents/README.md#cursor-global-instructions)
  before changing the template or refreshing only that rule.
2. Register missing shared personal MCP servers through Claude's native user-scope command.
3. Install the configured subagent runner from `latest`, then update declared Pi packages in the normal
  profile.
4. Refresh RTK's Pi extension when its dry run lists changes.
5. Refresh Herdr's Claude and Pi integrations unless status reports them current.
6. Install Moshi's Pi extension non-interactively with its native target-specific installer.
7. Install missing lockfile skills, update global skills, then **commit and push** a changed
lockfile.

RTK, Herdr and Moshi steps skip their integrations when the respective binary is missing. Their Pi
steps also require the `pi` binary. Herdr's native installer requires an extension directory;
the updater creates it when needed. Generated extensions stay outside Git.
Read [Coding agents](../docs/coding-agents/README.md) before editing copied configs or running updates.
It lists ownership and publication risks.
Read [Agent integrations](/docs/agent-integrations.md) before diagnosing hooks or plugins.
Moshi's Pi hook file is refreshed on each run.
Pairing and daemon/service setup remain outside this updater.
Redirecting installer stdin from `/dev/null` prevents first-run settings prompts during sync.
The redirect saves no preferences.
Read [Moshi's separate setup](../docs/agent-integrations.md#first-run-settings-during-sync)
for those machine-local preferences.

[`sync-personal-mcp.py`](/scripts/update-coding-agents/sync-personal-mcp.py) can run separately
with `python3`, without package upgrades or publication. It preserves matching registrations and
fails on conflicts; read [personal MCP setup](/docs/coding-agents/mcp.md) before applying changes.

Pi binary installation belongs to Mise. Package reconciliation reads the runner source from linked
settings, explicitly installs it, then runs `pi update --extensions --no-approve` from `$HOME`.
Explicit installation resolves `latest` and covers missing installations.
Both calls use the normal profile, exclude project packages, and omit `OPENAI_API_KEY`.
Failures stop the updater. No model, microphone, or authentication call is requested.

Pi's preferences and subagent configuration are Dotbot links, not managed copies.
Credentials, sessions, and locks are separate and untouched.
[Pi configuration](../docs/coding-agents/pi/configuration.md) lists the ownership boundaries.

## Obsidian vault checks

Read [Obsidian setup](/docs/obsidian.md) before running `scripts/obsidian.py` to provision settings
or check notes.

- `setup` installs declared tools/plugins, backs up changed owned files, and reconciles settings and
  the ruler.
- `sync` runs during workstation synchronization; it skips machines without the life vault.
- The app must be running with CLI access and completed Sync; incorrect vault selection stops setup.
- `check` validates touched prose and vault-wide local links without editing notes or making network
  requests.
- Run `python3 scripts/tests/test-obsidian.py` for isolated provisioning, prose, and link-check
  fixtures.

## Shared helpers and checks

[`lib/shell-helpers.sh`](/scripts/lib/shell-helpers.sh) supplies `print_separator`.
Updater helpers live beside their entrypoint under `scripts/update-coding-agents/`.

Run `just lint-sh` after shell changes. It checks selected entrypoints and follows sourced helpers
where configured; it does not execute installation behavior. Exercise changed behavior in an
isolated environment, never by running a real machine sync as a test.

Run `python3 scripts/tests/test-agent-harness.py` to check shared-role links, Pi settings, and
package reconciliation. It uses temporary homes and a fake Pi executable; no inference or sync runs.
Set `PI_PACKAGE_DIR` to the installed Pi package root to include compiled-host checks.
Those checks cover session persistence and effective startup policy in fresh workspaces.
The startup check reads installed user configuration and registers only the read tool.
It disables extensions and makes no tool or provider calls.
Read [harness verification](/docs/coding-agents/personal-workflow.md#fresh-startup-defaults) before
interpreting its results.
Run `python3 scripts/tests/test-personal-mcp.py` for isolated MCP registration and linking checks.
Run `python3 scripts/tests/test-markdown-app.py` for application guards and error propagation
without changing real file associations.
