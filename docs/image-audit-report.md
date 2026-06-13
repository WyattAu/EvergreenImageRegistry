# Evergreen Image Registry - Comprehensive Image Audit Report

**Generated:** 2026-06-13 **Scope:** All images in `images/` (excluding `_wip/` and `_archive/`) **Total Images
Audited:** 989 **Current Registry Version:** v30.0.0 (Phase 111)

> **Note:** This report replaces the stale audit originally generated on 2026-05-19 against 841 images. All counts below
> reflect a fresh scan of the current registry (989 images). Four deprecated images -- cayley, meshbird, immudb,
> immudb-proxy -- have been removed since the original audit.

---

## 1. Overview

The Evergreen Image Registry provides hardened, production-ready container images built to five pillars: security and
minimalism, reliability, configuration, documentation, and structural integrity. Images are distributed via GHCR
(primary) and Docker Hub (mirror).

This audit verifies compliance across all 989 active image directories by inspecting Dockerfiles, manifest metadata
(TOML), and SBOM artifacts.

---

## 2. Image Counts

| Metric                  | Count | Notes                                                           |
| ----------------------- | ----: | --------------------------------------------------------------- |
| Total image directories |   989 | Excludes `_wip/`, `_archive/`, and `tests/`                     |
| Total manifests         |   989 | `manifest.toml` present in every image directory                |
| Total Dockerfiles       |   988 | 1 image (`forgejo-runner-image`) has manifest but no Dockerfile |
| Total SBOMs             |   988 | `sbom.spdx.json` (SPDX 2.3); 1 missing (`forgejo-runner-image`) |
| FIPS variants           |     9 | `Dockerfile.fips` present                                       |
| Multi-stage builds      |   900 | Two or more `FROM` instructions (91.1% of Dockerfiles)          |
| Multi-arch manifests    |     0 | No images declare `multiarch = true` in manifest.toml           |

### FIPS-Enabled Images (9)

| Image    | Tier     |
| -------- | -------- |
| consul   | critical |
| cosign   | standard |
| envoy    | critical |
| keycloak | critical |
| mysql    | critical |
| nginx    | critical |
| postgres | critical |
| redis    | critical |
| vault    | critical |

---

## 3. Base Image Distribution

Base image determined from the final-stage `FROM` instruction (excluding intermediate `AS` stages) across 988
Dockerfiles.

| Base Image                          | Count |   Pct |
| ----------------------------------- | ----: | ----: |
| cgr.dev/chainguard/wolfi-base       |   596 | 60.4% |
| scratch                             |   380 | 38.5% |
| gcr.io/distroless/static-debian12   |     3 |  0.3% |
| cgr.dev/chainguard/static           |     2 |  0.2% |
| gcr.io/distroless/nodejs22-debian12 |     1 |  0.1% |
| debian (bookworm-slim)              |     1 |  0.1% |
| Other (all-FROM-as-AS edge cases)   |     5 |  0.5% |

### Compliance Notes

- **wolfi-base** and **scratch** together account for 976 of 988 Dockerfiles (98.8%), both of which are approved base
  images.
- **1 Dockerfile** uses `debian:bookworm-slim` as a final-stage base, which violates the banned-base-image policy
  (debian-slim is banned for final stages). This should be migrated to wolfi-base or a distroless equivalent.
- **5 Dockerfiles** have all `FROM` instructions tagged with `AS` (final stage uses a named alias), making automated
  base-image extraction ambiguous. These include: postgres, mysql, mariadb, mongodb, and others with complex multi-stage
  pipelines.

---

## 4. Security Compliance

All percentages calculated against 988 Dockerfiles.

| Directive / Feature         | Count |   Pct | Missing |
| --------------------------- | ----: | ----: | ------: |
| USER directive (non-root)   |   978 | 99.0% |      10 |
| STOPSIGNAL                  |   978 | 99.0% |      10 |
| EXPOSE (application ports)  |   972 | 98.4% |      16 |
| ENTRYPOINT                  |   946 | 95.7% |      42 |
| HEALTHCHECK (any)           |   987 | 99.9% |       1 |
| Real HEALTHCHECK (not NONE) |   856 | 86.6% |     132 |
| health-shim integration     |   718 | 72.7% |     270 |

### HEALTHCHECK Breakdown

| Type                | Count |   Pct |
| ------------------- | ----: | ----: |
| Real (http/tcp/cmd) |   856 | 86.6% |
| NONE                |   131 | 13.3% |
| Missing entirely    |     1 |  0.1% |

Of the 131 images with `HEALTHCHECK NONE`, most are scratch-based static binaries where the health-shim provides health
probing. The health-shim is integrated in 718 images (72.7%), covering the gap left by distroless images that lack a
shell.

### Images Missing USER Directive (10)

These are primarily base/utility images and RabbitMQ variants:

| Image               | Notes                                   |
| ------------------- | --------------------------------------- |
| distroless          | Base image; runs as non-root by default |
| wolfi-gcc           | Base/toolchain image                    |
| wolfi-jdk           | Base/toolchain image                    |
| wolfi-node          | Base/toolchain image                    |
| wolfi-python        | Base/toolchain image                    |
| rabbitmq-amqp       | Needs USER added                        |
| rabbitmq-delayed    | Needs USER added                        |
| rabbitmq-federation | Needs USER added                        |
| rabbitmq-mqtt       | Needs USER added                        |
| rabbitmq-stomp      | Needs USER added                        |

### Images Missing ENTRYPOINT (42)

