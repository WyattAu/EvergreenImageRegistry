#!/usr/bin/env python3
"""
Evergreen Hardened Image Registry - Pre-commit Dockerfile Validator
====================================================================
Validates Dockerfiles against security constraints BEFORE build.

Checks:
- C001: Non-root user (UID 65534)
- C003: No shell
- C004: No package manager
- C010: HEALTHCHECK present
- Base image priority (scratch > distroless > wolfi > debian-slim)
- NO ALPINE (CRITICAL RULE)
- Required labels
"""

import os
import sys
from pathlib import Path

# ANSI colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

ERRORS = []
WARNINGS = []


def print_error(msg):
    ERRORS.append(msg)
    print(f"{RED}ERROR:{NC} {msg}")


def print_warning(msg):
    WARNINGS.append(msg)
    print(f"{YELLOW}WARN:{NC} {msg}")


def print_success(msg):
    print(f"{GREEN}OK:{NC} {msg}")


def validate_dockerfile(filepath):
    """Validate a Dockerfile against security constraints."""

    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return False

    with open(filepath) as f:
        content = f.read()

    lines = content.split("\n")

    print(f"\n{BLUE}Validating: {filepath}{NC}")
    print("=" * 60)

    # Track findings
    has_user = False
    has_healthcheck = False
    has_labels = False
    uses_scratch = False
    uses_distroless = False
    uses_wolfi = False
    uses_debian_slim = False
    uses_alpine_base = False

    # Check each line
    for i, line in enumerate(lines, 1):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # CRITICAL: Check for Alpine (NEVER ALLOWED)
        if line_lower.startswith("from ") and "alpine" in line_lower:
            uses_alpine_base = True
            print_error(f"Line {i}: Alpine base image detected - NEVER ALLOWED")

        # Check base image type
        if line_lower.startswith("from "):
            if "scratch" in line_lower:
                uses_scratch = True
                print_success(f"Line {i}: Using scratch base (BEST)")
            elif "distroless" in line_lower:
                uses_distroless = True
                print_success(f"Line {i}: Using distroless base (GOOD)")
            elif "wolfi" in line_lower:
                uses_wolfi = True
                print_success(f"Line {i}: Using wolfi base (OK)")
            elif "debian-slim" in line_lower or "debian:bookworm" in line_lower:
                uses_debian_slim = True
                print_success(f"Line {i}: Using debian-slim base (FALLBACK)")
            elif "alpine" not in line_lower:
                print_warning(f"Line {i}: Unknown base image: {line_stripped}")

        # Check for USER directive (C001)
        if line_stripped.lower().startswith(
            "user "
        ) or line_stripped.lower().startswith("group "):
            has_user = True
            # Check for UID 65534
            if "65534" in line_stripped or "nobody" in line_stripped.lower():
                print_success(f"Line {i}: Non-root user configured (C001)")
            else:
                print_warning(f"Line {i}: User specified but not 65534/nobody")

        # Check for HEALTHCHECK (C010)
        if line_stripped.lower().startswith("healthcheck"):
            has_healthcheck = True
            print_success(f"Line {i}: HEALTHCHECK present (C010)")

        # Check for LABEL
        if line_stripped.lower().startswith("label "):
            has_labels = True
            if "org.opencontainers.image.title" in line_stripped:
                print_success(f"Line {i}: Required labels present")

        # Check for shell removal (C003)
        if "rm" in line_lower and (
            "/bin/sh" in line_lower or "/bin/bash" in line_lower
        ):
            print_success(f"Line {i}: Shell removed (C003)")

        # Check for package manager removal (C004)
        if "rm" in line_lower and ("apt" in line_lower or "apk" in line_lower):
            print_warning(f"Line {i}: Package manager removed - verify complete")

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY:")
    print("=" * 60)

    # Critical checks
    if uses_alpine_base:
        print_error("CRITICAL: Alpine base detected - MUST BE FIXED")

    if not has_user:
        print_error("C001 FAILED: No USER directive - image may run as root")

    if not has_healthcheck:
        print_warning("C010 WARNING: No HEALTHCHECK defined")

    if not has_labels:
        print_warning("LABELS WARNING: Missing required OCI labels")

    # Base image priority check
    if uses_scratch:
        print_success("Base priority: scratch (BEST)")
    elif uses_distroless:
        print_success("Base priority: distroless (GOOD)")
    elif uses_wolfi:
        print_success("Base priority: wolfi (OK)")
    elif uses_debian_slim:
        print_warning("Base priority: debian-slim (FALLBACK)")

    # Return pass/fail
    if ERRORS:
        print(f"\n{RED}FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s){NC}")
        return False
    else:
        print(f"\n{GREEN}PASSED: {len(WARNINGS)} warning(s){NC}")
        return True


def main():
    """Main entry point."""

    # Get files to check
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files:
        # Default: check all Dockerfiles in images/
        images_dir = Path("images")
        if images_dir.exists():
            files = [str(p) for p in images_dir.rglob("Dockerfile")]

    if not files:
        print("No Dockerfiles found to validate")
        sys.exit(0)

    print(f"{BLUE} Evergreen Hardened Image Registry{NC}")
    print(f"{BLUE} Pre-commit Dockerfile Validator{NC}")
    print(f"Checking {len(files)} file(s)")

    all_passed = True

    for filepath in files:
        if not validate_dockerfile(filepath):
            all_passed = False

    # Final summary
    print("\n" + "=" * 60)
    if all_passed:
        print(f"{GREEN}ALL CHECKS PASSED{NC}")
        sys.exit(0)
    else:
        print(f"{RED}VALIDATION FAILED - Fix errors before committing{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
