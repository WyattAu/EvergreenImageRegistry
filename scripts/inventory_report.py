#!/usr/bin/env python3
"""Generate canonical inventory metrics for active image directories."""

import argparse
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"
TIER_MAP = {"1": "critical", "2": "standard", "3": "standard"}
VALID_TIERS = {"critical", "standard"}
FROM_RE = re.compile(r"^FROM\s+(?P<reference>\S+)(?:\s+AS\s+\S+)?$", re.IGNORECASE)
TIER_RE = re.compile(r"evergreen\.image\.tier\s*=\s*['\"]([^'\"]+)", re.IGNORECASE)


def normalize_tier(value: str) -> str:
    """Normalize legacy numeric and named tier values."""
    normalized = value.strip().lower()
    return TIER_MAP.get(normalized, normalized)


def _load_manifest(path: Path) -> dict:
    try:
        return tomllib.loads(path.read_text(errors="replace"))
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def _manifest_tier(data: dict) -> str:
    metadata = data.get("metadata", {})
    return str(metadata.get("tier", data.get("tier", "standard")))


def _from_lines(text: str) -> list[dict]:
    results = []
    for number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = FROM_RE.match(line)
        if not match:
            continue
        reference = match.group("reference")
        results.append(
            {
                "line": number,
                "reference": reference,
                "pinned": reference.lower() == "scratch" or "@sha256:" in reference,
            }
        )
    return results


def _sbom_has_packages(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(data.get("packages"), list) and bool(data["packages"])


def scan() -> dict:
    images = []
    for directory in sorted(IMAGES.iterdir()):
        if not directory.is_dir() or directory.name.startswith(("_", ".")):
            continue
        dockerfile = directory / "Dockerfile"
        manifest = directory / "manifest.toml"
        if not dockerfile.exists() or not manifest.exists():
            continue

        text = dockerfile.read_text(errors="replace")
        manifest_data = _load_manifest(manifest)
        manifest_tier = _manifest_tier(manifest_data)
        dockerfile_tiers = TIER_RE.findall(text)
        tier = normalize_tier(manifest_tier)
        normalized_dockerfile_tiers = [normalize_tier(value) for value in dockerfile_tiers]
        tier_conflict = bool(normalized_dockerfile_tiers) and any(value != tier for value in normalized_dockerfile_tiers)
        if dockerfile_tiers and all(value.strip() in {"1", "2", "3"} for value in dockerfile_tiers):
            tier_conflict = False
        from_lines = _from_lines(text)
        unpinned_from = [item for item in from_lines if not item["pinned"]]
        images.append(
            {
                "name": directory.name,
                "tier": tier,
                "manifest_tier": manifest_tier,
                "dockerfile_tier": dockerfile_tiers[-1] if dockerfile_tiers else None,
                "tier_conflict": tier_conflict,
                "invalid_tier": tier not in VALID_TIERS,
                "dockerfile": True,
                "manifest": True,
                "sbom": (directory / "sbom.spdx.json").exists(),
                "sbom_has_packages": _sbom_has_packages(directory / "sbom.spdx.json"),
                "has_user": any(line.upper().startswith("USER ") for line in text.splitlines()),
                "has_healthcheck": any(line.upper().startswith("HEALTHCHECK ") for line in text.splitlines()),
                "all_from_pinned": not unpinned_from and bool(from_lines),
                "unpinned_from": unpinned_from,
            }
        )

    total = len(images)
    critical = [item for item in images if item["tier"] == "critical"]
    critical_unpinned = [item for item in critical if not item["all_from_pinned"]]
    return {
        "schema_version": 3,
        "total_images": total,
        "with_sbom": sum(item["sbom"] for item in images),
        "with_valid_sbom": sum(item["sbom_has_packages"] for item in images),
        "with_user": sum(item["has_user"] for item in images),
        "with_healthcheck": sum(item["has_healthcheck"] for item in images),
        "all_from_pinned": sum(item["all_from_pinned"] for item in images),
        "critical_total": len(critical),
        "critical_from_pinned": len(critical) - len(critical_unpinned),
        "critical_unpinned": len(critical_unpinned),
        "standard_unpinned": sum(item["tier"] != "critical" and not item["all_from_pinned"] for item in images),
        "tier_conflicts": sum(item["tier_conflict"] for item in images),
        "invalid_tiers": sum(item["invalid_tier"] for item in images),
        "critical_unpinned_images": [item["name"] for item in critical_unpinned],
        "images": images,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write the report to a JSON file")
    args = parser.parse_args()
    encoded = json.dumps(scan(), indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
