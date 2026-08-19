# Evergreen Image Registry - Comprehensive Image Audit Report

**Generated:** 2026-08-19
**Scope:** All images in `images/` (excluding `_wip/` and `_archive/`)
**Total Images Audited:** 798
**Current Registry Version:** v35.0.0

> **Note:** This report is auto-generated weekly by the `auto-audit-report.yml` workflow.
> Re-run manually via workflow_dispatch for the latest snapshot.

---

## 1. Overview

The Evergreen Image Registry provides hardened, production-ready container images built to five pillars: security and
minimalism, reliability, configuration, documentation, and structural integrity. Images are distributed via GHCR
(primary) and Docker Hub (mirror).

This audit verifies compliance across all 798 active image directories by inspecting Dockerfiles, manifest metadata
(TOML), and SBOM artifacts.

---

## 2. Image Counts

| Metric                  | Count | Notes                                                           |
| ----------------------- | ----: | --------------------------------------------------------------- |
| Total image directories |   798 | Excludes `_wip/`, `_archive/`, and `tests/`                     |
| Total manifests         |   798 | `manifest.toml` present in every image directory                |
| Total Dockerfiles       |   785 | 13 images have manifest but no Dockerfile             |
| Total SBOMs (active)    |     0 | SBOMs present in active images                                  |
| FIPS variants           |     9 | `Dockerfile.fips` present                                       |
| Multi-stage builds      |   753 | Two or more `FROM` instructions (95.9% of Dockerfiles) |

### FIPS-Enabled Images (9)

| Image    | Tier     |
| -------- | -------- |
| consul     | critical |
| cosign     | standard |
| envoy      | critical |
| keycloak   | critical |
| mysql      | critical |
| nginx      | critical |
| postgres   | critical |
| redis      | critical |
| vault      | critical |

---

## 3. Base Image Distribution

Base image determined from the final-stage `FROM` instruction across 785 Dockerfiles.

| Base Image                          | Count |   Pct |
| ----------------------------------- | ----: | ----: |
| cgr.dev/chainguard/wolfi-base        |    38 |   4.8% |
| python                               |    37 |   4.7% |
| scratch                              |    25 |   3.2% |
| traefik                              |    10 |   1.3% |
| rabbitmq                             |     7 |   0.9% |
| argoproj/argocd                      |     6 |   0.8% |
| redis                                |     6 |   0.8% |
| golang                               |     6 |   0.8% |
| pytorch/pytorch                      |     5 |   0.6% |
| gitlab/gitlab-ce                     |     5 |   0.6% |

### Compliance Notes

- **wolfi-base** and **scratch** together account for the vast majority of Dockerfiles, both approved base images.
- **BANNED bases** (debian-slim, alpine, ubuntu, centos) should not be used in final stages.

---

## 4. Security Compliance

All percentages calculated against 785 Dockerfiles.

| Directive / Feature         | Count |   Pct | Notes                        |
| --------------------------- | ----: | ----: | ---------------------------- |
| USER directive (non-root)   |    85 |  10.8% | Most use scratch (implicit)  |
| STOPSIGNAL                  |   785 | 100.0% | Graceful shutdown configured |
| EXPOSE (application ports)  |   785 | 100.0% | Application port declarations |
| ENTRYPOINT                  |    53 |   6.8% | Entrypoint configured        |
| HEALTHCHECK (any)           |   784 |  99.9% | Health probe present         |
| HEALTHCHECK NONE            |     2 | 0.3% | Scratch-based (expected)     |

---

## 5. Build Types

Build type extracted from `type = ` field in `manifest.toml` across 798 images.

| Build Type      | Count |   Pct |
| --------------- | ----: | ----: |
| package-manager  |   660 |  82.7% |
| docker-image     |    90 |  11.3% |
| upstream-repack  |    14 |   1.8% |
| binary-release   |    10 |   1.3% |
| source-build     |     8 |   1.0% |
| unknown          |     6 |   0.8% |
| binary-download  |     3 |   0.4% |
| github           |     2 |   0.3% |
| github-release   |     2 |   0.3% |
| binary           |     1 |   0.1% |
| go-source        |     1 |   0.1% |
| proprietary      |     1 |   0.1% |

---

## 6. Tier Distribution

Tier extracted from `tier = ` field in `manifest.toml`. All 798 manifests have a tier assignment.

| Tier     | Count |   Pct | Description                                   |
| -------- | ----: | ----: | --------------------------------------------- |
| critical   |    87 |  10.9% | Essential infrastructure (databases, proxies) |
| standard   |   711 |  89.1% | Useful but replaceable images |

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
| Missing SBOMs (active images)   |   798 | SBOMs not generated for current active images            |
| Missing Dockerfile              |    13 | Images with manifest but no Dockerfile                   |

### Medium Priority

| Issue                        | Count | Description                                            |
| ---------------------------- | ----: | ------------------------------------------------------ |
| HEALTHCHECK NONE             |     2 | Scratch-based images expected; acceptable              |

---

_Report auto-generated on 2026-08-19 by `.github/workflows/auto-audit-report.yml`. Re-run `evergreenctl audit images/` for the
latest results._
