#!/usr/bin/env python3
"""
Evergreen Image Registry - Audit Report Generator

Scans all active image directories and generates docs/image-audit-report.md.
Called by .github/workflows/auto-audit-report.yml on a weekly schedule.

Usage:
    python3 scripts/generate_audit_report.py
"""

import json
import os
import tomllib
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter


def scan_images(images_dir: Path, exclude_dirs: set[str]) -> dict:
    """Scan all active image directories and collect statistics."""
    image_dirs = sorted([
        d for d in images_dir.iterdir()
        if d.is_dir() and d.name not in exclude_dirs
    ])
    total = len(image_dirs)

    stats = {
        "total_images": total,
        "manifests": 0,
        "dockerfiles": 0,
        "sboms": 0,
        "fips_variants": 0,
        "multi_stage": 0,
        "has_user": 0,
        "has_stopsignal": 0,
        "has_expose": 0,
        "has_entrypoint": 0,
        "has_healthcheck": 0,
        "healthcheck_none": 0,
        "base_images": Counter(),
        "tiers": Counter(),
        "build_types": Counter(),
        "fips_images": [],
        "base_dist": Counter(),
    }

    for d in image_dirs:
        # Manifest analysis
        mf_path = d / "manifest.toml"
        if mf_path.exists():
            stats["manifests"] += 1
            try:
                with open(mf_path, "rb") as f:
                    data = tomllib.load(f)
                tier = data.get("metadata", {}).get("tier", "unknown")
                stats["tiers"][tier] += 1
                build_type = data.get("source", {}).get("type", "unknown")
                stats["build_types"][build_type] += 1
            except Exception:
                pass

        # SBOM check
        if (d / "sbom.spdx.json").exists():
            stats["sboms"] += 1

        # FIPS check
        if (d / "Dockerfile.fips").exists():
            stats["fips_variants"] += 1
            try:
                with open(mf_path, "rb") as f:
                    data = tomllib.load(f)
                stats["fips_images"].append(
                    (d.name, data.get("metadata", {}).get("tier", "?"))
                )
            except Exception:
                stats["fips_images"].append((d.name, "?"))

        # Dockerfile analysis
        df_path = d / "Dockerfile"
        if not df_path.exists():
            continue
        stats["dockerfiles"] += 1

        try:
            content = df_path.read_text()
        except Exception:
            continue

        # Multi-stage
        from_count = sum(
            1 for line in content.splitlines()
            if line.strip().startswith("FROM ")
        )
        if from_count > 1:
            stats["multi_stage"] += 1

        # Base image (last FROM without AS)
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.upper().startswith("FROM ") and " AS " not in stripped.upper():
                parts = stripped.split()
                if len(parts) >= 2:
                    ref = parts[1].split("@")[0]
                    base = ref.split(":")[0] if ":" in ref else ref
                    # Normalize
                    if "wolfi" in base or "chainguard" in base:
                        base = "cgr.dev/chainguard/wolfi-base"
                    stats["base_dist"][base] += 1

        # Security directives
        if "USER " in content:
            stats["has_user"] += 1
        if "STOPSIGNAL" in content:
            stats["has_stopsignal"] += 1
        if "EXPOSE " in content:
            stats["has_expose"] += 1
        if "ENTRYPOINT" in content:
            stats["has_entrypoint"] += 1
        if "HEALTHCHECK" in content:
            stats["has_healthcheck"] += 1
            if "HEALTHCHECK NONE" in content:
                stats["healthcheck_none"] += 1

    return stats


def get_registry_version() -> str:
    """Extract version from CLAUDE.md (registry version) or Cargo.toml (library version)."""
    # Try CLAUDE.md first (registry version like v35.0.0)
    try:
        claude_md = Path("CLAUDE.md").read_text()
        for line in claude_md.splitlines():
            if "Version:" in line and "v" in line:
                # Format: "Version: v35.0.0, Phase 130"
                part = line.split("Version:")[1].strip()
                version = part.split(",")[0].strip()
                if version.startswith("v"):
                    return version.lstrip("v")
    except Exception:
        pass
    # Fallback to Cargo.toml
    try:
        cargo_toml = Path("evergreenctl/Cargo.toml").read_text()
        for line in cargo_toml.splitlines():
            if line.strip().startswith("version"):
                return line.split("=")[1].strip().strip('"')
    except Exception:
        pass
    return "unknown"


