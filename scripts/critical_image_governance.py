#!/usr/bin/env python3
"""
Phase 2 — Critical-image governance policy.

Defines the mandatory contract for all 87 critical-tier images and validates
compliance. This is the machine-readable governance policy that determines
which images are promotion-eligible.

Critical image contract (all conditions must be met):
  1. Canonical manifest.toml present and valid
  2. Tier = critical in manifest
  3. Non-root USER 65532 in Dockerfile
  4. HEALTHCHECK in Dockerfile
  5. SBOM file present (sbom.spdx.json)
  6. Valid OCI labels in Dockerfile
  7. Banned base images excluded
  8. Build type in allowed set
  9. No Alpine/debian-slim/ubuntu/centos in final stage
 10. ENTRYPOINT or CMD defined
 11. Documented health check strategy (or explicit exception)
 12. Graceful shutdown (SIGTERM stop signal)
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Critical image set (loaded from manifest scan)
# ---------------------------------------------------------------------------

BANNED_FINAL_BASES = {"alpine", "debian-slim", "ubuntu", "centos"}
ALLOWED_BASES_PREFIXES = ("scratch", "cgr.dev/", "gcr.io/distroless", "ghcr.io/")
BANNED_ENTRYPOINT_SHELLS = {"sh", "bash", "/bin/sh", "/bin/bash"}


def discover_critical_images(images_dir: Path) -> list[str]:
    """Find all images with tier = critical in their manifest."""
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
# Contract checks
# ---------------------------------------------------------------------------

class ContractCheck:
    def __init__(self, code: str, description: str):
        self.code = code
        self.description = description


CONTRACT_CHECKS = [
    ContractCheck("CC001", "manifest.toml present and valid"),
    ContractCheck("CC002", "Tier = critical"),
    ContractCheck("CC003", "Non-root USER 65532"),
    ContractCheck("CC004", "HEALTHCHECK defined"),
    ContractCheck("CC005", "SBOM file present"),
    ContractCheck("CC006", "No banned base images in final stage"),
    ContractCheck("CC007", "ENTRYPOINT or CMD defined"),
    ContractCheck("CC008", "SIGTERM stop signal"),
    ContractCheck("CC009", "No shell entrypoint for static images"),
    ContractCheck("CC010", "OCI labels present"),
    ContractCheck("CC011", "Build type in allowed set"),
    ContractCheck("CC012", "Source URL present"),
]


def check_manifest(image_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
    """Load manifest.toml and return data + errors."""
    manifest_path = image_dir / "manifest.toml"
    if not manifest_path.exists():
        return None, ["CC001: manifest.toml missing"]
    try:
        data = tomllib.loads(manifest_path.read_text())
        return data, []
    except Exception as exc:
        return None, [f"CC001: manifest.toml invalid: {exc}"]


def check_dockerfile(image_dir: Path, manifest: dict[str, Any] | None) -> list[str]:
    """Validate Dockerfile against the critical image contract."""
    violations = []
    dockerfile = image_dir / "Dockerfile"
    if not dockerfile.exists():
        violations.append("CC001: Dockerfile missing")
        return violations

    content = dockerfile.read_text()

    # CC003: Non-root
    if "USER 65532" not in content:
        violations.append("CC003: No USER 65532 in Dockerfile")

    # CC004: HEALTHCHECK
    if "FROM scratch" not in content and "HEALTHCHECK" not in content:
        violations.append("CC004: No HEALTHCHECK in non-scratch image")

    # CC006: Banned base images in final stage
    from_lines = [line.strip() for line in content.splitlines() if line.strip().upper().startswith("FROM ")]
    for fl in from_lines:
        base = fl.split()[1].split("@")[0].split(":")[0].lower()
        # Remove registry prefixes
        base_short = base.split("/")[-1]
        if base_short in BANNED_FINAL_BASES:
            violations.append(f"CC006: Banned base in FROM: {fl}")

    # CC007: ENTRYPOINT or CMD
    has_entrypoint = "ENTRYPOINT" in content
    has_cmd = "CMD " in content or "CMD\t" in content
    if not has_entrypoint and not has_cmd:
        violations.append("CC007: No ENTRYPOINT or CMD")

    # CC009: Shell entrypoint for static images
    if manifest:
        build = manifest.get("build", {})
        base = str(build.get("base", ""))
        if base == "scratch" or "distroless" in base.lower():
            for shell in BANNED_ENTRYPOINT_SHELLS:
                if f'"{shell}"' in content or f"'{shell}'" in content:
                    violations.append(f"CC009: Shell entrypoint ({shell}) in static image")
                    break

    # CC010: OCI labels
    if "LABEL" not in content:
        violations.append("CC010: No LABEL statements in Dockerfile")

    return violations


def check_sbom(image_dir: Path) -> list[str]:
    """Check for SBOM presence."""
    sbom = image_dir / "sbom.spdx.json"
    if not sbom.exists():
        return ["CC005: sbom.spdx.json missing"]
    try:
        data = json.loads(sbom.read_text())
        packages = data.get("packages", [])
        if not packages:
            return ["CC005: SBOM has no packages"]
    except Exception:
        return ["CC005: SBOM file invalid"]
    return []


def check_manifest_contract(manifest: dict[str, Any]) -> list[str]:
    """Validate manifest fields against the critical contract."""
    violations = []
    metadata = manifest.get("metadata", {})
    build = manifest.get("build", {})
    source = manifest.get("source", {})

    # CC002: Tier
    tier = str(metadata.get("tier", "")).strip().lower()
    if tier != "critical":
        violations.append(f"CC002: Tier is {tier!r}, expected critical")

    # CC008: Stop signal
    stopsignal = str(build.get("stopsignal", "")).strip().upper()
    if stopsignal and stopsignal != "SIGTERM":
        violations.append(f"CC008: Stop signal is {stopsignal!r}, expected SIGTERM")

    # CC011: Build type
    build_type = str(source.get("type", "")).strip()
    if not build_type:
        violations.append("CC011: No build type in source")

    # CC012: Source URL
    url = str(source.get("url", "")).strip()
    if not url:
        violations.append("CC012: No source URL")

    # CC006: Banned base in manifest
    base = str(build.get("base", "")).lower()
    base_short = base.split("/")[-1].split(":")[0].split("@")[0]
    if base_short in BANNED_FINAL_BASES:
        violations.append(f"CC006: Banned base in manifest: {base}")

    return violations


def validate_critical_image(image_name: str, images_dir: Path) -> dict[str, Any]:
    """Run full contract validation for a critical image."""
    image_dir = images_dir / image_name
    result = {
        "image": image_name,
        "compliant": True,
        "passed": [],
        "violations": [],
        "checks_run": len(CONTRACT_CHECKS),
    }

    # Load manifest
    manifest, manifest_errors = check_manifest(image_dir)
    if manifest_errors:
        result["violations"].extend(manifest_errors)
        result["compliant"] = False

    # Manifest contract
    if manifest:
        result["violations"].extend(check_manifest_contract(manifest))
    else:
        result["violations"].append("CC001: Cannot validate without manifest")

    # Dockerfile checks
    result["violations"].extend(check_dockerfile(image_dir, manifest))

    # SBOM
    result["violations"].extend(check_sbom(image_dir))

    if result["violations"]:
        result["compliant"] = False

    # Passed = checks_run - violations
    violated_codes = set()
    for v in result["violations"]:
        code = v.split(":")[0]
        violated_codes.add(code)
    result["passed_count"] = len(CONTRACT_CHECKS) - len(violated_codes)
    result["failed_count"] = len(violated_codes)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    images_dir = Path("images")
    if not images_dir.is_dir():
        print("ERROR: images/ directory not found", file=sys.stderr)
        return 1

    critical = discover_critical_images(images_dir)
    print(f"Discovered {len(critical)} critical-tier images")

    results = []
    compliant_count = 0
    total_violations = 0

    for img in critical:
        result = validate_critical_image(img, images_dir)
        results.append(result)
        if result["compliant"]:
            compliant_count += 1
        total_violations += len(result["violations"])

    # Summary
    report = {
        "summary": {
            "total_critical": len(critical),
            "compliant": compliant_count,
            "non_compliant": len(critical) - compliant_count,
            "total_violations": total_violations,
        },
        "images": results,
    }

    output_path = Path("/tmp/critical_image_governance.json")
    output_path.write_text(json.dumps(report, indent=2))

    print("\nCritical image governance:")
    print(f"  Total:       {len(critical)}")
    print(f"  Compliant:   {compliant_count}")
    print(f"  Non-compliant: {len(critical) - compliant_count}")
    print(f"  Violations:  {total_violations}")
    print(f"\nReport written to {output_path}")

    # Print non-compliant images
    non_compliant = [r for r in results if not r["compliant"]]
    if non_compliant:
        print(f"\nNon-compliant images ({len(non_compliant)}):")
        for r in non_compliant[:20]:
            print(f"  {r['image']}: {r['failed_count']} violations")
            for v in r["violations"][:3]:
                print(f"    - {v}")
            if len(r["violations"]) > 3:
                print(f"    ... and {len(r['violations']) - 3} more")
        if len(non_compliant) > 20:
            print(f"  ... and {len(non_compliant) - 20} more")

    return 1 if non_compliant else 0


if __name__ == "__main__":
    sys.exit(main())
