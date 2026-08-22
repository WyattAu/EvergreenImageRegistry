#!/usr/bin/env python3
"""
Fix EIR stub Dockerfiles: add VERSION, ENTRYPOINT, USER, pin base images.

Usage:
    python3 scripts/fix-stubs.py --image victoriametrics
    python3 scripts/fix-stubs.py --batch victoriametrics,node-exporter,promtail
    python3 scripts/fix-stubs.py --all-sis  # Fix SIS-critical images
"""

import argparse
import re
import sys
from pathlib import Path

# SIS-critical images that should be fixed first
SIS_CRITICAL = [
    # Monitoring
    "victoriametrics",
    "vmalert",
    "victoria-logs",
    "promtail",
    "node-exporter",
    "blackbox-exporter",
    "cadvisor",
    "postgres-exporter",
    "redis-exporter",
    # Databases
    "postgres",
    "postgresql-17",
    "postgresql-16",
    "postgresql-18",
    "redis",
    "redis-7",
    "mariadb",
    # Apps
    "freshrss",
    "homepage",
    "uptime-kuma",
    "crowdsec",
    "synapse",
    "element-web",
    "paperless-ngx",
    # Infrastructure
    "wireguard",
]

# Known binary names and ports for images where the name doesn't match
BINARY_MAP = {
    "victoriametrics": ("victoria-metrics", 8428),
    "vmalert": ("vmalert", 8880),
    "victoria-logs": ("victoria-logs", 9428),
    "node-exporter": ("node_exporter", 9100),
    "blackbox-exporter": ("blackbox_exporter", 9115),
    "postgres-exporter": ("postgres_exporter", 9187),
    "redis-exporter": ("redis_exporter", 9121),
    "mysqld-exporter": ("mysqld_exporter", 9104),
}

# Known upstream image:tag mappings
UPSTREAM_VERSIONS = {
    "victoriametrics": "victoriametrics/victoria-metrics:v1.143.0",
    "vmalert": "victoriametrics/vmalert:v1.143.0",
    "victoria-logs": "victoriametrics/victoria-logs:v1.50.0",
    "node-exporter": "prom/node-exporter:v1.9.1",
    "blackbox-exporter": "prom/blackbox-exporter:v0.28.0",
    "postgres-exporter": "prometheuscommunity/postgres-exporter:v0.17.1",
    "redis-exporter": "oliver006/redis_exporter:v1.83.0",
    "promtail": "grafana/promtail:3.6.11",
    "cadvisor": "gcr.io/cadvisor/cadvisor:v0.52.1",
    "postgres": "postgres:17",
    "postgresql-17": "postgres:17",
    "postgresql-16": "postgres:16",
    "postgresql-18": "postgres:18",
    "redis": "redis:8.0-alpine",
    "redis-7": "redis:7.4-alpine",
    "mariadb": "mariadb:11.8",
    "freshrss": "freshrss/freshrss:1.26.1",
    "homepage": "gethomepage/homepage:v1.13.1",
    "uptime-kuma": "louislam/uptime-kuma:2.3.2",
    "crowdsec": "crowdsecurity/crowdsec:v1.7.8",
    "synapse": "matrixdotorg/synapse:v1.152.1",
    "element-web": "vectorim/element-web:v1.12.18",
    "paperless-ngx": "ghcr.io/paperless-ngx/paperless-ngx:2.20.15",
    "wireguard": "linuxserver/wireguard:1.0.20250521",
}


def get_binary_and_port(image_name, dockerfile_content):
    """Extract binary name and port from Dockerfile or use defaults."""
    # Check binary map first
    if image_name in BINARY_MAP:
        return BINARY_MAP[image_name]

    # Try to extract from HEALTHCHECK line
    port_match = re.search(
        r"healthcheck.*?--tcp.*?127\.0\.0\.1:(\d+)", dockerfile_content, re.IGNORECASE
    )
    port = port_match.group(1) if port_match else "8080"

    # Binary name = image name with - replaced by _
    binary = image_name.replace("-", "_")

    return (binary, int(port))


