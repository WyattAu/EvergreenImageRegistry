# Evergreen Image Registry

## Overview

Hardened container images for production: 987 images built non-root, distroless, and fully auditable. Registries:

- GHCR: `ghcr.io/wyattau/evergreenimageregistry/<image>:<version>` (primary)
- Docker Hub: `docker.io/wyattau/<image>:latest` (mirror)

Version: v34.0.0, Phase 130

## Repository Structure

```
images/<name>/
  Dockerfile          # Multi-stage build (builder → scratch/wolfi)
  manifest.toml       # Image metadata (version, tier, source, labels)
  README.md           # Per-image documentation
  sbom.spdx.json      # SPDX 2.3 SBOM
  .dockerignore       # Build context exclusions
```

~987 image directories under `images/`, excluding `_wip/` and `_archive/`.

## Image Standards (5 Pillars)

1. **Security & Minimalism**: Distroless/wolfi-base final stages, non-root (UID 65532), no shells/package managers
2. **Reliability**: HEALTHCHECK mandatory, semver versioning, graceful shutdown
3. **Configuration**: Env vars for all settings, secure defaults, stateless
4. **Documentation**: Per-image README with usage, security, SBOM link
5. **Structural Integrity**: Multi-stage builds, libc consistency, configurable UID

## Build Types

| Type            | Count | Description                             |
| --------------- | ----- | --------------------------------------- |
| binary-download | ~343  | Download pre-built binary from upstream |
| repack          | ~262  | Repackage upstream image with hardening |
| pkg-install     | ~175  | Install via apk/apt packages            |
| source-build    | ~55   | Build from source                       |

## Base Image Hierarchy

```
scratch (static binaries: Go, Rust, C)
  → wolfi-base (Chainguard: glibc + CA certs)
    → distroless (Google: language-specific runtimes)
```

BANNED for final stage: debian-slim, alpine, ubuntu, centos

## Key Tools

- **evergreenctl** (Rust): Image verification, drift detection, Dockerfile generation (20 subcommands)
- **health-shim** (Go): TCP/HTTP health probes for distroless images
- **pre-commit hooks**: 9 hooks (hadolint, constraints, no-alpine, trailing-whitespace)
- **pre-push gate**: 11 quality checks

## CI/CD

13+ GitHub Actions workflows:

- `build-on-push.yml` / `build-nightly.yml` / `build-on-demand.yml`
- `_build-reusable.yml` (core build+push+sign)
- `cosign-sign.yml`, `slsa-provenance.yml`, `sbom-attestation.yml`
- `nightly-scan.yml`, `daily-security-scan.yml`
- `auto-bump.yml`, `metrics-report.yml`

## Tier System

| Tier     | Description                                       | Label                               |
| -------- | ------------------------------------------------- | ----------------------------------- |
| critical | Essential infrastructure (databases, proxies, CI) | `evergreen.image.tier = "critical"` |
| standard | Useful but replaceable                            | `evergreen.image.tier = "standard"` |

## Compliance

- FIPS 140-2/3: 30 images with implementation plans (`compliance/fips/`)
- CIS/STIG: Benchmark scan scripts (`compliance/cis/`, `compliance/stig/`)
- ATO: Controls mapping, SSP, POA&M (`compliance/ato/`)

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

# Build locally
docker build -t evergreen-redis images/redis/
```

## Known Issues

- 426 images have `HEALTHCHECK NONE` (expected: scratch-based with no shell)
- 28 images missing SBOMs (970/987)
- 4 images removed (cayley, meshbird, immudb, immudb-proxy)
- Tier labels inconsistent across manifests (3 competing schemas)
- `docs/image-audit-report.md` is stale (reports on 841 images, current is 987)

## SIS Migration Status

- **68/70 EIR images** available for SimpleInfrastructureStack migration
- 35/38 SIS images (92%) have direct Evergreen equivalents
- Blocking: immich custom postgres (vector extensions), infra-webhook (custom build)
- Docker Hub mirror: `docker.io/wyattau/<image>:latest` for broader ecosystem access
