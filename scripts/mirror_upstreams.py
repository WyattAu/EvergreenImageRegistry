#!/usr/bin/env python3
"""Mirror all Docker Hub upstreams to GHCR to avoid rate limits.

For each active image:
1. Parse Dockerfile to find FROM <upstream>
2. Pull upstream from Docker Hub
3. Tag and push to ghcr.io/wyattau/evergreenimageregistry/__mirror__/<name>
4. Update Dockerfile to use mirror
"""
import re
import subprocess
import sys
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
REGISTRY = "ghcr.io/wyattau/evergreenimageregistry"
MIRROR_PREFIX = f"{REGISTRY}/__mirror__"

def get_upstream(dockerfile_path: Path) -> str | None:
    """Extract the upstream FROM from a Dockerfile."""
    text = dockerfile_path.read_text()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("FROM ") and "health-shim" not in s and "scratch" not in s:
            # Extract image name
            parts = s.split()
            if len(parts) >= 2:
                return parts[1]
    return None

def sanitize_name(upstream: str) -> str:
    """Convert upstream name to valid GHCR package name."""
    name = upstream.replace("/", "-").replace(":", "-")
    name = re.sub(r'[^a-zA-Z0-9._-]', '', name)
    return name.lower()

def main():
    mirrored = 0
    updated = 0
    skipped = 0

    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if not img_dir.is_dir() or img_dir.name.startswith("_"):
            continue

        dockerfile = img_dir / "Dockerfile"
        if not dockerfile.exists():
            continue

        upstream = get_upstream(dockerfile)
        if not upstream:
            continue

        # Check if already using mirror
        if "__mirror__" in upstream:
            skipped += 1
            continue

        mirror_name = sanitize_name(upstream)
        mirror_ref = f"{MIRROR_PREFIX}/{mirror_name}"

        # Pull from Docker Hub
        result = subprocess.run(
            ["docker", "pull", upstream],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"❌ PULL FAIL: {img_dir.name} <- {upstream}")
            continue

        # Tag for mirror
        subprocess.run(["docker", "tag", upstream, mirror_ref],
                      capture_output=True, timeout=30)

        # Push to GHCR
        result = subprocess.run(
            ["docker", "push", mirror_ref],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            mirrored += 1
            # Update Dockerfile
            text = dockerfile.read_text()
            text = text.replace(f"FROM {upstream}\n", f"FROM {mirror_ref}\n")
            dockerfile.write_text(text)
            updated += 1
            print(f"✅ {img_dir.name}: {upstream} → {mirror_ref}")
        else:
            print(f"⚠️ PUSH FAIL: {mirror_ref}")

        # Cleanup
        subprocess.run(["docker", "rmi", upstream, mirror_ref],
                      capture_output=True, timeout=30)

    print(f"\nMirrored: {mirrored} | Updated: {updated} | Skipped: {skipped}")

if __name__ == "__main__":
    main()
