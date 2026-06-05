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

# Postgres/MariaDB/MySQL images for scheduler-shim
SCHEDULER_IMAGES = {
    "postgres", "postgres-backup", "postgres-restore", "postgresql-patroni",
    "postgresql-14", "postgresql-15", "postgresql-16", "postgresql-17",
    "postgresql-18", "timescaledb",
    "mariadb", "mariadb-10", "mariadb-11", "mariadb-galera",
    "mysql", "mysql-8",
}

PROMETHEUS_LABELS = (
    'LABEL prometheus.io/scrape="true" \\\n'
    '      prometheus.io/port="9101" \\\n'
    '      prometheus.io/path="/metrics"'
)


def detect_shim_type(content: str) -> str | None:
    lower = content.lower()
    if "evergreenshim/db-shim" in lower:
        return "db"
    elif "evergreenshim/cache-shim" in lower:
        return "cache"
    elif "evergreenshim/health-shim" in lower:
        return "health"
    return None


def has_shim_wiring(content: str) -> bool:
    return ("COPY --from=shim" in content and
            ("/shim" in content or "/usr/local/bin/shim" in content))


def find_last_from_line(lines: list) -> int:
    """Find the last FROM line index (start of final stage)."""
    last = 0
    for i, line in enumerate(lines):
        if line.strip().upper().startswith("FROM "):
            last = i
    return last


def find_user_line(lines: list) -> int | None:
    """Find the USER line in the final stage."""
    final_start = find_last_from_line(lines)
    for i in range(final_start, len(lines)):
        if lines[i].strip().upper().startswith("USER "):
            return i
    return None


def find_shim_env_block(lines: list) -> tuple[int, int] | None:
    """Find the last ENV block that contains SHIM_ variables.
    Returns (start_line_idx, end_line_idx) or None."""
    final_start = find_last_from_line(lines)
    result = None

    i = final_start
    while i < len(lines):
        stripped = lines[i].strip()
        # Detect start of ENV block
        if stripped.upper().startswith("ENV "):
            # Check if this ENV block contains SHIM_ vars
            block_start = i
            block_end = i
            j = i + 1
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith('"') or s.startswith("SHIM_") or s.startswith("EVERGREEN") or s.startswith("PGDATA"):
                    block_end = j
                    j += 1
                elif s == "":
                    break
                else:
                    break
            # Check if block has SHIM_ vars
            block_text = "\n".join(lines[block_start:block_end + 1])
            if "SHIM_" in block_text:
                result = (block_start, block_end)
            i = block_end + 1
        else:
            i += 1

    return result


def find_any_env_block(lines: list) -> tuple[int, int] | None:
    """Find the last ENV block in the final stage."""
    final_start = find_last_from_line(lines)
    result = None

    i = final_start
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.upper().startswith("ENV "):
            block_start = i
            block_end = i
            j = i + 1
            while j < len(lines):
                s = lines[j].strip()
                if s.startswith('"') or s.startswith("SHIM_") or s.startswith("EVERGREEN") or s.startswith("PGDATA"):
                    block_end = j
                    j += 1
                elif s == "":
                    break
                else:
                    break
            result = (block_start, block_end)
            i = block_end + 1
        else:
            i += 1

    return result


def add_var_to_env_block(content: str, var_name: str, var_value: str) -> str:
    """Add a variable to the SHIM_ ENV block, or create new ENV block after USER."""
    lines = content.split("\n")
    var_line = f'{var_name}="{var_value}"'

    # Find SHIM_ ENV block first
    env_range = find_shim_env_block(lines)

    if env_range is not None:
        env_start, env_end = env_range
        last_line = lines[env_end]
        if last_line.rstrip().endswith("\\"):
            lines[env_end] = last_line.rstrip().rstrip("\\").rstrip()
            lines.insert(env_end + 1, f'    {var_line}')
        else:
            lines[env_end] = last_line + " \\"
            lines.insert(env_end + 1, f'    {var_line}')
        return "\n".join(lines)

    # Find USER line and add new ENV block after it
    user_idx = find_user_line(lines)
    if user_idx is not None:
        lines.insert(user_idx + 1, f"ENV {var_line}")
        return "\n".join(lines)

    # Fallback: add at end
    lines.append(f"ENV {var_line}")
    return "\n".join(lines)


def add_metrics_env(content: str) -> str:
    if "SHIM_METRICS_ENABLED" in content:
        return content
    return add_var_to_env_block(content, "SHIM_METRICS_ENABLED", "true")


def add_alerting_env(content: str) -> str:
    if "SHIM_ALERTING_ENABLED" in content:
        return content
    content = add_var_to_env_block(content, "SHIM_ALERTING_ENABLED", "false")
    content = add_var_to_env_block(content, "SHIM_ALERTING_WEBHOOK_URL", "")
    return content


def add_scheduler_env(content: str) -> str:
    if "SHIM_SCHEDULER_ENABLED" in content:
        return content
    content = add_var_to_env_block(content, "SHIM_SCHEDULER_ENABLED", "true")
    content = add_var_to_env_block(content, "SHIM_SCHEDULER_BACKUP_CRON", "0 2 * * *")
    return content


def add_prometheus_labels(content: str) -> str:
    if 'prometheus.io/scrape' in content:
        return content
    lines = content.split("\n")

    insert_idx = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip().upper().startswith("STOPSIGNAL"):
            insert_idx = i
            break

    for j, label_line in enumerate(PROMETHEUS_LABELS.split("\n")):
        lines.insert(insert_idx + j, label_line)

    return "\n".join(lines)


def process_image(image_dir: Path, dry_run: bool = False) -> tuple[str, str]:
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
        elif status == "skip" and msg not in ("already up to date", "no shim wiring"):
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
