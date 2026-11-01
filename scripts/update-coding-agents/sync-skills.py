#!/usr/bin/env python3
"""Reconcile declared global skills without publishing native installation state."""

import argparse
import filecmp
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLIENTS = {"pi": ".agents/skills", "claude-code": ".claude/skills", "cursor": ".cursor/skills"}
OPEN_SPEC = (
    "openspec-apply-change", "openspec-archive-change", "openspec-explore",
    "openspec-propose", "openspec-sync-specs", "openspec-update-change",
)
SOURCE = re.compile(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git$")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")


def present(path):
    return path.exists() or path.is_symlink()


def manifest():
    manifest_path = ROOT / "home/.agents/skills-manifest.json"
    safe_parents(manifest_path, ROOT)
    if manifest_path.is_symlink():
        raise ValueError("Unsafe skills manifest: %s" % manifest_path)
    declaration = json.loads(manifest_path.read_text())
    if (not isinstance(declaration, dict) or
            set(declaration) != {"version", "clients", "skills"} or
            type(declaration["version"]) is not int or declaration["version"] != 1):
        raise ValueError("Unsupported skills manifest format")
    clients = declaration["clients"]
    if (not isinstance(clients, list) or not all(isinstance(c, str) for c in clients)
            or set(clients) != set(CLIENTS) or len(clients) != 3):
        raise ValueError("Skill clients must be pi, claude-code, and cursor exactly once")
    if not isinstance(declaration["skills"], list):
        raise ValueError("Skill declarations must be a list")
    names = set()
    for item in declaration["skills"]:
        if not isinstance(item, dict) or set(item) != {"name", "source"}:
            raise ValueError("Invalid skill declaration")
        name, source = item["name"], item["source"]
        if not isinstance(name, str) or not NAME.fullmatch(name) or name in names:
            raise ValueError("Invalid or duplicate skill name: %r" % name)
        if not isinstance(source, str) or not SOURCE.fullmatch(source):
            raise ValueError("Invalid skill source for %s" % name)
        if (name in OPEN_SPEC or present(ROOT / "home/.agents/skills" / name)
                or present(ROOT / ".agents/skills" / name)):
            raise ValueError("Repository-owned skill name: %s" % name)
        names.add(name)
    return declaration


def safe_parents(path, boundary):
    """Reject path redirection below an already-resolved home or checkout."""
    current = boundary
    for part in path.relative_to(boundary).parts[:-1]:
        current = current / part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            raise ValueError("Unsafe skill parent: %s" % current)


def usable_skill(path, name):
    document = path / "SKILL.md"
    if not path.is_dir() or path.is_symlink() or not document.is_file() or document.is_symlink():
        return False
    try:
        text = document.read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        return False
    sections = text.split("\n---\n", 1)
    return (text.startswith("---\n") and len(sections) == 2 and
            bool(re.search(r"(?m)^name: " + re.escape(name) + r"\s*$", sections[0])) and
            bool(sections[1].strip()))


def check_link(path, expected):
    if not present(path):
        return False
    if not path.is_symlink() or path.resolve() != expected.resolve():
        raise ValueError("Conflicting skill destination: %s" % path)
    return True


def preflight(declaration, home):
    for client_root in CLIENTS.values():
        safe_parents(home / client_root / "entry", home)
    safe_parents(ROOT / ".agents/skills/entry", ROOT)
    safe_parents(ROOT / "home/.agents/skills/entry", ROOT)
    lock = home / ".agents/.skill-lock.json"
    safe_parents(lock, home)
    for client in ("pi", "claude-code"):
        directory = home / CLIENTS[client]
        if directory.exists():
            for candidate in directory.iterdir():
                if candidate.is_symlink() and not candidate.exists():
                    target = candidate.resolve()
                    if target == ROOT or ROOT in target.parents:
                        owned = ROOT / "home/.agents/skills" / candidate.name
                        generated = ROOT / ".agents/skills" / candidate.name
                        if target not in (owned, generated):
                            raise ValueError("Unknown broken repository skill link: %s" % candidate)
    authored = ROOT / "home/.agents/skills"
    for owned in authored.iterdir() if authored.exists() else ():
        if not owned.is_dir():
            continue
        for client in CLIENTS:
            check_link(home / CLIENTS[client] / owned.name, owned)

    if lock.is_symlink() and lock.resolve() != (ROOT / "home/.agents/.skill-lock.json").resolve():
        raise ValueError("Unknown lockfile link: %s" % lock)
    if present(lock) and not lock.is_symlink() and not lock.is_file():
        raise ValueError("Conflicting lockfile destination: %s" % lock)
    existing_lock = read_lock(lock) if lock.exists() else {"skills": {}}
    for item in declaration["skills"]:
        name = item["name"]
        recorded = existing_lock["skills"].get(name)
        if recorded and recorded.get("sourceUrl") != item["source"]:
            raise ValueError(
                "Source conflict for %s: lockfile declares %s" %
                (name, recorded.get("sourceUrl"))
            )
        content = home / ".agents/skills" / name
        if content.is_symlink() or (present(content) and not content.is_dir()):
            raise ValueError("Conflicting skill content: %s" % content)
        for client in ("claude-code", "cursor"):
            check_link(home / CLIENTS[client] / name, content)
    for name in OPEN_SPEC:
        generated = ROOT / ".agents/skills" / name
        if generated.is_symlink():
            raise ValueError("Conflicting generated skill: %s" % generated)
        document = generated / "SKILL.md"
        if document.is_symlink():
            raise ValueError("Conflicting generated skill document: %s" % document)
        for client in CLIENTS:
            check_link(home / CLIENTS[client] / name, generated)


