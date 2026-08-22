#!/usr/bin/env python3
"""
Migration script: debian-slim → wolfi/UBI for Evergreen Image Registry
Migrates final-stage base images per ADR-007 universal preference order.

Usage:
    python3 migrate_debian_to_wolfi.py [--dry-run] [--verbose]

Patterns handled:
    1. copy_binary_only: FROM debian-slim → FROM scratch
    2. install_packages: FROM debian-slim → FROM wolfi, apt-get → apk
    3. UID 65534 → 65532
    4. Add evergreen labels
    5. Add EXPOSE 9101, STOPSIGNAL SIGTERM
"""

import argparse
import glob
import logging
import os
import re

logger = logging.getLogger(__name__)

# Package mapping: Debian → wolfi (apk)
# Only packages commonly available in wolfi are mapped
PACKAGE_MAP = {
    "ca-certificates": "ca-certificates",
    "curl": "curl",
    "wget": "wget",
    "git": "git",
    "gnupg2": "gnupg",
    "gnupg": "gnupg",
    "python3": "python3",
    "python3-pip": "py3-pip",
    "python3-venv": "python3",
    "nodejs": "nodejs",
    "npm": "npm",
    "yarn": "yarn",
    "openjdk-17-jre-headless": "java-17-runtime",
    "openjdk-11-jre-headless": "java-11-runtime",
    "default-jdk-headless": "java-17",
    "default-jre-headless": "java-17-runtime",
    "sqlite3": "sqlite-libs",
    "libssl3": "openssl-libs",
    "libssl-dev": "openssl-dev",
    "postgresql-client": "postgresql-client",
    "redis": "redis",
    "rabbitmq-server": "rabbitmq-server",
    "fluent-bit": "fluent-bit",
    "mosquitto": "mosquitto",
    "nginx": "nginx",
    "apache2": "apache2",
    "ffmpeg": "ffmpeg",
    "jq": "jq",
    "unzip": "unzip",
    "zip": "zip",
    "tar": "tar",
    "bash": "bash",
    "libpq-dev": "postgresql-dev",
    "libpq5": "postgresql-libs",
    "postgresql-client-16": "postgresql-client",
    "libcurl4": "curl",
    "libxml2": "libxml2",
    "libxslt1.1": "libxslt",
    "openssh-client": "openssh-client",
    "openssh-server": "openssh-server",
    "supervisor": "supervisor",
    "tini": "tini",  # Won't be used (runtime --init) but keep mapping
    "socat": "socat",
    "netcat-openbsd": "netcat-openbsd",
    "procps": "procps",
    "util-linux": "util-linux",
    "coreutils": "coreutils",
    "findutils": "findutils",
    "grep": "grep",
    "sed": "sed",
    "awk": "gawk",
    "cron": "busybox",
    "logrotate": "logrotate",
    "gpg": "gnupg",
    "dirmngr": "gnupg",
    "apt-transport-https": None,  # Not needed in wolfi
    "software-properties-common": None,  # Not needed in wolfi
    "dbus": "dbus",
    "fontconfig": "fontconfig",
    "fonts-dejavu-core": "font-dejavu",
    "libfontconfig1": "fontconfig",
    "libfreetype6": "freetype",
    "libglib2.0-0": "glib",
    "libjpeg62-turbo": "libjpeg-turbo",
    "libpng16-16": "libpng",
    "libstdc++6": "libstdc++",
    "zlib1g": "zlib",
    "libffi-dev": "libffi-dev",
    "libffi7": "libffi",
    "make": "make",
    "cmake": "cmake",
    "gcc": "gcc",
    "g++": "g++",
    "build-essential": "build-base",
    "pkg-config": "pkgconf",
    "libgeos-dev": "geos-dev",
    "libgdal-dev": "gdal-dev",
    "libxml2-dev": "libxml2-dev",
    "libxslt1-dev": "libxslt-dev",
    "libldap-2.5-0": "openldap-libs",
    "libsasl2-2": "cyrus-sasl",
    "libexpat1": "expat",
    "libuuid1": "util-linux-libs",
    "uuid-runtime": "util-linux",
}

