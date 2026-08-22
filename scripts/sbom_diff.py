#!/usr/bin/env python3
"""
Evergreen Image Registry — SBOM Dependency Graph Diff
=====================================================
Compares SPDX SBOMs between two versions of an image to detect:
- New packages added
- Packages removed
- Version changes (upgrades/downgrades)
- Transitive dependency changes
- License changes

Usage:
  python3 scripts/sbom_diff.py --old images/redis/sbom.v1.json --new images/redis/sbom.v2.json
  python3 scripts/sbom_diff.py --image redis --compare v1.0.0 v1.0.1
  python3 scripts/sbom_diff.py --report images/redis/ --output diff-report.json

Features:
  - Dependency graph extraction from SBOM
  - Version delta tracking
  - License compliance checking
  - Transitive dependency change detection
  - Prometheus metrics for tracking
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"


def parse_spdx_packages(sbom_path: Path) -> dict:
    """Parse SPDX SBOM and extract package graph."""
    with open(sbom_path) as f:
        data = json.load(f)

    packages = {}
    relationships = []

    for pkg in data.get("packages", []):
        name = pkg.get("name", "")
        version = pkg.get("versionInfo", "unknown")
        supplier = pkg.get("supplier", "")
        download_location = pkg.get("downloadLocation", "")
        license_concluded = pkg.get("licenseConcluded", "NOASSERTION")

        packages[name] = {
            "version": version,
            "supplier": supplier,
            "download_location": download_location,
            "license": license_concluded,
            "checksums": {
                c.get("algorithm", ""): c.get("checksumValue", "")
                for c in pkg.get("checksums", [])
            },
        }

    for rel in data.get("relationships", []):
        relationships.append({
            "source": rel.get("spdxElementId", ""),
            "target": rel.get("relatedSpdxElement", ""),
            "type": rel.get("relationshipType", ""),
        })

    return {"packages": packages, "relationships": relationships}


def diff_sboms(old_data: dict, new_data: dict) -> dict:
    """Compute diff between two SBOM datasets."""
    old_pkgs = old_data["packages"]
    new_pkgs = new_data["packages"]

    old_names = set(old_pkgs.keys())
    new_names = set(new_pkgs.keys())

    added = new_names - old_names
    removed = old_names - new_names
    common = old_names & new_names

    # Version changes
    version_changes = []
    for name in sorted(common):
        old_ver = old_pkgs[name]["version"]
        new_ver = new_pkgs[name]["version"]
        if old_ver != new_ver:
            version_changes.append({
                "package": name,
                "old_version": old_ver,
                "new_version": new_ver,
                "upgrade": _is_upgrade(old_ver, new_ver),
            })

    # License changes
    license_changes = []
    for name in sorted(common):
        old_license = old_pkgs[name].get("license", "")
        new_license = new_pkgs[name].get("license", "")
        if old_license != new_license:
            license_changes.append({
                "package": name,
                "old_license": old_license,
                "new_license": new_license,
            })

    # Dependency relationship changes
    old_rels = {(r["source"], r["target"]): r["type"] for r in old_data["relationships"]}
    new_rels = {(r["source"], r["target"]): r["type"] for r in new_data["relationships"]}

    rel_added = set(new_rels.keys()) - set(old_rels.keys())
    rel_removed = set(old_rels.keys()) - set(new_rels.keys())

    return {
        "summary": {
            "old_total": len(old_pkgs),
            "new_total": len(new_pkgs),
            "added": len(added),
            "removed": len(removed),
            "version_changes": len(version_changes),
            "license_changes": len(license_changes),
            "dependency_changes": len(rel_added) + len(rel_removed),
        },
        "added_packages": [
            {"name": name, **new_pkgs[name]} for name in sorted(added)
        ],
        "removed_packages": [
            {"name": name, **old_pkgs[name]} for name in sorted(removed)
        ],
        "version_changes": version_changes,
        "license_changes": license_changes,
        "dependency_added": [
            {"source": s, "target": t, "type": new_rels[(s, t)]}
            for s, t in sorted(rel_added)
        ],
        "dependency_removed": [
            {"source": s, "target": t, "type": old_rels[(s, t)]}
            for s, t in sorted(rel_removed)
        ],
    }


def _is_upgrade(old_ver: str, new_ver: str) -> bool:
    """Heuristic: compare version strings."""
    old_parts = [int(x) for x in old_ver.split(".") if x.isdigit()]
    new_parts = [int(x) for x in new_ver.split(".") if x.isdigit()]
    return new_parts > old_parts if old_parts and new_parts else False


def generate_prometheus_metrics(diff: dict, image: str) -> str:
    """Generate Prometheus metrics from diff."""
    lines = []
    s = diff["summary"]

    lines.append(f'eir_sbom_diff_added{{image="{image}"}} {s["added"]}')
    lines.append(f'eir_sbom_diff_removed{{image="{image}"}} {s["removed"]}')
    lines.append(f'eir_sbom_diff_version_changes{{image="{image}"}} {s["version_changes"]}')
    lines.append(f'eir_sbom_diff_license_changes{{image="{image}"}} {s["license_changes"]}')
    lines.append(f'eir_sbom_diff_dependency_changes{{image="{image}"}} {s["dependency_changes"]}')

    # Track if critical packages changed
    critical_pkgs = {"openssl", "glibc", "libssl", "libc"}
    critical_changes = sum(
        1 for vc in diff["version_changes"]
        if vc["package"].lower() in critical_pkgs
    )
    lines.append(f'eir_sbom_diff_critical_changes{{image="{image}"}} {critical_changes}')

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SBOM dependency graph diff tool")
    parser.add_argument("--old", type=Path, help="Old SBOM file")
    parser.add_argument("--new", type=Path, help="New SBOM file")
    parser.add_argument("--image", type=str, help="Image name (for --compare mode)")
    parser.add_argument("--compare", nargs=2, metavar=("OLD_TAG", "NEW_TAG"),
                       help="Compare two tagged versions")
    parser.add_argument("--report", type=Path, help="Output diff report")
    parser.add_argument("--metrics", action="store_true",
                       help="Output Prometheus metrics")
    parser.add_argument("--output", type=Path, help="Write output to file")
    args = parser.parse_args()

    if args.old and args.new:
        old_data = parse_spdx_packages(args.old)
        new_data = parse_spdx_packages(args.new)
    elif args.image and args.compare:
        # Load from registry tags
        old_sbom = IMAGES_DIR / args.image / f"sbom.{args.compare[0]}.spdx.json"
        new_sbom = IMAGES_DIR / args.image / f"sbom.{args.compare[1]}.spdx.json"
        if not old_sbom.exists() or not new_sbom.exists():
            print(f"Error: SBOM files not found for {args.image} {args.compare}", file=sys.stderr)
            sys.exit(1)
        old_data = parse_spdx_packages(old_sbom)
        new_data = parse_spdx_packages(new_sbom)
    else:
        print("Error: Provide --old/--new or --image/--compare", file=sys.stderr)
        sys.exit(1)

    diff = diff_sboms(old_data, new_data)

    if args.metrics:
        metrics = generate_prometheus_metrics(diff, args.image or "unknown")
        if args.output:
            args.output.write_text(metrics)
        else:
            print(metrics)
    else:
        output = json.dumps(diff, indent=2)
        if args.output:
            args.output.write_text(output)
        else:
            print(output)


if __name__ == "__main__":
    main()
