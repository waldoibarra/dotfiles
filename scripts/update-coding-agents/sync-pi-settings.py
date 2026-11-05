#!/usr/bin/env python3
"""Merge tracked Pi defaults into local writable settings without modifying the source."""

import argparse
import json
import os
from pathlib import Path
import stat
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]


def read_settings(filename):
    """Require a JSON object; malformed settings must never be overwritten."""
    settings = json.loads(filename.read_text(encoding="utf-8"))
    if not isinstance(settings, dict):
        raise ValueError(f"Settings must be a JSON object: {filename}")
    return settings


def sync_settings(source, target):
    """Replace managed top-level values while retaining unspecified local keys."""
    defaults = read_settings(source)
    if source.resolve() == target.resolve() and not target.is_symlink():
        raise ValueError("Source and destination must be different files")
    target.parent.mkdir(parents=True, exist_ok=True)
    # Pi uses proper-lockfile with realpath:false, creating this same directory.
    lock = target.with_name(target.name + ".lock")
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise ValueError(
            f"Pi settings are locked: {lock}; retry after the writer finishes"
        ) from error
    staged = None
    try:
        linked = target.is_symlink()
        if linked and target.resolve() != source.resolve():
            raise ValueError(f"Refusing unrelated settings symlink: {target}")
        if target.exists() and os.path.samefile(source, target) and not linked:
            raise ValueError("Source and destination must not be hard links")
        existing = read_settings(target) if target.exists() else {}
        merged = {**existing, **defaults}
        if not linked and target.exists() and existing == merged:
            return False
        mode = stat.S_IMODE(target.stat().st_mode) if target.exists() and not linked else 0o600
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=target.parent, prefix=".settings-", delete=False
        ) as output:
            staged = Path(output.name)
            json.dump(merged, output, indent=2, ensure_ascii=False)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        staged.chmod(mode)
        os.replace(staged, target)
        return True
    finally:
        if staged is not None and staged.exists():
            staged.unlink()
        lock.rmdir()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "home/.pi/agent/settings.json")
    parser.add_argument("--target", type=Path, default=Path.home() / ".pi/agent/settings.json")
    args = parser.parse_args()
    try:
        changed = sync_settings(args.source, args.target)
    except (OSError, ValueError) as error:
        print(f"Cannot sync Pi settings: {error}", file=sys.stderr)
        return 1
    print("Updated local Pi settings." if changed else "Pi settings already current.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
