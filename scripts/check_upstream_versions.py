#!/usr/bin/env python3
"""Check upstream GitHub releases for version updates against local manifest.toml files."""

import json
import logging
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

GITHUB_API = "https://api.github.com/repos"
logger = logging.getLogger(__name__)


def parse_toml_simple(filepath):
    """Minimal TOML parser that extracts metadata.name, metadata.version, metadata.source."""
    data = {}
    current_section = None
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("["):
                current_section = line.strip("[]").strip()
                if current_section not in data:
                    data[current_section] = {}
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"')
            if current_section:
                data[current_section][key] = value
    return data


def get_latest_github_release(repo):
    """Query GitHub API for the latest release tag of a repo. Returns (tag, url) or (None, None)."""
    url = f"{GITHUB_API}/{repo}/releases/latest"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "evergreen-registry-upstream-check",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            release = json.loads(resp.read().decode())
            tag = release.get("tag_name", "")
            html_url = release.get("html_url", "")
            return tag, html_url
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        logger.warning("API error %d for %s", e.code, repo)
        return None, None
    except Exception as e:
        logger.warning("Failed to query %s: %s", repo, e)
        return None, None


def normalize_version(version_str):
    """Strip leading 'v' and extract semantic version."""
    v = version_str.strip()
    if v.lower().startswith("v"):
        v = v[1:]
    match = re.match(r"^(\d+(?:\.\d+)*)", v)
    return match.group(1) if match else v


def extract_github_repo(source_url):
    """Extract owner/repo from a GitHub source URL."""
    if not source_url:
        return None
    match = re.search(r"github\.com/([^/]+/[^/\s]+)", source_url)
    if match:
        repo = match.group(1).rstrip("/")
        if repo.endswith(".git"):
            repo = repo[:-4]
        return repo
    return None


def main():
    root = Path(os.environ.get("GITHUB_WORKSPACE", "."))
    manifest_files = sorted(root.glob("images/*/manifest.toml"))

    if not manifest_files:
        print("No manifest.toml files found.")
        return 0

    print(f"Checking {len(manifest_files)} manifests for upstream updates...\n")

    updates = []
    checked = 0
    skipped = 0

    for mf in manifest_files:
        image_name = mf.parent.name
        data = parse_toml_simple(mf)

        metadata = data.get("metadata", {})
        current_version = metadata.get("version", "")
        source_url = metadata.get("source", "")

        if not current_version:
            skipped += 1
            continue

        repo = extract_github_repo(source_url)
        if not repo:
            skipped += 1
            continue

        checked += 1
        latest_tag, latest_url = get_latest_github_release(repo)

        if not latest_tag:
            continue

        current_norm = normalize_version(current_version)
        latest_norm = normalize_version(latest_tag)

        if current_norm != latest_norm:
            updates.append(
                {
                    "image": image_name,
                    "current": current_version,
                    "latest": latest_tag,
                    "repo": repo,
                    "url": latest_url,
                }
            )
            status = "UPDATE AVAILABLE"
        else:
            status = "up to date"

        print(
            f"  {image_name:40s} {current_version:20s} -> {latest_tag:20s}  [{status}]"
        )

    print("\n=== Summary ===")
    print(f"Checked: {checked}, Skipped: {skipped}, Updates available: {len(updates)}")

    if updates:
        print("\n=== Updates Available ===")
        for u in updates:
            print(f"  {u['image']}: {u['current']} -> {u['latest']}")
            print(f"    Repo: {u['repo']}")
            print(f"    Release: {u['url']}")
            print()
        return 1
    else:
        print("\nAll checked images are up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
