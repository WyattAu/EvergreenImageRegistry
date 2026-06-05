#!/usr/bin/env python3
"""
wire_observability.py — Add observability config to all wired images.

Tasks:
  1. Add SHIM_METRICS_ENABLED="true" to all health-shim/db-shim/cache-shim images
  2. Add Prometheus scrape labels to all wired images
  3. Wire alerting-shim webhook env vars into DB images
  4. Wire scheduler-shim to backup for DB images (postgres/mariadb/mysql)

Usage:
    python3 scripts/wire_observability.py [--dry-run] [--image NAME]
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"

# All images from wire_db_shims.py DB_IMAGE_MAP
DB_IMAGE_MAP = {
    "postgresql-14", "postgresql-15", "postgresql-16", "postgresql-17",
    "postgresql-18", "postgres", "postgres-backup", "postgres-restore",
    "postgresql-patroni", "timescaledb", "postgresql-exporter",
    "postgres-exporter", "mariadb", "mariadb-10", "mariadb-11",
    "mariadb-galera", "mysql", "mysql-8",
    "redis", "redis-6", "redis-7", "redis7", "redis-cluster", "redis-sentinel",
}

# Postgres/MariaDB/MySQL images for scheduler-shim (subset of DB_IMAGE_MAP)
SCHEDULER_IMAGES = {
    "postgres", "postgres-backup", "postgres-restore", "postgresql-patroni",
    "postgresql-14", "postgresql-15", "postgresql-16", "postgresql-17",
    "postgresql-18", "timescaledb",
    "mariadb", "mariadb-10", "mariadb-11", "mariadb-galera",
    "mysql", "mysql-8",
    # Also include redis variants for scheduler
    "redis", "redis-6", "redis-7", "redis7", "redis-cluster", "redis-sentinel",
}

PROMETHEUS_LABELS = (
    'LABEL prometheus.io/scrape="true" \\\n'
    '      prometheus.io/port="9101" \\\n'
    '      prometheus.io/path="/metrics"'
)

ALERTING_ENV = (
    'SHIM_ALERTING_ENABLED="false" \\\n'
    'SHIM_ALERTING_WEBHOOK_URL=""'
)

SCHEDULER_ENV = (
    'SHIM_SCHEDULER_ENABLED="true" \\\n'
    'SHIM_SCHEDULER_BACKUP_CRON="0 2 * * *"'
)

METRICS_ENV = 'SHIM_METRICS_ENABLED="true"'


def detect_shim_type(content: str) -> str | None:
    """Detect which shim type is wired in this Dockerfile."""
    lower = content.lower()
    if "evergreenshim/db-shim" in lower:
        return "db"
    elif "evergreenshim/cache-shim" in lower:
        return "cache"
    elif "evergreenshim/health-shim" in lower:
        return "health"
    return None


def has_shim_wiring(content: str) -> bool:
    """Check if Dockerfile has any shim COPY/ENTRYPOINT."""
    return ("COPY --from=shim" in content and
            ("/shim" in content or "/usr/local/bin/shim" in content))


def has_env_block(content: str) -> bool:
    """Check if final stage has an ENV block."""
    lines = content.split("\n")
    in_final = False
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith("FROM ") and " AS " not in stripped.upper():
            in_final = True
        if in_final and stripped.upper().startswith("ENV "):
            return True
    return False


def find_user_line_index(lines: list) -> int | None:
    """Find the index of the USER line in the final stage."""
    final_from = -1
    from_count = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            from_count += 1
            final_from = i
    # USER line is typically after the last FROM
    for i in range(final_from, len(lines)):
        if lines[i].strip().upper().startswith("USER "):
            return i
    return None


def find_env_end_index(lines: list) -> int | None:
    """Find the end of the last ENV block in the final stage."""
    final_from = -1
    from_count = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            from_count += 1
            final_from = i

    env_start = None
    for i in range(final_from, len(lines)):
        stripped = lines[i].strip()
        if stripped.upper().startswith("ENV "):
            env_start = i
        elif env_start is not None and (stripped.startswith('"') or stripped.startswith("SHIM_")):
            continue
        elif env_start is not None:
            return i - 1
    if env_start is not None:
        return len(lines) - 1
    return None


def find_insert_point(lines: list) -> int:
    """Find where to insert ENV block: after existing ENV or after USER line."""
    # Check for existing ENV block
    env_end = find_env_end_index(lines)
    if env_end is not None:
        return env_end + 1

    # Find USER line
    user_idx = find_user_line_index(lines)
    if user_idx is not None:
        return user_idx + 1

    return len(lines)


def add_metrics_env(content: str) -> str:
    """Add SHIM_METRICS_ENABLED=true to ENV block."""
    if "SHIM_METRICS_ENABLED" in content:
        return content

    lines = content.split("\n")
    insert_idx = find_insert_point(lines)

    # Check if there's an existing ENV block at or near insert_idx
    # Look backward for ENV
    env_start = None
    for i in range(insert_idx - 1, -1, -1):
        stripped = lines[i].strip()
        if stripped.upper().startswith("ENV "):
            env_start = i
            break
        elif stripped == "":
            continue
        else:
            break

    if env_start is not None:
        # Find end of this ENV block
        env_end = env_start
        for i in range(env_start + 1, len(lines)):
            stripped = lines[i].strip()
            if stripped.startswith('"') or stripped.startswith("SHIM_") or stripped.startswith("EVERGREEN"):
                env_end = i
            else:
                break
        # Add to existing ENV block
        last_env_line = lines[env_end]
        if last_env_line.rstrip().endswith("\\"):
            lines[env_end] = last_env_line.rstrip().rstrip("\\").rstrip()
            lines.insert(env_end + 1, f'    {METRICS_ENV}')
        else:
            lines[env_end] = last_env_line + " \\"
            lines.insert(env_end + 1, f'    {METRICS_ENV}')
        return "\n".join(lines)
    else:
        # Add new ENV block
        lines.insert(insert_idx, f"ENV {METRICS_ENV}")
        return "\n".join(lines)


def add_alerting_env(content: str) -> str:
    """Add alerting-shim webhook env vars to DB images."""
    if "SHIM_ALERTING_ENABLED" in content:
        return content

    lines = content.split("\n")
    insert_idx = find_insert_point(lines)

    # Check for existing ENV block
    env_start = None
    for i in range(insert_idx - 1, -1, -1):
        stripped = lines[i].strip()
        if stripped.upper().startswith("ENV "):
            env_start = i
            break
        elif stripped == "":
            continue
        else:
            break

    if env_start is not None:
        env_end = env_start
        for i in range(env_start + 1, len(lines)):
            stripped = lines[i].strip()
            if stripped.startswith('"') or stripped.startswith("SHIM_") or stripped.startswith("EVERGREEN"):
                env_end = i
            else:
                break
        last_env_line = lines[env_end]
        if last_env_line.rstrip().endswith("\\"):
            lines[env_end] = last_env_line.rstrip().rstrip("\\").rstrip()
            for j, var_line in enumerate(ALERTING_ENV.split("\n")):
                lines.insert(env_end + 1 + j, f'    {var_line}')
        else:
            lines[env_end] = last_env_line + " \\"
            for j, var_line in enumerate(ALERTING_ENV.split("\n")):
                lines.insert(env_end + 1 + j, f'    {var_line}')
        return "\n".join(lines)
    else:
        lines.insert(insert_idx, f"ENV {ALERTING_ENV}")
        return "\n".join(lines)


def add_scheduler_env(content: str) -> str:
    """Add scheduler-shim env vars to DB images."""
    if "SHIM_SCHEDULER_ENABLED" in content:
        return content

    lines = content.split("\n")
    insert_idx = find_insert_point(lines)

    # Check for existing ENV block
    env_start = None
    for i in range(insert_idx - 1, -1, -1):
        stripped = lines[i].strip()
        if stripped.upper().startswith("ENV "):
            env_start = i
            break
        elif stripped == "":
            continue
        else:
            break

    if env_start is not None:
        env_end = env_start
        for i in range(env_start + 1, len(lines)):
            stripped = lines[i].strip()
            if stripped.startswith('"') or stripped.startswith("SHIM_") or stripped.startswith("EVERGREEN"):
                env_end = i
            else:
                break
        last_env_line = lines[env_end]
        if last_env_line.rstrip().endswith("\\"):
            lines[env_end] = last_env_line.rstrip().rstrip("\\").rstrip()
            for j, var_line in enumerate(SCHEDULER_ENV.split("\n")):
                lines.insert(env_end + 1 + j, f'    {var_line}')
        else:
            lines[env_end] = last_env_line + " \\"
            for j, var_line in enumerate(SCHEDULER_ENV.split("\n")):
                lines.insert(env_end + 1 + j, f'    {var_line}')
        return "\n".join(lines)
    else:
        lines.insert(insert_idx, f"ENV {SCHEDULER_ENV}")
        return "\n".join(lines)


def add_prometheus_labels(content: str) -> str:
    """Add Prometheus scrape labels before STOPSIGNAL or at end."""
    if 'prometheus.io/scrape' in content:
        return content

    lines = content.split("\n")

    # Insert before STOPSIGNAL or at end
    insert_idx = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip().upper().startswith("STOPSIGNAL"):
            insert_idx = i
            break

    for j, label_line in enumerate(PROMETHEUS_LABELS.split("\n")):
        lines.insert(insert_idx + j, label_line)

    return "\n".join(lines)


def process_image(image_dir: Path, dry_run: bool = False) -> tuple[str, str]:
    """Process a single image directory. Returns (status, message)."""
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        return "skip", "no Dockerfile"

    content = dockerfile.read_text()

    if not has_shim_wiring(content):
        return "skip", "no shim wiring"

    shim_type = detect_shim_type(content)
    image_name = image_dir.name
    original = content
    tasks_applied = []

    # Task 1: Add SHIM_METRICS_ENABLED to all wired images
    content = add_metrics_env(content)
    if content != original:
        tasks_applied.append("metrics")

    # Task 2: Add Prometheus labels
    before_labels = content
    content = add_prometheus_labels(content)
    if content != before_labels:
        tasks_applied.append("prometheus-labels")

    # Task 3: Add alerting env vars to DB-shim images only
    if shim_type == "db" and image_name in DB_IMAGE_MAP:
        before_alerting = content
        content = add_alerting_env(content)
        if content != before_alerting:
            tasks_applied.append("alerting")

    # Task 4: Add scheduler env vars to postgres/mariadb/mysql images
    if shim_type == "db" and image_name in SCHEDULER_IMAGES:
        before_scheduler = content
        content = add_scheduler_env(content)
        if content != before_scheduler:
            tasks_applied.append("scheduler")

    if content == original:
        return "skip", "already up to date"

    if dry_run:
        return "would-update", f"tasks={','.join(tasks_applied)}"

    dockerfile.write_text(content)
    return "updated", f"tasks={','.join(tasks_applied)}"


def main():
    parser = argparse.ArgumentParser(
        description="Add observability config to all wired images"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't write files, just report")
    parser.add_argument("--image", type=str,
                        help="Process only this image")
    args = parser.parse_args()

    print(f"Images directory: {IMAGES_DIR}")
    print()

    if not IMAGES_DIR.exists():
        print(f"ERROR: {IMAGES_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    # Collect image dirs
    image_dirs = sorted([
        d for d in IMAGES_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    ])

    if args.image:
        image_dirs = [d for d in image_dirs if d.name == args.image]
        if not image_dirs:
            print(f"ERROR: Image '{args.image}' not found", file=sys.stderr)
            sys.exit(1)

    stats = {"updated": 0, "skip": 0, "would-update": 0}
    errors = []

    for image_dir in image_dirs:
        try:
            status, msg = process_image(image_dir, args.dry_run)
        except Exception as e:
            status, msg = "error", str(e)
            errors.append(f"  {image_dir.name}: {msg}")
            print(f"  ERROR  {image_dir.name}: {msg}")
            continue

        stats[status] = stats.get(status, 0) + 1

        if status == "error":
            errors.append(f"  {image_dir.name}: {msg}")
            print(f"  ERROR  {image_dir.name}: {msg}")
        elif status == "updated":
            print(f"  UPDATE {image_dir.name}: {msg}")
        elif status == "would-update":
            print(f"  WOULD  {image_dir.name}: {msg}")
        elif status == "skip" and msg != "already up to date" and msg != "no shim wiring":
            print(f"  SKIP   {image_dir.name}: {msg}")

    print()
    print(f"Summary: {stats.get('updated', 0)} updated, "
          f"{stats.get('would-update', 0)} would-update, "
          f"{stats.get('skip', 0)} skipped")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(e)

    if args.dry_run:
        print("\n[DRY RUN] No files were modified")


if __name__ == "__main__":
    main()
