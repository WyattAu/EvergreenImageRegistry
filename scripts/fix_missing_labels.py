#!/usr/bin/env python3
"""Fix missing evergreen.base.image labels and remove stale labels from Dockerfiles."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = PROJECT_ROOT / "images"

FILES_NEEDING_LABEL = [
    "images/alpine-static/Dockerfile",
    "images/drone/Dockerfile",
    "images/gitlab/Dockerfile",
    "images/jellyfin/Dockerfile",
    "images/jellyfin-server/Dockerfile",
    "images/lidarr/Dockerfile",
    "images/milvus-etcd/Dockerfile",
    "images/milvus-minio/Dockerfile",
    "images/musl/Dockerfile",
    "images/openhab/Dockerfile",
    "images/oxidized/Dockerfile",
    "images/prowlarr/Dockerfile",
    "images/pulsar/Dockerfile",
    "images/python-alpine/Dockerfile",
    "images/python-slim/Dockerfile",
    "images/radarr/Dockerfile",
    "images/redis-vert/Dockerfile",
    "images/sonarr/Dockerfile",
    "images/x86_64-unknown-linux-musl/Dockerfile",
]

STALE_LABELS = [
    'evergreen.constraint.runtime="debian-slim"',
    'evergreen.constraint.debian_slim="true"',
]


def find_last_from(content: str) -> str:
    lines = content.splitlines()
    last_from = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("FROM ") or stripped == "FROM":
            last_from = stripped
    return last_from or ""


def classify_base_image(from_line: str) -> tuple[str, bool]:
    from_lower = from_line.lower()
    if "scratch" in from_lower:
        return "scratch", False
    if "wolfi" in from_lower or "chainguard" in from_lower:
        return "wolfi", False
    if (
        "debian" in from_lower
        or "ubuntu" in from_lower
        or "bookworm" in from_lower
        or "slim" in from_lower
    ):
        return "rhel-ubi", True
    if "alpine" in from_lower:
        return "wolfi", True
    return "unrecognized", False


def has_label(content: str, label_key: str) -> bool:
    return label_key in content


def remove_stale_labels(content: str) -> tuple[str, list[str]]:
    removed = []
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        should_remove = False
        for stale in STALE_LABELS:
            if stale in stripped:
                should_remove = True
                removed.append(stale)
                break
        if should_remove:
            continue
        new_lines.append(line)
    return "\n".join(new_lines), removed


def add_base_image_label(content: str, base_value: str, needs_migration: bool) -> str:
    lines = content.splitlines()

    insert_idx = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("LABEL evergreen.metrics.native"):
            insert_idx = i
            break

    if insert_idx is None:
        print("  WARNING: Could not find metrics label insertion point")
        return content

    label_line = f'LABEL evergreen.base.image="{base_value}"'
    if needs_migration:
        label_line = f"# TODO: migrate from unrecognized/deprecated base to wolfi or scratch\n{label_line}"

    lines.insert(insert_idx, label_line)
    return "\n".join(lines)


def process_file(rel_path: str) -> dict:
    full_path = PROJECT_ROOT / rel_path
    if not full_path.exists():
        return {"status": "error", "reason": "file not found"}

    content = full_path.read_text()

    if has_label(content, "evergreen.base.image"):
        return {"status": "skipped", "reason": "already has evergreen.base.image"}

    last_from = find_last_from(content)
    if not last_from:
        return {"status": "error", "reason": "no FROM line found"}

    base_value, needs_migration = classify_base_image(last_from)

    content = add_base_image_label(content, base_value, needs_migration)

    full_path.write_text(content)

    result = {
        "status": "fixed",
        "base_image": base_value,
        "from_line": last_from,
        "needs_migration": needs_migration,
    }
    return result


def scan_and_remove_stale_labels() -> list[dict]:
    results = []
    for dockerfile in sorted(IMAGES_DIR.glob("**/Dockerfile")):
        rel = dockerfile.relative_to(PROJECT_ROOT)
        content = dockerfile.read_text()
        new_content, removed = remove_stale_labels(content)
        if removed:
            dockerfile.write_text(new_content)
            results.append({"file": str(rel), "removed": removed})
    return results


def main():
    print("=" * 70)
    print("Phase 1: Adding missing evergreen.base.image labels")
    print("=" * 70)

    manual_intervention = []
    migration_needed = []

    for rel_path in FILES_NEEDING_LABEL:
        print(f"\n{rel_path}:")
        result = process_file(rel_path)
        print(f"  Status: {result['status']}")
        if result["status"] == "fixed":
            print(f"  FROM:   {result['from_line']}")
            print(f'  Label:  evergreen.base.image="{result["base_image"]}"')
            if result["needs_migration"]:
                migration_needed.append(rel_path)
                print("  *** MIGRATION NEEDED ***")
            if result["base_image"] == "unrecognized":
                manual_intervention.append(
                    {
                        "file": rel_path,
                        "from": result["from_line"],
                        "reason": "Unrecognized base image - needs manual classification",
                    }
                )
        elif result["status"] == "error":
            print(f"  ERROR: {result['reason']}")
            manual_intervention.append({"file": rel_path, "reason": result["reason"]})
        else:
            print(f"  {result['reason']}")

    print("\n" + "=" * 70)
    print("Phase 2: Removing stale labels")
    print("=" * 70)

    stale_results = scan_and_remove_stale_labels()
    if stale_results:
        for r in stale_results:
            print(f"  {r['file']}: removed {r['removed']}")
    else:
        print("  No stale labels found")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if manual_intervention:
        print(f"\nFiles needing MANUAL INTERVENTION ({len(manual_intervention)}):")
        for m in manual_intervention:
            print(f"  - {m['file']}")
            if "from" in m:
                print(f"    FROM: {m['from']}")
            print(f"    Reason: {m['reason']}")

    if migration_needed:
        print(f"\nFiles needing MIGRATION to approved base ({len(migration_needed)}):")
        for f in migration_needed:
            print(f"  - {f}")

    if not manual_intervention and not migration_needed:
        print("\nAll 20 files processed successfully. No manual intervention needed.")


if __name__ == "__main__":
    main()
