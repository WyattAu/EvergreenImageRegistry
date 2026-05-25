# Evergreen Image Registry -- Documentation

## Image Catalog

- [Full Image Catalog](catalog/index.html) -- 998 images with search, tier filtering, and version tracking.

## Standards and Policies

- [Security Standards](standards.md) -- Supply chain hardening, SBOM/SPDX compliance, digest pinning, vulnerability
  management.
- [Dockerfile Standards](dockerfile-standards.md) -- Security constraints (C001-C030), base image rules, HEALTHCHECK
  requirements, libc policies.

## CI/CD

- [CI/CD Pipeline Guide](ci-pipeline-guide.md) -- Tier-aware build pipeline, nightly rebuilds, SBOM generation, Cosign
  signing, multi-arch support.
- [Image Audit Report](image-audit-report.md) -- Results of the comprehensive image audit.

## Observability

- [Observability](observability.md) -- Health check strategies, Prometheus metrics, health-shim integration, Grafana
  dashboards.
- [Metrics Dashboard](metrics-dashboard.md) -- Operational metrics and dashboard configuration.
- [Reproducibility](reproducibility.md) -- Reproducible build guarantees, SOURCE_DATE_EPOCH, layer determinism.

## Operations

- [Common Problems](common-problems.md) -- Build failures, version mismatch resolution, Dockerfile debugging guide.
- [Dockerfile Bugs Found](dockerfile-bugs-found.md) -- Catalog of bugs discovered during the audit campaign.
- [Contributing Guide](contributing_guide.md) -- How to add images, follow the 11-gate quality check, pre-commit hooks,
  manifest standards.

## Internal Reports

- [SIS Migration Readiness](sis-migration-readiness.md) -- Migration assessment for legacy image sets.
- [SIS Deployment Lessons](sis-deployment-lessons.md) -- Operational lessons from production deployment.