# Packages that indicate UBI is needed (not available in wolfi)
UBI_ONLY_PACKAGES = {
    "slapd",
    "ldap-utils",  # OpenLDAP server
    "postfix",  # Mail server
    "courier-authlib",  # Mail
    "courier-imap",  # Mail
    "dovecot-core",  # Mail
    "dovecot-imapd",  # Mail
    "dovecot-pop3d",  # Mail
    "dovecot-lmtpd",  # Mail
    "fail2ban",  # Security
    "qbittorrent-nox",  # Torrent
    "transmission-daemon",  # Torrent
    "pdns-server",  # DNS
    "pdns-recursor",  # DNS
    "pgbouncer",  # PostgreSQL pooler
    "pgpool2",  # PostgreSQL pooler
    "elasticsearch",  # Search engine
    "opensearch-dashboards",  # Search UI
    "neo4j",  # Graph database
    "php-fpm",  # PHP (need to check wolfi php naming)
    "php-cli",  # PHP
    "php-mbstring",  # PHP extension
    "php-xml",  # PHP extension
    "php-curl",  # PHP extension
    "php-intl",  # PHP extension
    "php-zip",  # PHP extension
    "libapache2-mod-security2",  # Apache module
}

# wolfi-specific PHP packages
PHP_MAP = {
    "php-fpm": "php84-fpm",
    "php-cli": "php84",
    "php-mbstring": "php84-mbstring",
    "php-xml": "php84-xml",
    "php-curl": "php84-curl",
    "php-intl": "php84-intl",
    "php-zip": "php84-zip",
    "php-gd": "php84-gd",
    "php-mysql": "php84-mysql",
    "php-pgsql": "php84-pgsql",
    "php-redis": "php84-redis",
    "php-opcache": "php84-opcache",
    "php-json": "php84-json",
    "php-apcu": "php84-apcu",
    "default-jdk-headless": "java-17",
}

# Merge PHP map into main map
PACKAGE_MAP.update(PHP_MAP)

# Remove UBI-only packages from UBI_ONLY if they have wolfi equivalents
for pkg in UBI_ONLY_PACKAGES:
    if pkg in PHP_MAP:
        UBI_ONLY_PACKAGES.discard(pkg)