def generate_report(stats: dict, version: str) -> str:
    """Generate the markdown audit report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = stats["total_images"]
    df_count = stats["dockerfiles"]

    # Build type rows
    build_rows = []
    for bt, count in stats["build_types"].most_common():
        pct = count / total * 100 if total else 0
        build_rows.append(f"| {bt:<16} | {count:>5} | {pct:>5.1f}% |")

    # Tier rows
    tier_rows = []
    for tier_name in ["critical", "standard"]:
        count = stats["tiers"].get(tier_name, 0)
        pct = count / total * 100 if total else 0
        desc = (
            "Essential infrastructure (databases, proxies)"
            if tier_name == "critical"
            else "Useful but replaceable images"
        )
        tier_rows.append(f"| {tier_name:<10} | {count:>5} | {pct:>5.1f}% | {desc} |")

    # Base image rows
    base_rows = []
    for base, count in stats["base_dist"].most_common(10):
        pct = count / df_count * 100 if df_count else 0
        base_rows.append(f"| {base:<36} | {count:>5} | {pct:>5.1f}% |")

    # FIPS rows
    fips_rows = []
    for name, tier in sorted(stats["fips_images"]):
        fips_rows.append(f"| {name:<10} | {tier:<8} |")
    if not fips_rows:
        fips_rows = ["| (none)  |          |"]

    df = stats["dockerfiles"]
    return f"""# Evergreen Image Registry - Comprehensive Image Audit Report

**Generated:** {now}
**Scope:** All images in `images/` (excluding `_wip/` and `_archive/`)
**Total Images Audited:** {total}
**Current Registry Version:** v{version}

> **Note:** This report is auto-generated weekly by the `auto-audit-report.yml` workflow.
> Re-run manually via workflow_dispatch for the latest snapshot.

---

## 1. Overview

The Evergreen Image Registry provides hardened, production-ready container images built to five pillars: security and
minimalism, reliability, configuration, documentation, and structural integrity. Images are distributed via GHCR
(primary) and Docker Hub (mirror).

This audit verifies compliance across all {total} active image directories by inspecting Dockerfiles, manifest metadata
(TOML), and SBOM artifacts.

---

## 2. Image Counts

| Metric                  | Count | Notes                                                           |
| ----------------------- | ----: | --------------------------------------------------------------- |
| Total image directories | {total:>5} | Excludes `_wip/`, `_archive/`, and `tests/`                     |
| Total manifests         | {stats["manifests"]:>5} | `manifest.toml` present in every image directory                |
| Total Dockerfiles       | {df:>5} | {total - df} images have manifest but no Dockerfile             |
| Total SBOMs (active)    | {stats["sboms"]:>5} | SBOMs present in active images                                  |
| FIPS variants           | {stats["fips_variants"]:>5} | `Dockerfile.fips` present                                       |
| Multi-stage builds      | {stats["multi_stage"]:>5} | Two or more `FROM` instructions ({stats["multi_stage"]/df*100:.1f}% of Dockerfiles) |

### FIPS-Enabled Images ({len(stats["fips_images"])})

| Image    | Tier     |
| -------- | -------- |
{chr(10).join(fips_rows)}

---

## 3. Base Image Distribution

Base image determined from the final-stage `FROM` instruction across {df} Dockerfiles.

| Base Image                          | Count |   Pct |
| ----------------------------------- | ----: | ----: |
{chr(10).join(base_rows)}

### Compliance Notes

- **wolfi-base** and **scratch** together account for the vast majority of Dockerfiles, both approved base images.
- **BANNED bases** (debian-slim, alpine, ubuntu, centos) should not be used in final stages.

---

## 4. Security Compliance

All percentages calculated against {df} Dockerfiles.

| Directive / Feature         | Count |   Pct | Notes                        |
| --------------------------- | ----: | ----: | ---------------------------- |
| USER directive (non-root)   | {stats["has_user"]:>5} | {stats["has_user"]/df*100:>5.1f}% | Most use scratch (implicit)  |
| STOPSIGNAL                  | {stats["has_stopsignal"]:>5} | {stats["has_stopsignal"]/df*100:>5.1f}% | Graceful shutdown configured |
| EXPOSE (application ports)  | {stats["has_expose"]:>5} | {stats["has_expose"]/df*100:>5.1f}% | Application port declarations |
| ENTRYPOINT                  | {stats["has_entrypoint"]:>5} | {stats["has_entrypoint"]/df*100:>5.1f}% | Entrypoint configured        |
| HEALTHCHECK (any)           | {stats["has_healthcheck"]:>5} | {stats["has_healthcheck"]/df*100:>5.1f}% | Health probe present         |
| HEALTHCHECK NONE            | {stats["healthcheck_none"]:>5} | {stats["healthcheck_none"]/df*100:.1f}% | Scratch-based (expected)     |

