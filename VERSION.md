# VERSION - Sovereign Hardened Image Registry

## Project State

| Attribute | Value |
|-----------|-------|
| Project Name | Sovereign Hardened Image Registry |
| Version | 3.6.0 |
| Phase | Roadmap Phase 6 IN PROGRESS |
| Status | IN PROGRESS |
| Last Updated | 2026-04-20 |

---

## Phase Status

| Phase | Number | Status | Completion |
|-------|--------|--------|------------|
| Phase -1: Context Discovery | -1 | COMPLETED | 100% |
| Phase -0.5: Environment Materialization | -0.5 | COMPLETED | 100% |
| Phase 0: Requirements Engineering | 0 | COMPLETED | 100% |
| Phase 1: Epistemological Discovery | 1 | COMPLETED | 100% |
| Phase 2: Architecture Specification | 2 | COMPLETED | 100% |
| **Roadmap Phase 0: Fix Foundation** | **R0** | **COMPLETED** | **100%** |
| **Roadmap Phase 1: Supply Chain** | **R1** | **COMPLETED** | **100%** |
| **Roadmap Phase 2: Runtime Security** | **R2** | **COMPLETED** | **100%** |
| **Roadmap Phase 3: Test Coverage** | **R3** | **COMPLETED** | **100%** |
| **Roadmap Phase 3.5: Checksum Verification** | **R3.5** | **COMPLETED** | **100%** |
| **Roadmap Phase 4: HFT Hardening** | **R4** | **COMPLETED** | **100%** |
| **Roadmap Phase 5: Military Compliance** | **R5** | **COMPLETED** | **100%** |
| **Roadmap Phase 6: Continuous Monitoring** | **R6** | **IN PROGRESS** | **10%** |

---

## Error State

| Metric | Value |
|--------|-------|
| Current Error Level | 0 (NONE) |
| Rollback Checkpoint | N/A |
| Recovery Time Estimate | N/A |

---

## Key Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Images | 223 | 1000+ | Scaling to requiredimages.md |
| Images with working HEALTHCHECK | 211 (95%) | 100% | Near target |
| Images with pinned base tags | 223 (100%) | 100% | Met |
| Images with verified checksums | 74 (33%) | 100% | In progress |
| Images with CHECKSUMS files | 122 (55%) | 100% | Framework ready |
| HFT labels (Tier-1 images) | 113 (100%) | 100% | Met |
| Compliance frameworks | 5 | 5 | Met |
| Seccomp profiles | 5 | Per-category | Met |
| AppArmor profiles | 4 | Per-category | Met |
| Adversarial tests | 21 | 20+ | Met |
| Functional test suites | 3 | 3+ | Met |
| Test config coverage | 223 (100%) | 100% | Met |
| Yellow Papers | 4 | 4 | Met |
| Blue Papers | 2 | 2 | Met |
| Requirements | 247 | 247 | Met |
| ADRs | 5 | 5+ | Met |
| Phase plans | 7 | 7 | Met |
| CI workflows | 3 | 3+ | Met |
| Standards Covered | 8 | 8 | Met |

---

## Artifact Inventory

### Documentation
| Path | Description |
|------|-------------|
| `.specs/08_roadmap/master_plan.toml` | Master execution plan (47 tasks, v4.0.0) |
| `.specs/08_roadmap/phase_0_plan.md` | Phase 0 detailed plan |
| `.specs/08_roadmap/phase_1_plan.md` | Phase 1 detailed plan |
| `.specs/08_roadmap/phase_2_plan.md` | Phase 2 detailed plan |
| `.specs/08_roadmap/phase_3_plan.md` | Phase 3 detailed plan |
| `.specs/08_roadmap/phase_4_plan.md` | Phase 4 HFT hardening plan |
| `.specs/08_roadmap/phase_5_plan.md` | Phase 5 military compliance plan |
| `.specs/08_roadmap/phase_6_plan.md` | Phase 6 continuous monitoring plan |
| `.adrs/ADR-001-healthcheck-strategy.md` | HEALTHCHECK fix strategy |
| `.adrs/ADR-002-checksum-verification.md` | SHA256 verification strategy |
| `.adrs/ADR-003-debian-multistage.md` | Multi-stage conversion strategy |
| `.adrs/ADR-004-hft-label-schema.md` | HFT label schema (30+ labels) |
| `.adrs/ADR-005-military-compliance-framework.md` | Military compliance framework |

