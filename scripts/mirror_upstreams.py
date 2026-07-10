#!/usr/bin/env python3
"""Mirror Docker Hub upstreams to GHCR to avoid rate limits.

For each unique Docker Hub upstream across all Dockerfiles:
1. Pull from Docker Hub (once per unique image)
2. Tag and push to ghcr.io/wyattau/evergreenimageregistry/__mirror__/<name>
3. Update ALL Dockerfiles that reference it

Usage:
  python scripts/mirror_upstreams.py --dry-run    # Show what would be done
  python scripts/mirror_upstreams.py               # Execute mirroring
"""

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
REGISTRY = "ghcr.io/wyattau/evergreenimageregistry"
MIRROR_PREFIX = f"{REGISTRY}/__mirror__"

# Registries that are NOT Docker Hub — no need to mirror these
SKIP_REGISTRIES = {
    "ghcr.io",
    "quay.io",
    "cgr.dev",
    "lscr.io",
    "docker.dragonflydb.io",
    "public.ecr.aws",
    "gcr.io",
    "k8s.gcr.io",
    "registry.k8s.io",
    "mcr.microsoft.com",
    "rg.fr-par.scw.cloud",
}


def is_docker_hub(image: str) -> bool:
    """Check if an image reference points to Docker Hub (docker.io)."""
    # Docker Hub images have no registry prefix OR explicitly use docker.io
    # Images with a '/' in the first part and no '.' or ':' in host = Docker Hub
    if image.startswith("docker.io/"):
        return True
    for reg in SKIP_REGISTRIES:
        if image.startswith(reg + "/"):
            return False
    # No slash before the first part = official Docker Hub image (e.g. "python", "redis")
    # OR has format "user/repo" without a registry host
    # If there's a port (host:port/), it's a private registry
    first_part = image.split("/")[0]
    if ":" in first_part and not first_part.split(":")[1].isdigit():
        # e.g. "python:3.11" — first_part is "python:3.11", no host
        return True
    if "." not in first_part and ":" not in first_part:
        # No dots in host part = not a registry hostname = Docker Hub
        return True
    return False


def normalize_ref(image: str) -> str:
    """Normalize a Docker Hub reference to include docker.io/ prefix."""
    if image.startswith("docker.io/"):
        return image
    # Add library/ prefix for official images (no namespace)
    parts = image.split("/")
    if len(parts) == 1 or ("." not in parts[0] and ":" not in parts[0]):
        # Could be "python:3.11" or "user/repo"
        if "/" not in image or (
            len(parts) == 2 and "." not in parts[0] and ":" not in parts[0]
        ):
            if "/" not in image:
                # Official image: "python:3.11" → "docker.io/library/python:3.11"
                name, tag = image.split(":") if ":" in image else [image, "latest"]
                return f"docker.io/library/{name}:{tag}"
    return f"docker.io/{image}"


def sanitize_name(image: str) -> str:
    """Convert upstream name to valid GHCR package name."""
    # Remove docker.io/ prefix
    name = image.replace("docker.io/", "")
    name = name.replace("/", "-").replace(":", "-").replace("@", "-at-")
    name = re.sub(r"[^a-zA-Z0-9._-]", "", name)
    return name.lower()


def find_all_upstreams() -> dict[str, list[Path]]:
    """Find all Docker Hub upstreams and which Dockerfiles use them.

    Returns: {upstream_ref: [dockerfile_paths]}
    """
    upstreams = defaultdict(list)

    for img_dir in sorted(IMAGES_DIR.iterdir()):
        if not img_dir.is_dir() or img_dir.name.startswith("_"):
            continue
        if img_dir.name == "clawdius":
            continue

        dockerfile = img_dir / "Dockerfile"
        if not dockerfile.exists():
            continue

        text = dockerfile.read_text()
        for line in text.splitlines():
            s = line.strip()
            if not s.startswith("FROM "):
                continue
            # Skip shim, scratch, and mirror stages
            if any(
                skip in s
                for skip in [
                    "health-shim",
                    "evergreenshim",
                    "scratch",
                    "__mirror__",
                ]
            ):
                continue
            # Extract image ref (before AS keyword)
            parts = s.split()
            if len(parts) < 2:
                continue
            ref = parts[1]
            if is_docker_hub(ref):
                upstreams[ref].append(dockerfile)

    return upstreams


