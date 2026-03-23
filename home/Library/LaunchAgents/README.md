# LaunchAgents

This directory contains custom Homebrew service plist files that include environment
variables not supported by Homebrew's default plist generation.

## How It Works

Homebrew generates plist files for services but does not allow custom environment variables.
By placing your own plist files here, the `restart-brew-service-with-custom-plist.sh` script
can use them instead of Homebrew's defaults.

## Setup

Place custom plist files following the naming convention:
`homebrew.mxcl.<formula-name>.plist`

The plist is used by the service when running `./install.sh` via
[install.conf.yaml](/install.conf.yaml).

## Manual Setup

Use [scripts/restart-brew-service-with-custom-plist.sh](/scripts/restart-brew-service-with-custom-plist.sh)
to restart a service with its custom plist:

```bash
./scripts/restart-brew-service-with-custom-plist.sh <formula-name>
```

Example for Ollama:
```bash
./scripts/restart-brew-service-with-custom-plist.sh ollama
```

The script:
1. Stops the current service (if running)
2. Creates a symlink from `~/Library/LaunchAgents/` to this directory's plist
3. Starts the service using your custom plist via `brew services --file`

## Ollama Configuration

The `homebrew.mxcl.ollama.plist` file configures Ollama with:
- `OLLAMA_FLASH_ATTENTION=1`
- `OLLAMA_KEEP_ALIVE=900` (15 minutes in seconds)
- `OLLAMA_KV_CACHE_TYPE=q8_0`

> Note: Environment variables are not read from `.zshenv` because LaunchAgents do not inherit
> shell environment variables.