class DockerfileMigrator:
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            "total": 0,
            "migrated_to_scratch": 0,
            "migrated_to_wolfi": 0,
            "migrated_to_ubi": 0,
            "skipped_no_debian": 0,
            "skipped_build_only": 0,
            "unmapped_packages": set(),
            "errors": [],
        }

    def migrate_all(self, images_dir="images"):
        dockerfiles = sorted(glob.glob(os.path.join(images_dir, "*/Dockerfile")))
        self.stats["total"] = len(dockerfiles)

        for df_path in dockerfiles:
            try:
                self.migrate_dockerfile(df_path)
            except Exception as e:
                self.stats["errors"].append((df_path, str(e)))
                if self.verbose:
                    logger.error(f"{df_path}: {e}")

        self.print_stats()

    def migrate_dockerfile(self, df_path):
        with open(df_path) as f:
            content = f.read()

        # Check if debian-slim is in final stage
        from_lines = re.findall(
            r"^FROM\s+(.+?)(?:\s+AS\s+\w+)?\s*$", content, re.MULTILINE
        )
        if not from_lines:
            self.stats["skipped_no_debian"] += 1
            return

        last_from = from_lines[-1].strip()
        if not re.search(
            r"debian.*slim|debian:bookworm-slim|debian:bullseye-slim|debian:buster-slim",
            last_from,
            re.IGNORECASE,
        ):
            self.stats["skipped_no_debian"] += 1
            return

        # Check if multi-stage and debian-slim is only in build stage
        if len(from_lines) > 1:
            non_final = from_lines[:-1]
            debian_in_build = any(
                re.search(r"debian.*slim", f, re.IGNORECASE) for f in non_final
            )
            debian_in_final = bool(re.search(r"debian.*slim", last_from, re.IGNORECASE))
            if not debian_in_final and debian_in_build:
                self.stats["skipped_build_only"] += 1
                return

        # Determine migration target
        target = self.determine_target(content, from_lines)

        # Apply migration
        new_content = self.apply_migration(content, from_lines, target, df_path)

        if new_content != content:
            if target == "scratch":
                self.stats["migrated_to_scratch"] += 1
            elif target in ("ubi-micro", "ubi-minimal"):
                self.stats["migrated_to_ubi"] += 1
            else:
                self.stats["migrated_to_wolfi"] += 1

            if self.dry_run:
                logger.info(f"WOULD MIGRATE: {df_path} → {target}")
            else:
                with open(df_path, "w") as f:
                    f.write(new_content)
                rel = os.path.relpath(df_path)
                logger.info(f"MIGRATED: {rel} → {target}")

    def determine_target(self, content, from_lines):
        """Determine the best target base image."""
        # Extract final stage
        if len(from_lines) > 1:
            stages = re.split(r"^FROM\s+", content, flags=re.MULTILINE)
            final_stage = stages[-1]
        else:
            final_stage = content

        # Check if it's a copy-binary-only pattern (no apt-get in final stage)
        has_apt_install = bool(re.search(r"apt-get\s+(?:install|run)", final_stage))
        has_copy_from = bool(re.search(r"COPY\s+--from=", final_stage))
        has_other_runs = bool(
            re.search(
                r"RUN\s+(?!apt-get|groupadd|useradd|usermod|adduser|addgroup|ln\s|chmod|chown|mkdir|mv|cp|rm|true)",
                final_stage,
            )
        )

        if not has_apt_install and has_copy_from and not has_other_runs:
            return "scratch"

        # Check for UBI-only packages
        apt_matches = re.findall(
            r"apt-get\s+install[^;\n]*?([a-zA-Z0-9][\w\-.=:]*)", final_stage
        )
        all_packages = []
        for match in apt_matches:
            all_packages.extend(p.strip() for p in re.split(r"\s+", match) if p.strip())

        for pkg in all_packages:
            clean_pkg = re.sub(r"=.*$", "", pkg).strip()
            if clean_pkg in UBI_ONLY_PACKAGES:
                return "ubi-minimal"

        return "wolfi"

    def map_packages(self, debian_pkgs):
        """Map Debian package names to wolfi equivalents."""
        wolfi_pkgs = []
        unmapped = []

        for pkg in debian_pkgs:
            clean = re.sub(r"=.*$", "", pkg).strip()
            # Remove version pins like =1.2.3
            clean = clean.split("=")[0].strip()
            # Remove architecture like :amd64
            clean = clean.split(":")[0].strip()

            if not clean or clean.startswith("-") or clean.startswith("$"):
                continue

            mapped = PACKAGE_MAP.get(clean)
            if mapped is None:
                unmapped.append(clean)
                # Keep the original package name — might work in wolfi
                wolfi_pkgs.append(clean)
            elif mapped is not None and mapped != "":
                wolfi_pkgs.append(mapped)

        return wolfi_pkgs, unmapped

    def apply_migration(self, content, from_lines, target, df_path):
        """Apply the migration transformations."""
        image_name = os.path.basename(os.path.dirname(df_path))

        # Determine if multi-stage
        is_multi = len(from_lines) > 1

        if is_multi:
            # Split content into stages
            stages = re.split(r"(^FROM\s+.+$)", content, flags=re.MULTILINE)
            # stages alternates: [before-first-FROM, FROM-line, stage-content, FROM-line, stage-content, ...]
            # Last stage needs migration
            new_stages = []
            i = 0
            while i < len(stages):
                if i == 0:
                    new_stages.append(stages[i])
                    i += 1
                    continue

                from_line = stages[i]
                stage_content = stages[i + 1] if i + 1 < len(stages) else ""

                is_last = i >= len(stages) - 2

                if is_last:
                    # Migrate this stage
                    from_line, stage_content = self.migrate_stage(
                        from_line, stage_content, target, image_name
                    )
                else:
                    # Build stage — leave debian-slim but add hadolint ignore
                    pass

                new_stages.append(from_line)
                new_stages.append(stage_content)
                i += 2

            return "".join(new_stages)
        else:
            # Single-stage: replace FROM line in content, then apply transformations
            old_from_line = from_lines[0]
            # migrate_stage transforms the stage content but also returns the new FROM
            new_from, transformed = self.migrate_stage(
                old_from_line, content, target, image_name, is_single=True
            )
            # Replace the full FROM line (with FROM prefix) in the content
            full_old_from = re.search(
                r"^FROM\s+" + re.escape(old_from_line.strip()) + r"\s*$",
                content,
                re.MULTILINE,
            )
            if full_old_from:
                content = (
                    content[: full_old_from.start()]
                    + new_from.rstrip("\n")
                    + content[full_old_from.end() :]
                )
            else:
                # Fallback: replace just the image name after FROM
                content = re.sub(
                    r"(FROM\s+)" + re.escape(old_from_line.strip()),
                    r"\1cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007",
                    transformed,
                    count=1,
                )
            return content

    def migrate_stage(
        self, from_line, stage_content, target, image_name, is_single=False
    ):
        """Migrate a single stage."""
        # Replace FROM line
        if target == "scratch":
            new_from = "FROM scratch\n"
        elif target == "wolfi":
            new_from = (
                "FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007\n"
            )
        elif target == "ubi-micro":
            new_from = "FROM registry.access.redhat.com/ubi9/ubi-micro:latest\n"
        elif target == "ubi-minimal":
            new_from = "FROM registry.access.redhat.com/ubi9/ubi-minimal:latest\n"
        else:
            new_from = from_line

        # Transform apt-get to apk (wolfi only)
        if target == "wolfi":
            stage_content = self.transform_apt_to_apk(stage_content)
        elif target == "ubi-minimal" or target == "ubi-micro":
            stage_content = self.transform_apt_to_dnf(stage_content)

        # Update UID 65534 → 65532
        stage_content = re.sub(
            r"\bUSER\s+65534(?::\s*65534)?", "USER 65532:65532", stage_content
        )
        stage_content = re.sub(
            r"\badduser\s+.*?--uid\s+65534",
            "adduser -D -u 65532 nonroot",
            stage_content,
        )
        stage_content = re.sub(
            r"\bgroupadd\s+.*?--gid\s+65534", "addgroup -g 65532 nonroot", stage_content
        )
        stage_content = re.sub(
            r"\buseradd\s+.*?--uid\s+65534",
            "adduser -D -u 65532 nonroot",
            stage_content,
        )
        stage_content = re.sub(
            r"\busermod\s+.*?--uid\s+65534", "usermod -u 65532 nonroot", stage_content
        )
        # Also update chown references
        stage_content = re.sub(
            r"--chown=65534:65534", "--chown=65532:65532", stage_content
        )
        stage_content = re.sub(
            r"chown\s+-R\s+65534:65534", "chown -R 65532:65532", stage_content
        )
        stage_content = re.sub(r"\b65534:65534\b", "65532:65532", stage_content)

        # Update existing labels
        stage_content = re.sub(
            r'(evergreen\.hft\.uid\s*=\s*")65534(")', r"\g<1>65532\2", stage_content
        )

        # Build append block with new labels and directives
        append_lines = []

        # Base image label
        if "evergreen.base.image" not in stage_content:
            append_lines.append(f'LABEL evergreen.base.image="{target}"')

        # Observability labels
        if "evergreen.metrics.native" not in stage_content:
            append_lines.append('LABEL evergreen.metrics.native="ztunnel"')
        if "evergreen.health.type" not in stage_content:
            append_lines.append('LABEL evergreen.health.type="exec"')

        # EXPOSE 9101
        if "9101" not in stage_content:
            append_lines.append("EXPOSE 9101")

        # STOPSIGNAL
        if "STOPSIGNAL" not in stage_content:
            append_lines.append("STOPSIGNAL SIGTERM")

        # Append to end of stage content
        if append_lines:
            # Ensure there's a newline before our additions
            stage_content = (
                stage_content.rstrip("\n") + "\n" + "\n".join(append_lines) + "\n"
            )

        return new_from, stage_content

    # Dockerfile instructions that start a new block
    DOCKERFILE_INSTRUCTIONS = re.compile(
        r"^\s*(FROM|COPY|ADD|RUN|CMD|ENTRYPOINT|ENV|ARG|LABEL|EXPOSE|"
        r"USER|WORKDIR|HEALTHCHECK|STOPSIGNAL|VOLUME|ONBUILD|"
        r"MAINTAINER|SHELL|AS)\b",
        re.MULTILINE,
    )

    def _extract_run_blocks(self, content):
        """Extract complete RUN blocks (handling \\ continuation lines)."""
        blocks = []
        lines = content.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if re.match(r"^\s*RUN\s+", line):
                block_lines = [line]
                # Collect continuation lines (ending with \)
                while i + 1 < len(lines) and lines[i + 1].rstrip().endswith("\\"):
                    i += 1
                    block_lines.append(lines[i])
                # The next line (if it exists) is the terminal line of the RUN block
                # ONLY if it's a continuation (indented) and not a new instruction
                if (
                    i + 1 < len(lines)
                    and lines[i + 1].strip()
                    and not self.DOCKERFILE_INSTRUCTIONS.match(lines[i + 1])
                    and lines[i + 1].startswith((" ", "\t"))
                ):
                    i += 1
                    block_lines.append(lines[i])
                blocks.append("\n".join(block_lines))
            i += 1
        return blocks

    def _replace_run_blocks(self, content, replace_fn):
        """Replace RUN blocks using a replacement function."""
        lines = content.split("\n")
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if re.match(r"^\s*RUN\s+", line):
                block_lines = [line]
                while i + 1 < len(lines) and lines[i + 1].rstrip().endswith("\\"):
                    i += 1
                    block_lines.append(lines[i])
                if (
                    i + 1 < len(lines)
                    and lines[i + 1].strip()
                    and not self.DOCKERFILE_INSTRUCTIONS.match(lines[i + 1])
                    and lines[i + 1].startswith((" ", "\t"))
                ):
                    i += 1
                    block_lines.append(lines[i])
                block = "\n".join(block_lines)
                new_block = replace_fn(block)
                result.append(new_block)
            else:
                result.append(line)
            i += 1
        return "\n".join(result)

    def _extract_packages_from_apt(self, apt_block):
        """Extract package names from an apt-get install RUN block."""
        # Flatten continuation lines
        flat = apt_block.replace("\\\n", " ").replace("\\", " ")

        # Find the install command and get everything after it
        m = re.search(
            r"apt-get\s+install\s+(?:--no-install-recommends\s+)?(?:-y\s+)?(.+)", flat
        )
        if not m:
            return []

        pkg_str = m.group(1)
        # Stop at && that starts a non-package command
        # Keep only the part that contains package names
        pkg_str = re.sub(
            r"\s*&&\s*(rm|apt-get|dpkg|update-ca-certificates|groupadd|useradd|ln|chmod|chown|mkdir).*$",
            "",
            pkg_str,
            flags=re.DOTALL,
        )
        pkg_str = re.sub(r"\s*\|\|\s*true\s*$", "", pkg_str)

        packages = []
        for token in re.split(r"\s+", pkg_str):
            token = token.strip().rstrip(",")
            if (
                token
                and not token.startswith("#")
                and not token.startswith("-")
                and not token.startswith("$")
            ):
                # Clean version pins
                token = re.sub(r"=.*$", "", token)
                token = token.split(":")[0]
                # Filter out obvious non-package tokens
                if not token or len(token) < 2:
                    continue
                if token in (
                    "apt-get",
                    "dpkg",
                    "apt",
                    "true",
                    "dev/null",
                    "bookworm",
                    "buster",
                    "bullseye",
                    "sid",
                    "testing",
                    "stable",
                    "auto-remove",
                    "no-install-recommends",
                    "yes",
                ):
                    continue
                if not re.match(r"^[a-z][a-z0-9]", token):
                    continue
                packages.append(token)
        return packages

    def transform_apt_to_apk(self, content):
        """Transform apt-get commands to apk equivalents."""

        def replace_apt_block(block):
            if "apt-get" not in block:
                return block

            # Skip blocks that are only apt-get update (no install)
            if "apt-get install" not in block and "apt-get update" in block:
                return None  # Signal to remove this block

            if "apt-get install" not in block:
                return block

            packages = self._extract_packages_from_apt(block)
            wolfi_pkgs, unmapped = self.map_packages(packages)

            for u in unmapped:
                self.stats["unmapped_packages"].add(u)

            if not wolfi_pkgs:
                return None  # Remove block

            # Remove duplicates
            seen = set()
            unique = []
            for p in wolfi_pkgs:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)

            return f"RUN apk add --no-cache {' '.join(unique)}"

        def block_replacer(block):
            result = replace_apt_block(block)
            if result is None:
                return ""  # Remove block entirely
            return result

        content = self._replace_run_blocks(content, block_replacer)

        # Clean up blank lines left by removed blocks
        content = re.sub(r"\n{3,}", "\n\n", content)

        # Replace Debian-specific paths
        content = content.replace("/usr/lib/x86_64-linux-gnu/", "/usr/lib/")

        return content

    def transform_apt_to_dnf(self, content):
        """Transform apt-get commands to dnf equivalents for UBI."""
        ubi_map = {
            "ca-certificates": "ca-certificates",
            "python3-pip": "python3-pip",
            "python3-venv": "python3",
            "libpq-dev": "libpq-devel",
            "libpq5": "libpq",
            "libssl-dev": "openssl-devel",
            "libssl3": "openssl-libs",
            "libcurl4": "libcurl",
            "libxml2-dev": "libxml2-devel",
            "libxslt1-dev": "libxslt-devel",
            "build-essential": "gcc make",
            "nodejs": "nodejs",
            "npm": "npm",
            "curl": "curl",
            "wget": "wget",
            "git": "git",
            "gnupg2": "gnupg2",
            "jq": "jq",
            "sqlite3": "sqlite",
        }

        def replace_apt_block(block):
            if "apt-get" not in block:
                return block
            if "apt-get install" not in block and "apt-get update" in block:
                return None
            if "apt-get install" not in block:
                return block

            packages = self._extract_packages_from_apt(block)
            mapped = []
            for pkg in packages:
                clean = re.sub(r"=.*$", "", pkg).strip().split(":")[0]
                mapped.append(ubi_map.get(clean, clean))

            if not mapped:
                return None

            seen = set()
            unique = []
            for p in mapped:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)

            return f"RUN microdnf install -y {' '.join(unique)} && microdnf clean all"

        def block_replacer(block):
            result = replace_apt_block(block)
            if result is None:
                return ""
            return result

        content = self._replace_run_blocks(content, block_replacer)
        content = re.sub(r"\n{3,}", "\n\n", content)
        return content

    def print_stats(self):
        print(f"\n{'=' * 60}")
        print("MIGRATION STATISTICS")
        print(f"{'=' * 60}")
        print(f"  Total Dockerfiles scanned:    {self.stats['total']}")
        print(f"  Migrated to scratch:          {self.stats['migrated_to_scratch']}")
        print(f"  Migrated to wolfi:            {self.stats['migrated_to_wolfi']}")
        print(f"  Migrated to UBI:              {self.stats['migrated_to_ubi']}")
        print(f"  Skipped (no debian-slim):     {self.stats['skipped_no_debian']}")
        print(f"  Skipped (build-stage only):   {self.stats['skipped_build_only']}")
        print(f"  Unmapped packages:            {len(self.stats['unmapped_packages'])}")
        print(f"  Errors:                       {len(self.stats['errors'])}")

        if self.stats["unmapped_packages"]:
            print("\n  Unmapped packages (may need manual review):")
            for pkg in sorted(self.stats["unmapped_packages"]):
                print(f"    - {pkg}")

        if self.stats["errors"]:
            print("\n  Errors:")
            for path, err in self.stats["errors"][:20]:
                print(f"    - {path}: {err}")
            if len(self.stats["errors"]) > 20:
                print(f"    ... and {len(self.stats['errors']) - 20} more")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migrate debian-slim Dockerfiles to wolfi/UBI"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    migrator = DockerfileMigrator(dry_run=args.dry_run, verbose=args.verbose)
    migrator.migrate_all()