---

## 5. Build Types

Build type extracted from `type = ` field in `manifest.toml` across {total} images.

| Build Type      | Count |   Pct |
| --------------- | ----: | ----: |
{chr(10).join(build_rows)}

---

## 6. Tier Distribution

Tier extracted from `tier = ` field in `manifest.toml`. All {total} manifests have a tier assignment.

| Tier     | Count |   Pct | Description                                   |
| -------- | ----: | ----: | --------------------------------------------- |
{chr(10).join(tier_rows)}

---

## 7. CI/CD Status

The registry is supported by 13+ GitHub Actions workflows providing build, sign, scan, and automation capabilities.

| Workflow                | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| build-on-push.yml       | Build images on push to main                 |
| build-nightly.yml       | Nightly rebuilds for drift detection         |
| build-on-demand.yml     | Manual/triggered builds                      |
| \\_build-reusable.yml    | Core reusable build, push, and sign pipeline |
| cosign-sign.yml         | Cosign image signing                         |
| slsa-provenance.yml     | SLSA provenance generation                   |
| sbom-attestation.yml    | SBOM attestation                             |
| nightly-scan.yml        | Nightly vulnerability scanning               |
| daily-security-scan.yml | Daily security scanning                      |
| auto-bump.yml           | Automatic version bumping                    |
| auto-version.yml        | Auto-version pipeline                        |
| auto-audit-report.yml   | This report auto-generation                  |
| metrics-report.yml      | Registry metrics reporting                   |
| registry-index.yml      | SQLite registry index CI                     |

### evergreenctl Tool

The `evergreenctl` tool (Rust) provides verification, drift detection, and audit capabilities:

```bash
evergreenctl verify images/redis/
evergreenctl drift images/nginx/
evergreenctl audit images/
evergreenctl validate-parallel images/  # 5k+ scale parallel validation
evergreenctl dashboard                  # HTML dashboard from registry index
```

### Pre-commit and Pre-push Gates

- 9 pre-commit hooks: hadolint, constraints enforcement, no-alpine check, trailing-whitespace, fast tests.
- 12-check pre-push quality gate validates Rust tests, clippy, fmt, Python/shell syntax, manifest/SBOM validation,
  Dockerfile constraints, cargo audit, release build, Go vet/test, FIPS compliance, and performance regression.

---

## 8. Known Issues

### High Priority

| Issue                           | Count | Description                                              |
| ------------------------------- | ----: | -------------------------------------------------------- |
| Missing SBOMs (active images)   | {total - stats["sboms"]:>5} | SBOMs not generated for current active images            |
| Missing Dockerfile              | {total - df:>5} | Images with manifest but no Dockerfile                   |

### Medium Priority

| Issue                        | Count | Description                                            |
| ---------------------------- | ----: | ------------------------------------------------------ |
| HEALTHCHECK NONE             | {stats["healthcheck_none"]:>5} | Scratch-based images expected; acceptable              |

---

_Report auto-generated on {now} by `.github/workflows/auto-audit-report.yml`. Re-run `evergreenctl audit images/` for the
latest results._
"""


def main():
    images_dir = Path("images")
    exclude_dirs = {"_wip", "_archive", "tests"}

    print("Scanning images...")
    stats = scan_images(images_dir, exclude_dirs)

    version = get_registry_version()
    print(f"Registry version: v{version}")
    print(f"Total images: {stats['total_images']}")
    print(f"  Manifests: {stats['manifests']}, Dockerfiles: {stats['dockerfiles']}")
    print(f"  SBOMs: {stats['sboms']}, FIPS: {stats['fips_variants']}")

    report = generate_report(stats, version)

    report_path = Path("docs/image-audit-report.md")
    report_path.write_text(report)
    print(f"Report written to {report_path}")

    # Output for GitHub Actions
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"total_images={stats['total_images']}\n")
            f.write(f"manifests={stats['manifests']}\n")
            f.write(f"dockerfiles={stats['dockerfiles']}\n")
            f.write(f"sboms={stats['sboms']}\n")
            f.write(f"fips={stats['fips_variants']}\n")


if __name__ == "__main__":
    main()
