# Evergreen Image Registry - Roadmap

| Attribute | Value          |
| --------- | -------------- |
| Version   | 30.1.0         |
| Updated   | 2026-06-14     |
| Status    | STABLE         |
| Phases    | 0-112 complete |

---

## Current State (v30.0.0)

| Metric                   | Value                            | Status                      |
| ------------------------ | -------------------------------- | --------------------------- |
| Total images             | 987                              | --                          |
| HEALTHCHECK (real)       | 558/987 (56.5%)                  | DONE                        |
| HEALTHCHECK NONE         | 426/987 (43.2%)                  | Expected (scratch/no-shell) |
| Security labels (4)      | 100%                             | DONE                        |
| OCI labels (title)       | 99.8% (985/987)                  | DONE                        |
| SBOM                     | 99.6% (983/987)                  | DONE                        |
| Non-root USER            | 98.9% (975/987)                  | DONE                        |
| ENTRYPOINT               | 95.7% (944/987)                  | DONE                        |
| STOPSIGNAL               | 99.6% (981/987)                  | DONE                        |
| Multi-arch (amd64+arm64) | 849 declared                     | DONE                        |
| Docker Hub mirror        | 98 repos at docker.io/wyattau/   | DONE                        |
| CI/CD workflows          | 22 active                        | DONE                        |
| evergreenctl (Rust)      | v1.0.0, 142 tests                | DONE                        |
| health-shim (Go)         | v1.2.0, run+healthcheck+flag fix | DONE                        |
| Python test suite        | 70 tests                         | DONE                        |

---

## Audit Results (2026-06-13)

### Code Quality Audit Summary

| Component      | Tests | CRITICAL  | HIGH | MEDIUM | LOW |
| -------------- | ----- | --------- | ---- | ------ | --- |
| evergreenctl   | 126   | 1 (fixed) | 4    | 14     | 30  |
| health-shim    | 14    | 5 (fixed) | 6    | 9      | 8   |
| Python scripts | 70    | 4 (fixed) | 8    | 16     | 14  |
| CI/CD          | --    | 4 (fixed) | 12   | 22     | 18  |

### Issues Fixed in This Audit (14 files, 315 insertions, 275 deletions)

**evergreenctl (Rust):**

- sign.rs: Hardcoded registry corrected, manifest parsed once, configurable via env var
- generate.rs: Stub binary fallback removed, error swallowing removed, constants extracted
- deprecated.rs: Path traversal validation added

**health-shim (Go):**

- Dockerfile: Source filename corrected (main.go), silent build failure removed
- main.go: Graceful shutdown, atomic.Bool for startupSuccess, doubled HTTP prefix fixed
- main.go: Prometheus format corrected, HTTP method validation, version injectable

**Python scripts:**

- pre_commit_validator.py: Global mutable state removed, UID check corrected
- check_upstream_versions.py: Custom TOML parser replaced with tomllib

**CI/CD workflows:**

- shim-test.yml: Path filter corrected
- daily-security-scan.yml: Workflow dispatch fixed, dead env var removed
- \_build-reusable.yml: Secret handling hardened, certificate identity corrected
- build-nightly.yml: Baseline overwrite fixed
- upstream-watch.yml: Shell injection fixed, dead labels expression fixed

---

## Phase Plan: 103-110

### Phase 103: Deduplication and Cleanup

Priority: HIGH | Effort: 2-3 days

| Task                                                | Action                                   | Lines Removed |
| --------------------------------------------------- | ---------------------------------------- | ------------- |
| Merge cosign-sign.yml into sign-images.yml          | Delete cosign-sign.yml                   | 118           |
| Merge nightly-scan.yml into daily-security-scan.yml | Delete nightly-scan.yml                  | 462           |
| Delete generate_all_sboms.py                        | Keep shell version (Makefile-integrated) | 308           |
| Delete fix_wolfi_packages.py                        | Keep v2                                  | 187           |
| Archive populate*remediated_checksums*\*.py         | One-time migration scripts               | 1163          |
| Archive generate_tier3\*.py/.sh (6 files)           | One-time scaffolding                     | 5728          |
| Delete check_upstream_versions.py                   | Superseded by evergreenctl outdated      | 167           |
| Archive 14 one-time migration scripts               | Already executed                         | ~4000         |

**Total estimated cleanup: ~12,000 lines removed**

### Phase 104: CI/CD Hardening

Priority: HIGH | Effort: 1-2 days

| Task                               | Detail                                              |
| ---------------------------------- | --------------------------------------------------- |
| Pin all actions by SHA             | 12 action references use tags                       |
| Add missing concurrency groups     | 10 workflows lack concurrency control               |
| Split build-on-push.yml            | Separate PR (read-only) from push (write)           |
| Remove redundant shimctl build     | Unused step adds 2-3 min per run                    |
| Fix build-forgejo-runner-image.yml | Use docker/login-action instead of --password-stdin |

### Phase 105: Test Coverage Enhancement

Priority: MEDIUM | Effort: 3-5 days

| Component             | Gap                                             | Tests to Add          |
| --------------------- | ----------------------------------------------- | --------------------- |
| evergreenctl drift.rs | 0 unit tests for parse_dockerfile               | 8-10 tests            |
| evergreenctl bump.rs  | 0 unit tests for version extraction/replacement | 6-8 tests             |
| health-shim           | 15 error paths untested                         | ~15 tests             |
| health-shim           | No table-driven tests                           | Refactor + edge cases |
| Python scripts        | 6 scripts have no tests                         | ~20 tests             |

