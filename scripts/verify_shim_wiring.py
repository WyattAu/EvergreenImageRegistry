#!/usr/bin/env python3
"""
verify_shim_wiring.py — Verify shim wiring for EvergreenImageRegistry images.

Checks each Dockerfile for required shim integration elements:
  1. ARG SHIM_VERSION
  2. FROM ghcr.io/wyattau/evergreenshim/... AS shim
  3. COPY --from=shim (correct path for base type)
  4. HEALTHCHECK using shim
  5. ENTRYPOINT using shim
  6. EXPOSE 9101 (metrics)
  7. All 4 security labels (cap-drop, no-new-privileges, read-only-rootfs, seccomp)

Usage:
    python3 scripts/verify_shim_wiring.py                    # Check all wired images
    python3 scripts/verify_shim_wiring.py --image nginx      # Check single image
    python3 scripts/verify_shim_wiring.py --list             # List all migratable images
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "images"

REQUIRED_SECURITY_LABELS = [
    "evergreen.security.cap-drop",
    "evergreen.security.no-new-privileges",
    "evergreen.security.read-only-rootfs",
    "evergreen.security.seccomp",
]

REQUIRED_CHECKS = [
    "has_shim_version_arg",
    "has_shim_from",
    "has_shim_copy",
    "has_healthcheck_shim",
    "has_entrypoint_shim",
    "has_expose_9101",
    "has_security_labels",
]


def detect_base_type(content: str) -> str:
    """Detect the base image type of the final stage."""
    lines = content.split("\n")
    for line in reversed(lines):
        stripped = line.strip()
        if stripped.upper().startswith("FROM "):
            lower = stripped.lower()
            if "scratch" in lower:
                return "scratch"
            elif "wolfi" in lower:
                return "wolfi"
            elif "distroless" in lower:
                return "distroless"
            elif "debian" in lower or "ubuntu" in lower:
                return "debian"
            elif "alpine" in lower:
                return "alpine"
            else:
                return "other"
    return "unknown"


def get_shim_path(base_type: str, content: str = "") -> str:
    """Return the shim binary path based on actual usage in ENTRYPOINT."""
    # Detect the actual path used in ENTRYPOINT
    entrypoint_match = re.search(r"ENTRYPOINT\s+\[([^\]]+)\]", content)
    if entrypoint_match:
        entrypoint = entrypoint_match.group(1)
        if "/usr/local/bin/shim" in entrypoint:
            return "/usr/local/bin/shim"
    return "/shim"


def check_dockerfile(dockerfile: Path) -> dict:
    """Run all shim wiring checks on a Dockerfile. Returns dict of check results."""
    content = dockerfile.read_text()
    base_type = detect_base_type(content)
    shim_path = get_shim_path(base_type, content)

    checks = {
        "has_shim_version_arg": False,
        "has_shim_from": False,
        "has_shim_copy": False,
        "has_healthcheck_shim": False,
        "has_entrypoint_shim": False,
        "has_expose_9101": False,
        "has_security_labels": False,
    }

    # 1. ARG SHIM_VERSION
    if re.search(r"ARG\s+SHIM_VERSION\s*=", content):
        checks["has_shim_version_arg"] = True

    # 2. FROM evergreenshim/... AS shim
    if re.search(r"FROM\s+ghcr\.io/wyattau/evergreenshim/.*\s+AS\s+shim", content):
        checks["has_shim_from"] = True

    # 3. COPY --from=shim (correct path)
    if "COPY --from=shim" in content and (
        "/shim" in content or "/usr/local/bin/shim" in content
    ):
        checks["has_shim_copy"] = True

    # 4. HEALTHCHECK using shim (may span multiple lines)
    # 4. HEALTHCHECK using shim (may span multiple lines)
    # Check for both /shim and /usr/local/bin/shim paths
    healthcheck_pattern = (
        r"HEALTHCHECK.*?CMD\s+(?:\[\"?"
        + re.escape(shim_path)
        + r"\"?\s*,\s*\"healthcheck\"|"
        + re.escape(shim_path)
        + r"\s+healthcheck)"
    )
    alt_shim_path = "/usr/local/bin/shim" if shim_path == "/shim" else "/shim"
    healthcheck_pattern_alt = (
        r"HEALTHCHECK.*?CMD\s+(?:\[\"?"
        + re.escape(alt_shim_path)
        + r"\"?\s*,\s*\"healthcheck\"|"
        + re.escape(alt_shim_path)
        + r"\s+healthcheck)"
    )
    if re.search(healthcheck_pattern, content, re.DOTALL) or re.search(
        healthcheck_pattern_alt, content, re.DOTALL
    ):
        checks["has_healthcheck_shim"] = True
        checks["has_healthcheck_shim"] = True

    # 5. ENTRYPOINT using shim
    if re.search(
        r'ENTRYPOINT\s+\["?'
        + re.escape(shim_path)
        + r'"?\s*,\s*"run"(?:\s*,\s*"-c"\s*,\s*"[^"]+")?\]',
        content,
    ):
        checks["has_entrypoint_shim"] = True

    # 6. EXPOSE 9101
    if re.search(r"EXPOSE\s+.*9101", content):
        checks["has_expose_9101"] = True

    # 7. Security labels
    found_labels = 0
    for label in REQUIRED_SECURITY_LABELS:
        if label in content:
            found_labels += 1
    checks["has_security_labels"] = found_labels == len(REQUIRED_SECURITY_LABELS)

    return {
        "checks": checks,
        "base_type": base_type,
        "shim_path": shim_path,
        "passed": all(checks.values()),
        "fail_count": sum(1 for v in checks.values() if not v),
    }


def find_shim_images() -> list[Path]:
    """Find all image directories with shim wiring (ARG SHIM_VERSION in Dockerfile)."""
    images = []
    for image_dir in sorted(IMAGES_DIR.iterdir()):
        if not image_dir.is_dir() or image_dir.name.startswith("_"):
            continue
        dockerfile = image_dir / "Dockerfile"
        if not dockerfile.exists():
            continue
        content = dockerfile.read_text()
        if "ARG SHIM_VERSION" in content:
            images.append(image_dir)
    return images


def format_report(results: dict, verbose: bool = False) -> str:
    """Format verification results as a report."""
    lines = []
    total = len(results)
    passed = sum(1 for r in results.values() if r["passed"])
    failed = total - passed

    lines.append("Shim Wiring Verification Report")
    lines.append(f"{'=' * 60}")
    lines.append(f"Total images checked: {total}")
    lines.append(f"Passed: {passed} | Failed: {failed}")
    lines.append("")

    if failed > 0:
        lines.append("FAILED IMAGES:")
        lines.append("-" * 60)
        for name, result in sorted(results.items()):
            if not result["passed"]:
                lines.append(f"\n  {name} (base={result['base_type']}):")
                for check, ok in result["checks"].items():
                    status = "PASS" if ok else "FAIL"
                    lines.append(f"    [{status}] {check}")
        lines.append("")

    if verbose or failed == 0:
        lines.append("ALL PASSED IMAGES:")
        lines.append("-" * 60)
        for name, result in sorted(results.items()):
            if result["passed"]:
                lines.append(f"  {name} (base={result['base_type']})")

    lines.append("")
    lines.append(f"{'=' * 60}")
    if failed == 0:
        lines.append("RESULT: ALL CHECKS PASSED")
    else:
        lines.append(f"RESULT: {failed} image(s) FAILED")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Verify shim wiring for EvergreenImageRegistry images"
    )
    parser.add_argument("--image", type=str, help="Check only this image")
    parser.add_argument(
        "--list", action="store_true", help="List all migratable images"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show all results, not just failures"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.list:
        images = find_shim_images()
        print(f"Found {len(images)} migratable images:")
        for img in images:
            print(f"  {img.name}")
        return

    if args.image:
        image_dir = IMAGES_DIR / args.image
        if not image_dir.exists():
            print(
                f"ERROR: Image '{args.image}' not found in {IMAGES_DIR}",
                file=sys.stderr,
            )
            sys.exit(1)
        dockerfile = image_dir / "Dockerfile"
        if not dockerfile.exists():
            print(f"ERROR: No Dockerfile found in {image_dir}", file=sys.stderr)
            sys.exit(1)
        result = check_dockerfile(dockerfile)
        if args.json:
            import json

            print(json.dumps({args.image: result}, indent=2))
        else:
            results = {args.image: result}
            print(format_report(results, verbose=True))
            sys.exit(0 if result["passed"] else 1)
        return

    images = find_shim_images()
    if not images:
        print("ERROR: No migratable images found", file=sys.stderr)
        sys.exit(1)

    results = {}
    for image_dir in images:
        dockerfile = image_dir / "Dockerfile"
        results[image_dir.name] = check_dockerfile(dockerfile)

    if args.json:
        import json

        print(json.dumps(results, indent=2))
    else:
        print(format_report(results, verbose=args.verbose))

    failed = sum(1 for r in results.values() if not r["passed"])
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
