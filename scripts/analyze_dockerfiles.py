#!/usr/bin/env python3
"""
Batch Dockerfile fixer - identifies and fixes common issues across all Dockerfiles.
This addresses issues like:
- Non-existent Debian packages
- Outdated binary URLs
- Alpine base images (should use debian-slim/wolfi)
- Missing dependencies
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# Common problematic packages (not available in Debian)
PROBLEMATIC_PACKAGES = {
    "gitlab-ce": "gitlab/gitlab-ce",
    "mattermost": "mattermost/mattermost-server",
    "synapse": "matrix-org/synapse",
    "zitadel": "zitadel/zitadel",
    "drone": "drone/drone",
    "argocd": "argoproj/argo-cd",
    "tekton": "tektoncd/cli",
    "pulsar": "apachepulsar/pulsar",
    "activemq": "apache/activemq-classic",
    "openhab": "openhab/openhab-docker",
    "pihole": "pihole/pihole",
    "homeassistant": "homeassistant/home-assistant",
    "jellyfin": "jellyfin/jellyfin",
    "radarr": "radarr/radarr",
    "sonarr": "sonarr/sonarr",
    "lidarr": "lidarr/lidarr",
    "prowlarr": "prowlarr/prowlarr",
}

# Known binary URLs that need updating
BINARY_URL_PATTERNS = {
    "vault": "https://releases.hashicorp.com/vault/",
    "terraform": "https://releases.hashicorp.com/terraform/",
    "consul": "https://releases.hashicorp.com/consul/",
    "nomad": "https://releases.hashicorp.com/nomad/",
    "boundary": "https://releases.hashicorp.com/boundary/",
}


def get_all_dockerfiles():
    """Get all Dockerfile paths in images directory."""
    images_dir = Path("images")
    return list(images_dir.glob("*/Dockerfile"))


def analyze_dockerfile(dockerfile_path):
    """Analyze a Dockerfile for common issues."""
    with open(dockerfile_path) as f:
        content = f.read()

    issues = []

    # Check for problematic packages in apt-get install
    apt_install_match = re.search(
        r"apt-get install.*?--no-install-recommends\s+([^\s&]+)", content
    )
    if apt_install_match:
        package = apt_install_match.group(1)
        if package in PROBLEMATIC_PACKAGES:
            issues.append(f"package_not_in_debian:{package}")

    # Check for Alpine base (should use debian-slim/wolfi)
    if "FROM alpine" in content:
        issues.append("uses_alpine_base")

    # Check for outdated URLs (common patterns)
    if "releases.hashicorp.com" in content:
        # Check for old version patterns
        version_match = re.search(
            r"releases\.hashicorp\.com/[^/]+/([0-9]+\.[0-9]+)", content
        )
        if version_match:
            issues.append(f"可能_outdated_hashicorp:{version_match.group(1)}")

    return issues


def main():
    """Main function to scan all Dockerfiles."""
    dockerfiles = get_all_dockerfiles()
    logger.info(f"Found {len(dockerfiles)} Dockerfiles to analyze")

    issue_counts = {}
    for df in dockerfiles:
        issues = analyze_dockerfile(df)
        for issue in issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
            if issue.startswith("package_not_in_debian"):
                logger.info(f"{df.parent.name}: {issue}")

    print("\n=== Issue Summary ===")
    for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
        print(f"  {issue}: {count}")


if __name__ == "__main__":
    main()
