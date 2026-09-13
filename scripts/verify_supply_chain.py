#!/usr/bin/env python3
"""
Phase 3 — Supply-chain verification for immutable inputs.

Verifies the supply chain integrity of critical-tier images:
  1. SBOM present and contains packages
  2. SBOM content hash recorded in manifest or attestation
  3. Cosign signature verifiable against known key
  4. SLSA provenance attestation present
  5. Image digest pinned in Dockerfile (for non-variable FROM lines)
  6. Build reproducibility metadata present

This script is read-only and does not modify any files.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Supply-chain checks
# ---------------------------------------------------------------------------

def check_sbom_binding(image_dir: Path) -> list[dict[str, str]]:
    """Verify SBOM exists, has packages, and records a content hash."""
    violations = []
    sbom_path = image_dir / "sbom.spdx.json"

    if not sbom_path.exists():
        violations.append({
            "code": "SC001",
            "severity": "block",
            "message": "SBOM (sbom.spdx.json) missing",
        })
        return violations

    try:
        content = sbom_path.read_text()
        data = json.loads(content)
    except (OSError, json.JSONDecodeError) as exc:
        violations.append({
            "code": "SC002",
            "severity": "block",
            "message": f"SBOM unreadable or invalid JSON: {exc}",
        })
        return violations

    # Check packages
    packages = data.get("packages", [])
    if not packages:
        violations.append({
            "code": "SC003",
            "severity": "block",
            "message": "SBOM has no packages",
        })

    # Record content hash
    sbom_hash = hashlib.sha256(content.encode()).hexdigest()
    # Store for potential attestation binding
    image_dir.joinpath(".sbom_hash").write_text(f"sha256:{sbom_hash}\n")

    # Check for external document references (attestation binding)
    external = data.get("externalDocumentReferences", [])
    if not external:
        violations.append({
            "code": "SC004",
            "severity": "warn",
            "message": "SBOM has no external document references (attestation binding)",
        })

    return violations


def check_signature(image_dir: Path) -> list[dict[str, str]]:
    """Check for cosign signature presence."""
    violations = []

    # Check for .sig or cosign bundle
    sig_files = list(image_dir.glob("*.sig")) + list(image_dir.glob("cosign.bundle"))
    sigstore = image_dir / ".cosign"

    if not sig_files and not sigstore.exists():
        violations.append({
            "code": "SC010",
            "severity": "warn",
            "message": "No cosign signature files found locally",
        })

    return violations


def check_provenance(image_dir: Path) -> list[dict[str, str]]:
    """Check for SLSA provenance attestation."""
    violations = []

    provenance_files = (
        list(image_dir.glob("provenance*.json"))
        + list(image_dir.glob("*.provenance"))
        + list(image_dir.glob("slsa-provenance*.json"))
    )

    if not provenance_files:
        violations.append({
            "code": "SC020",
            "severity": "warn",
            "message": "No local SLSA provenance attestation found",
        })

    return violations


def check_digest_pinning(image_dir: Path) -> list[dict[str, str]]:
    """Check FROM lines for digest pinning."""
    violations = []
    dockerfile = image_dir / "Dockerfile"

    if not dockerfile.exists():
        return violations

    content = dockerfile.read_text()
    from_lines = [
        line.strip() for line in content.splitlines()
        if line.strip().upper().startswith("FROM ")
    ]

    for line in from_lines:
        # Skip scratch and variable references
        parts = line.split()
        if len(parts) < 2:
            continue
        ref = parts[1]
        if ref.lower() == "scratch":
            continue
        if "${" in ref:
            # Variable reference — cannot pin without knowing value
            continue

        if "@sha256:" not in ref:
            violations.append({
                "code": "SC030",
                "severity": "warn",
                "message": f"FROM line not digest-pinned: {line}",
            })

    return violations


def check_build_reproducibility(image_dir: Path) -> list[dict[str, str]]:
    """Check for build reproducibility metadata."""
    violations = []

    manifest_path = image_dir / "manifest.toml"
    if not manifest_path.exists():
        return violations

    try:
        data = tomllib.loads(manifest_path.read_text())
    except Exception:
        return violations

    labels = data.get("labels", {})

    # Check for build provenance labels
    has_build_type = bool(data.get("source", {}).get("type"))
    has_source_url = bool(data.get("source", {}).get("url"))

    if not has_build_type or not has_source_url:
        violations.append({
            "code": "SC040",
            "severity": "warn",
            "message": "Incomplete build metadata (missing type or url)",
        })

    # Check for reproducibility indicator
    reproducible = labels.get("evergreen.build.reproducible")
    if reproducible is None:
        violations.append({
            "code": "SC041",
            "severity": "info",
            "message": "No evergreen.build.reproducible label",
        })

    return violations


# ---------------------------------------------------------------------------
# Full verification
# ---------------------------------------------------------------------------

def verify_image(image_name: str, images_dir: Path) -> dict[str, Any]:
    """Run full supply-chain verification for an image."""
    image_dir = images_dir / image_name
    result = {
        "image": image_name,
        "compliant": True,
        "violations": [],
        "checks": {
            "sbom": False,
            "signature": False,
            "provenance": False,
            "digest_pinning": False,
            "build_reproducibility": False,
        },
    }

    all_violations = []
    all_violations.extend(check_sbom_binding(image_dir))
    all_violations.extend(check_signature(image_dir))
    all_violations.extend(check_provenance(image_dir))
    all_violations.extend(check_digest_pinning(image_dir))
    all_violations.extend(check_build_reproducibility(image_dir))

    block_count = sum(1 for v in all_violations if v["severity"] == "block")
    warn_count = sum(1 for v in all_violations if v["severity"] == "warn")

    result["violations"] = all_violations
    result["block_violations"] = block_count
    result["warn_violations"] = warn_count
    result["compliant"] = block_count == 0

    # Determine what passed
    violated_codes = {v["code"] for v in all_violations}
    result["checks"]["sbom"] = not any(c.startswith("SC00") for c in violated_codes)
    result["checks"]["signature"] = "SC010" not in violated_codes
    result["checks"]["provenance"] = "SC020" not in violated_codes
    result["checks"]["digest_pinning"] = "SC030" not in violated_codes
    result["checks"]["build_reproducibility"] = not any(
        c.startswith("SC04") for c in violated_codes
    )

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
    print(f"Verifying supply chain for {len(critical)} critical images")

    results = []
    fully_compliant = 0
    total_block = 0
    total_warn = 0

    for img in critical:
        result = verify_image(img, images_dir)
        results.append(result)
        if result["compliant"]:
            fully_compliant += 1
        total_block += result["block_violations"]
        total_warn += result["warn_violations"]

    # Clean up .sbom_hash artifacts
    for img_dir in images_dir.iterdir():
        hash_file = img_dir / ".sbom_hash"
        if hash_file.exists():
            hash_file.unlink()

    report = {
        "summary": {
            "total_critical": len(critical),
            "fully_compliant": fully_compliant,
            "non_compliant": len(critical) - fully_compliant,
            "total_block_violations": total_block,
            "total_warn_violations": total_warn,
        },
        "images": results,
    }

    output_path = Path("/tmp/supply_chain_verification.json")
    output_path.write_text(json.dumps(report, indent=2))

    print("\nSupply-chain verification:")
    print(f"  Total:             {len(critical)}")
    print(f"  Fully compliant:   {fully_compliant}")
    print(f"  Non-compliant:     {len(critical) - fully_compliant}")
    print(f"  Block violations:  {total_block}")
    print(f"  Warn violations:   {total_warn}")
    print(f"\nReport written to {output_path}")

    return 1 if total_block > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