42 Dockerfiles lack an `ENTRYPOINT` instruction. These include base images (scratch, distroless, alpine, debian-slim,
musl), architecture targets (aarch64-unknown-linux-musl, amd64, arm64, x86_64-unknown-linux-musl), firmware/OTA images
(athom, esphome-based, espurna, grub, homekit, tasmota, wled, zzh), and utility images (kdb, kdb-plus, ol_fileshare,
repo-security, repo-supervisor, secrets-scanner, secretz, shh, sssd, standard, static-c, upstream, zeromq, zoe,
scratch-base, openjre, courier-authlib, courier-imap, gitlab, pulsar).

---

## 5. Build Types

Build type extracted from `type = ` field in `manifest.toml` across 989 images. Six manifests are missing the type
field.

| Build Type      | Count |   Pct |
| --------------- | ----: | ----: |
| package-manager |   833 | 84.2% |
| docker-image    |   112 | 11.3% |
| source-build    |    11 |  1.1% |
| binary-release  |    11 |  1.1% |
| base-image      |     7 |  0.7% |
| github-release  |     2 |  0.2% |
| github          |     2 |  0.2% |
| apko            |     2 |  0.2% |
| proprietary     |     1 |  0.1% |
| go-source       |     1 |  0.1% |
| git             |     1 |  0.1% |
| exec            |     1 |  0.1% |
| binary-download |     1 |  0.1% |
| binary          |     1 |  0.1% |
| _(untyped)_     |     6 |  0.6% |

### Untyped Images (6)

The following manifests lack a `type = ` field and should be updated:

| Image            |
| ---------------- |
| authentik        |
| authentik-geoip  |
| authentik-proxy  |
| authentik-worker |
| gitlab-operator  |
| postgresql-18    |

---

## 6. Tier Distribution

Tier extracted from `tier = ` field in `manifest.toml`. All 989 manifests have a tier assignment.

| Tier     | Count |   Pct | Description                                   |
| -------- | ----: | ----: | --------------------------------------------- |
| standard |   896 | 90.6% | Useful but replaceable images                 |
| critical |    93 |  9.4% | Essential infrastructure (databases, proxies) |

---

## 7. CI/CD Status

The registry is supported by 13+ GitHub Actions workflows providing build, sign, scan, and automation capabilities.

| Workflow                | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| build-on-push.yml       | Build images on push to main                 |
| build-nightly.yml       | Nightly rebuilds for drift detection         |
| build-on-demand.yml     | Manual/triggered builds                      |
| \_build-reusable.yml    | Core reusable build, push, and sign pipeline |
| cosign-sign.yml         | Cosign image signing                         |
| slsa-provenance.yml     | SLSA provenance generation                   |
| sbom-attestation.yml    | SBOM attestation                             |
| nightly-scan.yml        | Nightly vulnerability scanning               |
| daily-security-scan.yml | Daily security scanning                      |
| auto-bump.yml           | Automatic version bumping                    |
| metrics-report.yml      | Registry metrics reporting                   |

### Signing and Attestation

All published images are signed with cosign and include SLSA provenance and SBOM attestations. The `evergreenctl` tool
(Rust) provides verification:

```bash
evergreenctl verify images/redis/
evergreenctl drift images/nginx/
evergreenctl audit images/
```

### Pre-commit and Pre-push Gates

- 9 pre-commit hooks: hadolint, constraints enforcement, no-alpine check, trailing-whitespace, and others.
- 11-check pre-push quality gate validates Dockerfile standards, manifest consistency, and structural integrity.

---

## 8. Known Issues

### High Priority

| Issue                           | Count | Description                                                      |
| ------------------------------- | ----: | ---------------------------------------------------------------- |
| Missing USER directive          |    10 | 5 base images (expected) + 5 RabbitMQ variants (should be fixed) |
| Missing ENTRYPOINT              |    42 | Base, firmware, and utility images without ENTRYPOINT            |
| Banned base image (debian-slim) |     1 | 1 Dockerfile uses `debian:bookworm-slim` in final stage          |
| Missing build type              |     6 | 6 manifests lack `type = ` field                                 |
| Missing SBOM                    |     1 | `forgejo-runner-image` has no SBOM or Dockerfile                 |
| No multi-arch support           |   989 | Zero images declare `multiarch = true`                           |

### Medium Priority

| Issue                        | Count | Description                                                         |
| ---------------------------- | ----: | ------------------------------------------------------------------- |
| HEALTHCHECK NONE             |   131 | Scratch-based images expected; non-scratch cases should be reviewed |
| Missing HEALTHCHECK entirely |     1 | 1 Dockerfile has no HEALTHCHECK instruction at all                  |
| Missing STOPSIGNAL           |    10 | Graceful shutdown not configured                                    |
| Missing EXPOSE               |    16 | No application port declarations                                    |
| All-FROM-as-AS ambiguity     |     5 | Base image extraction unreliable for complex multi-stage builds     |

### Resolved Since Previous Audit

| Improvement               |       Before |   After |                                  Delta |
| ------------------------- | -----------: | ------: | -------------------------------------: |
| Total images              |          841 |     989 |                                   +148 |
| SBOM coverage             |      970/987 | 988/989 |                             +18, 99.9% |
| HEALTHCHECK NONE          |          539 |     131 |                                   -408 |
| Real HEALTHCHECK          |          447 |     856 |                                   +409 |
| health-shim integration   |          N/A |     718 |                                    New |
| Tier label coverage       | Inconsistent | 989/989 |                                   100% |
| Removed deprecated images |          N/A |       4 | cayley, meshbird, immudb, immudb-proxy |

---

_Report generated on 2026-06-13 via automated scan of `images/` directory. Re-run `evergreenctl audit images/` for the
latest results._
