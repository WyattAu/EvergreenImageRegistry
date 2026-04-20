# Yellow Paper: Container Hardening Benchmarks — Industry Analysis

## Document Header

```yaml
---
document_id: YP-CONTAINER-HARDENING-BENCHMARKS-001
version: 1.0.0
status: DRAFT
domain: Container Security
subdomains: [Distroless, Hardening, Supply-Chain, Benchmarks, Best-Practices]
applicable_standards: [NIST SP 800-190, CIS Docker, OCI Image Spec, SLSA 3.0]
created: 2026-04-20
author: Nexus (Principal Systems Architect)
confidence_level: 0.92
tqa_level: 4
---
```

## Executive Summary

This Yellow Paper benchmarks the container image hardening practices of four major projects — Chainguard Wolfi, Bitnami, Google Distroless, and Red Hat UBI — to extract actionable patterns for the EvergreenImageRegistry.

**Key findings:**

| Dimension | Chainguard/Wolfi | Bitnami | Distroless | UBI Minimal |
|-----------|-----------------|---------|------------|-------------|
| **Base Philosophy** | Distroless-first, nightly rebuilds | Security-hardened full apps | Zero OS, app-only | Enterprise RHEL-derived |
| **CVE Approach** | Near-zero via constant rebuilds | Triage + VEX + EPSS | Track Debian security | Extended errata (10yr) |
| **Attack Surface** | Minimal (no shell/pkgmgr) | Moderate (shell + apt) | Minimal (no shell/pkgmgr) | Low (dnf available) |
| **SBOM** | SPDX-2.3, cosign-attached | Commercial, VEX statements | None native | RPM-based, RHEL tools |
| **Signing** | Sigstore/cosign keyless | in-toto attestation | Cosign keyless | Red Hat GPG + Cosign |
| **Non-Root** | Default `nonroot` (65532) | Default UID 1001 | `nonroot` variant | Manual, not default |

**Recommendation for EvergreenImageRegistry:** Adopt the Chainguard/Wolfi model as the primary pattern — declarative image builds via `apko`, distroless by default, nightly rebuilds, SBOM+signing as first-class. Supplement with Bitnami's VEX strategy for vulnerability triage.

**Scope:**
- IN: Image build tooling, CVE remediation, signing, SBOMs, user models, entrypoint patterns, multi-arch, versioning
- OUT: Runtime orchestration, network policies, storage
- ASSUMPTIONS: Linux x86_64/arm64, OCI-compliant registries

---

## Nomenclature

| Symbol | Description | Units | Domain | Source |
|--------|-------------|-------|--------|--------|
| $I_{dist}$ | Distroless image | Boolean | Classification | Analysis |
| $C_{cve}$ | CVE count | Integer | Security | Trivy/Grype |
| $S_{sbom}$ | SBOM presence | Boolean | Compliance | SPDX |
| $S_{sig}$ | Image signature | Boolean | Provenance | Cosign |
| $U_{app}$ | Application UID | Integer | Security | Config |
| $T_{rebuild}$ | Rebuild cadence | Duration | Process | CI/CD |
| $A_{arch}$ | Architecture support | Set | Platform | OCI |
| $V_{vex}$ | VEX statement | Boolean | Triage | OpenVEX |

---

## 1. Per-Project Analysis

### 1.1 Chainguard Wolfi Images

**Organization:** Chainguard (chainguard-images GitHub org)
**Registry:** `cgr.dev/chainguard/*`
**Base OS:** Wolfi (custom "un-distro")
**License:** Apache-2.0

#### 1.1.1 Base Images Provided

| Image | Purpose | libc | Typical Size |
|-------|---------|------|-------------|
| `wolfi-base` | General purpose base | glibc | ~5-10 MB |
| `wolfi-base-static` | Static binary base | musl | ~2 MB |
| `static` | Minimal static binary runtime | musl | ~2 MB |
| `glibc-dynamic` | Dynamic glibc apps | glibc | ~5 MB |
| `gcc-glibc` | C/C++ build toolchain | glibc | ~100 MB |
| `go` | Go compilation | glibc | ~300 MB |
| `python` | Python runtime | glibc | ~30-50 MB |
| `node` | Node.js runtime | glibc | ~50-80 MB |
| `java` (JRE/JDK) | Java runtime/build | glibc | ~80-200 MB |

Special cases: `static`, `busybox`, and `git` use Alpine/musl by default; Wolfi/glibc variants are tagged `:latest-glibc`.

#### 1.1.2 Package Management

