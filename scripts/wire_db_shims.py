#!/usr/bin/env python3
"""
Wire DB-specific shims into database images.

PostgreSQL/MariaDB/MySQL → db-shim (health+vault+backup+migration+audit)
Redis → cache-shim (health+cache)

Usage:
    python3 scripts/wire_db_shims.py --dry-run          # Preview changes
    python3 scripts/wire_db_shims.py --force              # Re-wire already wired
    python3 scripts/wire_db_shims.py --image postgresql-17  # Wire specific image
"""

import argparse
import os
import re

# Image → shim type mapping
DB_IMAGE_MAP = {
    # PostgreSQL
    "postgresql-14": "db",
    "postgresql-15": "db",
    "postgresql-16": "db",
    "postgresql-17": "db",
    "postgresql-18": "db",
    "postgres": "db",
    "postgres-backup": "db",
    "postgres-restore": "db",
    "postgresql-patroni": "db",
    "timescaledb": "db",
    "postgresql-exporter": "db",
    "postgres-exporter": "db",
    # MariaDB
    "mariadb": "db",
    "mariadb-10": "db",
    "mariadb-11": "db",
    "mariadb-galera": "db",
    # MySQL
    "mysql": "db",
    "mysql-8": "db",
    # Redis
    "redis": "cache",
    "redis-6": "cache",
    "redis-7": "cache",
    "redis7": "cache",
    "redis-cluster": "cache",
    "redis-sentinel": "cache",
}

# Shim binary image names
SHIM_IMAGES = {
    "db": "ghcr.io/wyattau/evergreenshim/db-shim",
    "cache": "ghcr.io/wyattau/evergreenshim/cache-shim",
}

# Environment variables per shim type
SHIM_ENV_VARS = {
    "db": {
        "SHIM_BACKUP_ENABLED": "false",
        "SHIM_BACKUP_DB_HOST": "localhost",
        "SHIM_BACKUP_DB_PORT": "5432",
        "SHIM_REPLICATION_ENABLED": "false",
        "SHIM_MIGRATION_ENABLED": "false",
        "SHIM_VAULT_ENABLED": "false",
        "SHIM_AUDIT_ENABLED": "true",
    },
    "cache": {
        "SHIM_CACHE_ENABLED": "true",
        "SHIM_CACHE_MAX_ENTRIES": "10000",
        "SHIM_CACHE_DEFAULT_TTL": "300",
        "SHIM_CACHE_EVICTION": "lru",
    },
}


def detect_base_type(dockerfile_content):
    """Detect if image uses scratch, wolfi, or debian base."""
    if re.search(r"FROM\s+scratch", dockerfile_content):
        return "scratch"
    elif "wolfi" in dockerfile_content or "chainguard" in dockerfile_content:
        return "wolfi"
    elif "debian" in dockerfile_content:
        return "debian"
    return "unknown"


def get_shim_path(base_type):
    """Get correct shim binary path for base type."""
    if base_type == "scratch":
        return "/shim"
    else:
        return "/usr/local/bin/shim"


def is_already_wired(db_type, dockerfile_content):
    """Check if image already has the target shim wired."""
    shim_image = SHIM_IMAGES[db_type]
    return shim_image in dockerfile_content


def get_env_block(db_type, base_type):
    """Generate ENV block for shim vars."""
    vars_dict = SHIM_ENV_VARS[db_type]
    lines = []
    for i, (k, v) in enumerate(vars_dict.items()):
        sep = " \\\n    " if i > 0 else ""
        lines.append(f'{sep}{k}="{v}"')
    return "".join(lines)


def wire_image(image_dir, db_type, dry_run=False, force=False):
    """Wire a single image with its DB shim."""
    dockerfile = os.path.join(image_dir, "Dockerfile")
    if not os.path.exists(dockerfile):
        return None, "no Dockerfile"

    with open(dockerfile) as f:
        content = f.read()

    if is_already_wired(db_type, content) and not force:
        return None, "already wired"

    base_type = detect_base_type(content)
    shim_image = SHIM_IMAGES[db_type]

    # Step 1: Replace health-shim FROM with target shim (handle both ${SHIM_VERSION} and hardcoded)
    content = re.sub(
        r"FROM\s+ghcr\.io/wyattau/evergreenshim/health-shim:(?:\$\{SHIM_VERSION\}|v[\d.]+)\s+AS\s+shim",
        f"FROM {shim_image}:${{SHIM_VERSION}} AS shim",
        content,
    )

    # Step 2: Add ENV vars for shim config (after USER line or before EXPOSE)
    env_block = get_env_block(db_type, base_type)
    if db_type == "db":
        # For DB images, add after USER line
        if "USER " in content and env_block not in content:
            content = re.sub(
                r"(USER\s+\S+\n)",
                f"\\1ENV {env_block}\n",
                content,
            )
    elif db_type == "cache" and "USER " in content and env_block not in content:
        content = re.sub(
            r"(USER\s+\S+\n)",
            f"\\1ENV {env_block}\n",
            content,
        )

    if dry_run:
        return content, "would-wire"

    with open(dockerfile, "w") as f:
        f.write(content)

    return content, "wired"


def main():
    parser = argparse.ArgumentParser(description="Wire DB shims into database images")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--force", action="store_true", help="Re-wire already wired images"
    )
    parser.add_argument("--image", type=str, help="Wire a specific image only")
    args = parser.parse_args()

    images_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
    )

    wired = 0
    skipped = 0
    errors = 0

    for image_name, db_type in sorted(DB_IMAGE_MAP.items()):
        if args.image and image_name != args.image:
            continue

        image_dir = os.path.join(images_dir, image_name)
        if not os.path.isdir(image_dir):
            print(f"  SKIP   {image_name}: directory not found")
            skipped += 1
            continue

        result, reason = wire_image(
            image_dir, db_type, dry_run=args.dry_run, force=args.force
        )

        if reason in ("wired", "would-wire"):
            wired += 1
            prefix = "[DRY RUN] " if args.dry_run else ""
            print(f"  {prefix}WIRED   {image_name} → {db_type}-shim")
        elif reason == "already wired":
            skipped += 1
            print(f"  SKIP   {image_name}: already wired to {db_type}-shim")
        else:
            skipped += 1
            print(f"  SKIP   {image_name}: {reason}")

    print(f"\nSummary: {wired} wired, {skipped} skipped, {errors} errors")
    if args.dry_run:
        print("[DRY RUN] No files were modified")


if __name__ == "__main__":
    main()