### CI/CD
| Path | Description |
|------|-------------|
| `.github/workflows/build.yml` | 6-stage build pipeline (TruffleHog fixed) |
| `.github/workflows/daily-security-scan.yml` | Daily CVE/SBOM/compliance monitoring |
| `.github/workflows/lint.yml` | Hadolint/markdown/yaml linting |
| `Dockerfile.ci` | Hermetic CI environment (13 pinned tools) |
| `scripts/update_ci_environment.sh` | CI environment version updater |

### Checksum Infrastructure
| Path | Description |
|------|-------------|
| `scripts/populate_checksums.py` | Fetches real SHA256 from upstream |
| `scripts/integrate_checksum_verification.py` | Inserts sha256sum into Dockerfiles |

### HFT Deployment
| Path | Description |
|------|-------------|
| `deploy/hft/docker-compose.network.yml` | CPU-pinned proxy manifests |
| `scripts/sovereign-entrypoint.sh` | Graceful signal forwarding entrypoint |

### Compliance Infrastructure
| Path | Description |
|------|-------------|
| `compliance/cis/run_cis_scan.sh` | CIS Docker Benchmark scanner |
| `compliance/stig/stig_checks.sh` | DISA STIG checker |
| `compliance/fips/fips_image_matrix.yaml` | 40 FIPS-required images |
| `compliance/ato/controls_mapping.yaml` | NIST SP 800-53 mapping (15 controls) |
| `compliance/ato/ssp/ssp_template.md` | System Security Plan template |
| `compliance/ato/poam/poam_current.yaml` | 7 open findings |
| `compliance/ato/risk/risk_register.yaml` | 4 assessed risks |

### Air-Gap Deployment
| Path | Description |
|------|-------------|
| `scripts/airgap/create_bundle.sh` | Offline deployment packaging |

### Test Infrastructure
| Path | Description |
|------|-------------|
| `images/tests/test_framework.sh` | Core constraint tests (C001-C019) |
| `images/tests/test_runner.sh` | Per-image test runner |
| `images/tests/test_config.yaml` | Config for all 223 images |
| `images/tests/adversarial/test_adversarial.sh` | 21 adversarial tests |
| `images/tests/functional/test_databases.sh` | Database functional tests |
| `images/tests/functional/test_proxies.sh` | Proxy functional tests |
| `images/tests/functional/test_security.sh` | Security tool tests |
| `images/tests/profiles/seccomp-default.json` | Baseline seccomp profile |
| `images/tests/profiles/seccomp-webserver.json` | Web server seccomp |
| `images/tests/profiles/seccomp-database.json` | Database seccomp |
| `images/tests/profiles/seccomp-monitoring.json` | Monitoring seccomp |
| `images/tests/profiles/seccomp-security.json` | Security tool seccomp |
| `images/tests/profiles/apparmor-default` | Baseline AppArmor profile |
| `images/tests/profiles/apparmor-webserver.conf` | Web server AppArmor |
| `images/tests/profiles/apparmor-database.conf` | Database AppArmor |
| `images/tests/profiles/apparmor-security.conf` | Security tool AppArmor |
| `images/tests/test_seccomp.sh` | Seccomp test runner |
| `images/tests/test_apparmor.sh` | AppArmor test runner |

### Reports
| Path | Description |
|------|-------------|
| `.reports/phase_0_completion_report.md` | Phase 0 report |
| `.reports/phase_1_completion_report.md` | Phase 1 report |
| `.reports/phase_2_completion_report.md` | Phase 2 report |
| `.reports/phase_3_completion_report.md` | Phase 3 report |
| `.reports/phase_3_5_completion_report.md` | Phase 3.5 checksum verification report |
| `.reports/phase_4_completion_report.md` | Phase 4 HFT hardening report |
| `.reports/phase_5_completion_report.md` | Phase 5 military compliance report |

---

**Last Updated: 2026-04-20**
