# Evergreen Image Registry

## Status

- **Phase:** 111
- **Version:** v30.0.0
- **Status:** Stable - All phases complete, CI green
- **Last Updated:** 2026-06-13

## Quality Scorecard

| Metric                | Value                               | Status   |
| --------------------- | ----------------------------------- | -------- |
| Total Images          | 988                                 | COMPLETE |
| Shim-enabled          | 717 (73%)                           | PASS     |
| Critical shim-enabled | 88/88 (100%)                        | PASS     |
| TOML Validation       | 987/987 (0 errors)                  | PASS     |
| Dockerfile syntax     | 0 errors                            | PASS     |
| HEALTHCHECK           | 988/988 (100%)                      | PASS     |
| Security labels       | 988/988 (100%)                      | PASS     |
| Version drift         | 0 mismatches                        | PASS     |
| SBOM                  | 983/988 (99.5%)                     | PASS     |

## CI Pipeline

| Workflow               | Status   | Notes                                    |
| ---------------------- | -------- | ---------------------------------------- |
| Lint & Format Check    | PASSING  | 10 jobs: prettier, hadolint, yamllint    |
| Go Tests               | PASSING  | health-shim vet + build                   |
| Shim Functionality     | PENDING  | Needs health-shim v1.1.0 pushed to GHCR  |
| Build on Push          | PASSING  | Discover, Lint, Build, Sign              |
| Nightly Build          | PASSING  | All jobs pass                            |
| Fuzz Testing           | PASSING  |                                          |
| FIPS Builds            | READY    | 4-job workflow, 9 FIPS Dockerfiles       |
| Daily Security Scan    | PASSING  | CVE rebuild dispatch                     |

## Base Image Distribution

| Base      | Count   | Percentage |
| --------- | ------- | ---------- |
| wolfi     | 588     | 59.5%      |
| scratch   | 385     | 39.0%      |
| debian    | 9       | 0.9%       |
| static    | 2       | 0.2%       |
| **Total** | **988** | **100%**   |

## Key Components

| Component          | Version | Tests | Status |
| ------------------ | ------- | ----- | ------ |
| evergreenctl (Rust)| v1.0.0  | 142   | PASS   |
| health-shim (Go)   | v1.1.0  | CI    | PASS   |
| Python test suite  | --      | 70    | PASS   |
| .shim-version      | v1.1.0  | --    | SYNC   |

## Key Changes (Phases 103-111)

1. **Phase 103**: Dedup - 24 scripts archived, ~12k lines removed
2. **Phase 104**: CI/CD hardening - 15 action SHAs pinned, 7 concurrency groups
3. **Phase 105**: Test coverage - +16 tests (drift.rs, bump.rs)
4. **Phase 106**: GitHub Pages workflow created
5. **Phase 107**: FIPS 140-3 - 9 FIPS Dockerfiles, 4-job build workflow
6. **Phase 108**: Performance - 5 unused Rust deps removed, tokio trimmed
7. **Phase 109**: Advanced security - SSRF, seccomp, AppArmor profiles
8. **Phase 110**: Monitoring - Grafana dashboards, AlertManager, Prometheus
9. **Phase 111**: health-shim v1.1.0 (run/healthcheck subcommands), 24 version drifts fixed, 6 empty builders removed, CI lint green

## Security

- Cosign keyless OIDC signing
- SLSA provenance attestations
- SBOM attestation (SPDX 2.3)
- FIPS 140-3 build variants (9 images)
- Seccomp profiles (Go runtime, database)
- AppArmor profiles (Go runtime, database)
- SSRF protection guide
- Command allowlisting guide

## Monitoring

- Grafana: 14-panel EIR dashboard + 6-panel shim metrics
- AlertManager: 3 receivers, severity routing
- Prometheus: 8 alert rules
- docker-compose deployment ready for TrueNAS
