#!/usr/bin/env python3
"""
Wire backup schedule configuration into DB-shim-wired images.

Adds SHIM_BACKUP_ENABLED, SHIM_BACKUP_SCHEDULE, SHIM_BACKUP_RETENTION_DAYS,
and SHIM_BACKUP_OUTPUT_DIR ENV vars to all images already wired with a DB shim.

Usage:
    python3 scripts/wire_backup_schedules.py --dry-run          # Preview changes
    python3 scripts/wire_backup_schedules.py --force            # Overwrite existing
    python3 scripts/wire_backup_schedules.py --image postgres   # Wire specific image
"""

import argparse
import os
import re

# All DB-shim-wired images (from wire_db_shim.py DB_IMAGE_MAP)
DB_SHIM_WIRED_IMAGES = [
    # PostgreSQL
    "postgresql-14",
    "postgresql-15",
    "postgresql-16",
    "postgresql-17",
    "postgresql-18",
    "postgres",
    "postgres-backup",
    "postgres-restore",
    "postgresql-patroni",
    "timescaledb",
    "postgresql-exporter",
    "postgres-exporter",
    # MariaDB
    "mariadb",
    "mariadb-10",
    "mariadb-11",
    "mariadb-galera",
    # MySQL
    "mysql",
    "mysql-8",
    # Redis
    "redis",
    "redis-6",
    "redis-7",
    "redis7",
    "redis-cluster",
    "redis-sentinel",
]

BACKUP_ENV_VARS = {
    "SHIM_BACKUP_ENABLED": "true",
    "SHIM_BACKUP_SCHEDULE": "0 2 * * *",
    "SHIM_BACKUP_RETENTION_DAYS": "7",
    "SHIM_BACKUP_OUTPUT_DIR": "/backups",
}


def build_backup_env_block() -> str:
    """Build the ENV block for backup schedule variables."""
    lines = []
    for i, (k, v) in enumerate(BACKUP_ENV_VARS.items()):
        sep = " \\\n    " if i > 0 else ""
        lines.append(f'{sep}{k}="{v}"')
    return "".join(lines)


def is_already_wired(dockerfile_content: str) -> bool:
    """Check if SHIM_BACKUP_SCHEDULE is already present."""
    return "SHIM_BACKUP_SCHEDULE" in dockerfile_content


def has_shim_base(dockerfile_content: str) -> bool:
    """Check if image has a shim FROM stage."""
    return "evergreenshim/" in dockerfile_content.lower()


def wire_image(image_dir: str, dry_run: bool = False, force: bool = False) -> tuple:
    """Add backup schedule ENV vars to a single image. Returns (status, message)."""
    dockerfile = os.path.join(image_dir, "Dockerfile")
    if not os.path.exists(dockerfile):
        return "skip", "no Dockerfile"

    with open(dockerfile) as f:
        content = f.read()

    if not has_shim_base(content):
        return "skip", "no shim wired"

    if is_already_wired(content) and not force:
        return "skip", "already wired"

    env_block = build_backup_env_block()

    # Strategy: find existing ENV block after USER line and append backup vars
    # If SHIM_BACKUP_ENABLED exists, replace the backup-related lines
    if "SHIM_BACKUP_ENABLED" in content:
        # Replace existing SHIM_BACKUP_ENABLED line value
        content = re.sub(
            r'SHIM_BACKUP_ENABLED="[^"]*"',
            'SHIM_BACKUP_ENABLED="true"',
            content,
        )
        # Add schedule/retention/output after SHIM_BACKUP_DB_PORT line if not present
        if "SHIM_BACKUP_SCHEDULE" not in content:
            content = re.sub(
                r'(SHIM_BACKUP_DB_PORT="[^"]*"[\s\\]*\n)',
                f"\\1    {env_block}\n",
                content,
                count=1,
            )
    else:
        # No existing backup config — add after the last ENV line in the shim block
        if "USER " in content:
            content = re.sub(
                r"(USER\s+\S+\n)",
                f"\\1ENV {env_block}\n",
                content,
                count=1,
            )

    if dry_run:
        return "would-wire", "backup schedule env vars added"

    with open(dockerfile, "w") as f:
        f.write(content)

    return "wired", "backup schedule env vars added"


def main():
    parser = argparse.ArgumentParser(
        description="Wire backup schedules into DB-shim-wired images"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing backup config"
    )
    parser.add_argument("--image", type=str, help="Wire a specific image only")
    args = parser.parse_args()

    images_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
    )

    wired = 0
    skipped = 0
    errors = 0

    for image_name in sorted(DB_SHIM_WIRED_IMAGES):
        if args.image and image_name != args.image:
            continue

        image_dir = os.path.join(images_dir, image_name)
        if not os.path.isdir(image_dir):
            print(f"  SKIP   {image_name}: directory not found")
            skipped += 1
            continue

        result, reason = wire_image(image_dir, dry_run=args.dry_run, force=args.force)

        if reason in ("wired", "would-wire"):
            wired += 1
            prefix = "[DRY RUN] " if args.dry_run else ""
            print(f"  {prefix}WIRED   {image_name}: {reason}")
        elif reason == "already wired":
            skipped += 1
            print(f"  SKIP   {image_name}: already wired")
        elif reason == "no shim wired":
            skipped += 1
            print(f"  SKIP   {image_name}: {reason}")
        else:
            skipped += 1
            print(f"  SKIP   {image_name}: {reason}")

    print(f"\nSummary: {wired} wired, {skipped} skipped, {errors} errors")
    if args.dry_run:
        print("[DRY RUN] No files were modified")


if __name__ == "__main__":
    main()
