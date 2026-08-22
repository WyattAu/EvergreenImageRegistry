#!/usr/bin/env python3
"""
Fast SBOM Generator — Generates SPDX 2.3 SBOMs from Dockerfile metadata.
No Docker build required. Works for repack images that inherit upstream packages.

Usage:
    python3 scripts/fast_sbom_generator.py [--image NAME] [--all] [--dry-run]
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"


def extract_base_image(dockerfile_content: str) -> str:
    """Extract the final stage base image from a Dockerfile."""
    lines = dockerfile_content.strip().split("\n")
    last_from = ""
    for line in lines:
        line = line.strip()
        if line.upper().startswith("FROM "):
            parts = line.split()
            if len(parts) >= 2:
                last_from = parts[1]
                # Handle AS alias
                if parts[1].upper() == "AS" and len(parts) >= 4:
                    last_from = parts[2]
    return last_from


def extract_packages(dockerfile_content: str) -> list:
    """Extract package names from RUN commands."""
    packages = []
    for line in dockerfile_content.split("\n"):
        line = line.strip()
        # apk add
        apk_match = re.search(r'apk\s+add\s+(?:--no-cache\s+)?(.+)', line)
        if apk_match:
            pkgs = apk_match.group(1).split()
            packages.extend([p for p in pkgs if not p.startswith("-")])
        # apt-get install
        apt_match = re.search(r'apt-get\s+install\s+(?:-y\s+)?(?:--no-install-recommends\s+)?(.+)', line)
        if apt_match:
            pkgs = apt_match.group(1).split()
            packages.extend([p for p in pkgs if not p.startswith("-")])
    return packages


def extract_labels(dockerfile_content: str) -> dict:
    """Extract LABEL directives."""
    labels = {}
    for line in dockerfile_content.split("\n"):
        line = line.strip()
        if line.upper().startswith("LABEL "):
            match = re.match(r'LABEL\s+(\S+?)=["\'](.+?)["\']', line)
            if match:
                labels[match.group(1)] = match.group(2)
    return labels


def extract_exposed_ports(dockerfile_content: str) -> list:
    """Extract EXPOSE ports."""
    ports = []
    for line in dockerfile_content.split("\n"):
        line = line.strip()
        if line.upper().startswith("EXPOSE "):
            ports.extend(line.split()[1:])
    return ports


def extract_env_vars(dockerfile_content: str) -> dict:
    """Extract ENV directives."""
    envs = {}
    for line in dockerfile_content.split("\n"):
        line = line.strip()
        if line.upper().startswith("ENV "):
            match = re.match(r'ENV\s+(\S+?)=(.+)', line)
            if match:
                envs[match.group(1)] = match.group(2).strip('"').strip("'")
    return envs


def generate_sbom_from_dockerfile(image_name: str, dockerfile_path: Path) -> dict:
    """Generate a SPDX 2.3 SBOM from Dockerfile metadata."""
    content = dockerfile_path.read_text()
    base_image = extract_base_image(content)
    packages = extract_packages(content)
    labels = extract_labels(content)
    _ports = extract_exposed_ports(content)
    _envs = extract_env_vars(content)
    timestamp = datetime.now(timezone.utc).isoformat()

    # Build SPDX document
    spdx = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"evergreen-{image_name}",
        "documentNamespace": f"https://github.com/WyattAu/EvergreenImageRegistry/images/{image_name}",
        "creationInfo": {
            "created": timestamp,
            "creators": [
                "Tool: evergreenctl-fast-sbom",
                "Organization: Evergreen Image Registry"
            ],
            "licenseListVersion": "3.21"
        },
        "packages": [],
        "relationships": []
    }

    # Add the image package
    version = labels.get("org.opencontainers.image.version", "unknown")
    image_pkg = {
        "SPDXID": f"SPDXRef-Package-{image_name}",
        "name": image_name,
        "versionInfo": version,
        "supplier": "Organization: Evergreen Image Registry",
        "downloadLocation": f"https://github.com/WyattAu/EvergreenImageRegistry/tree/main/images/{image_name}",
        "filesAnalyzed": False,
        "checksums": [],
        "primaryPackagePurpose": "CONTAINER",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": f"pkg:docker/{image_name}@{version}"
        }]
    }
    spdx["packages"].append(image_pkg)

    # Add base image package
    base_name = base_image.split("/")[-1].split(":")[0] if base_image else "unknown"
    base_version = base_image.split(":")[-1] if ":" in base_image else "latest"
    base_pkg = {
        "SPDXID": f"SPDXRef-Package-{base_name}",
        "name": base_name,
        "versionInfo": base_version,
        "supplier": f"upstream: {base_image}",
        "downloadLocation": f"https://hub.docker.com/r/{base_image.split(':')[0]}",
        "filesAnalyzed": False,
        "primaryPackagePurpose": "CONTAINER",
        "externalRefs": [{
            "referenceCategory": "PACKAGE-MANAGER",
            "referenceType": "purl",
            "referenceLocator": f"pkg:docker/{base_image.replace(':', '@')}"
        }]
    }
    spdx["packages"].append(base_pkg)
    spdx["relationships"].append({
        "spdxElementId": f"SPDXRef-Package-{image_name}",
        "relationshipType": "VARIANT_OF",
        "relatedSpdxElement": f"SPDXRef-Package-{base_name}"
    })

    # Add installed packages
    for pkg in packages:
        pkg_id = pkg.replace("/", "-").replace(".", "-")
        spdx["packages"].append({
            "SPDXID": f"SPDXRef-Package-{pkg_id}",
            "name": pkg,
            "versionInfo": "installed",
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "primaryPackagePurpose": "APPLICATION"
        })
        spdx["relationships"].append({
            "spdxElementId": f"SPDXRef-Package-{image_name}",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": f"SPDXRef-Package-{pkg_id}"
        })

    # Add health-shim if present
    if "shim" in content.lower() and "health-shim" in content.lower():
        shim_match = re.search(r'SHIM_VERSION=(\S+)', content)
        shim_version = shim_match.group(1) if shim_match else "v2.0.0"
        spdx["packages"].append({
            "SPDXID": "SPDXRef-Package-health-shim",
            "name": "evergreen-health-shim",
            "versionInfo": shim_version,
            "supplier": "Organization: Evergreen Image Registry",
            "downloadLocation": f"https://github.com/WyattAu/evergreenshim/releases/tag/{shim_version}",
            "filesAnalyzed": False,
            "primaryPackagePurpose": "APPLICATION"
        })
        spdx["relationships"].append({
            "spdxElementId": f"SPDXRef-Package-{image_name}",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": "SPDXRef-Package-health-shim"
        })

    return spdx


def main():
    parser = argparse.ArgumentParser(description="Fast SBOM generator from Dockerfiles")
    parser.add_argument("--image", help="Generate SBOM for a specific image")
    parser.add_argument("--all", action="store_true", help="Generate for all images without SBOMs")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--tier1", action="store_true", help="Only Tier 1 images")
    args = parser.parse_args()

    images = []

    if args.image:
        images = [args.image]
    elif args.all or args.tier1:
        for manifest in sorted(IMAGES_DIR.glob("*/manifest.toml")):
            img_name = manifest.parent.name
            sbom_path = manifest.parent / "sbom.spdx.json"

            # Skip if SBOM exists with packages
            if sbom_path.exists() and sbom_path.stat().st_size > 1000:
                continue

            # Tier filter
            if args.tier1:
                content = manifest.read_text()
                if 'tier = "critical"' not in content:
                    continue

            images.append(img_name)
    else:
        parser.print_help()
        return

    print(f"Processing {len(images)} images...")

    generated = 0
    skipped = 0
    failed = 0

    for img in images:
        dockerfile = IMAGES_DIR / img / "Dockerfile"
        sbom_path = IMAGES_DIR / img / "sbom.spdx.json"

        if not dockerfile.exists():
            failed += 1
            continue

        if args.dry_run:
            print(f"  Would generate: {sbom_path}")
            generated += 1
            continue

        try:
            spdx = generate_sbom_from_dockerfile(img, dockerfile)
            sbom_path.write_text(json.dumps(spdx, indent=2))
            pkg_count = len(spdx["packages"])
            print(f"  ✅ {img} ({pkg_count} packages)")
            generated += 1
        except Exception as e:
            print(f"  ❌ {img}: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Generated: {generated} | Skipped: {skipped} | Failed: {failed}")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()
