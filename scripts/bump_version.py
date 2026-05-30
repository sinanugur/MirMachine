#!/usr/bin/env python3
"""Update MirMachine version strings in one place.

Usage:
    python scripts/bump_version.py 0.3.0.5
    python scripts/bump_version.py 0.3.0.5 --include-changelog
    python scripts/bump_version.py 0.3.0.5 --dry-run
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from typing import List, Tuple


VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[A-Za-z0-9_.+-]*)?$")


def _replace_named_version(text: str, pattern: str, new_version: str) -> Tuple[str, str]:
    regex = re.compile(pattern, re.MULTILINE)
    match = regex.search(text)
    if not match:
        raise ValueError(f"Pattern not found: {pattern}")

    old_version = match.group("v")
    updated = regex.sub(
        lambda m: f"{m.group('prefix')}{new_version}{m.group('suffix')}",
        text,
        count=1,
    )
    return updated, old_version


def _update_file(path: Path, patterns: List[str], new_version: str, dry_run: bool) -> Tuple[bool, List[str]]:
    original = path.read_text(encoding="utf-8")
    updated = original
    old_versions: List[str] = []

    for pattern in patterns:
        updated, old_version = _replace_named_version(updated, pattern, new_version)
        old_versions.append(old_version)

    changed = updated != original
    if changed and not dry_run:
        path.write_text(updated, encoding="utf-8")
    return changed, old_versions


def _prepend_changelog_entry(path: Path, new_version: str, dry_run: bool) -> Tuple[bool, str]:
    original = path.read_text(encoding="utf-8")
    latest_header = re.search(
        r"^##\s+\[(?P<v>[^\]]+)\]\s+-\s+(?P<date>.+)$",
        original,
        re.MULTILINE,
    )
    if not latest_header:
        raise ValueError("Unable to find a changelog release header in CHANGELOG")

    previous_version = latest_header.group("v")
    if previous_version == new_version:
        return False, previous_version

    # Avoid duplicate headers if the version already exists deeper in the file.
    existing_version = re.search(
        rf"^##\s+\[{re.escape(new_version)}\]\s+-\s+.+$",
        original,
        re.MULTILINE,
    )
    if existing_version:
        return False, previous_version

    today = date.today().isoformat()
    new_entry = (
        f"## [{new_version}] - {today}\n"
        "### Changed\n"
        f"  - Version bump from {previous_version} to {new_version} across project metadata files.\n"
        "  - Package, workflow, and docs release strings were updated to stay in sync.\n"
        "### Added\n"
        "  - New release-note header scaffolded for this version.\n\n"
    )
    updated = f"{new_entry}{original}"
    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return True, previous_version


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump MirMachine version across project files.")
    parser.add_argument("version", help="New version string (example: 0.3.0.5)")
    parser.add_argument(
        "--include-changelog",
        action="store_true",
        help="Also prepend a new CHANGELOG heading for this version.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    args = parser.parse_args()

    if not VERSION_RE.match(args.version):
        raise SystemExit(
            "Invalid version format. Expected semantic-like version, e.g. 0.3.0.5"
        )

    targets = {
        Path("setup.py"): [
            r"(?P<prefix>version\s*=\s*\")(?P<v>[^\"]+)(?P<suffix>\",)",
        ],
        Path("scripts/MirMachine.py"): [
            r"(?P<prefix>__version__\s*=\s*')(?P<v>[^']+)(?P<suffix>')",
        ],
        Path("mirmachine/workflows/mirmachine_search.smk"): [
            r'(?P<prefix>__version__\s*=\s*\")(?P<v>[^\"]+)(?P<suffix>\")',
        ],
        Path("docs/conf.py"): [
            r"(?P<prefix>release\s*=\s*')(?P<v>[^']+)(?P<suffix>')",
        ],
    }

    changed_any = False
    for path, patterns in targets.items():
        changed, old_versions = _update_file(path, patterns, args.version, args.dry_run)
        changed_any = changed_any or changed
        old_display = ", ".join(old_versions)
        action = "would update" if args.dry_run else "updated"
        state = action if changed else "already up to date"
        print(f"{path}: {state} ({old_display} -> {args.version})")

    if args.include_changelog:
        changed, previous_version = _prepend_changelog_entry(
            Path("CHANGELOG"), args.version, args.dry_run
        )
        changed_any = changed_any or changed
        action = "would prepend" if args.dry_run else "prepended"
        state = action if changed else "already up to date"
        print(
            f"CHANGELOG: {state} (latest {previous_version}; target {args.version})"
        )

    if not changed_any:
        print("No file content changes were necessary.")


if __name__ == "__main__":
    main()
