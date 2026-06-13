#!/usr/bin/env python3
"""Add ca-certificates to wolfi-based Dockerfiles that are missing it."""

import logging
import os
import re

logger = logging.getLogger(__name__)

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

STATIC_IMAGES = {"alpine-static", "musl", "x86_64-unknown-linux-musl"}

IMAGES_TO_CHECK = [
    "alpine-static",
    "courier-authlib",
    "courier-imap",
    "dovecot",
    "musl",
    "openvpn",
    "postfix",
    "postgrey",
    "rspamd",
    "scratch",
    "spamassassin",
    "standard",
    "upstream",
    "x86_64-unknown-linux-musl",
]


def find_final_stage_start(lines):
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("FROM "):
            has_alias = re.match(r"^FROM\s+\S+\s+AS\s+\S+", stripped, re.IGNORECASE)
            if not has_alias:
                return i
    return None


def has_ca_certificates(lines, final_start):
    for i in range(final_start, len(lines)):
        if re.search(r"\bca-certificates\b", lines[i]):
            return True
    return False


def is_wolfi_base(lines, final_start):
    from_line = lines[final_start].strip()
    return "wolfi" in from_line or "chainguard" in from_line


def find_apk_add_in_final_stage(lines, final_start):
    for i in range(final_start, len(lines)):
        if re.search(r"apk\s+add\s+--no-cache", lines[i]):
            return i
    return None


def insert_apk_add_after_from(lines, final_start):
    insert_idx = final_start + 1
    while insert_idx < len(lines) and lines[insert_idx].strip() == "":
        insert_idx += 1
    new_line = "RUN apk add --no-cache ca-certificates\n"
    lines.insert(insert_idx, new_line)
    return lines


def add_ca_certs_to_apk_line(lines, apk_idx):
    line = lines[apk_idx]
    line = re.sub(
        r"(apk\s+add\s+--no-cache\s+)",
        r"\1ca-certificates ",
        line,
    )
    lines[apk_idx] = line
    return lines


def process_image(image_name):
    dockerfile_path = os.path.join(IMAGES_DIR, image_name, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        logger.info(f"SKIP (no Dockerfile): {image_name}")
        return

    with open(dockerfile_path) as f:
        lines = f.readlines()

    final_start = find_final_stage_start(lines)
    if final_start is None:
        logger.info(f"SKIP (no final FROM): {image_name}")
        return

    if not is_wolfi_base(lines, final_start):
        logger.info(f"SKIP (not wolfi/chainguard base): {image_name}")
        return

    if has_ca_certificates(lines, final_start):
        logger.info(f"SKIP (already has ca-certificates): {image_name}")
        return

    if image_name in STATIC_IMAGES:
        logger.info(f"SKIP (static image): {image_name}")
        return

    apk_idx = find_apk_add_in_final_stage(lines, final_start)

    if apk_idx is not None:
        lines = add_ca_certs_to_apk_line(lines, apk_idx)
        logger.info(f"MODIFIED (added to existing apk add): {image_name}")
    else:
        lines = insert_apk_add_after_from(lines, final_start)
        logger.info(f"MODIFIED (inserted new apk add line): {image_name}")

    with open(dockerfile_path, "w") as f:
        f.writelines(lines)


def main():
    logger.info("=== Adding ca-certificates to wolfi Dockerfiles ===")
    for image_name in IMAGES_TO_CHECK:
        process_image(image_name)
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
