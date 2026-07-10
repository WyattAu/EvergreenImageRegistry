#!/usr/bin/env python3
"""Generate architecture support matrix for all EIR images."""

import json
import subprocess
from pathlib import Path

REGISTRY = "ghcr.io/wyattau/evergreenimageregistry"
IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"


def get_arches(ref):
    """Get architectures supported by an image."""
    result = subprocess.run(
        ["docker", "manifest", "inspect", ref],
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        return []
    try:
        manifest = json.loads(result.stdout)
        arches = []
        for m in manifest.get("manifests", []):
            plat = m.get("platform", {})
            if plat.get("architecture") == "unknown":
                continue
            arch = plat.get("architecture", "?")
            variant = plat.get("variant", "")
            arches.append(f"{arch}/{variant}" if variant else arch)
        return sorted(arches)
    except Exception:
        return []


def main():
    images = []
    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if (
            not img_dir.is_dir()
            or img_dir.name.startswith("_")
            or img_dir.name == "clawdius"
        ):
            continue
        dockerfile = img_dir / "Dockerfile"
        if not dockerfile.exists():
            continue
        name = img_dir.name
        ref = f"{REGISTRY}/{name}:latest"

        # Determine expected tier from Dockerfile
        text = dockerfile.read_text()
        if "FROM scratch" in text or "FROM cgr.dev/chainguard" in text:
            build_type = "hardened"
        elif "mirror-" in text:
            build_type = "mirrored"
        else:
            build_type = "repack"

        arches = get_arches(ref)
        images.append(
            {
                "name": name,
                "build_type": build_type,
                "arches": arches,
                "multi_arch": len(arches) > 1,
            }
        )

    # Generate markdown
    print("| Image | Build Type | Architectures | Multi-arch |")
    print("|-------|-----------|---------------|------------|")
    for img in sorted(images, key=lambda x: (x["build_type"], x["name"])):
        arch_str = ", ".join(img["arches"]) if img["arches"] else "unknown"
        print(
            f"| {img['name']} | {img['build_type']} | {arch_str} | {'✅' if img['multi_arch'] else '❌'} |"
        )

    # Summary
    hardened = sum(1 for i in images if i["build_type"] == "hardened")
    mirrored = sum(1 for i in images if i["build_type"] == "mirrored")
    repack = sum(1 for i in images if i["build_type"] == "repack")
    multi = sum(1 for i in images if i["multi_arch"])

    print("\n## Summary")
    print(f"- Hardened: {hardened}")
    print(f"- Mirrored: {mirrored}")
    print(f"- Repack: {repack}")
    print(f"- Multi-arch: {multi}/{len(images)}")


if __name__ == "__main__":
    main()
