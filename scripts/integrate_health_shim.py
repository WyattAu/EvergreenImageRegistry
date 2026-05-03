#!/usr/bin/env python3
"""Integrate health-shim binary into 12 database Dockerfiles."""

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(REPO_ROOT, "images")

HEALTH_SHIM_STAGE = [
    "FROM golang:1.23-alpine AS health-shim-builder",
    "COPY images/health-shim/go.mod images/health-shim/main.go /build/",
    "RUN cd /build && CGO_ENABLED=0 go build -ldflags=\"-s -w\" -o /health-shim .",
]

DATABASES = [
    {
        "name": "postgresql",
        "health_cmd": "pg_isready -h localhost",
        "ready_cmd": "pg_isready -h localhost -q",
        "startup_cmd": "pg_isready -h localhost",
    },
    {
        "name": "redis",
        "health_cmd": "redis-cli ping",
        "ready_cmd": "redis-cli ping",
        "startup_cmd": "redis-cli ping",
    },
    {
        "name": "mariadb",
        "health_cmd": "mariadb-admin ping -h 127.0.0.1 --silent",
        "ready_cmd": "mariadb-admin ping -h 127.0.0.1 --silent",
        "startup_cmd": "mariadb-admin ping -h 127.0.0.1 --silent",
    },
    {
        "name": "mongodb",
        "health_cmd": "mongosh --eval \"db.adminCommand('ping')\"",
        "ready_cmd": "mongosh --eval \"db.adminCommand('ping')\"",
        "startup_cmd": "mongosh --eval \"db.adminCommand('ping')\"",
    },
    {
        "name": "valkey",
        "health_cmd": "valkey-cli ping",
        "ready_cmd": "valkey-cli ping",
        "startup_cmd": "valkey-cli ping",
    },
    {
        "name": "kafka",
        "health_cmd": "kafka-broker-api-versions --bootstrap-server localhost:9092",
        "ready_cmd": "kafka-broker-api-versions --bootstrap-server localhost:9092",
        "startup_cmd": "kafka-broker-api-versions --bootstrap-server localhost:9092",
    },
    {
        "name": "rabbitmq",
        "health_cmd": "rabbitmq-diagnostics -q ping",
        "ready_cmd": "rabbitmq-diagnostics -q check_running",
        "startup_cmd": "rabbitmq-diagnostics -q ping",
    },
    {
        "name": "mysql",
        "health_cmd": "mariadb-admin ping -h 127.0.0.1 --silent",
        "ready_cmd": "mariadb-admin ping -h 127.0.0.1 --silent",
        "startup_cmd": "mariadb-admin ping -h 127.0.0.1 --silent",
    },
    {
        "name": "elasticsearch",
        "health_cmd": "curl -sf http://localhost:9200/_cluster/health",
        "ready_cmd": "curl -sf http://localhost:9200/_cluster/health",
        "startup_cmd": "curl -sf http://localhost:9200/_cluster/health",
    },
    {
        "name": "opensearch",
        "health_cmd": "curl -sf http://localhost:9200",
        "ready_cmd": "curl -sf http://localhost:9200",
        "startup_cmd": "curl -sf http://localhost:9200",
    },
    {
        "name": "cassandra",
        "health_cmd": "nodetool status",
        "ready_cmd": "nodetool netstats",
        "startup_cmd": "nodetool status",
    },
    {
        "name": "couchdb",
        "health_cmd": "curl -sf http://localhost:5984/_up",
        "ready_cmd": "curl -sf http://localhost:5984/_up",
        "startup_cmd": "curl -sf http://localhost:5984/_up",
    },
]


def dockerfile_escape(value):
    return value.replace("\\", "\\\\").replace('"', '\\"')


