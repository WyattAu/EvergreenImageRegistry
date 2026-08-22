#!/usr/bin/env python3
"""Audit all `apk add` package names in Dockerfiles against wolfi's actual package index."""

import io
import json
import logging
import os
import re
import sys
import tarfile
import urllib.request
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / ".reports"
IMAGES_DIR = PROJECT_ROOT / "images"

APKINDEX_URL = "https://packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz"

SHELL_OPERATORS = {
    "&&",
    "||",
    "2>/dev/null",
    "2>&1",
    ">/dev/null",
    "1>/dev/null",
    "true",
    "false",
    "echo",
    "head",
    "ls",
    "grep",
    "cat",
    "xargs",
    "sha256sum",
    "squeeze",
    "main",
    "install",
    "sed",
    "awk",
    "find",
    "mkdir",
    "chmod",
    "chown",
    "rm",
    "cp",
    "mv",
    "strip",
    "ln",
    "cd",
    "test",
    "set",
    "export",
    "printf",
    "sort",
    "uniq",
    "wc",
    "cut",
    "tr",
    "tee",
    "touch",
    "make",
    "tar",
    "curl",
    "wget",
    "pip",
    "gem",
    "npm",
    "cargo",
    "rustc",
    "gcc",
    "g++",
    "cc",
    "cmake",
    "pkg-config",
    "pkgconf",
    "git",
    "git-core",
    "update-ca-certificates",
    "groupadd",
    "useradd",
    "adduser",
    "addgroup",
    "setcap",
    "scrape",
    "scanelf",
    "readelf",
    "objdump",
    "busybox",
    "sh",
    "bash",
    "ash",
    "dash",
}

DEBIAN_LIB_PATTERN = re.compile(r"^(lib\w+\d+(?:t64)?(?:-\d+(?:\.\d+)*)?(?:-\w+)*)$")

VERSIONED_PACKAGE_PATTERN = re.compile(r"^(.*?)[-_]\d+\.\d+")


def download_apkindex():
    logger.info(f"Downloading wolfi APKINDEX from {APKINDEX_URL} ...")
    req = urllib.request.Request(APKINDEX_URL)
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    return data


def parse_apkindex(data):
    logger.info("Parsing APKINDEX ...")
    packages = set()
    provides = set()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for member in tf.getmembers():
            if os.path.basename(member.name) == "APKINDEX":
                f = tf.extractfile(member)
                if f is None:
                    continue
                content = f.read().decode("utf-8", errors="replace")
                for block in content.split("\n\n"):
                    for line in block.strip().splitlines():
                        if line.startswith("P:"):
                            pkg_name = line[2:].strip()
                            if pkg_name:
                                packages.add(pkg_name)
                        elif line.startswith("p:"):
                            raw = line[2:].strip()
                            for entry in raw.split():
                                name = entry.split("=")[0]
                                name = name.split("/")[-1]
                                if name and not name.startswith("cmd:"):
                                    provides.add(name)
    logger.info(f"  {len(packages)} real packages, {len(provides)} virtual provides")
    return packages | provides


def extract_packages_from_dockerfile(dockerfile_path):
    content = dockerfile_path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    joined_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        while line.endswith("\\") and i + 1 < len(lines):
            line = line[:-1] + " " + lines[i + 1].strip()
            i += 1
        joined_lines.append(line)
        i += 1

    packages = set()
    for line in joined_lines:
        match = re.search(r"apk\s+add\s+(.+)", line)
        if not match:
            continue
        raw = match.group(1)
        raw = re.sub(r"--no-cache\b", "", raw)
        raw = re.sub(r"--[^=\s]+(?:=[^\s]*)?", "", raw)
        raw = re.sub(r"[;&|]", " ", raw)
        raw = re.sub(r">/?\s*\S+", " ", raw)
        raw = re.sub(r"2\s*>\s*\S+", " ", raw)
        raw = re.sub(r"\|\s*\S+", " ", raw)
        raw = re.sub(r"\$\{[^}]+\}", "__VAR__", raw)
        raw = re.sub(r"\$[A-Za-z_][A-Za-z0-9_]*", "__VAR__", raw)
        tokens = raw.split()
        for token in tokens:
            token = token.strip()
            if not token or token == "__VAR__":
                continue
            if re.match(r"^https?://", token):
                continue
            if re.match(r"^[/~]", token):
                continue
            if re.match(r"^[\{\}\(\)\[\];&|<>!`'\"\\]", token):
                continue
            if re.match(r"^[\d]+$", token):
                continue
            if token in SHELL_OPERATORS:
                continue
            if re.match(r"^-[a-zA-Z]", token):
                continue
            if re.match(r"^--", token):
                continue
            if token.endswith(".list"):
                continue
            if token.endswith(".conf"):
                continue
            if (
                token.endswith(".tar.gz")
                or token.endswith(".tar.xz")
                or token.endswith(".tgz")
            ):
                continue
            if token.endswith(".js") or token.endswith(".py") or token.endswith(".sh"):
                continue
            if re.match(r".*\.jar$", token):
                continue
            if token in (
                "COPY",
                "FROM",
                "RUN",
                "ADD",
                "ENTRYPOINT",
                "CMD",
                "ENV",
                "WORKDIR",
                "EXPOSE",
                "VOLUME",
                "ARG",
                "USER",
                "LABEL",
                "HEALTHCHECK",
                "STOPSIGNAL",
                "ONBUILD",
                "AS",
                "or",
                "http",
                "https",
                "main",
                "binary",
                "instructions.",
                "install",
            ):
                continue
            if '"' in token or "'" in token:
                continue
            packages.add(token)

    return packages


