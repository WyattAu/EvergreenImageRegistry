#!/usr/bin/env python3
"""
CRITICAL: Check for Alpine base images
========================================
Alpine Linux is NEVER allowed in Evergreen Hardened Image Registry.

This is a CRITICAL security requirement - Alpine has different
vulnerability profiles and may not meet our zero-trust standards.
"""

import logging
import re
import sys

logger = logging.getLogger(__name__)


def check_alpine(filepath):
    """Check if Dockerfile uses Alpine - NEVER ALLOWED."""

    with open(filepath) as f:
        content = f.read()

    # Check for Alpine in FROM statements
    alpine_pattern = re.compile(r"^\s*FROM\s+.*alpine", re.IGNORECASE)
    alpine_found = False

    for i, line in enumerate(content.split("\n"), 1):
        if alpine_pattern.match(line):
            logger.error("CRITICAL: %s:%d", filepath, i)
            logger.error("  %s", line.strip())
            logger.error("Alpine base detected - NEVER ALLOWED")
            logger.info("Use: debian-slim, distroless, wolfi, or scratch instead")
            alpine_found = True

    if alpine_found:
        return False

    logger.info("OK: %s - No Alpine base detected", filepath)
    return True


def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files:
        logger.info("No files to check")
        sys.exit(0)

    all_passed = True
    for filepath in files:
        if not check_alpine(filepath):
            all_passed = False

    if not all_passed:
        logger.error("FATAL: Alpine base images detected - CANNOT COMMIT")
        logger.info("Replace Alpine with: debian-slim, distroless, wolfi, or scratch")
        sys.exit(1)

    logger.info("ALL CHECKS PASSED - No Alpine detected")
    sys.exit(0)


if __name__ == "__main__":
    main()
