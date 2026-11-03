#!/usr/bin/env python3
"""Restore the large CTF inputs from the companion tar, checking SHA-256."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Path to the companion artifacts .tar")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    index = json.loads((root / "artifacts/index.json").read_text())
    expected = {f["path"]: f for f in index["files"] if f["distribution"] == "bundle"}
    found = set()
    with tarfile.open(args.bundle, "r:*") as bundle:
        for member in bundle:
            if member.name not in expected or not member.isfile():
                raise SystemExit(f"Unexpected archive member: {member.name}")
            parts = PurePosixPath(member.name).parts
            if member.name.startswith("/") or ".." in parts or member.name in found:
                raise SystemExit(f"Invalid archive path: {member.name}")
            record = expected[member.name]
            if member.size != record["bytes"]:
                raise SystemExit(f"Size mismatch: {member.name}")
            destination = root.joinpath(*parts)
            if not destination.resolve().is_relative_to(root):
                raise SystemExit(f"Destination outside repository: {member.name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_name(destination.name + ".restoring")
            digest = hashlib.sha256()
            try:
                with bundle.extractfile(member) as source, temporary.open("wb") as output:
                    while chunk := source.read(1024 * 1024):
                        digest.update(chunk)
                        output.write(chunk)
                if digest.hexdigest() != record["sha256"]:
                    raise SystemExit(f"SHA-256 mismatch: {member.name}")
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
            found.add(member.name)
            print(f"OK {member.name} ({member.size} bytes)")
    if found != set(expected):
        raise SystemExit("Missing files: " + ", ".join(sorted(set(expected) - found)))
    print(f"Restored and verified {len(found)} artifacts.")


if __name__ == "__main__":
    main()