Wolfi uses **apk** (Alpine Package Keeper) as its package manager, compatible with the `.apk` package format but using an independent repository at `apk.cgr.dev`.

- **Build tool:** `melange` — builds `.apk` packages from declarative YAML pipelines
- **Image assembler:** `apko` — bundles APKs into OCI images via declarative YAML manifests
- **Package granularity:** Wolfi packages are split into fine-grained sub-packages (e.g., `nginx` vs `nginx-doc` vs `nginx-modules`) to minimize image size
- **No package manager in final image:** Production (distroless) images exclude apk entirely; development variants include it for debugging
- **Version selection:** Packages track latest upstream releases; older versions retained for 6 months in the repository

```yaml
# Example apko image manifest
contents:
  packages:
    - wolfi-base
    - nginx
    - nginx-config
accounts:
  runas: nonroot
  users:
    - name: nonroot
      uid: 65532
entrypoint:
  command: /usr/sbin/nginx -g "daemon off;"
```

#### 1.1.3 Security Features

| Feature | Implementation |
|---------|---------------|
| **Distroless** | No shell (`/bin/sh`, `/bin/bash`) or package manager in production images |
| **Non-root default** | Runs as `nonroot` (UID 65532) by default |
| **Nightly rebuilds** | All images rebuilt from latest sources every night |
| **Meltdown/Spectre** | Mitigated at the glibc/kernel level (host kernel provides protections) |
| **Kernel hardening** | Wolfi has no kernel; relies on host container runtime kernel |
| **Minimal packages** | Only application + runtime dependencies included |
| **FIPS support** | Available via separate FIPS-compliant image variants |
| **STIG compliance** | STIG profiles available for select images |
| **VEX statements** | Security advisories published with OpenVEX via `chainctl` |
| **Vulnerability visualization** | Public CVE comparison dashboards for each image vs alternatives |

#### 1.1.4 Multi-Architecture

All Chainguard Images are published as OCI image indexes supporting:
- `linux/amd64`
- `linux/arm64`
- Some images additionally support `linux/arm/v7`, `linux/ppc64le`, `linux/s390x`

Architecture-specific images are directly referenceable with a suffix (e.g., `:latest-amd64`).

#### 1.1.5 CVE Patching Strategy

- **Nightly full rebuilds** from latest upstream source — this is the primary CVE mitigation mechanism
- **Automated security advisories** published when CVEs affect images
- **EOL grace period** for deprecated software (extended CVE support window)
- **Wolfi Security Feeds** available via `wolfi-dev/advisories` repository
- **Scanner integration** guides for Trivy and Grype with guidance on false positive/negative handling
- **Result:** Chainguard images consistently show near-zero CVEs in public vulnerability comparisons

#### 1.1.6 SBOMs and Signing

**SBOMs:**
- Format: SPDX-2.3
- Generated at build-time by `apko`
- Attached as OCI referrers (attestations)
- Downloadable via `cosign download attestation --predicate-type https://spdx.dev/Document`
- Per-package SBOMs for all Wolfi packages

**Signing:**
- Keyless signing via Sigstore/Cosign
- GitHub Actions workflow identity verified: `certificate-identity=https://github.com/chainguard-images/images/.github/workflows/release.yaml@refs/heads/main`
- OIDC issuer: `https://token.actions.githubusercontent.com`

#### 1.1.7 Entrypoints and Signal Handling

- Entrypoints specified declaratively in `apko` YAML manifests
- Vector form only (no shell wrapping): `["/usr/sbin/nginx", "-g", "daemon off;"]`
- Signal handling delegated to the application itself
- No init system (PID 1 is the application); for proper signal handling, applications must implement their own signal forwarding or use `tini`/`dumb-init` if needed
- Development image variants include busybox shell for debugging

#### 1.1.8 Versioning and Pinning

- **Tags:** `latest`, version-pinned (e.g., `nginx:1.25`), digest-pinnable
- **Unique tags:** Each build gets a unique immutable tag
- **Tag History API:** Available via `chainctl` for tracking image evolution
- **Digest-pinning recommended** for production via `frizbee`/`digestabot` tooling
- **Renovate integration** for automated digest updates

#### 1.1.9 Image Variants

Each image has multiple variants:
- **Production (distroless):** No shell, no package manager — smallest attack surface
- **Development:** Includes shell (busybox) and package manager for debugging
- **Root variants:** Runs as root for use cases requiring it (e.g., binding to port 80)

---

### 1.2 Bitnami Container Images

