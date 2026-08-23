# Evergreen Image Registry

## Overview

Hardened container images for production: 778 active images built non-root and fully auditable (20 stubs in _wip/). Registries:

- GHCR: `ghcr.io/wyattau/evergreenimageregistry/<image>:<version>` (primary)
- Docker Hub: `docker.io/wyattau/<image>:latest` (org mirror)

Version: v35.0.0, Phase 142 (differentiation moat complete)

## Repository Structure

```
images/<name>/
  Dockerfile          # Multi-stage build (builder → scratch/wolfi)
  Dockerfile.fips     # FIPS 140-2/3 variant (26 implemented, 30 planned)
  Dockerfile.arm64    # ARM64 edge variant
  manifest.toml       # Image metadata (version, tier, source, labels)
  README.md           # Per-image documentation
  sbom.spdx.json      # SPDX 2.3 SBOM (when present)
  .dockerignore       # Build context exclusions
```

~778 active image directories under `images/` (780 total dirs, 20 in `_wip/`, 0 in `_archive/`).

## Image Standards (5 Pillars)

1. **Security & Minimalism**: Non-root (UID 65532) enforced on all images, distroless/wolfi-base preferred for final stages, no shells/package managers
2. **Reliability**: HEALTHCHECK mandatory, semver versioning, graceful shutdown
3. **Configuration**: Env vars for all settings, secure defaults, stateless
4. **Documentation**: Per-image README with usage, security, SBOM link
5. **Structural Integrity**: Multi-stage builds, libc consistency, configurable UID

## Build Types

| Type            | Count | Description                             |
| --------------- | ----- | --------------------------------------- |
| package-manager |   643 | Install via apk/apt packages            |
| docker-image    |    90 | Repackage upstream image with hardening |
| upstream-repack |    14 | Repackage upstream with shim            |
| binary-release  |    10 | Download pre-built binary from upstream |
| source-build    |     8 | Build from source                       |
| Other           |     7 | github-release, go-source, etc.         |

## Base Image Hierarchy

```
scratch (static binaries: Go, Rust, C)
  → wolfi-base (Chainguard: glibc + CA certs)
    → distroless (Google: language-specific runtimes)
```

BANNED for final stage: debian-slim, alpine, ubuntu, centos

## Key Tools

### Core Tooling
- **evergreenctl** (Rust): Image verification, drift detection, Dockerfile generation (20+ subcommands, 20 constraints)
- **health-shim** (Go): TCP/HTTP health probes for distroless images
- **pre-commit hooks**: 13 hooks (hadolint, constraints, no-alpine, trailing-whitespace, prettier, markdownlint, yamllint, etc.)
- **pre-push gate**: 17+ quality checks (Rust tests, clippy, fmt, Python, shell, manifests, SBOMs, drift, constraints, workflow YAML, action SHA pinning, cargo audit, release build, Go vet/test, FIPS, performance regression)

### SBOM & Supply Chain
- **batch_generate_all_sboms.sh**: Full registry SBOM generator (all 798 images, parallel, retry)
- **generate_sbom_attestation.sh**: SBOM attestation signer (in-toto + cosign)
- **sbom_diff.py**: SBOM dependency graph diffing tool (version delta tracking)
- **sbom_dependency_graph.py**: Cross-image dependency tracking + transitive CVE propagation
- **sbom_coverage_report.py**: SBOM coverage metrics + dashboard generator

### Compliance & Security
- **generate_runtime_policy.py**: Runtime policy generator (Seccomp/AppArmor/NetworkPolicy/PSS from SBOM)
- **compliance/cis/generate_xccdf.sh**: SCAP/XCCDF evidence packager for auditors
- **vuln_sla_alert.py**: CVE SLA breach alerting with Slack/PagerDuty
- **generate_soc2_evidence.py**: SOC 2 evidence collection automation
- **policy_test_framework.py**: OPA/Rego policy unit testing framework
- **scanning_marketplace.py**: Multi-scanner consensus (Trivy + Grype)

### Kubernetes & Deployment
- **generate_helm_charts.sh**: Per-image Helm chart generator from library template
- **multi_cloud_auth.sh**: AWS IRSA / GCP Workload Identity / Azure Workload Identity setup
- **generate_arm_variants.sh**: ARM32/ARM64 edge variant builder
- **generate_offline_sboms.sh**: Air-gapped SBOM pre-generation

### Performance & Monitoring
- **build_performance_baselines.py**: Performance baseline builder (build time, size, layers)
- **export_metrics.py**: Prometheus metrics exporter (HTTP server or one-shot)

## CI/CD

40 active GitHub Actions workflows (all valid YAML, all SHA-pinned, 2 disabled):

