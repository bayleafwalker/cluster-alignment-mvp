#!/usr/bin/env python3
"""Verify every package payload file against manifest.json."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}


def payload_paths() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "manifest.json"
        and not any(part in IGNORED_PARTS for part in path.relative_to(ROOT).parts)
        and path.suffix != ".pyc"
    )


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    declared = {entry["path"]: entry for entry in manifest["files"]}
    actual = {str(path.relative_to(ROOT)): path for path in payload_paths()}
    errors: list[str] = []
    for missing in sorted(set(declared) - set(actual)):
        errors.append(f"missing payload: {missing}")
    for extra in sorted(set(actual) - set(declared)):
        errors.append(f"unmanifested payload: {extra}")
    for name in sorted(set(actual) & set(declared)):
        content = actual[name].read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if declared[name].get("sha256") != digest:
            errors.append(f"digest mismatch: {name}")
        if declared[name].get("bytes") != len(content):
            errors.append(f"size mismatch: {name}")
    if errors:
        print("manifest verification failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"manifest verified: {len(actual)} payload files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