def native(*args, env=None):
    run = subprocess.run(
        ["npx", "-y", "skills", *args], env=env, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, check=True,
    )
    output = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", run.stdout + "\n" + run.stderr)
    if re.search(r"(?im)^\s*(?:error:|failed to |✗)", output):
        raise RuntimeError("Native skills command reported failure: %s" % (run.stdout + run.stderr))
    return run


def same_tree(existing, staged):
    for base, other in ((existing, staged), (staged, existing)):
        for entry in base.rglob("*"):
            counterpart = other / entry.relative_to(base)
            if entry.is_symlink():
                if not counterpart.is_symlink() or os.readlink(entry) != os.readlink(counterpart):
                    return False
            elif entry.is_dir():
                if not counterpart.is_dir() or counterpart.is_symlink():
                    return False
            elif (not counterpart.is_file() or counterpart.is_symlink() or
                  not filecmp.cmp(entry, counterpart, shallow=False)):
                return False
    return True


def read_lock(path):
    if not path.exists():
        return {"version": 1, "skills": {}, "lastSelectedAgents": list(CLIENTS), "dismissed": []}
    value = json.loads(path.read_text())
    if (not isinstance(value, dict) or not isinstance(value.get("skills"), dict) or
            any(not isinstance(item, dict) for item in value["skills"].values())):
        raise ValueError("Invalid native skill lockfile: %s" % path)
    return value


def save_lock(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=str(path.parent), delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, indent=2)
        stream.write("\n")
    try:
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def adopt_missing_metadata(name, source, installed, lock, home):
    with tempfile.TemporaryDirectory(prefix="skills-adopt-") as scratch:
        staged_home = Path(scratch)
        env = {
            "PATH": os.environ["PATH"], "HOME": str(staged_home),
            "XDG_CONFIG_HOME": str(staged_home / ".config"),
            "CLAUDE_CONFIG_DIR": str(staged_home / ".claude"),
            "npm_config_cache": str(staged_home / ".npm"),
            "CI": "1", "DISABLE_TELEMETRY": "1",
        }
        native(
            "add", source[:-4], "--skill", name, "-a", "pi", "-a", "claude-code",
            "-a", "cursor", "-g", "-y", env=env,
        )
        staged = staged_home / ".agents/skills" / name
        if not usable_skill(staged, name) or not same_tree(installed, staged):
            raise ValueError(
                "Source conflict for %s: existing content differs from %s" % (name, source)
            )
        entry = read_lock(staged_home / ".agents/.skill-lock.json")["skills"].get(name)
        if not entry or entry.get("sourceUrl") != source:
            raise ValueError("Native source verification failed for %s" % name)
        latest = read_lock(home / ".agents/.skill-lock.json")
        latest["skills"][name] = entry
        save_lock(home / ".agents/.skill-lock.json", latest)


def link_missing(path, target):
    if check_link(path, target):
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(target)


def sync(declaration, home):
    lock_path = home / ".agents/.skill-lock.json"
    if lock_path.is_symlink():
        if lock_path.exists():
            original = lock_path.read_bytes()
            with tempfile.NamedTemporaryFile(dir=str(lock_path.parent), delete=False) as stream:
                replacement = Path(stream.name)
                stream.write(original)
            try:
                replacement.replace(lock_path)
            finally:
                if replacement.exists():
                    replacement.unlink()
        else:
            lock_path.unlink()
    lock = read_lock(lock_path)
    for item in declaration["skills"]:
        name, source = item["name"], item["source"]
        installed = home / ".agents/skills" / name
        entry = lock["skills"].get(name)
        if entry and entry.get("sourceUrl") != source:
            raise ValueError(
                "Source conflict for %s: lockfile declares %s" %
                (name, entry.get("sourceUrl"))
            )
        if installed.is_dir() and not usable_skill(installed, name):
            raise ValueError(
                "Incomplete skill %s; preserve content and restore SKILL.md manually" % name
            )
        if installed.is_dir() and not entry:
            adopt_missing_metadata(name, source, installed, lock, home)
        if not installed.is_dir():
            native(
                "add", source[:-4], "--skill", name, "-a", "pi", "-a", "claude-code",
                "-a", "cursor", "-g", "-y",
            )
            if not usable_skill(installed, name):
                raise RuntimeError("Native installation missing valid SKILL.md for %s" % name)
            entry = read_lock(lock_path)["skills"].get(name)
            if not entry or entry.get("sourceUrl") != source:
                raise RuntimeError(
                    "Native installation missing matching source metadata for %s" % name
                )
        for client in ("claude-code", "cursor"):
            link_missing(home / CLIENTS[client] / name, installed)
    native("update", "-g")
    for item in declaration["skills"]:
        name, source = item["name"], item["source"]
        if not usable_skill(home / ".agents/skills" / name, name):
            raise RuntimeError(
                "Native update left incomplete skill %s; restore its SKILL.md" % name
            )
        entry = read_lock(lock_path)["skills"].get(name)
        if not entry or entry.get("sourceUrl") != source:
            raise RuntimeError("Native update lost matching source metadata for %s" % name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    declaration = manifest()
    home = Path.home()
    preflight(declaration, home)
    if not args.preflight:
        sync(declaration, home)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print("Skill synchronization failed: %s" % error, file=sys.stderr)
        sys.exit(1)
