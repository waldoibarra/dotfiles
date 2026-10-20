#!/usr/bin/env python3
"""Provision shared formatting; check touched prose and vault-wide local links."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "home/.config/obsidian"
RULES = CONFIG / "markdownlint.json"


def write_text(destination, content):
    if destination.exists() and destination.read_text() == content:
        return False
    with tempfile.NamedTemporaryFile(
        mode="w", dir=destination.parent, prefix=".lint-", delete=False,
    ) as output:
        temporary = Path(output.name)
        try:
            output.write(content)
            output.close()
            temporary.replace(destination)
        finally:
            temporary.unlink(missing_ok=True)
    return True


def write_json(destination, value):
    # Obsidian may serialize equivalent settings differently; preserve those bytes and timestamps.
    if destination.exists() and json.loads(destination.read_text()) == value:
        return False
    return write_text(destination, json.dumps(value, indent=2) + "\n")


def backup(destination, vault, directory):
    if directory is None or not destination.exists():
        return
    content = destination.read_bytes()
    vault_id = hashlib.sha256(str(vault.resolve()).encode()).hexdigest()[:16]
    digest = hashlib.sha256(content).hexdigest()
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = directory / vault_id / destination.relative_to(vault) / (digest + '.bak')
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not target.exists():
        target.write_bytes(content)
        target.chmod(0o600)


def setup(vault, backups=None):
    plugin = vault / ".obsidian/plugins/markdownlint"
    if not (plugin / "manifest.json").is_file():
        raise ValueError("Install Obsidian Markdownlint before provisioning settings")
    target = vault / ".markdownlint.json"
    rules = json.loads(RULES.read_text())
    if target.is_symlink():
        raise ValueError("Refusing to replace a symlinked lint configuration")
    if target.exists() and json.loads(target.read_text()) != rules:
        if backups is None:
            raise ValueError("Existing lint rules differ; a backup destination is required")
        backup(target, vault, backups)
    data = plugin / "data.json"
    if data.is_symlink():
        raise ValueError("Refusing to replace symlinked plugin settings")
    settings = json.loads(data.read_text()) if data.exists() else {}
    if not isinstance(settings, dict):
        raise ValueError("Plugin settings must be a JSON object")
    desired = json.loads((CONFIG / "markdownlint-plugin.json").read_text())
    if any(settings.get(key) != value for key, value in desired.items()):
        backup(data, vault, backups)
    settings.update(desired)
    write_json(target, rules)
    write_json(data, settings)
    print("Shared rules and owned formatter settings reconciled.")


def obsidian(vault, *arguments):
    result = subprocess.run(
        ['obsidian', f'vault={vault.name}', *arguments],
        capture_output=True, text=True, check=False, timeout=90,
    )
    if result.returncode or result.stdout.lstrip().startswith('Error:'):
        message = result.stderr.strip() or result.stdout.strip() or 'Obsidian command failed'
        raise ValueError(message)
    return result.stdout.strip()


def inspect_vault(vault):
    output = obsidian(vault, 'eval', 'code=JSON.stringify({'
                      'vaultPath:app.vault.adapter.getBasePath(),configDir:app.vault.configDir,'
                      'syncEnabled:!!app.internalPlugins.plugins.sync?.enabled,'
                      'syncLabel:document.querySelector(".status-bar-item.plugin-sync")'
                      '?.getAttribute("aria-label"),'
                      'installed:Object.keys(app.plugins.manifests),'
                      'enabled:[...app.plugins.enabledPlugins],'
                      'snippets:[...app.customCss.enabledSnippets],'
                      'supportsSnippets:typeof app.customCss.setCssEnabledStatus==="function"})')
    state = json.loads(output.removeprefix('=> ').strip())
    if Path(state['vaultPath']).resolve() != vault.resolve():
        raise ValueError('Obsidian selected a different vault; no changes applied')
    if state['configDir'] != '.obsidian':
        raise ValueError('Only the standard .obsidian configuration directory is supported')
    return state


def install_tools():
    tools = json.loads((CONFIG / 'vault.json').read_text())['tools']
    declared = tomllib.loads((ROOT / 'home/.config/mise/config.toml').read_text())['tools']
    versions = [f'{name}@{declared[name]}' for name in tools]
    subprocess.run(['mise', 'install', '--yes', *versions], check=True, timeout=300)


def provision(vault, backups):
    vault = vault.resolve()
    desired = json.loads((CONFIG / 'vault.json').read_text())
    state = inspect_vault(vault)
    if state.get('syncEnabled') and state.get('syncLabel') != 'Fully synced':
        raise ValueError('Wait for Obsidian Sync to report Fully synced, then rerun setup')
    if not state.get('supportsSnippets'):
        raise ValueError('This Obsidian version does not expose the required snippet controls')
    # Reject redirected configuration directories before making any changes.
    for name in [
        '.markdownlint.json', '.obsidian/plugins/markdownlint/data.json', '.obsidian/snippets',
    ]:
        if not (vault / name).resolve().is_relative_to(vault):
            raise ValueError(f'Refusing configuration path outside the vault: {name}')
    install_tools()
    for plugin in desired['plugins']:
        if plugin not in state['installed']:
            obsidian(vault, 'plugin:install', f'id={plugin}')
    if 'markdownlint' in desired['plugins']:
        target = vault / '.markdownlint.json'
        data = vault / '.obsidian/plugins/markdownlint/data.json'
        settings = json.loads(data.read_text()) if data.exists() else {}
        owned = json.loads((CONFIG / 'markdownlint-plugin.json').read_text())
        if not isinstance(settings, dict):
            raise ValueError('Plugin settings must be a JSON object')
        changed = (
            not target.exists() or json.loads(target.read_text()) != json.loads(RULES.read_text())
            or any(settings.get(key) != value for key, value in owned.items())
        )
        disabled = changed and 'markdownlint' in state['enabled']
        if disabled:
            obsidian(vault, 'plugin:disable', 'id=markdownlint', 'filter=community')
        try:
            setup(vault, backups)
        finally:
            # Restore the existing enabled state even if a configuration write fails.
            if disabled:
                obsidian(vault, 'plugin:enable', 'id=markdownlint', 'filter=community')
    for plugin in desired['plugins']:
        if plugin not in state['enabled']:
            obsidian(vault, 'plugin:enable', f'id={plugin}', 'filter=community')
    snippets = vault / '.obsidian/snippets'
    snippets.mkdir(exist_ok=True)
    snippets_changed = False
    for name in desired['snippets']:
        target = snippets / (name + '.css')
        content = (CONFIG / (name + '.css')).read_text()
        if target.is_symlink():
            raise ValueError(f'Refusing symlinked snippet: {name}')
        if not target.exists() or target.read_text() != content:
            backup(target, vault, backups)
            write_text(target, content)
            snippets_changed = True
        if name not in state['snippets']:
            snippets_changed = True
            obsidian(
                vault, 'eval', 'code=app.customCss.setCssEnabledStatus('
                + json.dumps(name) + ',true)',
            )
    if snippets_changed:
        obsidian(
            vault, 'eval', 'code=(async()=>{await app.customCss.readSnippets();'
            'await app.customCss.loadSnippets();return "Snippets refreshed"})()',
        )
    verified = inspect_vault(vault)
    if (not set(desired['plugins']).issubset(verified['enabled']) or
            not set(desired['snippets']).issubset(verified['snippets'])):
        raise ValueError('Obsidian did not activate all declared plugins and snippets')
    print('Obsidian setup verified: declared tools, plugins, settings, and snippets applied.')


def targets(vault, names):
    vault = vault.resolve()
    result = []
    for name in names:
        candidate = (vault / name).resolve()
        if (not candidate.is_relative_to(vault) or candidate.suffix != ".md"
                or not candidate.is_file()):
            raise ValueError(f"Expected an existing Markdown file inside the vault: {name}")
        if any(part.startswith(".") for part in candidate.relative_to(vault).parts):
            raise ValueError("Hidden files are outside note checks")
        result.append(candidate)
    return result


def check(vault, names):
    vault = vault.resolve()
    files = targets(vault, names)
    # Explicit configuration avoids inheriting the caller's repository rules.
    with tempfile.TemporaryDirectory(prefix="vault-lint-") as temporary:
        config = Path(temporary) / ".markdownlint-cli2.jsonc"
        config.write_text(json.dumps({
            "config": {**json.loads(RULES.read_text()), "LIFE001": True},
            "customRules": [str(CONFIG / "communication.cjs")],
            "gitignore": False,
            "fix": False,
        }))
        lint_failed = False
        for note in files:
            print(f"Checking {note.relative_to(vault)}", flush=True)
            # stdin prevents the GUI's standard-only config from disabling agent rules.
            lint = subprocess.run(
                ["markdownlint-cli2", "--config", str(config), "-"],
                input=note.read_text(), text=True,
                cwd=temporary, check=False, timeout=120,
            )
            lint_failed |= lint.returncode != 0
        # Check incoming references too, without linting or changing unrelated prose.
        notes = sorted(
            p for p in vault.rglob("*.md")
            if not p.is_symlink()
            and not any(part.startswith(".") for part in p.relative_to(vault).parts)
            and p.resolve().is_relative_to(vault)
        )
        links = subprocess.run(
            ["lychee", "--config", str(CONFIG / "lychee.toml"), "--no-progress",
             *map(str, notes)],
            cwd=temporary, check=False, timeout=120,
        )
    return int(lint_failed or links.returncode != 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("setup", "sync", "check"))
    parser.add_argument("--vault", type=Path, default=Path.home() / "life")
    parser.add_argument("files", nargs="*", help="Touched Markdown paths relative to the vault")
    args = parser.parse_intermixed_args()
    vault = args.vault.expanduser().resolve()
    try:
        if not (vault / ".obsidian").is_dir():
            if args.action == 'sync':
                print('Obsidian setup skipped: open ~/life in Obsidian, '
                      'then run just obsidian-setup.')
                return 0
            raise ValueError("Expected an existing Obsidian vault")
        if args.action in ('setup', 'sync'):
            if args.files:
                raise ValueError("setup does not accept note paths")
            provision(vault, Path.home() / '.local/state/obsidian-setup/backups')
            return 0
        if not args.files:
            raise ValueError("check requires explicit touched Markdown paths")
        return check(vault, args.files)
    except (ValueError, OSError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