- **Build:** `build-on-push.yml` / `build-nightly.yml` / `build-on-demand.yml` / `_build-reusable.yml` (core build+push+sign)
- **Supply chain:** `slsa-provenance.yml` (L2), `slsa-provenance-l3.yml` (L3 with hermetic builds), `sbom-attestation.yml`, `sbom-validation.yml`
- **Compliance:** `cis-gate.yml`, `compliance-scan.yml`, `compliance-metrics.yml`
- **Security:** `daily-security-scan.yml`, `nightly-scan.yml`, `vuln-sla-monitor.yml`, `cve-sla-monitor.yml`
- **FIPS:** `fips-build-push.yml` (build+sign FIPS variants)
- **SBOM:** `sbom-full-registry.yml` (parallel batch generation for all 798 images)
- **Versioning:** `auto-bump.yml`, `auto-version.yml`, `upstream-watch.yml`
- **Reporting:** `auto-audit-report.yml`, `metrics-report.yml`, `registry-index.yml`, `image-size-monitor.yml`
- **Multi-arch:** `multi-arch-build.yml` (amd64/arm64/s390x/ppc64le for Tier 1)
- **Performance:** `performance-gate.yml` (build time regression gate)
- **Helm:** `helm-oci-publish.yml` (OCI chart publishing to GHCR)
- **Infra:** `actionlint.yml`, `lint.yml`, `fuzz.yml`, `go-test.yml`, `shim-test.yml`, `deploy-pages.yml`

All GitHub Actions pinned to commit SHA (supply chain security).

## Tier System

| Tier     | Count | Description                                       |
| -------- | ----- | ------------------------------------------------- |
| critical |    87 | Essential infrastructure (databases, proxies)     |
| standard |   691 | Useful but replaceable                            |

## Compliance

- FIPS 140-2/3: 26 images with Dockerfile.fips variants (30-image matrix, 4 planned)
- CIS/STIG: Benchmark scan scripts, SCAP/XCCDF output
- ATO: Controls mapping, SSP, POA&M
- CVE Patch SLA: 4h–30d response by severity/tier (`compliance/cve-patch-sla.md`)
- SOC 2: 45 controls mapped from constraint engine (`compliance/soc2/controls_mapping.yaml`)
- Runtime Policies: Seccomp/AppArmor/NetworkPolicy from SBOM

## Code Architecture

### Rust (evergreenctl)

31 modules with trait-based constraint system + policy engine:
- `validate_parallel.rs` — 20-constraint engine (C001-C020), no repack exemptions
- `policy.rs` — OPA/Rego policy-as-code engine (13 built-in policies + 3 compliance bundles)

### Kubernetes Operator

```
operator/
  main.go                    # Entry point
  Dockerfile                 # Container image (distroless)
  api/v1/
    evergreenimage_types.go  # Image tracking CRD
    evergreenpolicy_types.go # Compliance policy CRD
    evergrendrift_types.go   # Drift alert CRD
  controllers/
    evergreenimage_controller.go  # Auto-update reconciler
    drift_controller.go           # Drift detection
    compliance_controller.go      # Policy enforcement
  webhooks/
    admission_webhook.go          # Pod validation webhook
```

CRDs: `EvergreenImage`, `EvergreenPolicy`, `EvergreenDrift`

### Policy Engine (OPA/Rego)

13 built-in Rego policies + 3 compliance bundles:
- Dockerfile Security: Alpine/debian-slim/root detection
- Supply Chain: SBOM, digest pinning, secrets
- Base Image: Approved base image allowlist
- Non-root: USER 65532 enforcement
- Healthcheck: HEALTHCHECK requirement
- FIPS: Matrix compliance
- License: No GPL in Tier 1
- Vulnerability: Critical CVE threshold
- Size: Image size limit
- Labels: OCI label requirement
- **PCI DSS v4.0**: 12 controls (Req 2, 4, 6, 7, 8, 10, 11, 12)
- **HIPAA**: 10 controls (§164.312 access/audit/integrity/auth/TLS)
- **FedRAMP**: 20 controls (NIST 800-53 AC/AU/CM/IA/RA/SC/SI)

### Helm Charts

Library chart + 87 per-image charts published to GHCR OCI registry.

### Test Suites

261 tests across 3 suites (all passing) + policy test framework.

## Common Commands