def get_version(image_name):
    """Get version string for VERSION file."""
    upstream = UPSTREAM_VERSIONS.get(image_name, "")
    if ":" in upstream:
        return upstream.split(":")[-1]
    return ""


def fix_dockerfile(image_name, dry_run=False):
    """Fix a single stub Dockerfile."""
    img_dir = Path(f"images/{image_name}")
    dockerfile_path = img_dir / "Dockerfile"
    version_path = img_dir / "VERSION"

    if not dockerfile_path.exists():
        print(f"  ❌ {image_name}: No Dockerfile found")
        return False

    content = dockerfile_path.read_text()
    changes = []

    # 1. Add VERSION file
    version = get_version(image_name)
    if not version:
        print(f"  ⚠️  {image_name}: No version mapping, skipping")
        return False

    if not version_path.exists() or version_path.read_text().strip() != version:
        if not dry_run:
            version_path.write_text(version + "\n")
        changes.append(f"VERSION={version}")

    # 2. Check if ENTRYPOINT exists
    has_entrypoint = "ENTRYPOINT" in content

    if has_entrypoint:
        # Already has ENTRYPOINT, might just need VERSION
        if changes:
            print(
                f"  ✅ {image_name}: {'+'.join(changes)} (ENTRYPOINT already present)"
            )
        else:
            print(f"  ✅ {image_name}: Already fixed")
        return True

    # 3. Get binary name and port
    binary, port = get_binary_and_port(image_name, content)

    # 4. Determine if this is a distroless/slim image (no shell)
    # Distroless images can't use "shim run -c <binary>" because shim
    # needs to fork/exec. For distroless, we need to use the shim differently.
    # For now, assume all stubs have shells (they're FROM upstream images with shells)

    # 5. Fix FROM line to pin version
    upstream = UPSTREAM_VERSIONS.get(image_name, "")

    if upstream:
        # Replace bare FROM lines with versioned ones
        # Pattern: FROM <image> or FROM <image>:latest
        base_image = upstream.split(":")[0]
        content = re.sub(
            rf"FROM {re.escape(base_image)}(?::latest)?\s*$",
            f"FROM {upstream}",
            content,
            flags=re.MULTILINE,
        )
        changes.append(f"FROM={upstream}")

    # 6. Add ENTRYPOINT
    # For repack images (FROM upstream + COPY shim), the shim should wrap the original binary
    entrypoint = f"""
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/{binary}"]
"""
    content += entrypoint
    changes.append("ENTRYPOINT")

    # 7. Add USER if not present
    if "USER " not in content or content.count("USER ") == 0:
        content += "\nUSER 65532:65532\n"
        changes.append("USER=65532")

    # 8. Add OCI labels if missing
    if "org.opencontainers.image.title" not in content:
        labels = f'''
LABEL org.opencontainers.image.title="{image_name}" \\
      evergreen.image.tier="2"
'''
        content += labels
        changes.append("LABELS")

    if not dry_run:
        dockerfile_path.write_text(content)

    print(f"  ✅ {image_name}: {' + '.join(changes)}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Fix EIR stub Dockerfiles")
    parser.add_argument("--image", help="Fix a single image")
    parser.add_argument("--batch", help="Comma-separated list of images")
    parser.add_argument(
        "--all-sis", action="store_true", help="Fix all SIS-critical images"
    )
    parser.add_argument("--dry-run", action="store_true", help="Don't write changes")
    args = parser.parse_args()

    if args.image:
        images = [args.image]
    elif args.batch:
        images = args.batch.split(",")
    elif args.all_sis:
        images = SIS_CRITICAL
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Fixing {len(images)} images...\n")

    fixed = 0
    skipped = 0
    for img in images:
        img = img.strip()
        if not img:
            continue
        if fix_dockerfile(img, args.dry_run):
            fixed += 1
        else:
            skipped += 1

    print(f"\nDone: {fixed} fixed, {skipped} skipped")


if __name__ == "__main__":
    main()
