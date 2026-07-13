#!/usr/bin/env python3
"""Catalog Expansion Engine for Evergreen Image Registry."""

import json
import subprocess
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
EVERGREENCTL = str(
    Path(__file__).resolve().parent.parent
    / "evergreenctl"
    / "target"
    / "release"
    / "evergreenctl"
)

GITHUB_GO_PROJECTS = {
    "postgres-exporter": ("prometheus-community/postgres_exporter", 9187),
    "redis-exporter": ("oliver006/redis_exporter", 9121),
    "mysqld-exporter": ("prometheus/mysqld_exporter", 9104),
    "mongodb-exporter": ("percona/mongodb_exporter", 9216),
    "kafka-exporter": ("danielqsj/kafka_exporter", 9308),
    "rabbitmq-exporter": ("kbudde/rabbitmq_exporter", 9419),
    "pushgateway": ("prometheus/pushgateway", 9091),
    "caddy": ("caddyserver/caddy", 2019),
    "frp": ("fatedier/frp", 7000),
    "rathole": ("rapiz1/rathole", 7000),
    "gotty": ("sorenisanerd/gotty", 8080),
    "ttyd": ("tsl0922/ttyd", 7681),
    "goaccess": ("allinurl/goaccess", 7890),
    "polaris": ("FairwindsOps/polaris", 8080),
    "kube-bench": ("aquasecurity/kube-bench", 0),
    "kube-hunter": ("aquasecurity/kube-hunter", 0),
    "restic-rest-server": ("restic/rest-server", 8000),
    "minio-mc": ("minio/mc", 0),
    "mkcert": ("FiloSottile/mkcert", 0),
}

DH_OFFICIAL_IMAGES = {
    "cassandra": ("cassandra", 9042),
    "couchdb": ("apache/couchdb", 5984),
    "memcached": ("memcached", 11211),
    "zookeeper": ("zookeeper", 2181),
    "varnish": ("varnish", 6081),
    "httpd": ("httpd", 8080),
    "surrealdb": ("surrealdb/surrealdb", 8000),
}


def get_latest_tag(repo):
    try:
        r = subprocess.run(
            ["curl", "-s", f"https://api.github.com/repos/{repo}/releases/latest"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return json.loads(r.stdout).get("tag_name", "latest")
    except Exception:
        return "latest"


def create_image(name, upstream, port):
    img_dir = IMAGES_DIR / name
    if (img_dir / "Dockerfile").exists():
        return False

    img_dir.mkdir(parents=True, exist_ok=True)

    version = get_latest_tag(upstream) if "/" in upstream else "latest"
    clean_ver = version.lstrip("v")

    # Detect type
    if upstream.count("/") == 1 and "." not in upstream.split("/")[0]:
        stype = "upstream-repack"
    else:
        stype = "binary-download"

    manifest = f'''[metadata]
name = "{name}"
version = "{clean_ver}"
description = "{name} - Evergreen hardened image"
vendor = "Evergreen"
source = "https://github.com/{upstream}"
license = "Apache-2.0"
tier = "standard"

[build]
base = "scratch"
user = "65532:65532"
stopsignal = "SIGTERM"

[source]
type = "{stype}"
url = "https://github.com/{upstream}"

[runtime]
entrypoint = []

[ports]
expose = [{port if port else ""}{" " if port else ""}9101]
'''
    (img_dir / "manifest.toml").write_text(manifest)

    # Generate Dockerfile
    r = subprocess.run(
        [EVERGREENCTL, "generate", str(img_dir)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if r.returncode == 0:
        (img_dir / "Dockerfile").write_text(r.stdout)

    return True


def main():
    added = 0
    print("=== GitHub Go/Rust binary projects ===")
    for name, (repo, port) in sorted(GITHUB_GO_PROJECTS.items()):
        if create_image(name, repo, port):
            print(f"  ✅ {name} → github.com/{repo}")
            added += 1

    print("\n=== Docker Hub Official images ===")
    for name, (upstream, port) in sorted(DH_OFFICIAL_IMAGES.items()):
        if create_image(name, upstream, port):
            print(f"  ✅ {name} → {upstream}")
            added += 1

    print(f"\nTotal new images: {added}")


if __name__ == "__main__":
    main()