def process_dockerfile(db):
    name = db["name"]
    path = os.path.join(IMAGES_DIR, name, "Dockerfile")

    if not os.path.exists(path):
        print(f"  SKIP: {path} does not exist")
        return False

    with open(path) as f:
        content = f.read()

    if "health-shim-builder" in content:
        print(f"  SKIP: already integrated")
        return False

    lines = content.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]

    changes = []

    last_from_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*FROM\s+", line, re.IGNORECASE):
            last_from_idx = i

    if last_from_idx is None:
        print(f"  ERROR: no FROM found")
        return False

    insert_pos = last_from_idx
    if insert_pos > 0 and lines[insert_pos - 1].strip() != "":
        lines.insert(insert_pos, "")
        insert_pos += 1

    for j, stage_line in enumerate(HEALTH_SHIM_STAGE):
        lines.insert(insert_pos + j, stage_line)
    insert_pos += len(HEALTH_SHIM_STAGE)
    last_from_idx = insert_pos
    changes.append("Inserted health-shim-builder stage")

    copy_line = "COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim"
    lines.insert(last_from_idx + 1, copy_line)
    changes.append("Added COPY --from=health-shim-builder")

    env_insert = last_from_idx + 2
    hc = dockerfile_escape(db["health_cmd"])
    rc = dockerfile_escape(db["ready_cmd"])
    sc = dockerfile_escape(db["startup_cmd"])
    env_block = [
        f'ENV HEALTH_CMD="{hc}" \\',
        f'    READY_CMD="{rc}" \\',
        f'    STARTUP_CMD="{sc}" \\',
        "    EVERGREEN_LOG_LEVEL=info",
    ]
    for j, env_line in enumerate(env_block):
        lines.insert(env_insert + j, env_line)
    changes.append(
        f"Added ENV HEALTH_CMD READY_CMD STARTUP_CMD EVERGREEN_LOG_LEVEL"
    )

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("ENTRYPOINT"):
            continue

        exec_match = re.match(r"^ENTRYPOINT\s+\[(.+)]$", stripped)
        if exec_match:
            try:
                args = json.loads(f"[{exec_match.group(1)}]")
                cmd = " ".join(args)
                new_ep = "ENTRYPOINT " + json.dumps(
                    ["sh", "-c", "health-shim & exec " + cmd]
                )
                lines[i] = new_ep
                changes.append(f"Wrapped ENTRYPOINT -> {new_ep}")
            except json.JSONDecodeError:
                print(f"  WARNING: cannot parse ENTRYPOINT JSON: {stripped}")
            break

        shell_match = re.match(r"^ENTRYPOINT\s+(.+)$", stripped)
        if shell_match:
            cmd = shell_match.group(1)
            new_ep = "ENTRYPOINT " + json.dumps(
                ["sh", "-c", "health-shim & exec " + cmd]
            )
            lines[i] = new_ep
            changes.append(f"Wrapped ENTRYPOINT -> {new_ep}")
            break

    label_changes = []
    for i, line in enumerate(lines):
        if 'evergreen.health.type="exec"' in line:
            lines[i] = line.replace(
                'evergreen.health.type="exec"', 'evergreen.health.type="http"'
            )
            label_changes.append("evergreen.health.type: exec -> http")
        if 'evergreen.metrics.native="ztunnel"' in line:
            lines[i] = line.replace(
                'evergreen.metrics.native="ztunnel"',
                'evergreen.metrics.native="true"',
            )
            label_changes.append("evergreen.metrics.native: ztunnel -> true")
    if label_changes:
        changes.append("Updated labels: " + "; ".join(label_changes))

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

    for change in changes:
        print(f"  {change}")
    return True


def main():
    print("=" * 60)
    print("Integrating health-shim into database Dockerfiles")
    print("=" * 60)
    print()

    success = 0
    skipped = 0

    for db in DATABASES:
        print(f"[{db['name']}]")
        if process_dockerfile(db):
            success += 1
        else:
            skipped += 1
        print()

    print("-" * 60)
    print(f"Results: {success} modified, {skipped} skipped out of {len(DATABASES)}")
    print("-" * 60)

    if skipped > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
