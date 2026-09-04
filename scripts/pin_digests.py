#!/usr/bin/env python3
"""Pin FROM digests for critical-tier images using crane."""

import subprocess
import sys
from pathlib import Path


def get_critical_images(images_dir: str) -> list[str]:
    """Get list of critical-tier image directories."""
    critical = []
    for entry in sorted(Path(images_dir).iterdir()):
        if not entry.is_dir() or entry.name.startswith("_"):
            continue
        manifest = entry / "manifest.toml"
        if manifest.exists() and 'tier = "critical"' in manifest.read_text():
            critical.append(entry.name)
    return critical


def resolve_digest(image_ref: str) -> str | None:
    """Resolve image reference to digest using crane."""
    try:
        result = subprocess.run(
            ["crane", "digest", image_ref],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def parse_from_lines(dockerfile: Path) -> list[tuple[int, str, str]]:
    """Parse FROM lines, return (line_number, original_line, image_ref)."""
    results = []
    for i, line in enumerate(dockerfile.read_text().splitlines(), 1):
        if line.startswith("FROM "):
            # Extract image reference (before AS or end)
            parts = line.split()
            img = parts[1]
            # Skip if already pinned
            if "@sha256:" in img:
                continue
            # Skip ARG-based references (e.g., FROM ${BASE_IMAGE})
            if "${" in img:
                continue
            results.append((i, line, img))
    return results


def pin_image_in_dockerfile(dockerfile: Path, old_ref: str, new_ref: str) -> bool:
    """Replace image reference with digest-pinned version."""
    content = dockerfile.read_text()
    # Replace the image reference, preserving any tag
    new_content = content.replace(old_ref, new_ref)
    if new_content != content:
        dockerfile.write_text(new_content)
        return True
    return False


def main():
    images_dir = sys.argv[1] if len(sys.argv) > 1 else "images"
    dry_run = "--dry-run" in sys.argv

    critical = get_critical_images(images_dir)
    print(f"Found {len(critical)} critical-tier images")

    total_pins = 0
    success_pins = 0
    failed_pins = 0
    skipped = 0

    for img_name in critical:
        dockerfile = Path(images_dir) / img_name / "Dockerfile"
        if not dockerfile.exists():
            continue

        from_lines = parse_from_lines(dockerfile)
        if not from_lines:
            skipped += 1
            continue

        for line_num, original_line, img_ref in from_lines:
            total_pins += 1
            print(f"  Resolving {img_ref}...", end=" ", flush=True)

            digest = resolve_digest(img_ref)
            if digest:
                pinned_ref = f"{img_ref}@{digest}"
                if dry_run:
                    print(f"→ {pinned_ref}")
                else:
                    if pin_image_in_dockerfile(dockerfile, img_ref, pinned_ref):
                        print(f"✅ {pinned_ref}")
                        success_pins += 1
                    else:
                        print("❌ failed to replace")
                        failed_pins += 1
            else:
                print("⚠️  could not resolve digest")
                failed_pins += 1

    print("\n=== Summary ===")
    print(f"Total FROM lines: {total_pins}")
    print(f"Pinned: {success_pins}")
    print(f"Failed: {failed_pins}")
    print(f"Skipped (already pinned): {skipped}")


if __name__ == "__main__":
    main()
