#!/usr/bin/env python3
"""
Enforce non-root (USER 65532:65532) on all repack images.

Scans all Dockerfiles with evergreen.entrypoint.pattern or similar repack
labels, and adds USER 65532:65532 before the ENTRYPOINT/CMD if not already
present.

For images that need writable directories (databases, queues, etc.),
adds chown commands before the USER directive.
"""

import sys
from pathlib import Path

IMAGES_DIR = Path("images")

# Known data-bearing images that need chown for writable directories
# Format: image_name -> list of (directory, ownership) tuples
DATA_DIR_IMAGES = {
    "activemq": [("/var/lib/activemq", "65532:65532")],
    "apache": [("/usr/local/apache2", "65532:65532")],
    "arangodb": [("/var/lib/arangodb3", "65532:65532")],
    "cassandra": [("/var/lib/cassandra", "65532:65532")],
    "clickhouse": [("/var/lib/clickhouse", "65532:65532")],
    "cockroachdb": [("/cockroach/cockroach-data", "65532:65532")],
    "consul": [("/consul/data", "65532:65532")],
    "couchdb": [("/opt/couchdb/data", "65532:65532")],
    "elasticsearch": [("/usr/share/elasticsearch/data", "65532:65532")],
    "etcd": [("/bitnami/etcd/data", "65532:65532")],
    "flink": [("/opt/flink", "65532:65532")],
    "grafana": [("/var/lib/grafana", "65532:65532")],
    "influxdb": [("/var/lib/influxdb2", "65532:65532")],
    "jenkins": [("/var/jenkins_home", "65532:65532")],
    "kafka": [("/var/lib/kafka/data", "65532:65532")],
    "kibana": [("/usr/share/kibana", "65532:65532")],
    "mariadb": [("/var/lib/mysql", "65532:65532")],
    "minio": [("/data", "65532:65532")],
    "mongodb": [("/data/db", "65532:65532"), ("/data/configdb", "65532:65532")],
    "mssql": [("/var/opt/mssql", "65532:65532")],
    "mysql": [("/var/lib/mysql", "65532:65532")],
    "nats": [("/nats-server", "65532:65532")],
    "neo4j": [("/data", "65532:65532"), ("/logs", "65532:65532")],
    "nextcloud": [("/var/www/html", "65532:65532")],
    "nighthawk": [("/tmp", "65532:65532")],
    "odoo": [("/var/lib/odoo", "65532:65532")],
    "opensearch": [("/usr/share/opensearch/data", "65532:65532")],
    "patroni": [("/home/postgres", "65532:65532")],
    "phpmyadmin": [("/var/www/html", "65532:65532")],
    "postgres": [("/var/lib/postgresql/data", "65532:65532")],
    "prometheus": [("/prometheus", "65532:65532")],
    "rabbitmq": [("/var/lib/rabbitmq", "65532:65532")],
    "redis": [("/data", "65532:65532")],
    "redmine": [("/usr/src/redmine/files", "65532:65532")],
    "riak": [("/var/lib/riak", "65532:65532")],
    "rocketchat": [("/uploads", "65532:65532")],
    "scylladb": [("/var/lib/scylla", "65532:65532")],
    "sonarqube": [("/opt/sonarqube/data", "65532:65532")],
    "spark": [("/opt/spark", "65532:65532")],
    "vault": [("/vault/file", "65532:65532"), ("/vault/config", "65532:65532")],
    "zookeeper": [("/var/lib/zookeeper", "65532:65532")],
}

# Images that are known to be problematic with non-root (need special handling)
# These will get a comment instead of auto-fix
SPECIAL_CASES = {
    "homeassistant-supervisor",  # Needs root for supervisor
    "portainer",                 # Needs root for Docker socket
}


def is_repack(dockerfile_content: str) -> bool:
    """Check if this is a repack image."""
    markers = [
        "evergreen.entrypoint.pattern",
        "evergreen.image.repack",
        "evergreen.base.image",
    ]
    return any(m in dockerfile_content for m in markers)