### Phase 106: Documentation Site Deployment

Priority: MEDIUM | Effort: 0.5-1 day

| Task                         | Detail                                               |
| ---------------------------- | ---------------------------------------------------- |
| Create Jekyll build workflow | GitHub Actions workflow for pages-build-deployment   |
| Verify all doc links         | Internal and external link validation                |
| Update image-audit-report.md | Current report is stale (reports 841, actual is 987) |

### Phase 107: FIPS 140-3 Build Variants

Priority: LOW | Effort: 5-7 days

| Task                          | Detail                                                 |
| ----------------------------- | ------------------------------------------------------ |
| Implement FIPS build variants | 30 images with implementation plans (compliance/fips/) |
| BoringCrypto builds           | Go images with GOEXPERIMENT=boringcrypto               |
| BoringSSL builds              | Rust images with aws-lc-rs (already using)             |
| OpenSSL FIPS builds           | C/C++ images with OpenSSL 3.x FIPS module              |

### Phase 108: Performance Optimization

Priority: LOW | Effort: 2-3 days

| Task                            | Detail                                     |
| ------------------------------- | ------------------------------------------ |
| evergreenctl tokio feature trim | Use only rt-multi-thread + macros + time   |
| Remove chrono dependency        | Use time crate (already pulled by reqwest) |
| Remove unused url dependency    | Listed in Cargo.toml but never imported    |
| Health-shim metrics recording   | Unify mutex + atomic patterns              |

### Phase 109: Advanced Security

Priority: LOW | Effort: 3-5 days

| Task                                 | Detail                                                  |
| ------------------------------------ | ------------------------------------------------------- |
| Seccomp profiles per category        | Apply security/seccomp/ profiles to images              |
| AppArmor profiles                    | Apply security/apparmor/ profiles to images             |
| SSRF protections for health-shim     | Block RFC 1918/link-local in /http/ and /tcp/ endpoints |
| Command allowlisting for health-shim | Restrict /cmd/ endpoint to configurable allowlist       |

### Phase 110: Scaling and Monitoring

Priority: LOW | Effort: 2-3 days

| Task                            | Detail                                                      |
| ------------------------------- | ----------------------------------------------------------- |
| Grafana dashboards deployment   | Deploy dashboards/evergreen-shim-metrics.json to production |
| AlertManager integration        | Wire ShimBus alerting into production Grafana               |
| Performance regression baseline | Collect and compare production metrics                      |
| ARM64 hardware testing          | Validate multi-arch on real ARM hardware                    |

---

## Phase 111: health-shim v1.1.0 + CI Lint Green

Priority: HIGH | Effort: 1 day | Status: COMPLETE

| Task                                 | Status |
| ------------------------------------ | ------ |
| health-shim v1.1.0 (run/healthcheck) | DONE   |
| 717 Dockerfiles updated to v1.1.0    | DONE   |
| 24 version drifts fixed              | DONE   |
| 6 empty builder stages removed       | DONE   |
| Prettier/YAMLLint/cargo fmt fixes    | DONE   |
| upstream-watch parser fix            | DONE   |
| daily-security-scan artifact fix     | DONE   |
| nightly timeout 30->120min           | DONE   |
| Monitoring deployment stack          | DONE   |
| immich-postgres with pgvector        | DONE   |
| 5 stale dependabot PRs closed        | DONE   |
| clawdius excluded from lint          | DONE   |

---

## Phase 112: health-shim v1.2.0 + Monitoring Deployed

Priority: HIGH | Effort: 1 day | Status: COMPLETE

| Task                                  | Status |
| ------------------------------------- | ------ |
| health-shim v1.2.0 (flag parsing fix) | DONE   |
| --help passthrough fix                | DONE   |
| 718 Dockerfiles updated to v1.2.0     | DONE   |
| Prometheus ENTRYPOINT path fix        | DONE   |
| Monitoring deployed to TrueNAS        | DONE   |
| Native entrypoints (no overrides)     | DONE   |
| Grafana datasources + dashboards      | DONE   |
| oauth2-proxy verified (flags pass)    | DONE   |
| Keycloak verified (JVM boots)         | DONE   |

---

## Known Gaps

- 5 auth-gated `:latest` FROM refs (dependabot, lancedb, scylladb, tigergraph x2)
- 100 `${VERSION}` build-time FROM refs (acceptable -- resolved at build time)
- 360 images without multi-arch (C-extension Python ~80, amd64-only upstream ~200, GPU/ML ~50, niche ~30)
- Forgejo v15 cancel-in-progress bug (fixed in v16, July 16, 2026)
- Win11 VM runner offline (needs SPICE console access)
- 5 images missing SBOMs (988 images, 983 SBOMs)
- Evergreen node-exporter not published to GHCR (using official prom/node-exporter)

## NOT Recommended

| Item                                                   | Reason                                               |
| ------------------------------------------------------ | ---------------------------------------------------- |
| LICENSE per image                                      | SBOMs already capture license info                   |
| Migrate 15 debian images to wolfi                      | High regression risk                                 |
| Per-image docker-compose files                         | Unmaintainable at 987 scale                          |
| Builder image multi-arch (golang, rust, maven, gradle) | Digest-pinned Debian needs per-arch digests, low ROI |
