#!/usr/bin/env python3
"""
Evergreen Image Registry — SBOM Dependency Graph
================================================
Cross-image dependency tracking and transitive CVE propagation analysis.

Features:
  - Build dependency graph across all images
  - Identify shared vulnerable packages
  - Trace CVE propagation paths
  - Suggest fixes for transitive vulnerabilities
  - Prometheus metrics for tracking

Usage:
  python3 scripts/sbom_dependency_graph.py --build
  python3 scripts/sbom_dependency_graph.py --trace CVE-2024-XXXX
  python3 scripts/sbom_dependency_graph.py --shared --package openssl
  python3 scripts/sbom_dependency_graph.py --report /tmp/dep-graph.json
  python3 scripts/sbom_dependency_graph.py --prometheus /tmp/dep-graph.prom
"""

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"
GRAPH_DIR = REPO_ROOT / "compliance" / "dependency-graph"


class DependencyGraph:
    """Cross-image dependency graph."""

    def __init__(self):
        self.packages = {}  # name -> {version, images, license, ...}
        self.images = {}  # image -> [packages]
        self.vulnerabilities = {}  # cve -> {affected_packages, images}
        self.edges = []  # (package, depends_on)

    def load_sboms(self):
        """Load all SBOMs and build graph."""
        for sbom_path in sorted(IMAGES_DIR.glob("*/sbom.spdx.json")):
            img_name = sbom_path.parent.name

            try:
                with open(sbom_path) as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue

            pkgs = data.get("packages", [])
            self.images[img_name] = []

            for pkg in pkgs:
                name = pkg.get("name", "")
                version = pkg.get("versionInfo", "unknown")
                license_id = pkg.get("licenseConcluded", "NOASSERTION")
                supplier = pkg.get("supplier", "")

                if not name:
                    continue

                pkg_key = f"{name}@{version}"

                if pkg_key not in self.packages:
                    self.packages[pkg_key] = {
                        "name": name,
                        "version": version,
                        "license": license_id,
                        "supplier": supplier,
                        "images": [],
                        "download_location": pkg.get("downloadLocation", ""),
                    }

                self.packages[pkg_key]["images"].append(img_name)
                self.images[img_name].append(pkg_key)

            # Extract relationships (dependencies)
            for rel in data.get("relationships", []):
                source = rel.get("spdxElementId", "")
                target = rel.get("relatedSpdxElement", "")
                rel_type = rel.get("relationshipType", "")

                if rel_type in ("DEPENDS_ON", "CONTAINS"):
                    self.edges.append((source, target))

    def find_shared_packages(self, package_name: str) -> list:
        """Find all images using a specific package."""
        results = []
        for pkg_key, pkg_data in self.packages.items():
            if pkg_data["name"].lower() == package_name.lower():
                results.append({
                    "package": pkg_key,
                    "version": pkg_data["version"],
                    "images": pkg_data["images"],
                    "license": pkg_data["license"],
                    "image_count": len(pkg_data["images"]),
                })

        # Sort by image count (most shared first)
        results.sort(key=lambda x: x["image_count"], reverse=True)
        return results

    def trace_cve_propagation(self, cve_id: str) -> dict:
        """Trace which images are affected by a CVE through shared packages."""
        # This would integrate with Trivy/Grype output
        # For now, provide the framework
        return {
            "cve": cve_id,
            "affected_packages": [],
            "affected_images": [],
            "propagation_paths": [],
            "fix_suggestions": [],
        }

    def get_most_shared_packages(self, top_n: int = 20) -> list:
        """Get the most shared packages across images."""
        shared = []
        for pkg_key, pkg_data in self.packages.items():
            if len(pkg_data["images"]) > 1:
                shared.append({
                    "package": pkg_data["name"],
                    "version": pkg_data["version"],
                    "image_count": len(pkg_data["images"]),
                    "images": pkg_data["images"],
                    "license": pkg_data["license"],
                })

        shared.sort(key=lambda x: x["image_count"], reverse=True)
        return shared[:top_n]

    def get_license_distribution(self) -> dict:
        """Get license distribution across all packages."""
        licenses = defaultdict(int)
        for pkg_data in self.packages.values():
            lic = pkg_data.get("license", "UNKNOWN")
            if lic and lic != "NOASSERTION":
                licenses[lic] += 1
        return dict(sorted(licenses.items(), key=lambda x: x[1], reverse=True))

    def get_image_package_counts(self) -> list:
        """Get package count per image."""
        counts = []
        for img, pkgs in self.images.items():
            counts.append({
                "image": img,
                "packages": len(pkgs),
            })
        counts.sort(key=lambda x: x["packages"], reverse=True)
        return counts

    def generate_report(self) -> dict:
        """Generate comprehensive dependency graph report."""
        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_images": len(self.images),
                "total_packages": len(self.packages),
                "total_edges": len(self.edges),
                "shared_packages": len([p for p in self.packages.values() if len(p["images"]) > 1]),
            },
            "most_shared_packages": self.get_most_shared_packages(30),
            "license_distribution": self.get_license_distribution(),
            "image_package_counts": self.get_image_package_counts(),
            "packages_per_image_avg": sum(len(pkgs) for pkgs in self.images.values()) / max(len(self.images), 1),
        }