**Organization:** Bitnami / Broadcom (bitnami/containers GitHub repo)
**Registry:** `docker.io/bitnami/*` (newer: Photon-based BSI images)
**Legacy Registry:** `docker.io/bitnamilegacy/*` (Debian-based)
**License:** Apache-2.0

#### 1.2.1 Base Images

Bitnami has undergone a **major platform migration**:

| Era | Base | Package Manager | Status |
|-----|------|-----------------|--------|
| Legacy | Minideb (custom Debian) | `apt` + install scripts | Archived to `bitnamilegacy/*` |
| Current (BSI) | Photon OS | `tdnf` | Active |

**Minideb (Legacy):**
- Custom minimal Debian image maintained by Bitnami
- Stripped-down to ~80-100 MB base
- Included `apt` but with curated package set
- Install scripts (`install_deps.sh`, `install_app.sh`) for reproducible builds

**Photon OS (Current BSI):**
- VMware's cloud-optimized, security-hardened enterprise Linux
- `tdnf` (Tiny DNF) package manager — fast, lightweight
- FIPS-compliant options available
- STIG-hardened profiles available
- Designed specifically for container workloads

#### 1.2.2 Package Installation (Legacy Minideb Pattern)

```dockerfile
FROM bitnami/minideb:bookworm
# Bitnami's install scripts handle dependency resolution
RUN install_packages libssl3 libxml2
# Custom scripts extract and configure the application
RUN bitnami-pkg unpack nginx-1.25.3-0-linux-amd64-debian-12
```

The Bitnami approach used:
- Pre-built tarball packages (`bitnami-pkg`) containing the application
- `install_packages` helper wrapping `apt-get`
- Layered installs: system deps -> app package -> config -> cleanup

#### 1.2.3 Non-Root Strategy

- **Default user:** UID 1001 (dedicated `bitnami` user)
- Applied via `USER 1001` in Dockerfile
- Filesystem ownership set appropriately for data directories
- Some images require `root` for initial startup then drop privileges (for port binding, etc.)

```dockerfile
RUN useradd -r -u 1001 -g root -s /sbin/nologin bitnami
USER 1001
```

#### 1.2.4 Volumes and Data Persistence

Bitnami images follow a consistent volume pattern:
- `/bitnami/{app}` — application installation directory
- `/bitnami/{app}/data` — persistent data (often a volume)
- `/bitnami/{app}/conf` — configuration files (often mounted)

Helm charts standardize volume mounts with PVC templates and init containers for data initialization.

#### 1.2.5 Entrypoint Pattern

Bitnami uses a **libentrypoint.sh** pattern — a shared entrypoint script library that handles:
- Environment variable parsing and configuration generation
- Runtime configuration (dynamic config file rendering)
- Initialization scripts (in `/docker-entrypoint-initdb.d/` or similar)
- Signal handling (trap-based, forwards SIGTERM to child process)
- Graceful shutdown

```dockerfile
ENTRYPOINT ["/opt/bitnami/scripts/nginx/run.sh"]
CMD ["/opt/bitnami/scripts/nginx/entrypoint.sh"]
```

The `run.sh` script typically:
1. Sources libentrypoint.sh
2. Validates environment variables
3. Dynamically generates config files from templates
4. Executes the application with proper signal forwarding

#### 1.2.6 Configuration Management

- **Environment variables:** Primary configuration mechanism; extensive env var support
- **Configuration files:** Generated at startup from templates
- **Mounted configs:** Support for ConfigMap/Secret mounts via standard paths
- **Helm values:** Helm charts map values.yaml to container env vars

#### 1.2.7 Multi-Stage Builds

Bitnami does NOT use multi-stage builds in the traditional sense. Instead:
- Application is pre-packaged as a `bitnami-pkg` tarball
- Single-stage Dockerfile installs the tarball
- Build dependencies are cleaned up in the same layer

#### 1.2.8 Image Size Optimization

- Minideb base: ~80 MB
- Typical app images: 200-500 MB
- Strategy: Minimal base OS + pre-compiled packages + cleanup steps
- NOT as small as distroless alternatives (trade-off for functionality)

#### 1.2.9 Security Updates

- **Dual scanning:** Trivy + Grype on every PR
- **VEX statements:** Commercial feature — vulnerability triage with VEX, KEV (Known Exploited Vulnerabilities), and EPSS (Exploit Prediction Scoring System) scores
- **Near-zero vulnerability target:** BSI images marketed as having near-zero CVEs
- **SBOMs:** Available (commercial) with secure bill of materials
- **Provenance:** in-toto attestation for supply chain verification
- **Retention policy:** 6-month deprecation window, then archived

#### 1.2.10 Helm Charts and Kubernetes Integration

