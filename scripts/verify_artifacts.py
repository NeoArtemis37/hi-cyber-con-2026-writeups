#!/usr/bin/env python3
"""Check the artifact inventory, sizes and SHA-256 digests."""

import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complete", action="store_true", help="Require the companion bundle too")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    index = json.loads((root / "artifacts/index.json").read_text())
    checked = missing = failed = 0
    for record in index["files"]:
        path = root / record["path"]
        if not path.is_file():
            if record["distribution"] == "bundle" and not args.complete:
                missing += 1
                continue
            print(f"MISSING {record['path']}")
            failed += 1
            continue
        digest = hashlib.sha256()
        with path.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                digest.update(chunk)
        if path.stat().st_size != record["bytes"] or digest.hexdigest() != record["sha256"]:
            print(f"FAILED {record['path']}")
            failed += 1
        else:
            checked += 1
    print(f"Verified: {checked}; missing optional bundle files: {missing}; failures: {failed}.")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
