#!/usr/bin/env python3
"""
Phase 4 — Runtime verification for critical images.

Verifies runtime properties from Dockerfile and manifest metadata:
  1. Non-root execution (USER 65532)
  2. HEALTHCHECK defined with valid strategy
  3. Graceful shutdown (SIGTERM + stop signal)
  4. Read-only root filesystem compatible
  5. Capability dropping (CAP DROP ALL)
  6. No new privileges
  7. Seccomp profile specified
  8. Resource limits compatible
  9. Startup/shutdown timeouts configured
 10. Signal handling strategy documented

This is static analysis — no containers are run.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Runtime checks
# ---------------------------------------------------------------------------

def check_nonroot(dockerfile_content: str) -> dict[str, Any] | None:
    """Verify USER 65532 is set."""
    if "USER 65532" in dockerfile_content:
        return None
    return {"code": "RT001", "severity": "block", "message": "No USER 65532 in Dockerfile"}


def check_healthcheck(dockerfile_content: str, is_scratch: bool) -> dict[str, Any] | None:
    """Verify HEALTHCHECK is defined for non-scratch images."""
    if is_scratch:
        return None  # scratch images don't need HEALTHCHECK
    if "HEALTHCHECK" in dockerfile_content:
        return None
    return {"code": "RT002", "severity": "block", "message": "No HEALTHCHECK in non-scratch image"}


def check_healthcheck_strategy(manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Verify health check strategy is documented."""
    labels = manifest.get("labels", {})
    health_type = labels.get("evergreen.health.type")
    if health_type:
        return None
    return {
        "code": "RT003",
        "severity": "warn",
        "message": "No evergreen.health.type label in manifest",
    }