```bash
# SBOM generation
./scripts/batch_generate_all_sboms.sh --parallel 4
python3 scripts/sbom_coverage_report.py --dashboard docs/sbom-coverage.md

# SBOM analysis
python3 scripts/sbom_diff.py --old v1.json --new v2.json
python3 scripts/sbom_dependency_graph.py --shared --package openssl

# Compliance
python3 scripts/generate_soc2_evidence.py --gap-analysis
./compliance/cis/generate_xccdf.sh --all
python3 scripts/vuln_sla_alert.py --check --slack $WEBHOOK

# Policy
python3 scripts/policy_test_framework.py --test
python3 scripts/generate_runtime_policy.py --image redis --type all

# Helm
./scripts/generate_helm_charts.sh --tier1 --publish
helm install redis oci://ghcr.io/wyattau/evergreenimageregistry/charts/redis

# Performance
python3 scripts/build_performance_baselines.py --tier1 --compare

# Multi-cloud
./scripts/multi_cloud_auth.sh --provider aws
./scripts/multi_cloud_auth.sh --verify

# Scanning
python3 scripts/scanning_marketplace.py --image redis --scanner all

# Edge
./scripts/generate_arm_variants.sh --tier1 --arch arm64 --edge-profile
./scripts/generate_offline_sboms.sh --tier1 --output /opt/offline-sboms/

# Smoke testing
./scripts/smoke_test.sh                          # Test all images
./scripts/smoke_test.sh redis nginx grafana      # Test specific images
./scripts/smoke_test.sh --tier critical           # Test critical-tier only

# VEX generation
python3 scripts/generate_missing_vex.py           # Generate VEX for images without it

# Non-root enforcement
python3 scripts/enforce_nonroot.py                # Add USER 65532 to all repack images
python3 scripts/enforce_nonroot.py --dry-run      # Preview changes
```

## Validation Status (Phase 142)

| Metric | Value |
|--------|-------|
| Total images | 778 |
| Non-root compliance | **100%** (778/778 enforced) |
| BLOCK violations | **0** (C003 no repack exemption) |
| WARN violations | 835 |
| INFO violations | 35 |
| SBOM coverage | **100%** (778/778) |
| VEX documents | **87** (all critical-tier) |
| Digest-pinned FROM lines | **126** (critical-tier) |
| CI workflows | **40** (all valid, all SHA-pinned) |
| Tests | **261/261 passing** |
| FIPS variants | 26 implemented, 30 planned |
| Helm charts | 87 per-image + library chart |
| Wolfi-base variants | **14** (all build+run verified) |
| K8s CRDs | 3 + admission webhook |
| Rego policies | **16** (13 built-in + 3 compliance bundles) |
| Scripts | **82** automation scripts |

### Competitive Scorecard

| Dimension | EIR | Wolfi | UBI | Distroless | Bitnami |
|-----------|-----|-------|-----|------------|---------|
| Image breadth | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ |
| Security hardening | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Supply chain | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Compliance tooling | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ |
| Operational tooling | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ | ⭐⭐⭐ |
| Enterprise readiness | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| K8s integration | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| FIPS coverage | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ |
| **Overall** | **⭐⭐⭐⭐½** | **⭐⭐⭐** | **⭐⭐⭐⭐** | **⭐⭐⭐** | **⭐⭐⭐⭐** |

### Unique Capabilities (No Competitor Matches)

1. **K8s Operator** — Auto-update + drift detection + compliance enforcement + admission webhook
2. **SBOM Dependency Graph** — Cross-image package tracking + transitive CVE propagation
3. **Performance Regression Gate** — Build time baselines with threshold blocking
4. **Policy-as-Code Marketplace** — PCI DSS / HIPAA / FedRAMP Rego bundles + test framework
5. **Runtime Policy Generator** — SBOM → Seccomp/AppArmor/NetworkPolicy/PSS
6. **SBOM Diffing** — Version delta tracking with Prometheus metrics
7. **Automated CIS/STIG + SCAP/XCCDF** — No other registry has this
8. **Multi-Scanner Consensus** — Trivy + Grype for reduced false positives
9. **Multi-Cloud Auth** — AWS IRSA / GCP Workload Identity / Azure Workload Identity
10. **Edge Computing** — ARM32/ARM64 variants + minimal images + offline SBOMs

## Known Issues

- 2 images have FIPS-only Dockerfile.fips (no regular Dockerfile): postgresql, kubescape
- Tier labels standardized but some legacy schemas exist
- All 778 images have real SBOMs with package data
- 4 FIPS variants remaining (ScyllaDB, Falco blocked upstream; tempo, OPA not in registry)
- Digest pinning: 126/778 (16%) — critical tier partially complete
- 5 images with ARG-based FROM lines (envoy, freshrss, jenkins, paperless-ngx, postgres)
- K8s operator needs kubebuilder code generation (`make generate manifests`)
- 778/778 images have USER 65532:65532 (enforced by C003 without repack exemption)
- 14 wolfi-base variants verified: build ✅, run ✅, non-root ✅

## Monitoring & Metrics

- **Prometheus exporter**: 20+ metrics, HTTP or one-shot
- **Grafana dashboards**: 3 dashboards (image-registry, shim-metrics, compliance)
- **CVE SLA tracking**: Automated daily checks with Slack/PagerDuty alerts
- **Performance baselines**: Build time tracking with regression detection
- **Dependency graph**: Cross-image package analysis

## SIS Migration Status

- **68/70 EIR images** available for SimpleInfrastructureStack migration
- 35/38 SIS images (92%) have direct Evergreen equivalents
- Blocking: immich custom postgres (vector extensions), infra-webhook (custom build)