def classify_invalid(pkg):
    if DEBIAN_LIB_PATTERN.match(pkg):
        return "debian-lib"
    if VERSIONED_PACKAGE_PATTERN.match(pkg):
        return "versioned"
    if pkg.startswith("php") and re.search(r"\d\.\d", pkg):
        return "debian-php"
    return "unknown"


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("WOLFI PACKAGE AUDIT")
    print("=" * 70)

    index_data = download_apkindex()
    wolfi_packages = parse_apkindex(index_data)
    logger.info(f"Loaded {len(wolfi_packages)} packages from wolfi index")

    dockerfiles = sorted(IMAGES_DIR.glob("*/Dockerfile"))
    logger.info(f"Found {len(dockerfiles)} Dockerfiles to scan")

    all_pkg_to_images = defaultdict(set)
    image_pkgs = {}

    for df in dockerfiles:
        image_name = df.parent.name
        pkgs = extract_packages_from_dockerfile(df)
        if pkgs:
            image_pkgs[image_name] = pkgs
            for pkg in pkgs:
                all_pkg_to_images[pkg].add(image_name)

    logger.info(f"Extracted packages from {len(image_pkgs)} Dockerfiles")
    logger.info(f"Found {len(all_pkg_to_images)} unique package names")

    valid_packages = sorted(pkg for pkg in all_pkg_to_images if pkg in wolfi_packages)
    invalid_packages = {
        pkg: sorted(images)
        for pkg, images in sorted(all_pkg_to_images.items())
        if pkg not in wolfi_packages
    }

    invalid_classified = defaultdict(list)
    for pkg in invalid_packages:
        cat = classify_invalid(pkg)
        invalid_classified[cat].append(pkg)

    total = len(all_pkg_to_images)
    valid_count = len(valid_packages)
    invalid_count = len(invalid_packages)
    pct = (valid_count / total * 100) if total else 0

    print("-" * 70)
    print(f"RESULTS: {valid_count}/{total} valid ({pct:.1f}%), {invalid_count} invalid")
    print("-" * 70)

    for cat in ["debian-lib", "debian-php", "versioned", "unknown"]:
        pkgs = invalid_classified.get(cat, [])
        if pkgs:
            print(f"\n  [{cat}] ({len(pkgs)} packages):")
            for p in pkgs:
                images = invalid_packages[p]
                print(
                    f"    {p}  (used in: {', '.join(images[:3])}{'...' if len(images) > 3 else ''})"
                )

    print()

    json_output = {
        "valid_packages": valid_packages,
        "invalid_packages": invalid_packages,
    }
    json_path = REPORTS_DIR / "wolfi_invalid_packages.json"
    json_path.write_text(json.dumps(json_output, indent=2) + "\n", encoding="utf-8")
    logger.info(f"JSON report written to {json_path}")

    md_lines = []
    md_lines.append("# Wolfi Package Audit Report\n")
    md_lines.append("**Generated**: Automated audit against wolfi APKINDEX\n")
    md_lines.append(f"**Source**: `{APKINDEX_URL}`\n")

    md_lines.append("## Summary\n")
    md_lines.append("| Metric | Value |")
    md_lines.append("|--------|-------|")
    md_lines.append(f"| Total unique packages | {total} |")
    md_lines.append(f"| Valid (in wolfi) | {valid_count} |")
    md_lines.append(f"| Invalid (not in wolfi) | {invalid_count} |")
    md_lines.append(f"| Valid percentage | {pct:.1f}% |")
    md_lines.append(f"| Dockerfiles scanned | {len(dockerfiles)} |")
    md_lines.append(f"| Dockerfiles with `apk add` | {len(image_pkgs)} |\n")

    if invalid_packages:
        md_lines.append("## Invalid Packages\n")
        md_lines.append("| Package | Category | Dockerfiles | Images |")
        md_lines.append("|---------|----------|-------------|--------|")
        for pkg in sorted(invalid_packages):
            images = invalid_packages[pkg]
            cat = classify_invalid(pkg)
            md_lines.append(
                f"| `{pkg}` | {cat} | {len(images)} | {', '.join(images[:5])}{'...' if len(images) > 5 else ''} |"
            )
        md_lines.append("")

    md_lines.append("## Category Breakdown\n")
    md_lines.append("| Category | Count | Examples |")
    md_lines.append("|----------|-------|----------|")
    for cat in ["debian-lib", "debian-php", "versioned", "unknown"]:
        pkgs = invalid_classified.get(cat, [])
        examples = ", ".join(f"`{p}`" for p in pkgs[:5])
        md_lines.append(f"| {cat} | {len(pkgs)} | {examples or '—'} |")
    md_lines.append("")

    md_lines.append("## Per-Image Summary\n")
    for image_name in sorted(image_pkgs):
        pkgs = image_pkgs[image_name]
        v = sorted(p for p in pkgs if p in wolfi_packages)
        inv = sorted(p for p in pkgs if p not in wolfi_packages)
        md_lines.append(f"### `{image_name}`\n")
        if v:
            md_lines.append(f"**Valid** ({len(v)}): {', '.join(f'`{p}`' for p in v)}\n")
        if inv:
            md_lines.append(
                f"**Invalid** ({len(inv)}): {', '.join(f'`{p}`' for p in inv)}\n"
            )
        if not inv:
            md_lines.append("All packages valid.\n")

    md_lines.append("## Full Valid Package List\n")
    md_lines.append(", ".join(f"`{p}`" for p in valid_packages))
    md_lines.append("")

    md_path = REPORTS_DIR / "wolfi_package_audit.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    logger.info(f"Markdown report written to {md_path}")

    if invalid_count > 0:
        print(f"\n{'!' * 70}")
        print(f"ACTION REQUIRED: {invalid_count} invalid package(s) found!")
        print(f"{'!' * 70}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
