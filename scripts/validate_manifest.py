#!/usr/bin/env python3
"""
Phase 1 — Canonical manifest.toml contract validator.

Every image directory MUST contain a manifest.toml with these canonical fields.
The contract is the single source of truth for image identity, tier, version,
build type, and security posture.

Canonical schema:
  [metadata]     — name, version, tier, description (required)
                   vendor, source, license, upstream_version (optional)
  [build]        — base, user, stopsignal (required)
  [source]       — type, url (required)
  [runtime]      — entrypoint (required)
  [ports]        — expose (optional)
  [labels]       — OCI + evergreen labels (validated for consistency)

This script:
  - Loads every manifest.toml
  - Validates required fields
  - Normalizes legacy tier values
  - Detects label drift between manifest and Dockerfile
  - Produces a JSON report with per-image outcomes
  - Exits nonzero when any BLOCK condition is found
"""

from __future__ import annotations

import json
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Schema definition
# ---------------------------------------------------------------------------

REQUIRED_METADATA = {"name", "version", "tier", "description"}
REQUIRED_BUILD = {"base", "user", "stopsignal"}
REQUIRED_SOURCE = {"type", "url"}
REQUIRED_RUNTIME = {"entrypoint"}

VALID_TIERS = {"critical", "standard"}
VALID_BUILD_TYPES = {
    "package-manager",
    "docker-image",
    "upstream-repack",
    "binary-release",
    "source-build",
    "github-release",
    "go-source",
}

# Labels that must match manifest fields when present
LABEL_FIELD_MAP = {
    "org.opencontainers.image.title": ("metadata", "name"),
    "org.opencontainers.image.version": ("metadata", "version"),
    "evergreen.image.tier": ("metadata", "tier"),
}

# Banned legacy tier values (numeric, lowercase variants)
LEGACY_TIER_MAP = {
    "1": "critical",
    "2": "standard",
    "tier1": "critical",
    "tier2": "standard",
    "critical-tier": "critical",
    "standard-tier": "standard",
}

BANNED_BASES = {
    "alpine",
    "debian-slim",
    "debian:slim",
    "ubuntu",
    "centos",
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ValidationError:
    severity: str  # "block" | "warn" | "info"
    code: str
    message: str
    field: str | None = None


@dataclass
class ManifestResult:
    image: str
    path: str
    valid: bool = True
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)
    info: list[ValidationError] = field(default_factory=list)
    normalized_tier: str | None = None
    manifest_data: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------

def normalize_tier(raw: str) -> str:
    """Normalize a tier string to canonical form."""
    lower = raw.strip().lower()
    if lower in VALID_TIERS:
        return lower
    if lower in LEGACY_TIER_MAP:
        return LEGACY_TIER_MAP[lower]
    # Try numeric
    if lower.isdigit():
        return LEGACY_TIER_MAP.get(lower, lower)
    return lower


def validate_manifest(data: dict[str, Any], image_name: str) -> list[ValidationError]:
    """Validate a parsed TOML manifest against the canonical schema."""
    errors: list[ValidationError] = []

    # --- metadata section ---
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(ValidationError("block", "M001", "Missing [metadata] section"))
        return errors

    for key in REQUIRED_METADATA:
        if key not in metadata:
            errors.append(
                ValidationError("block", "M002", f"Missing required metadata.{key}", f"metadata.{key}")
            )

    # Tier validation
    raw_tier = metadata.get("tier", "")
    if raw_tier:
        normalized = normalize_tier(str(raw_tier))
        if normalized not in VALID_TIERS:
            errors.append(
                ValidationError("block", "M003", f"Invalid tier: {raw_tier!r}", "metadata.tier")
            )

    # --- build section ---
    build = data.get("build")
    if not isinstance(build, dict):
        errors.append(ValidationError("block", "M010", "Missing [build] section"))
    else:
        for key in REQUIRED_BUILD:
            if key not in build:
                errors.append(
                    ValidationError("block", "M011", f"Missing required build.{key}", f"build.{key}")
                )

        # Banned base images
        base = build.get("base", "")
        if base:
            base_lower = base.split(":")[0].split("@")[0].lower()
            for banned in BANNED_BASES:
                if base_lower == banned or base_lower.endswith("/" + banned):
                    errors.append(
                        ValidationError("block", "M012", f"Banned base image: {base}", "build.base")
                    )

        # Non-root enforcement
        user = build.get("user", "")
        if user and "65532" not in str(user) and "65534" not in str(user) and "nobody" not in str(user):
            errors.append(
                ValidationError("warn", "M013", f"Non-standard USER: {user}", "build.user")
            )

    # --- source section ---
    source = data.get("source")
    if not isinstance(source, dict):
        errors.append(ValidationError("block", "M020", "Missing [source] section"))
    else:
        for key in REQUIRED_SOURCE:
            if key not in source:
                errors.append(
                    ValidationError("block", "M021", f"Missing required source.{key}", f"source.{key}")
                )
        build_type = source.get("type", "")
        if build_type and build_type not in VALID_BUILD_TYPES:
            errors.append(
                ValidationError("warn", "M022", f"Unknown build type: {build_type!r}", "source.type")
            )

    # --- runtime section ---
    runtime = data.get("runtime")
    if not isinstance(runtime, dict):
        errors.append(ValidationError("warn", "M030", "Missing [runtime] section"))
    else:
        for key in REQUIRED_RUNTIME:
            if key not in runtime:
                errors.append(
                    ValidationError("warn", "M031", f"Missing runtime.{key}", f"runtime.{key}")
                )

    # --- labels drift detection ---
    labels = data.get("labels")
    if isinstance(labels, dict):
        for label_key, (section, field_name) in LABEL_FIELD_MAP.items():
            label_val = str(labels.get(label_key, "")).strip()
            section_data = data.get(section, {})
            if isinstance(section_data, dict):
                field_val = str(section_data.get(field_name, "")).strip()
                if label_val and field_val and label_val != field_val:
                    errors.append(
                        ValidationError(
                            "warn", "M040",
                            f"Label drift: {label_key}={label_val!r} vs {section}.{field_name}={field_val!r}",
                            f"labels.{label_key}",
                        )
                    )

    return errors


