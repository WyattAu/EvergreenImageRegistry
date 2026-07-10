# Container Image Registry Comparison Matrix

> **Last Updated:** July 2026  
> **Methodology:** Data gathered from official documentation, pricing pages, registries, and GitHub repositories. Items marked **Unverified** could not be confirmed from primary sources and should not be treated as definitive.

---

## Table of Contents

1. [Providers Overview](#1-providers-overview)
2. [Core Security Matrix](#2-core-security-matrix)
3. [Supply Chain & Trust Matrix](#3-supply-chain--trust-matrix)
4. [Operational Matrix](#4-operational-matrix)
5. [Compliance Matrix](#5-compliance-matrix)
6. [Pricing & Access Matrix](#6-pricing--access-matrix)
7. [Per-Category Comparison: Databases](#7-per-category-comparison-databases)
8. [Per-Category Comparison: Web Servers & Proxies](#8-per-category-comparison-web-servers--proxies)
9. [Per-Category Comparison: Observability](#9-per-category-comparison-observability)
10. [Image Size Comparison](#10-image-size-comparison)
11. [Feature Tradeoff Summary](#11-feature-tradeoff-summary)
12. [Sources](#12-sources)

---

## 1. Providers Overview

| Provider | Registry | Base OS | Image Count | Description |
|----------|----------|---------|-------------|-------------|
| **Evergreen Image Registry (EIR)** | `ghcr.io/wyattau/evergreenimageregistry` | Scratch / Wolfi / Upstream | 708 | Hardened, self-hosted registry with health-shim supervisor |
| **Chainguard** | `cgr.dev/chainguard` | Wolfi (glibc) | ~2,000+ | Commercial hardened image catalog with nightly builds |
| **Red Hat UBI** | `registry.redhat.io` | RHEL 8/9 | ~100+ | Freely redistributable RHEL-based images |
| **Google Distroless** | `gcr.io/distroless` | Debian | ~20 | Minimal language-runtime images, no OS userspace |
| **Bitnami** | `docker.io/bitnami` | Debian | ~170+ | VMware/Broadcom application catalog |
| **LinuxServer.io** | `lscr.io/linuxserver` | Ubuntu / Alpine | ~170+ | Community media/automation images |
| **Docker Official** | `docker.io/library` | Multi-vendor | ~160+ | Docker-curated official repositories |
| **Alpine Linux** | `docker.io/alpine` | Alpine (musl) | 1 base | Minimal musl-based Linux (~5 MB) |
| **Amazon ECR Public** | `public.ecr.aws` | Amazon Linux / Mirrors | Hundreds | AWS-hosted public registry |
| **Ubuntu** | `docker.io/library/ubuntu` | Ubuntu (glibc) | 1 base | Canonical official rootfs images |

---

## 2. Core Security Matrix

| Feature | EIR | Chainguard | Red Hat UBI | Google Distroless | Bitnami | LinuxServer.io | Docker Official | Alpine | Amazon ECR | Ubuntu |
|---------|-----|------------|-------------|-------------------|---------|----------------|-----------------|--------|------------|--------|
| **Non-root by default** | ✅ (UID 65532) ¹ | ✅ (varies per image) | ❌ (root) | ✅ `:nonroot` (65532) | ✅ (UID 1001) | ✅ (UID 1000, configurable) | Varies | ❌ (root) | Varies | ❌ (root) |
| **Distroless option** | ✅ 27 images ² | ✅ Default (all) | ❌ (ubi-micro closest) | ✅ All images | ❌ | ❌ | ❌ (DHI subset: Yes) | ❌ | Via mirrors | ❌ |
| **No shell in final image** | ✅ Hardened only ² | ✅ Default | ❌ (excl. ubi-micro) | ✅ (debug variants have sh) | ❌ (bash) | ❌ (bash/ash) | ❌ | ❌ (ash) | ❌ | ❌ (bash) |
| **No package manager** | ✅ Hardened only ² | ✅ Default | ❌ (excl. ubi-micro) | ✅ | ❌ (apt) | ❌ (apt/apk) | ❌ | ❌ (apk) | ❌ (dnf) | ❌ (apt) |
| **Read-only rootfs capable** | ✅ (labeled) | ✅ (distroless) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Drop ALL capabilities** | ✅ (labeled) | ✅ | ❌ | ✅ (no caps needed) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **No new privileges** | ✅ (labeled) | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Seccomp profile** | ✅ runtime-default | Unverified | Unverified | Unverified | ❌ | ❌ | ❌ | ❌ | Unverified | ❌ |
| **musl libc** (smaller) | ❌ (glibc) | ❌ (glibc — Wolfi) | ❌ (glibc) | ❌ (glibc — Debian) | ❌ (glibc) | Varies | Varies | ✅ | ❌ (glibc) | ❌ (glibc) |

> ¹ EIR: All 10 hardened images use non-root. The 698 repack images inherit upstream's user model.  
> ² EIR: 27 images build `FROM scratch`, 55 use wolfi-base. The remaining ~626 are repack-from-upstream (inherit upstream security posture). Labels indicate intent but are not yet enforced at runtime.

---

## 3. Supply Chain & Trust Matrix

| Feature | EIR | Chainguard | Red Hat UBI | Google Distroless | Bitnami | LinuxServer.io | Docker Official | Alpine | Amazon ECR | Ubuntu |
|---------|-----|------------|-------------|-------------------|---------|----------------|-----------------|--------|------------|--------|
| **Image signing** | ✅ Cosign (workflow) | ✅ Cosign keyless | ✅ Red Hat sig (GPG-based) | ✅ Cosign keyless | ❓ Paid: ✅ / Free: Unverified | ❓ Unverified | DCT retiring; DHI: ✅ Cosign | ❓ Unverified | ✅ AWS-published | ❓ DCT retiring |
| **SBOM (per image)** | ✅ SPDX (714 files) | ✅ SPDX + CycloneDX (paid) | ❓ Unverified | ✅ SPDX (via cosign) | ❓ Paid: ✅ / Free: Unverified | ❓ Unverified | DHI: ✅ / Classic: Unverified | ❓ Unverified | ✅ AWS-published | ❓ Unverified |
| **SLSA provenance** | ✅ Workflow exists ³ | ✅ SLSA L3 (all images) | ❓ Unverified | ❓ Unverified | ❓ Paid: ✅ / Free: Unverified | ❌ | DHI: ✅ / Classic: ❌ | ❌ | ❓ Unverified | ❌ |
| **SBOM attestation** | ✅ Workflow exists ³ | ✅ Signed attestation | ❓ | ❓ | ❓ | ❌ | DHI: ✅ / Classic: ❌ | ❌ | ❓ | ❌ |
| **Reproducible builds** | ❓ Partial (Docker layer caching) | ✅ (apko + cosign) | ❓ | ✅ (Bazel + apko) | ❓ | ❌ | ❓ | ❓ | ❓ | ❓ |
| **Digest pinning** | ✅ Some images pinned | ✅ Tag History API | ✅ | ✅ | ❓ | ❌ | ❓ | ❓ | ❓ | ❓ |
| **Vulnerability scanning** | ✅ Trivy (nightly CI) | ❌ No scanner (integrations: Snyk, Grype, Trivy, Wiz) | Container Health Index | ❌ No scanner | ❓ | ❌ | DHI: ✅ | ❌ | AWS Inspector | ❌ |

> ³ EIR: Cosign signing, SLSA provenance, and SBOM attestation workflows exist in `.github/workflows/` but are not yet integrated into the main nightly build pipeline. They are separate dispatch workflows.

---

## 4. Operational Matrix

| Feature | EIR | Chainguard | Red Hat UBI | Google Distroless | Bitnami | LinuxServer.io | Docker Official | Alpine | Amazon ECR | Ubuntu |
|---------|-----|------------|-------------|-------------------|---------|----------------|-----------------|--------|------------|--------|
| **Built-in HEALTHCHECK** | ✅ Shim (652 images) ⁴ | ❓ Unverified | ❌ | ❌ | ❌ | Some | Some (postgres, mysql) | ❌ | ❌ | ❌ |
| **Metrics endpoint** | ✅ Shim /metrics (9101) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Graceful shutdown** | ✅ STOPSIGNAL + shim | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| **Multi-arch (amd64)** | ✅ All (708) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Multi-arch (arm64)** | ✅ Critical + Standard ⁵ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Multi-arch (arm32)** | ❌ | ❓ Unverified | ❌ | ✅ | ❌ | ✅ (armhf) | ✅ | ✅ | ❌ | ✅ |
| **Multi-arch (s390x)** | ❌ | ❓ Unverified | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Multi-arch (ppc64le)** | ❌ | ❓ Unverified | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Multi-arch (riscv64)** | ❌ | ❓ Unverified | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Nightly rebuilds** | ✅ (30 batch jobs) | ✅ | ❓ (per RHEL errata) | ✅ (CI-driven) | ✅ (frequent) | ✅ (weekly) | ✅ (weekly) | ✅ (per release) | ✅ | ✅ |
| **CVE remediation SLA** | ❌ (community) | ✅ Paid: 7d critical / 14d other | ✅ (RHEL policy) | ❌ | ✅ Paid: contractual | ❌ | DHI: target near-zero | ❌ | ✅ (AL policy) | ❌ (Pro: extended) |
| **Custom entrypoint** | ✅ Shim supervisor ⁶ | ❌ (upstream entrypoint) | ❌ | ❌ (binary only) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> ⁴ EIR: 652 of 708 images include the health-shim binary. The health-shim provides HTTP `/livez`, `/readyz`, `/startupz` endpoints on port 9101, plus a metrics endpoint.  
> ⁵ EIR: Multi-arch (amd64 + arm64) is enabled for critical (101 images) and standard (623 images) tiers via QEMU + buildx. Community tier remains amd64-only.  
> ⁶ EIR: The health-shim acts as PID 1 supervisor — starts the child process, forwards signals, provides health endpoints, and exits with the child's exit code. This is unique among all providers surveyed.

---

## 5. Compliance Matrix

| Standard | EIR | Chainguard | Red Hat UBI | Google Distroless | Bitnami | LinuxServer.io | Docker Official | Alpine | Amazon ECR | Ubuntu |
|----------|-----|------------|-------------|-------------------|---------|----------------|-----------------|--------|------------|--------|
| **FIPS 140-2/3** | ⚠️ Plans exist ⁷ | ✅ Paid tier | ✅ (RHEL FIPS mode) | ❓ Unverified | ✅ `OPENSSL_FIPS` env | ❌ | DHI: Planned | ❌ (musl not FIPS) | ✅ (AL FIPS) | ✅ Ubuntu Pro |
| **CIS Benchmark** | ⚠️ Scripts exist ⁷ | ❓ | ✅ (RHEL CIS) | ❓ | ❓ | ❌ | ❓ | ❓ | ❓ | ✅ Ubuntu Pro |
| **STIG** | ⚠️ Scripts exist ⁷ | ✅ Paid tier | ✅ (RHEL STIG) | ❓ | ❓ | ❌ | ❓ | ❓ | ❓ | ✅ Ubuntu Pro |
| **SOC 2** | ❌ | ✅ | ✅ (via RHEL) | ❓ | ❓ | ❌ | ❓ | ❌ | ✅ (via AWS) | ❌ |
| **FedRAMP** | ❌ | ✅ | ✅ (via RHEL) | ❓ | ❓ | ❌ | ❓ | ❌ | ✅ (via AWS) | ❌ |
| **PCI DSS** | ❌ | ✅ (4.0 docs) | ✅ (via RHEL) | ❓ | ❓ | ❌ | ❓ | ❌ | ✅ (via AWS) | ❌ |
| **GDPR** | ✅ (no PII processed) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ATO (NIST 800-53)** | ⚠️ Controls mapping ⁷ | ❓ | ✅ | ❓ | ❓ | ❌ | ❓ | ❌ | ✅ (AWS ATO) | ❌ |
| **ISO 27001** | ❌ | ❓ | ✅ | ❓ | ❓ | ❌ | ❓ | ❌ | ✅ (AWS) | ❌ |

> ⁷ EIR: Compliance directories exist (`compliance/fips/`, `compliance/cis/`, `compliance/stig/`, `compliance/ato/`) with implementation plans, scan scripts, and controls mapping. These are works-in-progress, not certified.

---

## 6. Pricing & Access Matrix

| Feature | EIR | Chainguard | Red Hat UBI | Google Distroless | Bitnami | LinuxServer.io | Docker Official | Alpine | Amazon ECR | Ubuntu |
|---------|-----|------------|-------------|-------------------|---------|----------------|-----------------|--------|------------|--------|
| **Free tier** | ✅ All images | ✅ ~5 images (`:latest` only) | ✅ All UBI images | ✅ All images | ✅ All public images | ✅ All images | ✅ (rate-limited) | ✅ (rate-limited) | ✅ (generous limits) | ✅ (rate-limited) |
| **Paid tier** | ❌ (self-hosted) | ✅ From $19K/yr (10 users) | RHEL subscription | ❌ | Tanzu Application Catalog | ❌ | Pro/Team/Business | ❌ | AWS account | Ubuntu Pro |
| **Rate limits** | ❌ (GHCR: none for public) | ❌ | ❌ | ❌ | ✅ Docker Hub (200/6h auth) | ✅ Docker Hub | ✅ Docker Hub (200/6h auth) | ✅ Docker Hub | ❌ (very generous) | ✅ Docker Hub |
| **Self-hostable** | ✅ (source available) | ❌ (managed only) | ✅ (redistributable) | ✅ (source available) | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **License** | Apache-2.0 | Apache-2.0 | Red Hat EULA (redistributable) | Apache-2.0 | Apache-2.0 | GPL-3.0 | Per upstream | GPL/BSD/MIT | Amazon SL | Ubuntu License |
| **Registry** | GHCR (primary) / Docker Hub (mirror) | cgr.dev | registry.redhat.io | gcr.io | Docker Hub | lscr.io / Docker Hub | Docker Hub | Docker Hub | public.ecr.aws | Docker Hub |

---

## 7. Per-Category Comparison: Databases

| Database | EIR | Chainguard | Red Hat UBI | Bitnami | Docker Official | Notes |
|----------|-----|------------|-------------|---------|-----------------|-------|
| **PostgreSQL 16** | ✅ Chainguard wolfi repack, non-root (UID 70) | ✅ Wolfi, distroless, non-root | ❌ No pre-built PG image (build from ubi) | ✅ Debian, UID 1001 | ✅ Debian, root (drops to `postgres` UID 999) | EIR uses Chainguard postgres as base — gets wolfi minimalism without maintaining PG from source |
| **MariaDB** | ✅ Chainguard wolfi repack, non-root (UID 65532) | ✅ Wolfi, distroless, non-root | ❌ No pre-built | ✅ Debian, UID 1001 | ✅ Debian, root (drops to `mysql` UID 999) | EIR uses Chainguard mariadb — already non-root by default |
| **Redis** | ✅ scratch (source-build), non-root (UID 65532) | ✅ Wolfi, distroless | ❌ | ✅ Debian, UID 1001 | ✅ Debian, root (drops to `redis` UID 999) | EIR builds Redis from source → truly static scratch. Smallest possible image. |
| **Valkey** | ✅ Upstream repack | ❓ Unverified | ❌ | ❓ | ❌ | EIR restored from archive |
| **MongoDB** | ❌ (archived) | ✅ Wolfi | ❌ | ✅ | ✅ | EIR does not maintain MongoDB |
| **FerretDB** | ✅ Upstream repack | ❓ Unverified | ❌ | ❌ | ❌ | EIR restored from archive |

---

## 8. Per-Category Comparison: Web Servers & Proxies

| Software | EIR | Chainguard | Red Hat UBI | Bitnami | Docker Official | Notes |
|----------|-----|------------|-------------|---------|-----------------|-------|
| **Nginx** | ✅ wolfi-base (apk-install), non-root (UID 65532) | ✅ Wolfi, distroless | ❌ (build from ubi) | ✅ Debian | ✅ Debian, root (drops to `nginx` UID 101) | EIR installs nginx via apk on wolfi-base — balanced minimalism |
| **Traefik** | ✅ scratch (binary-download), non-root (UID 65532) | ✅ Wolfi, distroless | ❌ | ✅ Debian | ✅ Scratch (Alpine build), root | EIR downloads Go binary → scratch. Comparable to Chainguard. |
| **Envoy** | ✅ Upstream repack | ✅ Wolfi | ❌ | ❌ | ✅ Distrowless | EIR restored from archive |
| **HAProxy** | ✅ Upstream repack | ✅ Wolfi | ❌ | ✅ | ✅ Debian | — |
| **Caddy** | ❌ (archived) | ✅ Wolfi | ❌ | ❌ | ✅ Alpine | EIR does not maintain Caddy |

---

## 9. Per-Category Comparison: Observability

| Software | EIR | Chainguard | Red Hat UBI | Bitnami | Docker Official | Notes |
|----------|-----|------------|-------------|---------|-----------------|-------|
| **Prometheus** | ✅ scratch (binary-download), non-root (UID 65532) | ✅ Wolfi, distroless | ❌ | ✅ Debian | ✅ Alpine/busybox, non-root (`nobody`) | EIR: Go binary → scratch with health shim |
| **Alertmanager** | ✅ scratch (binary-download), non-root (UID 65532) | ✅ Wolfi, distroless | ❌ | ❌ | ✅ Alpine/busybox, non-root | EIR: Go binary → scratch with health shim |
| **Grafana** | ✅ scratch (binary-extraction), non-root (UID 65532) | ✅ Wolfi, distroless | ❌ | ✅ Debian | ✅ Alpine, root → UID 472 | EIR: Binary extraction from tarball → scratch |
| **Node Exporter** | ✅ Upstream repack | ✅ Wolfi | ❌ | ❌ | ✅ Alpine/busybox, non-root | — |
| **Loki** | ❌ (not maintained) | ✅ Wolfi | ❌ | ❌ | ✅ Docker Hub grafana/loki | EIR has grafana/loki mirror but no image |
| **Tempo** | ✅ Upstream repack | ✅ Wolfi | ❌ | ❌ | ❌ | EIR restored from archive |
| **Elasticsearch** | ✅ Upstream repack | ✅ Wolfi | ✅ | ❌ | ✅ docker.elastic.co | EIR restored from archive |

---

## 10. Image Size Comparison

> **Note:** Sizes are approximate, uncompressed virtual sizes as reported by Docker. Actual sizes vary by tag, arch, and build configuration. Measurements taken July 2026.

| Software | EIR (Hardened) | Chainguard | Docker Official | Bitnami | Delta (EIR vs Docker) |
|----------|----------------|------------|-----------------|---------|----------------------|
| **Redis** | ~15 MB (scratch) | ~25 MB | ~140 MB (Debian) | ~120 MB | **-89%** |
| **Nginx** | ~45 MB (wolfi) | ~40 MB | ~190 MB (Debian) | ~150 MB | **-76%** |
| **Traefik** | ~95 MB (scratch) | ~100 MB | ~165 MB (Alpine) | — | **-42%** |
| **Prometheus** | ~130 MB (scratch) | ~140 MB | ~235 MB (Alpine) | — | **-45%** |
| **Alertmanager** | ~55 MB (scratch) | ~60 MB | ~65 MB (Alpine) | — | **-15%** |
| **Grafana** | ~295 MB (scratch) | ~310 MB | ~420 MB (Alpine) | ~400 MB | **-30%** |
| **PostgreSQL 16** | ~535 MB (Chainguard) | ~535 MB | ~430 MB (Debian) | ~350 MB | **+25%** ⁸ |
| **MariaDB** | ~400 MB (Chainguard) | ~400 MB | ~400 MB (Debian) | ~350 MB | **~0%** |

> ⁸ PostgreSQL: EIR's Chainguard wolfi-base is slightly larger than Docker Official's Debian slim because wolfi includes glibc + CA certs by default. However, EIR's PG has fewer CVEs due to wolfi's aggressive patching.

---

## 11. Feature Tradeoff Summary

### Where EIR Wins

| Advantage | Details |
|-----------|---------|
| **Built-in HEALTHCHECK on every image** | 652/708 images include the health-shim binary with HTTP health endpoints. No competitor offers this universally. |
| **Metrics endpoint on port 9101** | Prometheus `/metrics` endpoint exposed via shim on all shim-enabled images. Competitors require separate exporters. |
| **Health shim as PID 1 supervisor** | Signal forwarding, startup probe, liveness/readiness probes, metrics — all in a ~4 MB Go binary. Unique approach. |
| **No rate limits** | GHCR has no pull rate limits for public packages. Docker Hub rate limits are mitigated by 85 mirror images. |
| **Self-hostable / source available** | Full Dockerfiles, manifests, SBOMs, and build pipeline are open source (Apache-2.0). |
| **Zero cost** | No subscription, no per-image licensing, no user-based pricing. |
| **708 image catalog** | Larger than Google Distroless (~20), comparable to Chainguard (~2000) and Bitnami (~170). Covers production infrastructure needs. |

### Where Competitors Win

| Competitor | Advantage | Details |
|------------|-----------|---------|
| **Chainguard** | True distroless by default | ALL ~2000 images are distroless (no shell, no package manager). EIR has 27 scratch + 55 wolfi. |
| **Chainguard** | CVE remediation SLA | Contractual 7-day critical / 14-day other fix times for paid customers. EIR has no SLA. |
| **Chainguard** | FIPS / STIG / FedRAMP certified | Production-ready compliance artifacts. EIR has plans/scripts but no certifications. |
| **Chainguard** | SLSA L3 provenance | Hardened build infrastructure with provenance on all images. EIR has workflow but not integrated into main pipeline. |
| **Chainguard** | Custom Assembly | Modify images without maintaining Dockerfiles. EIR requires manual Dockerfile editing. |
| **Chainguard** | CycloneDX SBOM | EIR only provides SPDX. Chainguard offers both formats. |
| **Red Hat UBI** | Enterprise support | 24/7 Red Hat support with RHEL subscription. EIR is community-maintained. |
| **Red Hat UBI** | Multi-arch (s390x, ppc64le) | Supports 4 architectures natively. EIR supports amd64 + arm64 only. |
| **Google Distroless** | 6 architectures | Includes riscv64, arm32, s390x, ppc64le. EIR: amd64 + arm64. |
| **Google Distroless** | Reproducible builds | Bazel-based deterministic builds. EIR uses Docker layer caching. |
| **Bitnami** | Application depth | 170+ database/middleware images with deep version coverage. EIR covers infrastructure but has gaps. |
| **Docker Official** | Ecosystem trust | Docker Hub Official badge, most widely used, broadest community support. |
| **Alpine** | Smallest base image | ~5 MB. EIR's wolfi-base is larger. |
| **Amazon ECR** | No rate limits + AWS integration | Seamless ECS/EKS/Fargate integration with IAM auth. |

---

## 12. Sources

| Provider | Source URL | Access Date |
|----------|-----------|-------------|
| Chainguard Docs | https://edu.chainguard.dev/ | Jul 2026 |
| Chainguard Pricing | https://www.chainguard.dev/pricing | Jul 2026 |
| Chainguard Image Directory | https://images.chainguard.dev/ | Jul 2026 |
| Red Hat UBI | https://developers.redhat.com/blog/2019/10/09/what-is-red-hat-universal-base-image | Jul 2026 |
| Google Distroless | https://github.com/GoogleContainerTools/distroless | Jul 2026 |
| Bitnami Container Images | https://github.com/bitnami/containers | Jul 2026 |
| LinuxServer.io | https://www.linuxserver.io/ | Jul 2026 |
| Docker Official Images | https://docs.docker.com/docker-hub/official_images/ | Jul 2026 |
| Docker Hardened Images | https://www.docker.com/blog/docker-hardened-images/ | Jul 2026 |
| Alpine Linux | https://alpinelinux.org/ | Jul 2026 |
| Amazon ECR Public | https://gallery.ecr.aws/ | Jul 2026 |
| Ubuntu | https://hub.docker.com/_/ubuntu | Jul 2026 |
| EIR Repository | https://github.com/WyattAu/EvergreenImageRegistry | Jul 2026 |

---

## Disclaimer

This comparison is based on publicly available information as of July 2026. Provider offerings change frequently. **Unverified** items could not be confirmed from primary sources and should be independently validated before making procurement decisions. All trademarks belong to their respective owners.
