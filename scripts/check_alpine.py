#!/usr/bin/env python3
"""
CRITICAL: Check for Alpine base images
========================================
Alpine Linux is NEVER allowed in Sovereign Hardened Image Registry.

This is a CRITICAL security requirement - Alpine has different
vulnerability profiles and may not meet our zero-trust standards.
"""

import sys
import re

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'

def check_alpine(filepath):
    """Check if Dockerfile uses Alpine - NEVER ALLOWED."""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check for Alpine in FROM statements
    alpine_pattern = re.compile(r'^\s*FROM\s+.*alpine', re.IGNORECASE)
    alpine_found = False
    
    for i, line in enumerate(content.split('\n'), 1):
        if alpine_pattern.match(line):
            print(f"{RED}CRITICAL: {filepath}:{i}{NC}")
            print(f"  {line.strip()}")
            print(f"  {RED}ERROR: Alpine base detected - NEVER ALLOWED{NC}")
            print(f"  Use: debian-slim, distroless, wolfi, or scratch instead")
            alpine_found = True
    
    if alpine_found:
        return False
    
    print(f"{GREEN}OK: {filepath} - No Alpine base detected{NC}")
    return True


def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not files:
        print("No files to check")
        sys.exit(0)
    
    all_passed = True
    for filepath in files:
        if not check_alpine(filepath):
            all_passed = False
    
    if not all_passed:
        print(f"\n{RED}FATAL: Alpine base images detected - CANNOT COMMIT{NC}")
        print("Replace Alpine with: debian-slim, distroless, wolfi, or scratch")
        sys.exit(1)
    
    print(f"\n{GREEN}ALL CHECKS PASSED - No Alpine detected{NC}")
    sys.exit(0)


if __name__ == '__main__':
    main()