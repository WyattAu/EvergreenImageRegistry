# Evergreen Image Registry

## Overview

Hardened container images for production: 798 images built non-root, distroless, and fully auditable. Registries:

- GHCR: `ghcr.io/wyattau/evergreenimageregistry/<image>:<version>` (primary)
- Docker Hub: `docker.io/wyattau/<image>:latest` (org mirror)

Version: v35.0.0, Phase 130

## Repository Structure

```
images/<name>/
  Dockerfile          # Multi-stage build (builder → scratch/wolfi)
  manifest.toml       # Image metadata (version, tier, source, labels)
  README.md           # Per-image documentation
  sbom.spdx.json      # SPDX 2.3 SBOM (when present)
  .dockerignore       # Build context exclusions
```

~798 active image directories under `images/`, excluding `_wip/` and `_archive/`.

## Image Standards (5 Pillars)

1. **Security & Minimalism**: Distroless/wolfi-base final stages, non-root (UID 65532), no shells/package managers
2. **Reliability**: HEALTHCHECK mandatory, semver versioning, graceful shutdown
3. **Configuration**: Env vars for all settings, secure defaults, stateless
4. **Documentation**: Per-image README with usage, security, SBOM link
5. **Structural Integrity**: Multi-stage builds, libc consistency, configurable UID

## Build Types

| Type            | Count | Description                             |
| --------------- | ----- | --------------------------------------- |
| package-manager |   660 | Install via apk/apt packages            |
| docker-image    |    90 | Repackage upstream image with hardening |
| upstream-repack |    14 | Repackage upstream with shim            |
| binary-release  |    10 | Download pre-built binary from upstream |
| source-build    |     8 | Build from source                       |
| Other           |    16 | github-release, proprietary, etc.       |

## Base Image Hierarchy

```
scratch (static binaries: Go, Rust, C)
  → wolfi-base (Chainguard: glibc + CA certs)
    → distroless (Google: language-specific runtimes)
```

BANNED for final stage: debian-slim, alpine, ubuntu, centos

## Key Tools

- **evergreenctl** (Rust): Image verification, drift detection, Dockerfile generation (20+ subcommands)
- **health-shim** (Go): TCP/HTTP health probes for distroless images
- **pre-commit hooks**: 9 hooks (hadolint, constraints, no-alpine, trailing-whitespace)
- **pre-push gate**: 12 quality checks

## CI/CD

23 GitHub Actions workflows:

- `build-on-push.yml` / `build-nightly.yml` / `build-on-demand.yml`
- `_build-reusable.yml` (core build+push+sign)
- `cosign-sign.yml`, `slsa-provenance.yml`, `sbom-attestation.yml`
- `nightly-scan.yml`, `daily-security-scan.yml`
- `auto-bump.yml`, `auto-version.yml`, `auto-audit-report.yml`
- `metrics-report.yml`, `registry-index.yml`

## Tier System

| Tier     | Count | Description                                       |
| -------- | ----- | ------------------------------------------------- |
| critical |    87 | Essential infrastructure (databases, proxies)     |
| standard |   711 | Useful but replaceable                            |

## Compliance

- FIPS 140-2/3: 9 images with Dockerfile.fips variants
- CIS/STIG: Benchmark scan scripts (`compliance/cis/`, `compliance/stig/`)
- ATO: Controls mapping, SSP, POA&M (`compliance/ato/`)

## Code Architecture

### Rust (evergreenctl)

28 modules with trait-based constraint system:

```
src/
  cli.rs          # CLI definition + path validation (SRP)
  run.rs          # Command dispatcher (SRP)
  output.rs       # Output formatting utilities (KISS)
  error.rs        # Typed error definitions
  manifest.rs     # TOML manifest parsing
  drift.rs        # Drift detection (uses dockerfile_utils)
  generate.rs     # Dockerfile generation from manifest
  validate_parallel.rs  # Trait-based constraint system (OCP)
  registry_index.rs     # SQLite registry metadata
  dashboard.rs    # HTML dashboard generation
  auto_version.rs # Auto-version pipeline
  ... (28 total)
```

### Python Scripts

30 scripts for automation:

- `generate_audit_report.py` — Auto-generates audit report
- `pre_commit_validator.py` — Dockerfile constraint validation
- `check_upstream_versions.py` — Version drift detection
- `enforce_policy.py` — Policy enforcement

### Test Suites

242 tests across 4 suites:

- Library: 159 unit tests
- Integration: 59 tests
- E2E: 6 tests
- Property-based: 18 tests

## Common Commands

```bash
# Verify an image
evergreenctl verify images/redis/

# Check for drift between manifest and Dockerfile
evergreenctl drift images/nginx/

# Generate Dockerfile from manifest
evergreenctl generate images/postgres/

# Audit all images for stubs/placeholders
evergreenctl audit images/

# Parallel validation (5k+ scale)
evergreenctl validate-parallel images/

# Generate HTML dashboard
evergreenctl dashboard

# Auto-version pipeline
evergreenctl auto-version images/

# Build locally
docker build -t evergreen-redis images/redis/
```

## Known Issues

- 0 SBOMs in active images (197 in `_archive/`)
- 13 images have manifest but no Dockerfile
- Tier labels standardized but some legacy schemas exist
- CLAUDE.md was stale at 987 images (now accurate at 798)

## SIS Migration Status

- **68/70 EIR images** available for SimpleInfrastructureStack migration
- 35/38 SIS images (92%) have direct Evergreen equivalents
- Blocking: immich custom postgres (vector extensions), infra-webhook (custom build)
- Docker Hub mirror: `docker.io/wyattau/<image>:latest` for broader ecosystem access