def has_user(dockerfile_content: str) -> bool:
    """Check if USER directive already exists."""
    return (
        "USER 65532" in dockerfile_content
        or "USER 65534" in dockerfile_content
        or "USER nobody" in dockerfile_content
    )


def find_insert_point(lines: list[str]) -> int:
    """
    Find the line index where USER 65532:65532 should be inserted.
    Strategy: Insert before the last ENTRYPOINT or CMD, but after all
    RUN/COPY/LABEL instructions in the final stage.
    """
    last_entrypoint_idx = None
    last_cmd_idx = None
    last_from_idx = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            last_from_idx = i
        if stripped.upper().startswith("ENTRYPOINT"):
            last_entrypoint_idx = i
        if stripped.upper().startswith("CMD "):
            last_cmd_idx = i

    # Insert before ENTRYPOINT if it exists, otherwise before CMD
    if last_entrypoint_idx is not None:
        return last_entrypoint_idx
    if last_cmd_idx is not None:
        return last_cmd_idx

    # Fallback: insert before the last LABEL or EXPOSE
    for i in range(len(lines) - 1, last_from_idx, -1):
        stripped = lines[i].strip()
        if stripped.upper().startswith("LABEL ") or stripped.upper().startswith("EXPOSE "):
            return i

    # Ultimate fallback: append at end
    return len(lines)


def needs_chown(image_name: str) -> list[tuple[str, str]]:
    """Return list of (directory, ownership) that need chown for this image."""
    return DATA_DIR_IMAGES.get(image_name, [])


def fix_dockerfile(dockerfile_path: Path, dry_run: bool = False) -> bool:
    """
    Add USER 65532:65532 to a Dockerfile if needed.
    Returns True if changes were made.
    """
    content = dockerfile_path.read_text()

    if not is_repack(content):
        return False
    if has_user(content):
        return False

    image_name = dockerfile_path.parent.name
    if image_name in SPECIAL_CASES:
        print(f"  SKIP (special case): {image_name}")
        return False

    lines = content.split("\n")

    # Determine if we need chown lines
    chown_dirs = needs_chown(image_name)

    # Find where to insert USER
    insert_idx = find_insert_point(lines)

    # Build lines to insert
    insert_lines = []

    # Add chown for data directories if needed
    if chown_dirs:
        for directory, ownership in chown_dirs:
            # Check if chown already exists for this directory
            if f"chown -R {ownership} {directory}" not in content:
                insert_lines.append(
                    f"RUN mkdir -p {directory} && chown -R {ownership} {directory}"
                )

    # Add USER directive
    insert_lines.append("USER 65532:65532")

    # Insert the lines
    for j, new_line in enumerate(insert_lines):
        lines.insert(insert_idx + j, new_line)

    new_content = "\n".join(lines)

    if not dry_run:
        dockerfile_path.write_text(new_content)

    chown_info = f" (+ chown for {', '.join(d for d, _ in chown_dirs)})" if chown_dirs else ""
    print(f"  FIXED: {image_name}{chown_info}")
    return True


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE ===\n")

    fixed = 0
    skipped = 0
    total = 0

    # Find all Dockerfiles
    for dockerfile in sorted(IMAGES_DIR.glob("*/Dockerfile")):
        # Skip _wip and _archive
        if "_wip" in str(dockerfile) or "_archive" in str(dockerfile):
            continue

        total += 1
        if fix_dockerfile(dockerfile, dry_run):
            fixed += 1
        else:
            content = dockerfile.read_text()
            if is_repack(content) and has_user(content):
                skipped += 1

    print("\n=== Summary ===")
    print(f"Total Dockerfiles scanned: {total}")
    print(f"Fixed (added USER 65532:65532): {fixed}")
    print(f"Already had USER: {skipped}")
    print(f"Non-repack or skipped: {total - fixed - skipped}")


if __name__ == "__main__":
    main()
