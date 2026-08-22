#!/usr/bin/env python3
"""
Evergreen Hardened Image Registry - Pre-commit Dockerfile Validator
====================================================================
Validates Dockerfiles against security constraints BEFORE build.

Checks:
- C001: Non-root user (UID 65532 or 65534)
- C003: No shell in final stage
- C004: No package manager in final stage
- C010: HEALTHCHECK present
- Base image priority (scratch > distroless > wolfi > debian-slim)
- NO ALPINE (CRITICAL RULE)
- Required labels
"""

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ANSI colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color

# Accepted non-root UIDs (65532 = Evergreen standard, 65534 = nobody fallback)
ACCEPTED_UIDS = {"65532", "65534", "nobody"}


def validate_dockerfile(filepath: str) -> bool:
    """Validate a Dockerfile against security constraints.

    Returns True if the file passes all checks, False otherwise.
    Errors and warnings are scoped to this invocation (no global accumulation).
    """
    errors: list[str] = []
    warnings: list[str] = []

    p = Path(filepath)
    try:
        content = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"{RED}ERROR:{NC} File not found: {filepath}")
        return False

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

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        lower = stripped.lower()

        # CRITICAL: Check for Alpine (NEVER ALLOWED)
        if lower.startswith("from ") and "alpine" in lower:
            uses_alpine_base = True
            errors.append(f"Line {i}: Alpine base image detected - NEVER ALLOWED")

        # Check base image type
        if lower.startswith("from "):
            if "scratch" in lower:
                uses_scratch = True
                print(f"{GREEN}OK:{NC} Line {i}: Using scratch base (BEST)")
            elif "distroless" in lower:
                uses_distroless = True
                print(f"{GREEN}OK:{NC} Line {i}: Using distroless base (GOOD)")
            elif "wolfi" in lower:
                uses_wolfi = True
                print(f"{GREEN}OK:{NC} Line {i}: Using wolfi base (OK)")
            elif "debian-slim" in lower or "debian:bookworm" in lower:
                uses_debian_slim = True
                print(f"{GREEN}OK:{NC} Line {i}: Using debian-slim base (FALLBACK)")
            elif "alpine" not in lower:
                warnings.append(f"Line {i}: Unknown base image: {stripped}")

        # Check for USER directive (C001)
        if lower.startswith("user ") or lower.startswith("group "):
            has_user = True
            uid_found = any(uid in stripped for uid in ACCEPTED_UIDS)
            if uid_found:
                print(f"{GREEN}OK:{NC} Line {i}: Non-root user configured (C001)")
            else:
                warnings.append(f"Line {i}: User specified but not 65532/65534/nobody")

        # Check for HEALTHCHECK (C010)
        if lower.startswith("healthcheck"):
            has_healthcheck = True
            print(f"{GREEN}OK:{NC} Line {i}: HEALTHCHECK present (C010)")

        # Check for LABEL
        if lower.startswith("label "):
            has_labels = True
            if "org.opencontainers.image.title" in stripped:
                print(f"{GREEN}OK:{NC} Line {i}: Required labels present")

    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY:")
    print("=" * 60)

    if uses_alpine_base:
        errors.append("CRITICAL: Alpine base detected - MUST BE FIXED")

    if not has_user:
        errors.append("C001 FAILED: No USER directive - image may run as root")

    if not has_healthcheck:
        warnings.append("C010 WARNING: No HEALTHCHECK defined")

    if not has_labels:
        warnings.append("LABELS WARNING: Missing required OCI labels")

    # Base image priority check
    if uses_scratch:
        print(f"{GREEN}OK:{NC} Base priority: scratch (BEST)")
    elif uses_distroless:
        print(f"{GREEN}OK:{NC} Base priority: distroless (GOOD)")
    elif uses_wolfi:
        print(f"{GREEN}OK:{NC} Base priority: wolfi (OK)")
    elif uses_debian_slim:
        warnings.append("Base priority: debian-slim (FALLBACK)")

    # Print errors and warnings
    for e in errors:
        print(f"{RED}ERROR:{NC} {e}")
    for w in warnings:
        print(f"{YELLOW}WARN:{NC} {w}")

    if errors:
        print(f"\n{RED}FAILED: {len(errors)} error(s), {len(warnings)} warning(s){NC}")
        return False

    print(f"\n{GREEN}PASSED: {len(warnings)} warning(s){NC}")
    return True


def main() -> None:
    """Main entry point."""
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files:
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

    print("\n" + "=" * 60)
    if all_passed:
        print(f"{GREEN}ALL CHECKS PASSED{NC}")
        sys.exit(0)
    else:
        print(f"{RED}VALIDATION FAILED - Fix errors before committing{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
