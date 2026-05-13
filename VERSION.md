# Evergreen Image Registry

## Status

- **Phase:** 88
- **Version:** v27.0.0
- **Status:** Stable - Full roadmap execution complete (Phases 66-88)
- **Last Updated:** 2026-05-13

## Quality Scorecard

| Metric                | Value                          | Status             |
| --------------------- | ------------------------------ | ------------------ |
| Total Images          | 998                            | COMPLETE           |
| TOML Validation       | 998/998 (0 errors)             | PASS               |
| JSON SBOM             | 998/998 (0 errors)             | PASS               |
| .dockerignore         | 998/998 (100%)                | PASS               |
| README.md             | 998/998 (100%)                | PASS               |
| manifest.toml         | 998/998 (100%)                | PASS               |
| sbom.spdx.json        | 998/998 (100%)                | PASS               |
| Anti-patterns         | 0 real (1 false positive)     | PASS               |
| OCI title             | 998/998 (100%)                | PASS               |
| OCI description       | 997/998 (99.9%)               | PASS               |
| OCI source            | 995/998 (99.7%)               | PASS               |
| OCI version           | 996/998 (99.8%)               | PASS               |
| Non-root USER         | 993/998 (99.5%)               | PASS               |
| ENTRYPOINT            | 956/998 (95.8%)               | PASS               |
| STOPSIGNAL            | 994/998 (99.6%)               | PASS               |
| HEALTHCHECK NONE      | 438/998 (43.9%)               | EXPECTED (scratch) |
| HEALTHCHECK real      | 559/998 (56.0%)               | PASS               |
| HEALTHCHECK shim      | 1/998 (health-shim)           | PASS               |
| FROM digest pin       | 1511/2001 (75.5%)             | PASS               |
| Multi-arch TARGETARCH | 283 declared + 398 scratch    | PASS               |
| Dockerfile syntax     | 0 errors                      | PASS               |
| Orphaned commands     | 0                             | PASS               |
| Determinism           | Zstd + SOURCE_DATE_EPOCH      | PASS               |
| Rigor (real binary)   | 99.8% (996/998)               | PASS               |
| Deprecated images     | 3 marked (cayley, meshbird, immudb) | TRACKED       |
| Policy enforcement    | 9 policies defined            | PASS               |

## Code Quality Audit (2026-05-13)

| Metric               | Value                          | Status |
| -------------------- | ------------------------------ | ------ |
| Rust tests           | 65/65 unit + 47/47 integration | PASS   |
| Rust clippy          | 0 warnings                     | PASS   |
| Rust fmt             | PASS                           | PASS   |
| Rust release build   | PASS                           | PASS   |
| Python ruff lint     | 0 errors (32 scripts)          | PASS   |
| Python ruff format   | 0 errors (32 scripts)          | PASS   |
| Python syntax        | 32/32 scripts                  | PASS   |
| Shell syntax         | 25/25 scripts                  | PASS   |
| Manifest TOML        | 998/998                        | PASS   |
| SBOM JSON            | 998/998                        | PASS   |
| Documentation emojis | 0                              | PASS   |
| Pre-push gate        | 10-gate (all PASS)             | PASS   |

## Git Hooks

- **Pre-commit:** trailing-whitespace, EOF fixer, YAML/JSON lint, merge-conflict, hadolint, constraints, no-alpine,
  fast-tests (clippy+fmt+ruff+py+sh)
- **Pre-push:** 10-gate: Rust unit tests, Rust integration tests, clippy, fmt, Python syntax + ruff lint, Shell syntax,
  Manifest TOML, SBOM JSON, Dockerfile constraints, Rust release build

## CI Pipeline

- 15 GitHub Actions workflows (build, lint, scan, sign, provenance, fuzz, nightly, daily-security, auto-bump,
  readme-update, sbom-drift-detection, actionlint, manifest-validation, sbom-validation, no-alpine)
- Gate/Lint/Discover: 100% pass
- Remaining build failures: ALL upstream issues (0 code bugs)
- Dockerfile.ci: 16 pinned tools (docker, buildx, trivy, grype, cosign, syft, hadolint, helm, kubectl, crane, yq,
  trufflehog, shellcheck, ruff, go, actionlint)

## Completed Roadmap Phases

| Phase | Description                                     | Key Deliverable                        |
| ----- | ----------------------------------------------- | -------------------------------------- |
| 66    | Upstream failure resolution                    | 5 images bumped, 3 deprecated, caddy org fixed |
| 67    | Test framework expansion                      | Already complete (946/1013 real configs)  |
| 68    | evergreenctl test expansion                   | 112 tests (65 unit + 47 integration)    |
| 69    | Digest pinning analysis                       | 75.5% pinned, 0 runtime gaps              |
| 70    | CI hardening                                  | 5 new CI jobs, 3 tools in Dockerfile.ci  |
| 71-72 | Multi-arch expansion                          | 21 images gained TARGETARCH support      |
| 73-74 | SBOM depth and drift detection                | sbom_drift_detect.py + nightly CI job     |
| 75-76 | evergreenctl maturation                       | report, deprecated, completion commands  |
| 77-78 | Health-shim expansion                         | TCP/HTTP probes, structured metrics, tests |
| 79-83 | Policy-as-code and operational excellence       | image_policy.yaml, enforce_policy.py, metrics dashboard, auto-bump workflow |

## evergreenctl Subcommands (18 total)

audit, bump, ci-diff, completion, deprecated, discover, drift, generate, migrate, outdated, pin-digests,
report, sign, snapshot, validate, verify, verify-all
