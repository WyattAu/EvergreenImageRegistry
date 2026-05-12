#!/usr/bin/env python3
"""Fix Dockerfiles where apt-get commands appear in the final (wolfi) stage.

wolfi uses apk, not apt-get. This script converts apt-get RUN blocks to apk add
in the final stage of each Dockerfile.

Usage:
    python3 scripts/fix_apt_in_wolfi.py --dry-run
    python3 scripts/fix_apt_in_wolfi.py --apply
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

APT_TO_APK = {
    "ca-certificates": "ca-certificates",
    "curl": "curl",
    "wget": "wget",
    "git": "git",
    "bash": "bash",
    "make": "make",
    "python3": "python3",
    "python3-pip": "py3-pip",
    "py3-pip": "py3-pip",
    "python3-dev": "python3-dev",
    "nodejs": "nodejs",
    "npm": "npm",
    "ruby": "ruby",
    "ruby-dev": "ruby-dev",
    "openssl": "openssl",
    "libssl-dev": "openssl-dev",
    "openssl-dev": "openssl-dev",
    "libffi-dev": "libffi-dev",
    "gcc": "build-base",
    "g++": "build-base",
    "build-base": "build-base",
    "build-essential": "build-base",
    "libxml2-dev": "libxml2-dev",
    "libxslt1-dev": "libxslt-dev",
    "libxslt-dev": "libxslt-dev",
    "zlib1g-dev": "zlib-dev",
    "zlib-dev": "zlib-dev",
    "libjpeg-dev": "libjpeg-turbo-dev",
    "libpng-dev": "libpng-dev",
    "openssh-client": "openssh-client",
    "openssh-server": "openssh-server",
    "sqlite3": "sqlite-libs",
    "sqlite-libs": "sqlite-libs",
    "libsqlite3-dev": "sqlite-dev",
    "sqlite-dev": "sqlite-dev",
    "libpq-dev": "postgresql-dev",
    "postgresql-dev": "postgresql-dev",
    "postgresql-client": "postgresql-client",
    "netcat-openbsd": "netcat-openbsd",
    "unzip": "unzip",
    "zip": "zip",
    "tar": "tar",
    "gnupg": "gnupg",
    "apache2": "apache2",
    "nginx": "nginx",
    "php-fpm": "php84-fpm",
    "php-cli": "php84",
    "php84-fpm": "php84-fpm",
    "php84": "php84",
    "java-runtime": "java-17-runtime",
    "java-17": "java-17-runtime",
    "default-jre": "temurin-17-jre",
    "cron": "busybox-suid",
    "logrotate": "logrotate",
    "rsync": "rsync",
    "socat": "socat",
    "jq": "jq",
    "yq": "yq",
    "fontconfig": "fontconfig",
    "fonts-liberation": "font-liberation",
    "libglib2.0-0": "glib",
    "py3-lxml": "py3-lxml",
    "libcurl4-openssl-dev": "curl-openssl-dev",
    "ffmpeg": "ffmpeg",
    "tzdata": "tzdata",
    "dumb-init": "dumb-init",
    "xdg-utils": "xdg-utils",
    "libyaml-dev": "yaml-dev",
    "libgeos-dev": "geos",
    "libgd-dev": "gd-dev",
    "libmemcached-dev": "libmemcached-dev",
    "pkg-config": "pkgconf",
    "pkgconf": "pkgconf",
}

IMAGES_ROOT = Path(__file__).resolve().parent.parent / "images"


@dataclass
class ConversionResult:
    path: str
    status: str  # "converted", "partial", "skipped", "removed"
    details: str = ""
    original_lines: list = field(default_factory=list)
    new_lines: list = field(default_factory=list)


def find_last_from_line(lines: list[str]) -> int:
    last_from = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^FROM\s", stripped, re.IGNORECASE):
            last_from = i
    return last_from


def extract_run_block(lines: list[str], start: int) -> tuple[int, str]:
    """Extract a multi-line RUN block starting at `start`. Returns (end_line_exclusive, full_text)."""
    parts = [lines[start]]
    i = start + 1
    while i < len(lines) and lines[i - 1].rstrip().endswith("\\"):
        parts.append(lines[i])
        i += 1
    return i, "".join(parts)


def find_all_apt_run_blocks(lines: list[str], from_line: int) -> list[tuple[int, int]]:
    """Find all RUN blocks containing apt-get after from_line. Returns list of (start, end_exclusive)."""
    blocks = []
    i = from_line + 1
    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r"^RUN\s", stripped, re.IGNORECASE):
            end, text = extract_run_block(lines, i)
            if "apt-get" in text:
                blocks.append((i, end))
            i = end
        else:
            i += 1
    return blocks


def classify_complexity(run_text: str) -> str:
    """Classify how complex an apt-get RUN block is."""
    has_gpg = bool(re.search(r"gnupg|gpg.*--dearmor|apt-key", run_text))
    has_repo_add = bool(
        re.search(r"echo.*deb\s+.*>.*sources\.list|add-apt-repository", run_text)
    )
    has_purge = "apt-get purge" in run_text or "apt-get autoremove" in run_text
    has_multiple_updates = run_text.count("apt-get update") > 1
    has_custom_repo = has_gpg and has_repo_add
    has_build_from_source = bool(
        re.search(
            r"\b(make|cmake|configure|gcc|g\+\+)\b.*\b(install|make install)\b",
            run_text,
        )
    )

    if has_custom_repo or has_multiple_updates:
        return "complex_repo"
    if has_build_from_source and has_purge:
        return "complex_build"
    if has_purge:
        return "purge_pattern"
    return "simple"


def extract_apt_packages(run_text: str) -> list[str]:
    """Extract package names from apt-get install commands in the RUN block text."""
    packages = []
    for m in re.finditer(
        r"apt-get\s+install\s+(?:-y\s+)?(?:--no-install-recommends\s+)?(.+?)(?=\s*&&|;|\nRUN|\Z)",
        run_text,
        re.DOTALL,
    ):
        pkg_str = m.group(1)
        pkg_str = re.sub(r"#.*$", "", pkg_str, flags=re.MULTILINE)
        pkg_str = re.sub(r"\\", " ", pkg_str)
        pkg_str = re.sub(r"\s+", " ", pkg_str).strip()
        for p in pkg_str.split():
            p = p.strip()
            if not p:
                continue
            if p.startswith("-") or p.startswith("$"):
                continue
            if re.match(r"^(rm|apt-get|&&|;|\|)", p):
                continue
            if "/" in p or "*" in p:
                continue
            if re.match(r"^\d", p):
                continue
            packages.append(p)
    return packages


def extract_non_apt_commands(run_text: str) -> list[str]:
    """Extract non-apt-get commands from a RUN block (pip, npm, useradd, etc)."""
    commands = []
    for part in re.split(r"\s*&&\s*", run_text):
        part = part.strip().strip("\\").strip()
        if not part:
            continue
        if "apt-get" in part:
            continue
        if re.match(r"rm\s+-rf\s+/var/(lib|cache)/apt", part):
            continue
        if re.search(r"/var/(lib|cache)/apt", part):
            continue
        if re.match(r"apt-get\s+(clean|autoremove|purge)", part):
            continue
        if part.startswith("RUN "):
            part = part[4:].strip()
        part = re.sub(r"\s+", " ", part).strip()
        if part:
            commands.append(part)
    return commands


def convert_packages(packages: list[str]) -> tuple[list[str], list[str]]:
    """Convert apt packages to apk packages. Returns (apk_packages, unknown_packages)."""
    apk_pkgs = []
    seen = set()
    unknown = []
    for p in packages:
        if p in APT_TO_APK:
            apk = APT_TO_APK[p]
            if apk not in seen:
                apk_pkgs.append(apk)
                seen.add(apk)
        elif p in seen:
            continue
        else:
            unknown.append(p)
    return apk_pkgs, unknown


def needs_break_system_packages(cmd: str) -> str:
    """Add --break-system-packages to pip install if missing."""
    if re.search(r"\bpip3?\s+install\b", cmd) and "--break-system-packages" not in cmd:
        cmd = re.sub(r"(pip3?\s+install)", r"\1 --break-system-packages", cmd)
    return cmd


def process_dockerfile(path: str) -> ConversionResult:
    with open(path) as f:
        lines = f.readlines()

    last_from = find_last_from_line(lines)
    if last_from < 0:
        return ConversionResult(path, "skipped", "No FROM line found")

    blocks = find_all_apt_run_blocks(lines, last_from)
    if not blocks:
        return ConversionResult(path, "skipped", "No apt-get in final stage")

    if len(blocks) > 1:
        complexity = "multiple_blocks"
    else:
        _, text = extract_run_block(lines, blocks[0][0])
        complexity = classify_complexity(text)

    if complexity == "complex_repo":
        return ConversionResult(
            path,
            "skipped",
            "Complex: adds custom GPG key + apt repo (needs manual conversion)",
        )

    if complexity == "multiple_blocks":
        return ConversionResult(
            path, "skipped", "Multiple apt-get RUN blocks (needs manual review)"
        )

    start, end = blocks[0]
    _, run_text = extract_run_block(lines, start)
    original_block = lines[start:end]

    apt_packages = extract_apt_packages(run_text)
    apk_packages, unknown_packages = convert_packages(apt_packages)
    non_apt_commands = extract_non_apt_commands(run_text)

    result = ConversionResult(path, "", "")
    result.original_lines = original_block

    if not apk_packages and not non_apt_commands:
        result.status = "removed"
        result.details = f"All packages unknown/unneeded: {unknown_packages}"
        result.new_lines = []
        return result

    new_run_parts = []

    if apk_packages:
        new_run_parts.append(f"RUN apk add --no-cache {' '.join(apk_packages)}")

    for cmd in non_apt_commands:
        cmd = needs_break_system_packages(cmd)
        new_run_parts.append(f"RUN {cmd}")

    if unknown_packages:
        result.status = "partial"
        result.details = (
            f"Converted {apk_packages}, removed unknown: {unknown_packages}"
        )
    else:
        result.status = "converted"
        result.details = f"Converted to: apk add --no-cache {' '.join(apk_packages)}"
        if non_apt_commands:
            result.details += f" + {len(non_apt_commands)} other commands"

    result.new_lines = [line + "\n" for line in new_run_parts]
    return result


def apply_conversion(path: str, result: ConversionResult):
    with open(path) as f:
        lines = f.readlines()

    last_from = find_last_from_line(lines)
    blocks = find_all_apt_run_blocks(lines, last_from)
    if not blocks:
        return

    start, end = blocks[0]
    if result.status == "removed":
        lines[start:end] = []
    else:
        lines[start:end] = result.new_lines

    with open(path, "w") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(description="Fix apt-get in wolfi Dockerfiles")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would change without applying"
    )
    parser.add_argument("--apply", action="store_true", help="Apply the changes")
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        parser.print_help()
        sys.exit(1)

    dockerfiles = sorted(IMAGES_ROOT.glob("*/Dockerfile"))
    results = []

    for df in dockerfiles:
        result = process_dockerfile(str(df))
        if result.status and result.status != "skipped":
            results.append(result)

    converted = [r for r in results if r.status == "converted"]
    partial = [r for r in results if r.status == "partial"]
    removed = [r for r in results if r.status == "removed"]
    skipped = [r for r in results if r.status == "skipped"]

    print(f"\n{'=' * 80}")
    print("DRY RUN: apt-get to apk conversion for wolfi Dockerfiles")
    print(f"{'=' * 80}")
    print(f"Total with apt-get in final stage: {len(results)}")
    print(f"  Successfully converted:  {len(converted)}")
    print(f"  Partially converted:    {len(partial)}")
    print(f"  Removed (empty blocks): {len(removed)}")
    print(f"  Skipped (too complex):   {len(skipped)}")
    print()

    if converted:
        print(f"--- CONVERTED ({len(converted)}) ---")
        for r in converted[:10]:
            print(f"  {r.path}")
            print(f"    -> {r.details}")
        if len(converted) > 10:
            print(f"  ... and {len(converted) - 10} more")

    if partial:
        print(f"\n--- PARTIALLY CONVERTED ({len(partial)}) ---")
        for r in partial[:10]:
            print(f"  {r.path}")
            print(f"    -> {r.details}")
        if len(partial) > 10:
            print(f"  ... and {len(partial) - 10} more")

    if removed:
        print(f"\n--- REMOVED ({len(removed)}) ---")
        for r in removed:
            print(f"  {r.path}")
            print(f"    -> {r.details}")

    if skipped:
        print(f"\n--- SKIPPED ({len(skipped)}) ---")
        for r in skipped:
            print(f"  {r.path}")
            print(f"    -> {r.details}")

    print(f"\n{'=' * 80}")
    print("EXAMPLE CONVERSIONS (before -> after):")
    print(f"{'=' * 80}")
    for r in (converted + partial)[:5]:
        print(f"\n--- {r.path} ---")
        orig = "".join(r.original_lines).strip()
        new = "".join(r.new_lines).strip() if r.new_lines else "(removed)"
        print(f"  BEFORE: {orig}")
        print(f"  AFTER:  {new}")

    if args.apply:
        print(f"\n{'=' * 80}")
        print("APPLYING CHANGES...")
        print(f"{'=' * 80}")
        for r in results:
            if r.status in ("converted", "partial", "removed"):
                apply_conversion(r.path, r)
                print(f"  [OK] {r.path} ({r.status})")
        print(f"\nDone. Modified {len(converted) + len(partial) + len(removed)} files.")
    elif args.dry_run:
        print(f"\n{'=' * 80}")
        print("DRY RUN - no files were modified. Use --apply to make changes.")
        print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