def load_and_validate(path: Path, image_name: str) -> ManifestResult:
    """Load a manifest.toml and validate it."""
    result = ManifestResult(image=image_name, path=str(path))

    try:
        raw = path.read_bytes()
    except OSError as exc:
        result.valid = False
        result.errors.append(ValidationError("block", "M099", f"Cannot read: {exc}"))
        return result

    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        result.valid = False
        result.errors.append(ValidationError("block", "M098", f"Invalid TOML: {exc}"))
        return result

    result.manifest_data = data

    errors = validate_manifest(data, image_name)
    for e in errors:
        if e.severity == "block":
            result.errors.append(e)
        elif e.severity == "warn":
            result.warnings.append(e)
        else:
            result.info.append(e)

    if result.errors:
        result.valid = False

    raw_tier = data.get("metadata", {}).get("tier", "")
    if raw_tier:
        result.normalized_tier = normalize_tier(str(raw_tier))

    return result


# ---------------------------------------------------------------------------
# Label consistency with Dockerfile
# ---------------------------------------------------------------------------

def check_dockerfile_label_drift(manifest: ManifestResult, images_dir: Path) -> list[ValidationError]:
    """Check for label drift between manifest.toml and Dockerfile labels."""
    warnings = []
    dockerfile = images_dir / manifest.image / "Dockerfile"
    if not dockerfile.exists():
        return warnings

    try:
        df_content = dockerfile.read_text()
    except OSError:
        return warnings

    data = manifest.manifest_data or {}
    labels = data.get("labels", {})
    if not isinstance(labels, dict):
        return warnings

    for label_key, value in labels.items():
        if label_key.startswith("evergreen."):
            if label_key not in df_content:
                warnings.append(
                    ValidationError(
                        "warn", "M041",
                        f"Label {label_key} in manifest but missing from Dockerfile",
                        f"labels.{label_key}",
                    )
                )

    return warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    images_dir = Path("images")
    if not images_dir.is_dir():
        print("ERROR: images/ directory not found", file=sys.stderr)
        return 1

    results: list[ManifestResult] = []
    stats = {"total": 0, "valid": 0, "block": 0, "warn": 0, "info": 0}

    image_dirs = sorted(
        d for d in images_dir.iterdir()
        if d.is_dir()
        and not d.name.startswith("_")
        and (d / "manifest.toml").exists()
    )

    for img_dir in image_dirs:
        stats["total"] += 1
        manifest_path = img_dir / "manifest.toml"
        result = load_and_validate(manifest_path, img_dir.name)

        # Dockerfile label drift check
        df_warnings = check_dockerfile_label_drift(result, images_dir)
        result.warnings.extend(df_warnings)

        results.append(result)

        if result.valid:
            stats["valid"] += 1
        else:
            stats["block"] += 1
        stats["warn"] += len(result.warnings)
        stats["info"] += len(result.info)

    # Output report
    report = {
        "summary": {
            "total_manifests": stats["total"],
            "valid": stats["valid"],
            "block_violations": stats["block"],
            "warn_violations": stats["warn"],
            "info_violations": stats["info"],
        },
        "images": [],
    }

    for r in results:
        entry = {
            "image": r.image,
            "valid": r.valid,
            "normalized_tier": r.normalized_tier,
        }
        if r.errors:
            entry["errors"] = [
                {"code": e.code, "message": e.message, "field": e.field}
                for e in r.errors
            ]
        if r.warnings:
            entry["warnings"] = [
                {"code": e.code, "message": e.message, "field": e.field}
                for e in r.warnings
            ]
        if r.info:
            entry["info"] = [
                {"code": e.code, "message": e.message, "field": e.field}
                for e in r.info
            ]
        report["images"].append(entry)

    output_path = Path("/tmp/manifest_validation.json")
    output_path.write_text(json.dumps(report, indent=2))
    print(f"Manifest validation: {stats['valid']}/{stats['total']} valid")
    print(f"  BLOCK: {stats['block']}  WARN: {stats['warn']}  INFO: {stats['info']}")
    print(f"Report written to {output_path}")

    # Print BLOCK violations for visibility
    if stats["block"] > 0:
        print("\nBLOCK violations:")
        for r in results:
            if not r.valid:
                for e in r.errors:
                    print(f"  {r.image}: [{e.code}] {e.message}")

    return 1 if stats["block"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
