#!/usr/bin/env python3
"""Hash user-provided ZIP/PDF packages without extracting or executing content.

This checks file identity/integrity, not scientific validity or provenance.
Only names, sizes and hashes are emitted; data rows are never copied.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


MAX_EXPANDED_BYTES = 64 * 1024 * 1024


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def inspect_package(path, limit=MAX_EXPANDED_BYTES):
    path = Path(path)
    raw = path.read_bytes()
    item = {"name": path.name, "bytes": len(raw), "sha256": sha256(raw)}
    if path.suffix.lower() == ".pdf":
        if not raw.startswith(b"%PDF-"):
            raise ValueError("PDF signature missing")
        item["format"] = "pdf"
        return item
    if path.suffix.lower() != ".zip":
        raise ValueError("Only ZIP and PDF are supported")
    item["format"] = "zip"
    with zipfile.ZipFile(path) as archive:
        members = [info for info in archive.infolist() if not info.is_dir()]
        names = [info.filename for info in members]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate member names")
        if sum(info.file_size for info in members) > limit:
            raise ValueError("Expanded archive exceeds limit")
        for name in names:
            posix = PurePosixPath(name)
            if posix.is_absolute() or ".." in posix.parts or "\\" in name:
                raise ValueError("Unsafe member name")
        item["members"] = []
        for info in sorted(members, key=lambda x: x.filename):
            # Reading also checks each ZIP CRC. Nothing is extracted.
            payload = archive.read(info)
            item["members"].append({"name": info.filename,
                                    "bytes": len(payload), "sha256": sha256(payload)})
    return item


def inventory(directory):
    packages, errors = [], []
    for path in sorted(Path(directory).iterdir()):
        if path.suffix.lower() not in {".zip", ".pdf"}:
            continue
        try:
            packages.append(inspect_package(path))
        except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as exc:
            errors.append({"name": path.name, "error": str(exc)})
    by_hash = {}
    for package in packages:
        for member in package.get("members", []):
            by_hash.setdefault(member["sha256"], []).append(
                {"package": package["name"], "member": member["name"]})
    duplicates = [{"sha256": digest, "locations": locations}
                  for digest, locations in sorted(by_hash.items())
                  if len({x["package"] for x in locations}) > 1]
    return {"schema_version": 1,
            "scope": "identity/integrity only; no scientific reproduction",
            "packages": packages, "cross_package_identical_members": duplicates,
            "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = inventory(args.directory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
