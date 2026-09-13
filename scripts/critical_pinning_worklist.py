#!/usr/bin/env python3
"""Generate a deterministic worklist for critical-tier FROM digest pinning."""

import argparse
import json
import tomllib
from pathlib import Path

from inventory_report import scan


def _manifest_context(image: str) -> dict:
    path = Path("images") / image / "manifest.toml"
    try:
        data = tomllib.loads(path.read_text())
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    metadata = data.get("metadata", {})
    source = data.get("source", {})
    return {
        "version": metadata.get("version", data.get("version", "")),
        "upstream_version": metadata.get("upstream_version", ""),
        "source_url": source.get("url", data.get("source_url", "")),
        "source_type": source.get("type", data.get("source_type", "")),
    }


def build_worklist(report: dict) -> dict:
    entries = []
    for image in report["images"]:
        if image["tier"] != "critical" or image["all_from_pinned"]:
            continue
        context = _manifest_context(image["name"])
        for source in image["unpinned_from"]:
            entries.append(
                {
                    "image": image["name"],
                    "dockerfile": f"images/{image['name']}/Dockerfile",
                    "line": source["line"],
                    "reference": source["reference"],
                    "manifest_version": context.get("version", ""),
                    "upstream_version": context.get("upstream_version", ""),
                    "source_url": context.get("source_url", ""),
                    "source_type": context.get("source_type", ""),
                    "status": "requires-upstream-resolution",
                }
            )
    entries.sort(key=lambda item: (item["image"], item["line"], item["reference"]))
    return {
        "schema_version": 2,
        "source_inventory_schema": report["schema_version"],
        "critical_images": report["critical_total"],
        "fully_pinned_critical_images": report["critical_from_pinned"],
        "unresolved_entries": len(entries),
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    worklist = build_worklist(scan())
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(worklist, indent=2, sort_keys=True) + "\n")
    print(f"Critical pinning worklist: {worklist['unresolved_entries']} entries")


if __name__ == "__main__":
    main()
