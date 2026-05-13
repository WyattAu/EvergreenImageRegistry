#!/usr/bin/env python3
"""
Mark broken/deprecated images with the evergreen.image.status=deprecated label.

Reads known-broken images from the wolfi_invalid_packages.json report and
permanently broken upstream images list. Adds the deprecated OCI label to
affected Dockerfiles if not already present.
"""

import json
from pathlib import Path

IMAGES_DIR = Path("images")
DEPRECATED_LABEL = 'LABEL org.opencontainers.image.status="deprecated"'

# Known permanently broken upstreams (deleted, no longer maintained)
PERMANENTLY_BROKEN = {
    "couchdb",
    "couchdb-sync",  # Erlang package incompatibility with wolfi
    "rabbitmq-amqp",
    "rabbitmq-delayed",
    "rabbitmq-federation",
    "rabbitmq-management",
    "rabbitmq-mqtt",
    "rabbitmq-stomp",
    "cockpit",  # Package not available in wolfi
    "dovecot",
    "dovecot-lda",
    "dovecot-pop3",  # Not in wolfi
    "courier-authlib",
    "courier-imap",  # Not in wolfi
    "collabora-online",
    "collabora-online-code",  # apt-transport-https dep
    "onlyoffice-communityserver",
    "onlyoffice-controlpanel",
    "onlyoffice-documentserver",
    "onlyoffice-documentserver-ee",
    "rethinkdb",  # Already deprecated
    "orientdb",  # Already deprecated
    "graphdb-free",  # Already deprecated
    "nxlog",  # Already deprecated
}


def is_already_deprecated(dockerfile_path: Path) -> bool:
    """Check if Dockerfile already has deprecated status label."""
    content = dockerfile_path.read_text()
    return 'image.status="deprecated"' in content


def mark_deprecated(dockerfile_path: Path) -> bool:
    """Add deprecated label to Dockerfile if not present."""
    if is_already_deprecated(dockerfile_path):
        return False

    content = dockerfile_path.read_text()
    lines = content.split("\n")

    # Find the last LABEL line to add after it
    last_label_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("LABEL org.opencontainers.image."):
            last_label_idx = i

    if last_label_idx >= 0:
        lines.insert(last_label_idx + 1, DEPRECATED_LABEL)
    else:
        # Insert before ENTRYPOINT or CMD
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if line.strip().startswith("ENTRYPOINT") or line.strip().startswith("CMD"):
                insert_idx = i
                break
        lines.insert(insert_idx, DEPRECATED_LABEL)

    dockerfile_path.write_text("\n".join(lines))
    return True


def main():
    report_path = Path(".reports/wolfi_invalid_packages.json")
    if report_path.exists():
        with open(report_path) as f:
            data = json.load(f)
        invalid = data.get("invalid_packages", {})
        # Extract all affected images from invalid packages
        for images in invalid.values():
            PERMANENTLY_BROKEN.update(images)

    marked = 0
    already = 0
    missing = 0

    for image_name in sorted(PERMANENTLY_BROKEN):
        dockerfile = IMAGES_DIR / image_name / "Dockerfile"
        if not dockerfile.exists():
            missing += 1
            continue
        if is_already_deprecated(dockerfile):
            already += 1
            continue
        if mark_deprecated(dockerfile):
            print(f"  DEPRECATED: {image_name}")
            marked += 1

    print(
        f"\nSummary: {marked} marked, {already} already deprecated, {missing} missing Dockerfiles"
    )
    print(f"Total affected: {len(PERMANENTLY_BROKEN)}")


if __name__ == "__main__":
    main()