def pull_and_mirror(upstream: str, mirror_ref: str, dry_run: bool = False) -> bool:
    """Pull upstream, tag as mirror, push to GHCR."""
    normalized = normalize_ref(upstream)
    print(f"  Pull: {normalized}")
    if dry_run:
        print(f"  Tag:  {upstream} → {mirror_ref}")
        print(f"  Push: {mirror_ref}")
        return True

    # Pull
    result = subprocess.run(
        ["docker", "pull", upstream],
        capture_output=True,
        text=True,
        timeout=180,
    )
    if result.returncode != 0:
        print(f"  ❌ PULL FAIL: {result.stderr.strip()}")
        return False

    # Tag
    result = subprocess.run(
        ["docker", "tag", upstream, mirror_ref],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print(f"  ❌ TAG FAIL: {result.stderr.strip()}")
        return False

    # Push
    result = subprocess.run(
        ["docker", "push", mirror_ref],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        print(f"  ❌ PUSH FAIL: {result.stderr.strip()}")
        return False

    print("  ✅ Mirrored")
    return True


def update_dockerfile(dockerfile: Path, upstream: str, mirror_ref: str):
    """Update a Dockerfile to use the mirror instead of Docker Hub."""
    text = dockerfile.read_text()
    # Handle: FROM <upstream>\n and FROM <upstream> AS <stage>\n
    # Use word boundary to avoid partial matches
    pattern = re.compile(
        rf"(FROM\s+){re.escape(upstream)}(\s+AS\s+|\s*$|\s+--platform=)",
        re.MULTILINE,
    )
    new_text = pattern.sub(rf"\1{mirror_ref}\2", text)
    if new_text != text:
        dockerfile.write_text(new_text)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Mirror Docker Hub upstreams to GHCR")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done"
    )
    args = parser.parse_args()

    print("Scanning Dockerfiles for Docker Hub upstreams...")
    upstreams = find_all_upstreams()

    if not upstreams:
        print("No Docker Hub upstreams found.")
        return

    print(f"\nFound {len(upstreams)} unique Docker Hub upstreams:\n")

    # Sort by number of references (most used first)
    for upstream in sorted(upstreams, key=lambda x: len(upstreams[x]), reverse=True):
        count = len(upstreams[upstream])
        mirror_name = sanitize_name(upstream)
        mirror_ref = f"{MIRROR_PREFIX}/{mirror_name}"
        print(
            f"  {upstream:50s} → {mirror_ref} ({count} ref{'s' if count > 1 else ''})"
        )

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        return

    print(f"\nProceeding to mirror {len(upstreams)} upstreams...\n")
    # Login to GHCR first
    subprocess.run(
        "gh auth token | docker login ghcr.io -u WyattAu --password-stdin",
        shell=True,
        timeout=30,
        capture_output=True,
    )

    mirrored = 0
    failed = 0
    updated = 0

    for upstream in sorted(upstreams, key=lambda x: len(upstreams[x]), reverse=True):
        mirror_name = sanitize_name(upstream)
        mirror_ref = f"{MIRROR_PREFIX}/{mirror_name}"

        print(f"\nProcessing: {upstream}")
        if pull_and_mirror(upstream, mirror_ref, dry_run=False):
            mirrored += 1
            # Update all Dockerfiles that reference this upstream
            for dockerfile in upstreams[upstream]:
                if update_dockerfile(dockerfile, upstream, mirror_ref):
                    updated += 1
                    print(f"  Updated: {dockerfile.relative_to(IMAGES_DIR.parent)}")
        else:
            failed += 1

        # Cleanup local image to save disk
        subprocess.run(
            ["docker", "rmi", upstream, mirror_ref],
            capture_output=True,
            timeout=30,
        )

    print(f"\n{'=' * 60}")
    print(f"Mirrored: {mirrored} | Failed: {failed} | Updated files: {updated}")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
