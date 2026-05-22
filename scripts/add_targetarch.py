#!/usr/bin/env python3
"""Add ARG TARGETARCH to Dockerfiles for multi-arch support."""

import argparse
import re
import sys
from pathlib import Path

EXCLUDED_IMAGES = {
    "nvidia-cuda",
    "nvidia",
    "cuda",
    "ollama-cuda",
    "ollama-gpu",
    "ollama-rocm",
    "pytorch-cuda",
    "pytorch-gpu",
    "deepspeed",
    "automatic1111",
    "comfyui",
    "invokeai",
    "litellm",
}


def has_targetarch(content):
    return bool(re.search(r"ARG\s+TARGETARCH", content, re.IGNORECASE))


def is_scratch_only(content):
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("FROM "):
            ref = stripped[5:].split()[0].lower()
            if ref not in ("scratch",):
                return False
    return True


def add_targetarch(content):
    lines = content.split("\n")
    new_lines = []
    added = False

    for line in lines:
        new_lines.append(line)
        if not added and re.match(r"^ARG\s+VERSION=", line, re.IGNORECASE):
            new_lines.append("ARG TARGETARCH")
            added = True

    return "\n".join(new_lines), added


def process_image(image_dir, dry_run):
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        return None

    content = dockerfile.read_text()

    if has_targetarch(content):
        return None

    if is_scratch_only(content):
        return None

    name = image_dir.name
    if name in EXCLUDED_IMAGES:
        return None

    new_content, added = add_targetarch(content)

    if not added:
        return None

    if dry_run:
        print(f"  [DRY-RUN] Would add ARG TARGETARCH to {name}")
        return None

    dockerfile.write_text(new_content)
    print(f"  Added ARG TARGETARCH to {name}")
    return name


def main():
    parser = argparse.ArgumentParser(description="Add ARG TARGETARCH to Dockerfiles")
    parser.add_argument("--dry-run", action="store_true", help="Dry run")
    parser.add_argument("--images", nargs="*", help="Specific images to process")
    parser.add_argument("--images-dir", default="images", help="Images directory")
    args = parser.parse_args()

    images_dir = Path(args.images_dir)

    if args.images:
        targets = [Path(args.images_dir) / name for name in args.images]
    else:
        targets = sorted([d for d in images_dir.iterdir() if d.is_dir()])

    added = 0
    skipped = 0
    errors = 0

    for target in targets:
        try:
            result = process_image(target, args.dry_run)
            if result is not None:
                added += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ERROR: {target.name}: {e}")

    print(f"\nSummary: {added} modified, {skipped} unchanged, {errors} errors")

    if args.dry_run:
        print("(Dry run - no files were modified)")
        return 0

    if added == 0:
        print("No changes needed - all eligible images already have ARG TARGETARCH")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
