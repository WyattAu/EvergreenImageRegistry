#!/usr/bin/env python3
"""Detect drift between SBOM manifests and Dockerfile package declarations.

For each image in images/, compares the package list recorded in sbom.spdx.json
against the packages installed in the Dockerfile (via apk add, apt-get install,
pip install). Reports orphaned SBOM entries and missing SBOM entries.
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"

SKIP_DIRS = {"tests", "profiles", "adversarial", "functional"}

DOCKERFILE_INSTALL_RE = re.compile(
    r"""
    (?:^|\s&&\s|;\s|\|\|\s)
    (?:
        apk\s+add\s+(?:--[^ ]*\s+)*
        |
        apt-get\s+(?:update\s+&&\s+)?install\s+(?:-y\s+(?:--[^ ]*\s+)*)?
        |
        apt\s+install\s+(?:-y\s+(?:--[^ ]*\s+)*)?
        |
        pip(?:3)?\s+install\s+(?:-[^ ]*\s+)*
    )
    (?P<pkgs>[^\n&;|]+)
    """,
    re.VERBOSE,
)

PKG_SPLIT_RE = re.compile(r"\s+")

CONTAINER_PURPOSES = {"CONTAINER", "SOURCE", "OPERATING-SYSTEM"}


@dataclass
class DriftResult:
    image: str
    dockerfile_packages: list[str] = field(default_factory=list)
    sbom_packages: list[str] = field(default_factory=list)
    orphaned_sbom: list[str] = field(default_factory=list)
    missing_sbom: list[str] = field(default_factory=list)
    sbom_missing: bool = False
    dockerfile_missing: bool = False
    discrepancies: int = 0

    def compute(self) -> None:
        df_set = {normalize(p) for p in self.dockerfile_packages}
        sbom_set = {normalize(p) for p in self.sbom_packages}
        self.orphaned_sbom = sorted(sbom_set - df_set)
        self.missing_sbom = sorted(df_set - sbom_set)
        self.discrepancies = len(self.orphaned_sbom) + len(self.missing_sbom)


def normalize(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[=<>~].*", "", name)
    name = name.split("/")[-1]
    return name


def get_image_dirs(single_image: str | None = None) -> list[Path]:
    if single_image:
        target = IMAGES_DIR / single_image
        if not target.is_dir():
            logger.error(f"image directory not found: {target}")
            sys.exit(2)
        return [target]
    dirs = []
    for d in sorted(IMAGES_DIR.iterdir()):
        if d.is_dir() and d.name not in SKIP_DIRS and not d.name.startswith("."):
            dirs.append(d)
    return dirs


def extract_sbom_packages(image_dir: Path) -> list[str]:
    sbom_path = image_dir / "sbom.spdx.json"
    if not sbom_path.exists():
        return []
    with open(sbom_path) as f:
        data = json.load(f)
    packages: list[str] = []
    for pkg in data.get("packages", []):
        purpose = pkg.get("primaryPackagePurpose", "")
        if purpose in CONTAINER_PURPOSES:
            continue
        name = pkg.get("name", "")
        if name:
            packages.append(name)
    return packages


def extract_dockerfile_packages(image_dir: Path) -> list[str]:
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        return []
    content = dockerfile.read_text()
    packages: list[str] = []
    for match in DOCKERFILE_INSTALL_RE.finditer(content):
        raw = match.group("pkgs").strip()
        if not raw or raw.startswith("$"):
            continue
        for token in PKG_SPLIT_RE.split(raw):
            token = token.strip()
            if not token or token.startswith("-") or token.startswith("$"):
                continue
            if "\\" in token:
                token = token.split("\\")[0].strip()
            if token:
                packages.append(token)
    return packages


def analyze_image(image_dir: Path) -> DriftResult:
    result = DriftResult(image=image_dir.name)
    sbom_path = image_dir / "sbom.spdx.json"
    dockerfile_path = image_dir / "Dockerfile"

    if not sbom_path.exists():
        result.sbom_missing = True
    if not dockerfile_path.exists():
        result.dockerfile_missing = True

    result.sbom_packages = extract_sbom_packages(image_dir)
    result.dockerfile_packages = extract_dockerfile_packages(image_dir)
    result.compute()
    return result


def format_table(results: list[DriftResult]) -> str:
    lines: list[str] = []
    lines.append(
        f"{'IMAGE':<30} {'SBOM PKGs':>10} {'DF PKGs':>10} {'ORPHANED':>10} {'MISSING':>10}"
    )
    lines.append("-" * 72)
    total_orphaned = 0
    total_missing = 0
    images_with_issues = 0
    for r in results:
        if r.sbom_missing or r.dockerfile_missing:
            status = "MISSING FILES"
            lines.append(f"{r.image:<30} {status:>50}")
            images_with_issues += 1
            continue
        lines.append(
            f"{r.image:<30} {len(r.sbom_packages):>10} {len(r.dockerfile_packages):>10} "
            f"{len(r.orphaned_sbom):>10} {len(r.missing_sbom):>10}"
        )
        total_orphaned += len(r.orphaned_sbom)
        total_missing += len(r.missing_sbom)
        if r.discrepancies > 0:
            images_with_issues += 1
    lines.append("-" * 72)
    lines.append(
        f"{'TOTAL':<30} {'':>10} {'':>10} {total_orphaned:>10} {total_missing:>10}"
    )
    lines.append(f"\nImages with discrepancies: {images_with_issues}/{len(results)}")

    for r in results:
        if r.discrepancies == 0:
            continue
        lines.append(f"\n--- {r.image} ---")
        if r.orphaned_sbom:
            lines.append(f"  Orphaned SBOM entries ({len(r.orphaned_sbom)}):")
            for p in r.orphaned_sbom:
                lines.append(f"    - {p}")
        if r.missing_sbom:
            lines.append(f"  Missing SBOM entries ({len(r.missing_sbom)}):")
            for p in r.missing_sbom:
                lines.append(f"    + {p}")

    return "\n".join(lines)


def format_json(results: list[DriftResult]) -> str:
    output = {
        "total_images": len(results),
        "images_with_discrepancies": sum(1 for r in results if r.discrepancies > 0),
        "total_orphaned_sbom": sum(len(r.orphaned_sbom) for r in results),
        "total_missing_sbom": sum(len(r.missing_sbom) for r in results),
        "images": [],
    }
    for r in results:
        entry: dict = {
            "image": r.image,
            "sbom_package_count": len(r.sbom_packages),
            "dockerfile_package_count": len(r.dockerfile_packages),
            "orphaned_sbom": r.orphaned_sbom,
            "missing_sbom": r.missing_sbom,
            "discrepancies": r.discrepancies,
        }
        if r.sbom_missing:
            entry["sbom_missing"] = True
        if r.dockerfile_missing:
            entry["dockerfile_missing"] = True
        output["images"].append(entry)
    return json.dumps(output, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect drift between SBOM manifests and Dockerfile package declarations."
    )
    parser.add_argument(
        "--image", type=str, default=None, help="Check a single image by name"
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output results as JSON"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        help="Only report images with more than N discrepancies (default: 0)",
    )
    args = parser.parse_args()

    image_dirs = get_image_dirs(args.image)
    results = [analyze_image(d) for d in image_dirs]

    if args.threshold > 0:
        results = [r for r in results if r.discrepancies > args.threshold]
    else:
        results = [r for r in results if r.discrepancies > 0]

    if args.json_output:
        all_results = results
        print(format_json(all_results))
    else:
        if not results:
            logger.info("All images clean. No SBOM drift detected.")
            sys.exit(0)
        print(format_table(results))

    has_discrepancies = any(r.discrepancies > 0 for r in results)
    sys.exit(1 if has_discrepancies else 0)


if __name__ == "__main__":
    main()
