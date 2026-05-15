# =============================================================================

# PHASE 5: MILITARY COMPLIANCE - Detailed Execution Plan

# =============================================================================

# Version: 1.0.0

# Status: PENDING

# Date: 2026-04-20

#

# ABSTRACT: This phase brings the Evergreen Image Registry into compliance with

# military and government security standards including CIS Docker Benchmark,

# DISA STIG, FIPS 140-2, air-gapped deployment requirements, and ATO

# artifact generation. Phase 4 must pass all quality gates before this phase

# begins.

# =============================================================================

## Table of Contents

1. [Task Inventory](#1-task-inventory)
2. [5.1 CIS Docker Benchmark Compliance](#2-51-cis-docker-benchmark-compliance)
3. [5.2 DISA STIG Automated Scanning](#3-52-disa-stig-automated-scanning)
4. [5.3 FIPS 140-2 Build Variants](#4-53-fips-140-2-build-variants)
5. [5.4 Air-Gapped Deployment](#5-54-air-gapped-deployment)
6. [5.5 ATO Artifacts](#6-55-ato-artifacts)
7. [Quality Gates](#7-quality-gates)

---

## 1. Task Inventory

### Dependency Graph

```
Phase 4 (all gates passed)
    |
    +--> T5.1.1 (docker-bench-security in CI) ──> Independent
    +--> T5.1.2 (score thresholds + gating) ──> Depends on T5.1.1
    |
    +--> T5.2.1 (stig_checks.sh integration) ──> Independent
    +--> T5.2.2 (CKL output generation) ──> Depends on T5.2.1
    |
    +--> T5.3.1 (FIPS base images) ──> Independent
    +--> T5.3.2 (Go FIPS mode) ──> Independent
    +--> T5.3.3 (OpenSSL FIPS) ──> Independent
    +--> T5.3.4 (fips_image_matrix) ──> Depends on T5.3.1, T5.3.2, T5.3.3
    |
    +--> T5.4.1 (air-gap bundle creation) ──> Independent
    +--> T5.4.2 (offline SBOM) ──> Depends on T5.4.1
    +--> T5.4.3 (registry mirrors) ──> Depends on T5.4.1
    |
    +--> T5.5.1 (controls mapping) ──> Depends on T5.1.1, T5.2.1
    +--> T5.5.2 (SSP template) ──> Depends on T5.5.1
    +--> T5.5.3 (POA&M template) ──> Depends on T5.5.1
```

### Parallel Execution Streams

```
Stream A: CIS Benchmark (T5.1.1 -> T5.1.2) ── 8 hours
Stream B: DISA STIG (T5.2.1 -> T5.2.2) ── 10 hours
Stream C: FIPS Builds (T5.3.1, T5.3.2, T5.3.3 -> T5.3.4) ── 20 hours
Stream D: Air-Gap (T5.4.1 -> T5.4.2, T5.4.3) ── 12 hours
Stream E: ATO Docs (T5.5.1 -> T5.5.2 -> T5.5.3) ── 8 hours
```

| Stream    | Wall-Clock    | Dependencies             |
| --------- | ------------- | ------------------------ |
| A         | 8 hours       | None                     |
| B         | 10 hours      | None                     |
| C         | 20 hours      | None (merge at T5.3.4)   |
| D         | 12 hours      | None (merge at T5.4.2/3) |
| E         | 8 hours       | A, B must complete first |
| **Total** | **~20 hours** |                          |

---

## 2. 5.1 CIS Docker Benchmark Compliance

### T5.1.1: Integrate docker-bench-security in CI

**Problem:** No automated CIS Docker Benchmark scanning exists. Manual compliance checks are error-prone and
non-repeatable.

**Solution:** Add `docker-bench-security` (Aqua Security fork) to CI pipeline.

**Files to create:**

| File                                  | Purpose                                              |
| ------------------------------------- | ---------------------------------------------------- |
| `.github/workflows/cis-benchmark.yml` | CI workflow triggering on PR and push to main        |
| `compliance/cis/cis_config.yaml`      | Benchmark configuration: sections to run, exclusions |
| `compliance/cis/cis_baseline.json`    | Expected pass/fail baseline for comparison           |
| `scripts/run_cis_benchmark.sh`        | Wrapper script with output formatting                |

**Implementation:**

1. Add `docker-bench-security` as a CI step in GitHub Actions
2. Run against each built image in the registry
3. Sections to audit (CIS Docker Benchmark v1.6+):
   - 1.x Host Configuration
   - 2.x Docker daemon configuration
   - 4.x Container Runtime
   - 5.x Docker Operations
4. Generate JSON + console output
5. Upload results as CI artifacts

**Exclusions:** Document justified exceptions in `cis_config.yaml` with rationale (e.g., "scratch images cannot contain
/etc/passwd modifications").

### T5.1.2: Score Thresholds and CI Gating

**Solution:** Define minimum CIS scores and gate merges.

| Gate                            | Threshold | Action      |
| ------------------------------- | --------- | ----------- |
| Pass rate (all checks)          | >= 80%    | Warn        |
| Pass rate (all checks)          | >= 90%    | Block merge |
| Critical failures (section 4/5) | 0         | Block merge |
| New regressions vs baseline     | 0         | Block merge |

**Files to create:**

| File                                   | Purpose                                                              |
| -------------------------------------- | -------------------------------------------------------------------- |
| `compliance/cis/score_thresholds.yaml` | Threshold definitions per image tier                                 |
| `scripts/cis_gate.sh`                  | Gate script: compare results to thresholds, exit non-zero on failure |

---

## 3. 5.2 DISA STIG Automated Scanning

### T5.2.1: Integrate stig_checks.sh

**Problem:** DISA STIG compliance requires manual evaluation against the Docker/Container STIG (currently
SRG-APP-000XXX). No automated scanning exists.

**Solution:** Create `stig_checks.sh` that evaluates images against DISA STIG requirements.

**Files to create:**

| File                                 | Purpose                          |
| ------------------------------------ | -------------------------------- |
| `scripts/stig_checks.sh`             | Automated STIG evaluation script |
| `compliance/stig/stig_config.yaml`   | STIG sections and applicability  |
| `compliance/stig/stig_controls.yaml` | STIG control ID -> check mapping |

**STIG checks to automate:**

| STIG ID        | Check                      | Method                    |
| -------------- | -------------------------- | ------------------------- |
| SRG-APP-000016 | Container runs as non-root | Inspect USER directive    |
| SRG-APP-000029 | Container has HEALTHCHECK  | Inspect HEALTHCHECK       |
| SRG-APP-000030 | No SSH in container        | Scan filesystem           |
| SRG-APP-000031 | No setuid binaries         | Find setuid files         |
| SRG-APP-000032 | Read-only root filesystem  | Verify mount flags        |
| SRG-APP-000033 | No sensitive data in ENV   | Scan for secrets patterns |
| SRG-APP-000034 | Capabilities restricted    | Inspect cap_add/cap_drop  |
| SRG-APP-000035 | Seccomp profile applied    | Verify seccomp            |
| SRG-APP-000036 | No privileged containers   | Verify not privileged     |
| SRG-APP-000037 | No new privileges          | Verify no-new-privileges  |
| SRG-APP-000038 | PID limits set             | Verify pids_limit         |
| SRG-APP-000039 | Resource limits set        | Verify memory/CPU limits  |
| SRG-APP-000040 | /tmp mounted tmpfs         | Verify tmpfs mount        |

### T5.2.2: CKL Output Generation

**Problem:** ATO assessors require CKL (Security Content Automation Protocol checklist) format for evidence submission.

**Solution:** Generate STIG results in XCCDF/CKL format compatible with DISA STIG Viewer.

**Files to create:**

| File                                            | Purpose                               |
| ----------------------------------------------- | ------------------------------------- |
| `scripts/generate_ckl.py`                       | Convert STIG check results to CKL XML |
| `compliance/stig/templates/stig_docker.ckl.xml` | CKL template with STIG metadata       |
| `compliance/stig/output/`                       | Directory for generated CKL files     |

---

## 4. 5.3 FIPS 140-2 Build Variants

### T5.3.1: FIPS Base Images

**Problem:** Standard base images use non-FIPS-validated cryptographic modules.

**Solution:** Create FIPS-compliant base image variants.

| Standard Image                  | FIPS Variant                         | FIPS Module               |
| ------------------------------- | ------------------------------------ | ------------------------- |
| `debian:bookworm-slim`          | `debian:bookworm-slim-fips`          | OpenSSL 3.0 FIPS provider |
| `gcr.io/distroless/static`      | Build from source with BoringCrypto  | BoringCrypto              |
| `cgr.dev/chainguard/wolfi-base` | `cgr.dev/chainguard/wolfi-base-fips` | Chainguard FIPS           |
| `redhat/ubi9-minimal`           | `redhat/ubi9-minimal-fips`           | RHEL OpenSSL FIPS         |

**Files to create:**

| File                                 | Purpose          |
| ------------------------------------ | ---------------- |
| `images/fips/Dockerfile.debian-fips` | FIPS Debian base |
| `images/fips/Dockerfile.wolfi-fips`  | FIPS Wolfi base  |
| `images/fips/Dockerfile.ubi-fips`    | FIPS UBI base    |

### T5.3.2: Go FIPS Mode

**Solution:** Build Go binaries with `GOFIPS=1` for images containing Go applications.

| Setting        | Value                           |
| -------------- | ------------------------------- |
| `GOEXPERIMENT` | `boringcrypto`                  |
| `GOFIPS`       | `1`                             |
| `CGO_ENABLED`  | `1` (required for boringcrypto) |

**Files to create:**

| File                                  | Purpose                                         |
| ------------------------------------- | ----------------------------------------------- |
| `images/fips/Dockerfile.go-fips`      | Go FIPS build stage template                    |
| `compliance/fips/go_fips_config.yaml` | Go version -> boringcrypto compatibility matrix |

### T5.3.3: OpenSSL FIPS Provider

**Solution:** Enable OpenSSL 3.0 FIPS provider in non-scratch images.

```dockerfile
RUN apt-get update && apt-get install -y openssl libssl3 && \
    openssl fipsinstall -out /etc/ssl/fipsmodule.cnf -module /usr/lib/ossl-modules/fips.so && \
    sed -i 's/^# .*\bfips = /fips = /' /etc/ssl/openssl.cnf
```

**Files to create:**

| File                                  | Purpose                             |
| ------------------------------------- | ----------------------------------- |
| `images/fips/Dockerfile.openssl-fips` | OpenSSL FIPS configuration stage    |
| `compliance/fips/fips_validation.sh`  | Runtime FIPS validation script      |
| `compliance/fips/fips_test.go`        | Go test verifying FIPS crypto usage |

### T5.3.4: FIPS Image Matrix

**Files to create:**

| File                                     | Purpose                                               |
| ---------------------------------------- | ----------------------------------------------------- |
| `compliance/fips/fips_image_matrix.yaml` | Maps each image to FIPS variant and validation status |

**Matrix structure:**

```yaml
images:
  - name: nginx
    standard_image: images/nginx/Dockerfile
    fips_image: images/fips/nginx/Dockerfile
    fips_module: openssl-3.0-fips
    status: planned
  - name: coredns
    standard_image: images/coredns/Dockerfile
    fips_image: images/fips/coredns/Dockerfile
    fips_module: go-boringcrypto
    status: planned
```

---

## 5. 5.4 Air-Gapped Deployment

### T5.4.1: Air-Gap Bundle Creation

**Problem:** Military environments have no external network access. All images, tools, and metadata must be transferable
via physical media.

**Solution:** Create self-contained offline bundles.

**Files to create:**

| File                                        | Purpose                       |
| ------------------------------------------- | ----------------------------- |
| `scripts/create_airgap_bundle.sh`           | Bundle creation script        |
| `compliance/airgap/bundle_manifest.yaml`    | Bundle contents manifest      |
| `compliance/airgap/bundle_checksums.sha256` | SHA256 of all bundle contents |

**Bundle contents:**

| Component                      | Format          | Size Estimate |
| ------------------------------ | --------------- | ------------- |
| Container images (OCI tar)     | `.tar`          | ~2-5 GB       |
| SBOM (SPDX JSON)               | `.spdx.json`    | ~50 MB        |
| VEX (vulnerability exceptions) | `.vex.json`     | ~1 MB         |
| CIS benchmark results          | `.json`         | ~500 KB       |
| STIG check results + CKL       | `.xml`, `.json` | ~2 MB         |
| Image signatures (cosign)      | `.sig`          | ~10 MB        |
| Installation script            | `.sh`           | ~50 KB        |
| README with checksums          | `.md`           | ~10 KB        |

### T5.4.2: Offline SBOM

**Files to create:**

| File                               | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| `scripts/generate_offline_sbom.sh` | Generate SPDX SBOM without network access     |
| `compliance/airgap/sbom_merge.py`  | Merge per-image SBOMs into registry-wide SBOM |

**Toolchain:**

- `syft` for SPDX SBOM generation (works offline with cached DB)
- `grype` for vulnerability matching against cached database
- Pre-downloaded vulnerability DB included in bundle

### T5.4.3: Registry Mirrors

**Files to create:**

| File                                   | Purpose                                   |
| -------------------------------------- | ----------------------------------------- |
| `compliance/airgap/mirror_setup.sh`    | Configure local registry mirror           |
| `compliance/airgap/mirror_compose.yml` | Docker Compose for local registry         |
| `compliance/airgap/mirror_sync.sh`     | Sync images from bundle to local registry |

**Local registry stack:**

| Component       | Tool                 | Port |
| --------------- | -------------------- | ---- |
| Registry        | `registry:2`         | 5000 |
| UI              | `docker-registry-ui` | 8080 |
| TLS termination | `nginx`              | 443  |

---

## 6. 5.5 ATO Artifacts

### T5.5.1: Controls Mapping

**Files to create:**

| File                                   | Purpose                                          |
| -------------------------------------- | ------------------------------------------------ |
| `compliance/ato/controls_mapping.yaml` | NIST SP 800-53 control -> implementation mapping |
| `compliance/ato/controls_evidence/`    | Evidence files per control                       |

**Control families to map:**

| Family                     | Controls               | Focus                                   |
| -------------------------- | ---------------------- | --------------------------------------- |
| AC (Access Control)        | AC-2, AC-3, AC-4, AC-6 | Container auth, capability restrictions |
| AU (Audit)                 | AU-2, AU-3, AU-12      | Container logging, audit trails         |
| CA (Assessment)            | CA-2, CA-7             | Security assessments, CI scanning       |
| CM (Configuration)         | CM-2, CM-3, CM-6       | Image configuration, supply chain       |
| IA (Identification)        | IA-2, IA-5             | Authentication, credential management   |
| RA (Risk Assessment)       | RA-5                   | Vulnerability scanning (Trivy, Grype)   |
| SA (System Assurance)      | SA-11, SA-12           | Secure development, supply chain        |
| SC (System Communications) | SC-8, SC-12, SC-13     | TLS, cryptography, FIPS                 |
| SI (System Integrity)      | SI-2, SI-7             | Patching, integrity verification        |

### T5.5.2: SSP Template

**Files to create:**

| File                                 | Purpose                       |
| ------------------------------------ | ----------------------------- |
| `compliance/ato/ssp/ssp_template.md` | System Security Plan template |

See `compliance/ato/ssp/ssp_template.md` for full template.

### T5.5.3: POA&M Template

**Files to create:**

| File                                     | Purpose                          |
| ---------------------------------------- | -------------------------------- |
| `compliance/ato/poam/poam_current.yaml`  | Current POA&M with open findings |
| `compliance/ato/poam/poam_template.yaml` | Template for future findings     |

See `compliance/ato/poam/poam_current.yaml` for current findings.

### T5.5.4: Risk Register

**Files to create:**

| File                                     | Purpose                             |
| ---------------------------------------- | ----------------------------------- |
| `compliance/ato/risk/risk_register.yaml` | Risk register with identified risks |

See `compliance/ato/risk/risk_register.yaml` for current risk register.

---

## 7. Quality Gates

### QG-5.1: CIS Benchmark Compliance

| Criterion               | Threshold   | Measurement                   |
| ----------------------- | ----------- | ----------------------------- |
| CIS pass rate           | >= 90%      | `run_cis_benchmark.sh` output |
| Critical check failures | 0           | Sections 4.x, 5.x             |
| CI pipeline integration | Operational | Workflow runs green           |

### QG-5.2: DISA STIG Compliance

| Criterion                 | Threshold         | Measurement                          |
| ------------------------- | ----------------- | ------------------------------------ |
| STIG checks automated     | 13+ checks        | `stig_checks.sh --count`             |
| CKL generation            | Working           | `generate_ckl.py` produces valid XML |
| STIG Viewer compatibility | Passes validation | Open CKL in DISA STIG Viewer         |

### QG-5.3: FIPS 140-2 Compliance

| Criterion                  | Threshold                            | Measurement                       |
| -------------------------- | ------------------------------------ | --------------------------------- | ------------ |
| FIPS base images built     | 3+ (debian, wolfi, ubi)              | `docker images                    | grep fips`   |
| FIPS validation at runtime | `openssl list -providers` shows FIPS | `fips_validation.sh`              |
| Go FIPS binaries           | BoringCrypto linked                  | `go tool nm                       | grep boring` |
| FIPS image matrix          | All Tier 1 images mapped             | `fips_image_matrix.yaml` complete |

### QG-5.4: Air-Gap Readiness

| Criterion        | Threshold                 | Measurement                                     |
| ---------------- | ------------------------- | ----------------------------------------------- |
| Bundle creation  | End-to-end working        | `create_airgap_bundle.sh` produces valid bundle |
| Bundle integrity | SHA256 matches manifest   | `sha256sum -c bundle_checksums.sha256`          |
| Offline SBOM     | Generated without network | `generate_offline_sbom.sh`                      |
| Registry mirror  | Operational               | `docker pull localhost:5000/nginx` succeeds     |

### QG-5.5: ATO Artifact Completeness

| Criterion       | Threshold                         | Measurement                         |
| --------------- | --------------------------------- | ----------------------------------- |
| Controls mapped | 25+ NIST controls                 | `controls_mapping.yaml` entry count |
| SSP template    | Complete with all 6 sections      | Manual review                       |
| POA&M           | All high findings have milestones | `poam_current.yaml` review          |
| Risk register   | All identified risks documented   | `risk_register.yaml` review         |

---

**END OF PHASE 5 PLAN**