Bitnami provides **first-class Helm chart support** — this is a major differentiator:
- Helm charts for every containerized application
- Comprehensive `values.yaml` with sensible defaults
- Supports PVC, ConfigMap, Secret, RBAC, ServiceAccount, NetworkPolicy
- Production-ready patterns: anti-affinity, PDB, HPA
- Separate `bitnami/charts` repository

---

### 1.3 Google Distroless

**Organization:** Google (GoogleContainerTools GitHub org)
**Registry:** `gcr.io/distroless/*`, `registry.k8s.io/distroless/*` (k8s)
**Base OS:** Debian 12 (Bookworm) and Debian 13 (Trixie)
**License:** Apache-2.0

#### 1.3.1 Base Images Provided

| Image | Purpose | Size |
|-------|---------|------|
| `static-debian12` | Statically linked binaries | ~2 MB |
| `base-debian12` | Base with CA certs + timezone | ~20 MB |
| `base-nossl-debian12` | Base without OpenSSL | ~18 MB |
| `cc-debian12` | C/C++ runtime (glibc) | ~25 MB |
| `python3-debian12` | Python 3 runtime | ~50 MB |
| `java17-debian13` | Java 17 JRE | ~180 MB |
| `nodejs22-debian13` | Node.js 22 runtime | ~130 MB |

All images also come in `:nonroot` and `:debug` variants:
- `:nonroot` — runs as `nobody` (UID 65534)
- `:debug` — includes busybox shell for debugging
- `:debug-nonroot` — debug + non-root

#### 1.3.2 Build System

