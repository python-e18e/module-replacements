"""Validate the published replacement manifest using only the standard library."""

import json
import re
from pathlib import Path


FIELDS = ("name", "alternative", "minimum_python", "guidance", "source")
NAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")
VERSION = re.compile(r"^3\.\d+$")


def validate(path=Path(__file__).with_name("replacements.json")):
    entries = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("catalog must be a JSON array")
    names = set()
    for number, entry in enumerate(entries, 1):
        if not isinstance(entry, dict) or any(
            not isinstance(entry.get(field), str) or not entry[field].strip()
            for field in FIELDS
        ):
            raise ValueError(f"entry {number}: missing or empty field")
        name = re.sub(r"[-_.]+", "-", entry["name"]).lower()
        if not NAME.fullmatch(entry["name"]) or name in names:
            raise ValueError(f"entry {number}: invalid or duplicate package name")
        if not VERSION.fullmatch(entry["minimum_python"]):
            raise ValueError(f"entry {number}: minimum_python must be 3.x")
        if not entry["source"].startswith("https://"):
            raise ValueError(f"entry {number}: source must use HTTPS")
        names.add(name)
    return len(entries)


if __name__ == "__main__":
    print(f"Validated {validate()} replacements.")