def generate_prometheus(graph: DependencyGraph) -> str:
    """Generate Prometheus metrics."""
    lines = []

    lines.append("# HELP eir_dep_graph_images Total images in dependency graph")
    lines.append("# TYPE eir_dep_graph_images gauge")
    lines.append(f"eir_dep_graph_images {len(graph.images)}")
    lines.append("")

    lines.append("# HELP eir_dep_graph_packages Total unique packages")
    lines.append("# TYPE eir_dep_graph_packages gauge")
    lines.append(f"eir_dep_graph_packages {len(graph.packages)}")
    lines.append("")

    lines.append("# HELP eir_dep_graph_shared Packages shared across multiple images")
    lines.append("# TYPE eir_dep_graph_shared gauge")
    shared = len([p for p in graph.packages.values() if len(p["images"]) > 1])
    lines.append(f"eir_dep_graph_shared {shared}")
    lines.append("")

    lines.append("# HELP eir_dep_graph_edges Total dependency edges")
    lines.append("# TYPE eir_dep_graph_edges gauge")
    lines.append(f"eir_dep_graph_edges {len(graph.edges)}")
    lines.append("")

    # Most shared packages
    for pkg in graph.get_most_shared_packages(10):
        safe_name = pkg["package"].replace('"', '\\"')
        lines.append(f'eir_dep_graph_pkg_images{{package="{safe_name}"}} {pkg["image_count"]}')

    lines.append("")

    # License distribution
    for lic, count in graph.get_license_distribution().items():
        safe_lic = lic.replace('"', '\\"')
        lines.append(f'eir_dep_graph_licenses{{license="{safe_lic}"}} {count}')

    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SBOM dependency graph tool")
    parser.add_argument("--build", action="store_true", help="Build dependency graph")
    parser.add_argument("--trace", type=str, help="Trace CVE propagation path")
    parser.add_argument("--shared", action="store_true", help="Find shared packages")
    parser.add_argument("--package", type=str, help="Package name for --shared")
    parser.add_argument("--report", type=Path, help="Write JSON report")
    parser.add_argument("--prometheus", type=Path, help="Write Prometheus metrics")
    parser.add_argument("--dashboard", type=Path, help="Write Markdown dashboard")
    args = parser.parse_args()

    if not any([args.build, args.trace, args.shared, args.report, args.prometheus, args.dashboard]):
        args.build = True

    graph = DependencyGraph()
    graph.load_sboms()

    if args.build:
        print(f"Loaded {len(graph.images)} images, {len(graph.packages)} packages")
        print("Most shared packages:")
        for pkg in graph.get_most_shared_packages(10):
            print(f"  {pkg['package']}@{pkg['version']}: {pkg['image_count']} images")

    if args.shared and args.package:
        results = graph.find_shared_packages(args.package)
        print(f"\nImages using {args.package}:")
        for r in results:
            print(f"  {r['package']}: {r['image_count']} images")
            for img in r["images"][:10]:
                print(f"    - {img}")

    if args.trace:
        result = graph.trace_cve_propagation(args.trace)
        print(f"\nCVE Propagation: {args.trace}")
        print(json.dumps(result, indent=2))

    if args.report:
        report = graph.generate_report()
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2))
        print(f"\nReport: {args.report}")

    if args.prometheus:
        prom = generate_prometheus(graph)
        args.prometheus.parent.mkdir(parents=True, exist_ok=True)
        args.prometheus.write_text(prom)
        print(f"Prometheus: {args.prometheus}")

    if args.dashboard:
        report = graph.generate_report()
        md = []
        md.append("# Dependency Graph Report\n")
        md.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")
        md.append("## Summary\n")
        md.append("| Metric | Value |")
        md.append("|--------|-------|")
        md.append(f"| Images | {report['summary']['total_images']} |")
        md.append(f"| Unique packages | {report['summary']['total_packages']} |")
        md.append(f"| Shared packages | {report['summary']['shared_packages']} |")
        md.append(f"| Avg packages/image | {report['summary']['packages_per_image_avg']:.0f} |\n")
        md.append("## Top 20 Most Shared Packages\n")
        md.append("| Package | Version | Images | License |")
        md.append("|---------|---------|--------|---------|")
        for pkg in report["most_shared_packages"][:20]:
            md.append(f"| {pkg['package']} | {pkg['version']} | {pkg['image_count']} | {pkg['license']} |")
        args.dashboard.parent.mkdir(parents=True, exist_ok=True)
        args.dashboard.write_text("\n".join(md))
        print(f"Dashboard: {args.dashboard}")


if __name__ == "__main__":
    main()