- **Bazel** — primary build system (not Dockerfiles)
- `rules_distroless` Bazel rules for custom image composition
- `rules_oci` for OCI image generation
- Debian packages installed via custom Bazel rules (not apt)
- Highly reproducible builds (Bazel's hermeticity)

#### 1.3.3 Distroless Philosophy

The core principle: **"Language focused docker images, minus the operating system."**

$$\text{Distroless} \implies (\nexists \text{/bin/sh} \land \nexists \text{package-manager} \land \nexists \text{init-system})$$

This means:
- No shell (no `/bin/sh`, `/bin/bash`)
- No package manager (no `apt`, `dpkg`)
- No init system (no `systemd`, `sysvinit`)
- Only application + its direct runtime dependencies
- ENTRYPOINT must be in vector form: `["/app"]` not `"app"`

#### 1.3.4 CVE Patching

- Tracks upstream Debian security updates
- GitHub Actions automatically generate PRs when Debian packages update (`.github/workflows/update-deb-package-snapshots.yml`)
- Security updates are pulled from Debian's security repositories
- No nightly full rebuilds — updates are triggered by Debian security releases

#### 1.3.5 SBOMs and Signing

**Signing:**
- Keyless Cosign signing
- Verification: `cosign verify $IMAGE --certificate-oidc-issuer https://accounts.google.com --certificate-identity keyless@distroless.iam.gserviceaccount.com`
- Public key: `cosign.pub` in repository root

**SBOMs:**
- No native SBOM generation (unlike Chainguard)
- Users must generate SBOMs themselves using tools like Syft

#### 1.3.6 Multi-Architecture

Comprehensive multi-arch support:
- Debian 12: `amd64`, `arm64`, `arm/v7`, `s390x`, `ppc64le`
- Debian 13: adds `riscv64`
- Python 3 and Node.js images have more limited arch support

#### 1.3.7 Entrypoints

- No shell means ENTRYPOINT/CMD must be in **vector form**
- No shell-based signal handling — the application must handle signals directly
- For Go binaries compiled with `CGO_ENABLED=0`, signal handling works natively
- JVM images have a default entrypoint: `["java", "-jar", ...]`
- Node.js images have a default entrypoint for running JS files

#### 1.3.8 Debugging

- `:debug` tag adds busybox shell
- Debug variant: `docker run --entrypoint=sh -ti myimage:debug`
- Pattern: `debug-<existing tag>` for combining with other variants (e.g., `:debug-nonroot`)
- `ldd` not included (it's a shell script)

#### 1.3.9 Users and Adopters

- Kubernetes core images (since v1.15)
- Knative
- Tekton
- Teleport

#### 1.3.10 Key Limitations

- No shell makes debugging harder (requires debug variant or sidecar)
- No package manager means no runtime dependency installation
- No init system means PID 1 signal handling responsibility on the app
- Debian-based (not purpose-built for containers)
- No SBOM generation
- No VEX statements

---

### 1.4 Red Hat UBI (Universal Base Image) Minimal

**Organization:** Red Hat
**Registry:** `registry.access.redhat.com/ubi8/*`, `registry.access.redhat.com/ubi9/*`
**Base OS:** RHEL 8/9 stripped down
**License:** Free to use and redistribute (UBI); support requires subscription

#### 1.4.1 Base Images Provided

| Image | Purpose | Size |
|-------|---------|------|
| `ubi8-minimal` | Minimal runtime base | ~80 MB |
| `ubi8` | Standard base | ~210 MB |
| `ubi8-init` | With systemd init | ~230 MB |
| `ubi8-micro` | Ultra-minimal (dnf removed) | ~30 MB |
| `ubi9-minimal` | RHEL 9 minimal | ~80 MB |
| `ubi9-micro` | RHEL 9 ultra-minimal | ~30 MB |

#### 1.4.2 Package Management

- **dnf** (or `microdnf` on minimal/micro images)
- `microdnf` — stripped-down dnf with fewer dependencies
- UBI has access to RHEL package repositories (free content sets)
- Standard `dnf install` workflow for adding packages

```dockerfile
FROM registry.access.redhat.com/ubi9/ubi-minimal
RUN microdnf install -y nginx && microdnf clean all
```

#### 1.4.3 Security Features

| Feature | Implementation |
|---------|---------------|
| **Extended errata** | 10-year security support lifecycle |
| **FIPS compliance** | FIPS-certified crypto modules |
| **STIG profiles** | DISA STIG guides for RHEL |
| **SELinux** | Full SELinux support (labels preserved) |
| **CVE tracking** | Red Hat Security Advisories (RHSA) |
| **Scanning** | Clair integration, Red Hat Insights |
| **GPG signing** | GPG-signed RPM packages and container images |

#### 1.4.4 Non-Root

- NOT default — runs as root by default
- Users must manually configure non-root execution
- OpenShift enforces random UIDs via SCC (Security Context Constraints)

#### 1.4.5 SBOMs and Signing

- **SBOMs:** Generated via RPM metadata; Red Hat provides CVE data per RPM
- **Signing:** GPG signing of container images and RPMs
- **Cosign:** Available for Red Hat container images
- **Provenance:** Not native; would require external tooling

#### 1.4.6 Multi-Architecture

- `linux/amd64` (primary)
- `linux/arm64` (available for UBI 8 and 9)
- `linux/ppc64le`, `linux/s390x` (select images)

#### 1.4.7 Enterprise Integration

- Deep OpenShift integration (default base images)
- Red Hat Insights for vulnerability monitoring
- Ansible Automation Platform integration
- Red Hat Certified Container program for partner images
- Air-gapped installation support

#### 1.4.8 Key Strengths

- Enterprise support with SLA
- 10-year lifecycle (predictable security updates)
- FIPS compliance for regulated industries
- SELinux labels preserved
- Broad ecosystem of certified partner containers

#### 1.4.9 Key Limitations

- Larger image sizes than distroless alternatives
- Package manager present (increased attack surface)
- Root by default
- Not purpose-built for containers (RHEL derivative)
- No native SBOM generation (RPM metadata is the SBOM)
- Requires subscription for full support

---

## 2. Comparison Matrix

### 2.1 Primary Dimensions (15+)

| # | Dimension | Chainguard/Wolfi | Bitnami | Distroless | UBI Minimal |
|---|-----------|-----------------|---------|------------|-------------|
| 1 | **Base Philosophy** | Distroless-first, purpose-built un-distro | Security-hardened full apps | Zero-OS, app-only | Enterprise RHEL-derived |
| 2 | **Base OS** | Wolfi (custom) | Photon OS / Minideb | Debian 12/13 | RHEL 8/9 |
| 3 | **Package Manager** | apk (Alpine-compatible) | tdnf / apt | None (build-time via Bazel) | dnf / microdnf |
| 4 | **Pkg Mgr in Final Image** | No (production) | Yes | No | Yes (microdnf) |
| 5 | **Shell in Final Image** | No (production) | Yes | No (unless `:debug`) | Yes |
| 6 | **Build Tool** | apko + melange (YAML) | Dockerfile + bitnami-pkg | Bazel | Dockerfile |
| 7 | **Image Size (base)** | 2-10 MB | 80-100 MB | 2-20 MB | 30-80 MB |
| 8 | **Non-Root Default** | Yes (UID 65532) | Yes (UID 1001) | `:nonroot` variant | No (root default) |
| 9 | **CVE Remediation** | Nightly rebuilds | Triage + VEX + KEV/EPSS | Debian security tracking | RHEL errata (10yr) |
| 10 | **SBOM** | SPDX-2.3, built-in | Commercial, with VEX | Not native | RPM metadata |
| 11 | **Image Signing** | Cosign keyless (Sigstore) | in-toto attestation | Cosign keyless | GPG + Cosign |
| 12 | **Multi-Arch** | amd64, arm64, arm/v7, ppc64le, s390x | amd64, arm64 | amd64, arm64, arm, s390x, ppc64le, riscv64 | amd64, arm64, ppc64le, s390x |
| 13 | **FIPS Support** | Yes (separate variants) | Yes (BSI) | No | Yes (built-in) |
| 14 | **STIG Support** | Yes | Yes | No | Yes (RHEL STIGs) |
| 15 | **Debug Variant** | Yes (dev images) | Yes (shell included) | Yes (`:debug` tag) | N/A (shell present) |
| 16 | **Entrypoint Pattern** | Vector form (apko YAML) | libentrypoint.sh + scripts | Vector form (app-specific) | Standard Docker CMD |
| 17 | **Signal Handling** | App-responsibility | libentrypoint.sh (trap-based) | App-responsibility | App-responsibility |
| 18 | **Helm Charts** | Growing catalog | First-class (Bitnami charts) | None | OpenShift templates |
| 19 | **Reproducibility** | High (declarative YAML) | Medium (Dockerfile + scripts) | Very high (Bazel hermeticity) | Medium (Dockerfile) |
| 20 | **VEX Statements** | Yes (OpenVEX via advisories) | Yes (KEV + EPSS scoring) | No | Via RHSA advisories |
| 21 | **Init System** | None | None (script-based) | None | Optional (ubi-init) |
| 22 | **Config Management** | Environment-based | Env vars + templates | N/A | Env vars + dnf |

### 2.2 CVE Comparison (Representative, from Chainguard public data)

| Image | Chainguard | Bitnami | Distroless | UBI |
|-------|-----------|---------|------------|-----|
| nginx | ~0 | ~2 | ~3 | ~5 |
| python | ~0 | ~1 | ~2 | ~4 |
| node | ~0 | ~1 | ~1 | ~3 |
| postgres | ~0 | ~2 | N/A | ~6 |

*Note: CVE counts vary by date and scanner. Chainguard's nightly rebuild strategy keeps counts near-zero.*

---

## 3. Recommendations for EvergreenImageRegistry

### 3.1 Patterns to Adopt

#### PATTERN-001: Declarative Image Builds

Adopt the **apko/melange pattern** for image construction:
- Define images as YAML manifests (not Dockerfiles)
- Build packages with declarative melange pipelines
- Assemble images with apko from package sets
- Enables full reproducibility and auditability

```yaml
contents:
  packages:
    - wolfi-base
    - my-app
accounts:
  runas: nonroot
entrypoint:
  command: /usr/bin/my-app
```

#### PATTERN-002: Distroless by Default

- Production images SHALL NOT contain a shell or package manager
- Provide `:debug` variants with busybox for troubleshooting
- Provide `:dev` variants with full tooling for development

#### PATTERN-003: Non-Root by Default

- All images SHALL run as `nonroot` (UID 65532) by default
- Provide `:root` variants only when explicitly required (with documentation)
- Filesystem ownership: root owns binaries, nonroot owns data directories

#### PATTERN-004: Nightly Rebuild Strategy

- Implement nightly full rebuilds from latest upstream source
- This is the single most effective CVE mitigation strategy observed
- Combine with automated vulnerability scanning (Trivy + Grype)

#### PATTERN-005: SBOM + Signing as First-Class

- Generate SPDX-2.3 SBOMs at build time
- Attach SBOMs as OCI referrers (attestations)
- Sign all images with Cosign (keyless, Sigstore-backed)
- Verify signatures in CI/CD pipelines before deployment

#### PATTERN-006: VEX for Vulnerability Triage

- Adopt OpenVEX for vulnerability triage (Chainguard pattern)
- Include KEV and EPSS scores for prioritization (Bitnami pattern)
- Publish security advisories with machine-readable VEX documents
- NOT every CVE requires action — VEX provides context

#### PATTERN-007: Vector-Form Entrypoints

- All ENTRYPOINT and CMD directives SHALL use vector form
- No shell wrapping: `["/app"]` not `"app"` or `["/bin/sh", "-c", "app"]`
- Applications must handle their own PID 1 signal responsibilities
- For applications requiring init-like behavior, use `tini` explicitly

#### PATTERN-008: Multi-Arch from Day One

- Publish all images as OCI image indexes
- Support at minimum: `linux/amd64`, `linux/arm64`
- Provide architecture-specific tags for deterministic pulls

#### PATTERN-009: Digest-Based Versioning

- Immutable tags based on content-addressable digests
- `latest` tag for convenience (not for production)
- Version tags for semver tracking (e.g., `v1.2.3`)
- Automated digest update tooling (frizbee/digestabot pattern)

#### PATTERN-010: Entrypoint Script Library

For images requiring initialization logic, adopt a **libentrypoint.sh pattern** (inspired by Bitnami but simplified for distroless):
- Minimal init script that handles signal forwarding
- Environment variable parsing
- Configuration template rendering
- Graceful shutdown with PID 1 signal handling

### 3.2 Anti-Patterns to Avoid

#### ANTI-PATTERN-001: Shell-Form Entrypoints

```dockerfile
# WRONG
ENTRYPOINT /usr/bin/my-app
CMD my-app --config /etc/app.conf

# CORRECT
ENTRYPOINT ["/usr/bin/my-app"]
CMD ["--config", "/etc/app.conf"]
```

#### ANTI-PATTERN-002: Running as Root

Never ship images that run as root by default. Even if the application "needs" root for port binding, use `sysctl net.ipv4.ip_unprivileged_port_start=0` or run behind a reverse proxy.

#### ANTI-PATTERN-003: Leaving Package Manager in Production Images

Package managers (`apk`, `apt`, `dnf`) in production images:
- Increase attack surface
- Allow runtime dependency changes (breaks immutability)
- Add unnecessary size
- Provide tools for post-exploitation

#### ANTI-PATTERN-004: Mutable Tags in Production

Never use `:latest` in production deployments. Always pin by digest or explicit version tag.

#### ANTI-PATTERN-005: Ignoring Signal Handling

Applications running as PID 1 must handle signals. Without proper signal handling:
- `SIGTERM` from Kubernetes may not trigger graceful shutdown
- Zombie processes may accumulate
- `docker stop` may timeout and send `SIGKILL`

#### ANTI-PATTERN-006: Large Monolithic Images

Avoid including unnecessary tools, documentation, or development libraries in production images. Each additional binary is an additional attack vector.

#### ANTI-PATTERN-007: Baking Secrets in Images

Never include secrets, API keys, or credentials in image layers. Use:
- Runtime environment variables (with secret injection)
- Mounted secrets (Kubernetes Secrets, Vault CSI)
- Build-time secrets with multi-stage builds (secrets in build stage only)

#### ANTI-PATTERN-008: No SBOM or Provenance

Shipping images without SBOMs or build provenance is an anti-pattern for any registry that claims security focus.

---

## 4. Recommended Architecture for EvergreenImageRegistry

### 4.1 Image Hierarchy

```
Tier 1 (Critical Infrastructure):
  └── scratch / static-distroless
      └── Evergreen Static Base (~2 MB)
          └── Application-specific images

Tier 2 (Runtime Images):
  └── wolfi-base / distroless/cc
      └── Evergreen Runtime Base (~10 MB)
          └── Language runtimes (Python, Node, Go)
              └── Application-specific images

Tier 3 (Middleware):
  └── Evergreen Middleware Base (~30 MB)
      └── nginx, postgres, redis, etc.
          └── Application-specific images
```

### 4.2 Build Pipeline

```
Source Code
    │
    ▼
[Melange] ─── Build .apk packages from YAML
    │
    ▼
[apko] ─── Assemble OCI image from package set
    │
    ├── [Syft] ─── Generate SPDX SBOM
    ├── [Cosign] ─── Sign image (keyless)
    ├── [Trivy + Grype] ─── Vulnerability scan
    └── [OpenVEX] ─── Generate VEX for any findings
    │
    ▼
[Push] ─── Publish to registry with attestations
```

### 4.3 Tag Strategy

| Tag Pattern | Purpose | Mutability |
|-------------|---------|-----------|
| `latest` | Development convenience | Mutable |
| `v{major}.{minor}.{patch}` | Semver release | Immutable |
| `sha256:{digest}` | Content-addressable | Immutable |
| `dev` | Development variant (with shell) | Mutable |
| `debug` | Debug variant (with busybox) | Mutable |
| `fips` | FIPS-compliant variant | Immutable |

---

## 5. Key Takeaways

1. **Nightly rebuilds are the most effective CVE mitigation.** Chainguard's approach of rebuilding everything from latest source every night consistently achieves near-zero CVEs. This is more effective than backporting patches.

2. **Distroless is the new standard.** Both Chainguard and Google Distroless prove that removing shells and package managers from production images is both feasible and standard practice. Bitnami's move to Photon OS also reflects this direction.

3. **SBOMs + Signing are table stakes.** Any hardened image registry must generate SBOMs and sign images. The Chainguard pattern (SPDX-2.3 via apko, Cosign keyless) is the most mature.

4. **VEX completes the picture.** Bitnami's approach of combining VEX with KEV/EPSS scores for vulnerability triage is best-in-class. Not every CVE is exploitable; VEX provides the context to make that determination.

5. **Non-root is non-negotiable.** All four projects support non-root execution. Chainguard and Bitnami default to it. Distroless provides it as a variant. UBI should but doesn't (relies on OpenShift SCCs).

6. **Declarative builds beat Dockerfiles for reproducibility.** Both apko (YAML) and Bazel (Starlark) provide more reproducible builds than Dockerfiles. For EvergreenImageRegistry, apko is recommended due to its simplicity and OCI-native approach.

7. **Debug variants solve the "no shell" usability problem.** All distroless projects provide debug variants with a shell. This is the correct pattern — secure by default, debuggable when needed.

---

## Bibliography

| ID | Citation | Relevance | TQA |
|----|----------|-----------|-----|
| [^1] | Chainguard Images GitHub — github.com/chainguard-images | Primary research source | 5 |
| [^2] | Chainguard Academy — edu.chainguard.dev | Documentation and best practices | 5 |
| [^3] | Bitnami Containers GitHub — github.com/bitnami/containers | Primary research source | 5 |
| [^4] | Google Distroless GitHub — github.com/GoogleContainerTools/distroless | Primary research source | 5 |
| [^5] | Red Hat UBI — catalog.redhat.com | Enterprise reference | 4 |
| [^6] | Wolfi OS — github.com/wolfi-dev | Base distribution details | 5 |
| [^7] | apko — github.com/chainguard-dev/apko | Build tool reference | 5 |
| [^8] | melange — github.com/chainguard-dev/melange | Package build reference | 5 |
| [^9] | NIST SP 800-190 | Container security baseline | 5 |
| [^10] | OCI Image Spec v1.0 | Image format specification | 5 |
| [^11] | SLSA 3.0 | Supply chain levels for software artifacts | 4 |
| [^12] | SPDX 2.3 | SBOM standard | 4 |

---

## Knowledge Graph Concepts

| ID | Concept | Language | Source | Confidence |
|----|---------|----------|--------|-------------|
| CONCEPT-001 | Distroless | EN | Google/Chainguard | 1.0 |
| CONCEPT-002 | Wolfi Un-Distro | EN | Chainguard | 0.95 |
| CONCEPT-003 | apk Package Manager | EN | Alpine/Wolfi | 1.0 |
| CONCEPT-004 | SBOM (SPDX) | EN | SPDX/nTIA | 1.0 |
| CONCEPT-005 | Cosign Keyless Signing | EN | Sigstore | 1.0 |
| CONCEPT-006 | VEX (Vulnerability Exploitability) | EN | OpenVEX | 0.95 |
| CONCEPT-007 | KEV (Known Exploited Vulnerabilities) | EN | CISA | 0.95 |
| CONCEPT-008 | EPSS (Exploit Prediction Scoring) | EN | FIRST.org | 0.95 |
| CONCEPT-009 | FIPS 140-3 | EN | NIST | 1.0 |
| CONCEPT-010 | STIG (Security Technical Implementation Guide) | EN | DISA | 1.0 |
| CONCEPT-011 | Bazel Hermeticity | EN | Google | 0.95 |
| CONCEPT-012 | libentrypoint.sh Pattern | EN | Bitnami | 0.90 |
| CONCEPT-013 | in-toto Attestation | EN | in-toto | 0.90 |
| CONCEPT-014 | OCI Referrers | EN | OCI | 1.0 |
| CONCEPT-015 | Photon OS | EN | VMware | 0.85 |

---

## Quality Checklist

- [x] Nomenclature defined before mathematical content
- [x] All symbols defined and units specified
- [x] Executive summary with comparison table
- [x] Four project analyses with specific data
- [x] 22-dimension comparison matrix
- [x] Recommendations with rationale
- [x] Anti-patterns with examples
- [x] Architecture recommendation
- [x] Bibliography complete
- [x] Knowledge graph concepts extracted

---

## Document Control

| Version | Date | Status | Author |
|---------|------|--------|--------|
| 1.0.0 | 2026-04-20 | DRAFT | Nexus |
