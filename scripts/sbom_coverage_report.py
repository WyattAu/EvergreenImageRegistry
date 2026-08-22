#!/usr/bin/env python3
"""
Evergreen Image Registry — SBOM Coverage Report
================================================
Generates comprehensive SBOM coverage metrics across all 798 images.
Tracks per-tier coverage, package counts, license distribution, and
produces Prometheus-compatible metrics.

Usage:
  python3 scripts/sbom_coverage_report.py --output /tmp/sbom-coverage.prom
  python3 scripts/sbom_coverage_report.py --dashboard docs/sbom-coverage.md
  python3 scripts/sbom_coverage_report.py --json /tmp/sbom-coverage.json
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"


def scan_registry() -> dict:
    """Scan all images and collect SBOM + manifest data."""
    results = {
        "total_images": 0,
        "with_sbom": 0,
        "with_sbom_valid": 0,
        "without_sbom": 0,
        "without_dockerfile": 0,
        "by_tier": defaultdict(lambda: {"total": 0, "sbom": 0, "valid_sbom": 0}),
        "by_build_type": defaultdict(lambda: {"total": 0, "sbom": 0}),
        "packages_total": 0,
        "licenses": Counter(),
        "large_sboms": [],  # >10k packages
        "empty_sboms": [],
        "images_without_sbom": [],
    }

    for manifest_path in sorted(IMAGES_DIR.glob("*/manifest.toml")):
        img_name = manifest_path.parent.name
        results["total_images"] += 1

        # Parse manifest
        tier = "standard"
        build_type = "unknown"
        try:
            content = manifest_path.read_text()
            tier_match = re.search(r'tier\s*=\s*"(\w+)"', content)
            if tier_match:
                tier = tier_match.group(1)
            type_match = re.search(r'build_type\s*=\s*"([^"]+)"', content)
            if type_match:
                build_type = type_match.group(1)
        except Exception:
            pass

        results["by_tier"][tier]["total"] += 1
        results["by_build_type"][build_type]["total"] += 1

        # Check SBOM
        sbom_path = manifest_path.parent / "sbom.spdx.json"
        dockerfile_path = manifest_path.parent / "Dockerfile"

        if not dockerfile_path.exists():
            results["without_dockerfile"] += 1

        if sbom_path.exists():
            results["with_sbom"] += 1
            results["by_tier"][tier]["sbom"] += 1
            results["by_build_type"][build_type]["sbom"] += 1

            try:
                with open(sbom_path) as f:
                    sbom_data = json.load(f)

                packages = sbom_data.get("packages", [])
                pkg_count = len(packages)

                if pkg_count > 0:
                    results["with_sbom_valid"] += 1
                    results["by_tier"][tier]["valid_sbom"] += 1
                    results["packages_total"] += pkg_count

                    # License tracking
                    for pkg in packages:
                        license_id = pkg.get("licenseConcluded", "NOASSERTION")
                        if license_id and license_id != "NOASSERTION":
                            results["licenses"][license_id] += 1

                    if pkg_count > 10000:
                        results["large_sboms"].append({"image": img_name, "packages": pkg_count})
                else:
                    results["empty_sboms"].append(img_name)
            except Exception:
                results["empty_sboms"].append(img_name)
        else:
            results["without_sbom"] += 1
            results["images_without_sbom"].append(img_name)

    return results


def generate_prometheus(data: dict) -> str:
    """Generate Prometheus exposition format."""
    lines = []
    total = data["total_images"]
    now = datetime.utcnow().isoformat() + "Z"

    # Coverage metrics
    lines.append("# HELP eir_sbom_coverage_total Total images in registry")
    lines.append("# TYPE eir_sbom_coverage_total gauge")
    lines.append(f"eir_sbom_coverage_total {total}")
    lines.append("")

    lines.append("# HELP eir_sbom_coverage_with_sbom Images with SBOM file")
    lines.append("# TYPE eir_sbom_coverage_with_sbom gauge")
    lines.append(f"eir_sbom_coverage_with_sbom {data['with_sbom']}")
    lines.append("")

    lines.append("# HELP eir_sbom_coverage_valid SBOMs with actual packages")
    lines.append("# TYPE eir_sbom_coverage_valid gauge")
    lines.append(f"eir_sbom_coverage_valid {data['with_sbom_valid']}")
    lines.append("")

    lines.append("# HELP eir_sbom_coverage_ratio Fraction of images with valid SBOMs")
    lines.append("# TYPE eir_sbom_coverage_ratio gauge")
    ratio = data["with_sbom_valid"] / total if total > 0 else 0
    lines.append(f"eir_sbom_coverage_ratio {ratio:.4f}")
    lines.append("")

    lines.append("# HELP eir_sbom_coverage_target Target coverage ratio")
    lines.append("# TYPE eir_sbom_coverage_target gauge")
    lines.append("eir_sbom_coverage_target 1.0")
    lines.append("")

    # Per-tier coverage
    for tier, counts in sorted(data["by_tier"].items()):
        t = counts["total"]
        s = counts["valid_sboms"]
        ratio = s / t if t > 0 else 0
        lines.append(f'eir_sbom_tier_coverage{{tier="{tier}"}} {ratio:.4f}')
    lines.append("")

    # Per-build-type coverage
    for bt, counts in sorted(data["by_build_type"].items()):
        t = counts["total"]
        s = counts["sbom"]
        ratio = s / t if t > 0 else 0
        lines.append(f'eir_sbom_build_type_coverage{{build_type="{bt}"}} {ratio:.4f}')
    lines.append("")

    # Package metrics
    lines.append("# HELP eir_sbom_packages_total Total packages across all SBOMs")
    lines.append("# TYPE eir_sbom_packages_total gauge")
    lines.append(f"eir_sbom_packages_total {data['packages_total']}")
    lines.append("")

    avg = data["packages_total"] / data["with_sbom_valid"] if data["with_sbom_valid"] > 0 else 0
    lines.append("# HELP eir_sbom_packages_avg Average packages per image")
    lines.append("# TYPE eir_sbom_packages_avg gauge")
    lines.append(f"eir_sbom_packages_avg {avg:.1f}")
    lines.append("")

    # Top licenses
    for license_id, count in data["licenses"].most_common(20):
        safe_id = license_id.replace('"', '\\"')
        lines.append(f'eir_sbom_licenses{{license="{safe_id}"}} {count}')

    lines.append("")
    lines.append(f"# HELP eir_sbom_report_timestamp Timestamp of report generation")
    lines.append(f"# TYPE eir_sbom_report_timestamp gauge")
    lines.append(f"eir_sbom_report_timestamp {datetime.utcnow().timestamp():.0f}")
    lines.append("")

    return "\n".join(lines)


def generate_dashboard(data: dict) -> str:
    """Generate Markdown dashboard."""
    total = data["total_images"]
    valid = data["with_sbom_valid"]
    ratio = valid / total if total > 0 else 0

    md = []
    md.append("# SBOM Coverage Report")
    md.append("")
    md.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("| Metric | Value |")
    md.append("|--------|-------|")
    md.append(f"| Total images | {total} |")
    md.append(f"| With SBOM | {data['with_sbom']} |")
    md.append(f"| Valid SBOM (packages > 0) | {valid} |")
    md.append(f"| Coverage ratio | {ratio:.1%} |")
    md.append(f"| Total packages tracked | {data['packages_total']:,} |")
    md.append(f"| Without Dockerfile | {data['without_dockerfile']} |")
    md.append(f"| Empty/template SBOMs | {len(data['empty_sboms'])} |")
    md.append("")

    md.append("## Coverage by Tier")
    md.append("")
    md.append("| Tier | Total | With SBOM | Coverage |")
    md.append("|------|-------|-----------|----------|")
    for tier in ["critical", "standard"]:
        counts = data["by_tier"][tier]
        t = counts["total"]
        s = counts["valid_sboms"]
        r = s / t if t > 0 else 0
        md.append(f"| {tier} | {t} | {s} | {r:.1%} |")
    md.append("")

    md.append("## Coverage by Build Type")
    md.append("")
    md.append("| Build Type | Total | With SBOM | Coverage |")
    md.append("|------------|-------|-----------|----------|")
    for bt, counts in sorted(data["by_build_type"].items()):
        t = counts["total"]
        s = counts["sbom"]
        r = s / t if t > 0 else 0
        md.append(f"| {bt} | {t} | {s} | {r:.1%} |")
    md.append("")

    if data["licenses"]:
        md.append("## Top 15 Licenses")
        md.append("")
        md.append("| License | Count |")
        md.append("|---------|-------|")
        for lic, count in data["licenses"].most_common(15):
            md.append(f"| {lic} | {count:,} |")
        md.append("")

    if data["images_without_sbom"]:
        md.append(f"## Images Without SBOM ({len(data['images_without_sbom'])})")
        md.append("")
        for img in data["images_without_sbom"][:50]:
            md.append(f"- {img}")
        if len(data["images_without_sbom"]) > 50:
            md.append(f"- ... and {len(data['images_without_sbom']) - 50} more")
        md.append("")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="SBOM coverage report")
    parser.add_argument("--output", type=Path, help="Prometheus metrics output")
    parser.add_argument("--dashboard", type=Path, help="Markdown dashboard output")
    parser.add_argument("--json", type=Path, help="JSON report output")
    args = parser.parse_args()

    data = scan_registry()

    if args.output:
        prom = generate_prometheus(data)
        args.output.write_text(prom)
        print(f"Prometheus metrics: {args.output}")

    if args.dashboard:
        dash = generate_dashboard(data)
        args.dashboard.parent.mkdir(parents=True, exist_ok=True)
        args.dashboard.write_text(dash)
        print(f"Dashboard: {args.dashboard}")

    if args.json:
        # Convert defaultdict for JSON serialization
        json_data = {
            "total_images": data["total_images"],
            "with_sbom": data["with_sbom"],
            "with_sbom_valid": data["with_sbom_valid"],
            "without_sbom": data["without_sbom"],
            "without_dockerfile": data["without_dockerfile"],
            "packages_total": data["packages_total"],
            "by_tier": {k: dict(v) for k, v in data["by_tier"].items()},
            "by_build_type": {k: dict(v) for k, v in data["by_build_type"].items()},
            "top_licenses": data["licenses"].most_common(50),
            "empty_sboms": data["empty_sboms"],
            "images_without_sbom": data["images_without_sbom"],
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
        args.json.write_text(json.dumps(json_data, indent=2))
        print(f"JSON report: {args.json}")

    # Print summary to stdout
    total = data["total_images"]
    valid = data["with_sbom_valid"]
    ratio = valid / total if total > 0 else 0
    print(f"\nCoverage: {valid}/{total} ({ratio:.1%})")
    print(f"Remaining: {total - valid} images need SBOMs")


if __name__ == "__main__":
    main()