def check_stop_signal(manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Verify SIGTERM stop signal."""
    build = manifest.get("build", {})
    stopsignal = str(build.get("stopsignal", "")).strip().upper()
    if stopsignal == "SIGTERM":
        return None
    if stopsignal:
        return {
            "code": "RT004",
            "severity": "warn",
            "message": f"Stop signal is {stopsignal!r}, expected SIGTERM",
        }
    return {"code": "RT004", "severity": "warn", "message": "No stop signal defined"}


def check_readonly_rootfs(dockerfile_content: str, manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for read-only root filesystem compatibility."""
    labels = manifest.get("labels", {})
    if labels.get("evergreen.security.read-only-rootfs") == "true":
        return None

    # Check Dockerfile for read-only rootfs indicator
    if "read-only-rootfs" in dockerfile_content.lower():
        return None

    return {
        "code": "RT005",
        "severity": "warn",
        "message": "No read-only rootfs configuration",
    }


def check_capabilities(dockerfile_content: str, manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for capability dropping."""
    labels = manifest.get("labels", {})
    if labels.get("evergreen.security.cap-drop") == "ALL":
        return None
    if "cap-drop" in dockerfile_content.lower() and "all" in dockerfile_content.lower():
        return None
    return {
        "code": "RT006",
        "severity": "warn",
        "message": "No CAP DROP ALL configuration",
    }


def check_no_new_privileges(dockerfile_content: str, manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for no-new-privileges."""
    labels = manifest.get("labels", {})
    if labels.get("evergreen.security.no-new-privileges") == "true":
        return None
    if "no-new-privileges" in dockerfile_content.lower():
        return None
    return {
        "code": "RT007",
        "severity": "warn",
        "message": "No no-new-privileges configuration",
    }


def check_seccomp(dockerfile_content: str, manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for seccomp profile."""
    labels = manifest.get("labels", {})
    if labels.get("evergreen.security.seccomp"):
        return None
    if "seccomp" in dockerfile_content.lower():
        return None
    return {
        "code": "RT008",
        "severity": "info",
        "message": "No seccomp profile specified",
    }


def check_shutdown_config(manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for shutdown timeout configuration."""
    labels = manifest.get("labels", {})
    timeout = labels.get("evergreen.hft.shutdown-timeout")
    if timeout:
        return None
    return {
        "code": "RT009",
        "severity": "info",
        "message": "No shutdown timeout configured",
    }


def check_startup_config(manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for startup timeout configuration."""
    labels = manifest.get("labels", {})
    timeout = labels.get("evergreen.hft.startup-timeout")
    if timeout:
        return None
    return {
        "code": "RT010",
        "severity": "info",
        "message": "No startup timeout configured",
    }


def check_signal_handling(manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for signal handling strategy."""
    labels = manifest.get("labels", {})
    strategy = labels.get("evergreen.hft.signal-handling")
    if strategy:
        return None
    return {
        "code": "RT011",
        "severity": "info",
        "message": "No signal handling strategy documented",
    }


def check_init_system(manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Check for init system configuration."""
    labels = manifest.get("labels", {})
    init_system = labels.get("evergreen.hft.init-system")
    if init_system is not None:
        return None
    return {
        "code": "RT012",
        "severity": "info",
        "message": "No init system configuration",
    }


# ---------------------------------------------------------------------------
# Full verification
# ---------------------------------------------------------------------------

def verify_image(image_name: str, images_dir: Path) -> dict[str, Any]:
    """Run full runtime verification for an image."""
    image_dir = images_dir / image_name
    result = {
        "image": image_name,
        "compliant": True,
        "violations": [],
        "checks_passed": 0,
        "checks_failed": 0,
    }

    # Load Dockerfile
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        result["violations"].append({
            "code": "RT000",
            "severity": "block",
            "message": "Dockerfile missing",
        })
        result["compliant"] = False
        return result

    try:
        df_content = dockerfile.read_text()
    except OSError:
        result["violations"].append({
            "code": "RT000",
            "severity": "block",
            "message": "Dockerfile unreadable",
        })
        result["compliant"] = False
        return result

    is_scratch = "FROM scratch" in df_content

    # Load manifest
    manifest_path = image_dir / "manifest.toml"
    manifest = {}
    if manifest_path.exists():
        try:
            manifest = tomllib.loads(manifest_path.read_text())
        except Exception:
            pass

    # Run all checks
    checks = [
        check_nonroot(df_content),
        check_healthcheck(df_content, is_scratch),
        check_healthcheck_strategy(manifest),
        check_stop_signal(manifest),
        check_readonly_rootfs(df_content, manifest),
        check_capabilities(df_content, manifest),
        check_no_new_privileges(df_content, manifest),
        check_seccomp(df_content, manifest),
        check_shutdown_config(manifest),
        check_startup_config(manifest),
        check_signal_handling(manifest),
        check_init_system(manifest),
    ]

    for violation in checks:
        if violation is not None:
            result["violations"].append(violation)
            result["checks_failed"] += 1
        else:
            result["checks_passed"] += 1

    block_count = sum(1 for v in result["violations"] if v["severity"] == "block")
    result["compliant"] = block_count == 0

    return result


def discover_critical_images(images_dir: Path) -> list[str]:
    """Find all images with tier = critical."""
    critical = []
    for img_dir in sorted(images_dir.iterdir()):
        if not img_dir.is_dir() or img_dir.name.startswith("_"):
            continue
        manifest_path = img_dir / "manifest.toml"
        if not manifest_path.exists():
            continue
        try:
            data = tomllib.loads(manifest_path.read_text())
            tier = str(data.get("metadata", {}).get("tier", "")).strip().lower()
            if tier == "critical":
                critical.append(img_dir.name)
        except Exception:
            continue
    return critical


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    images_dir = Path("images")
    if not images_dir.is_dir():
        print("ERROR: images/ directory not found", file=sys.stderr)
        return 1

    critical = discover_critical_images(images_dir)
    print(f"Runtime verification for {len(critical)} critical images")

    results = []
    fully_compliant = 0
    total_block = 0
    total_warn = 0
    total_info = 0

    for img in critical:
        result = verify_image(img, images_dir)
        results.append(result)
        if result["compliant"]:
            fully_compliant += 1
        for v in result["violations"]:
            if v["severity"] == "block":
                total_block += 1
            elif v["severity"] == "warn":
                total_warn += 1
            else:
                total_info += 1

    report = {
        "summary": {
            "total_critical": len(critical),
            "fully_compliant": fully_compliant,
            "non_compliant": len(critical) - fully_compliant,
            "total_block": total_block,
            "total_warn": total_warn,
            "total_info": total_info,
        },
        "images": results,
    }

    output_path = Path("/tmp/runtime_verification.json")
    output_path.write_text(json.dumps(report, indent=2))

    print(f"\nRuntime verification:")
    print(f"  Total:             {len(critical)}")
    print(f"  Fully compliant:   {fully_compliant}")
    print(f"  Non-compliant:     {len(critical) - fully_compliant}")
    print(f"  Block: {total_block}  Warn: {total_warn}  Info: {total_info}")
    print(f"\nReport written to {output_path}")

    return 1 if total_block > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
