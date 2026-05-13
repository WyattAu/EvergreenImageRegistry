# Evergreen Image Registry

## Status
- **Phase:** 63
- **Version:** v26.13.0
- **Status:** Stable - Phase 63 complete: Go health-shim 6 test functions, newRouter() refactor
- **Last Updated:** 2026-05-13

## Quality Scorecard
| Metric | Value | Status |
|--------|-------|--------|
| Total Images | 998 | COMPLETE |
| TOML Validation | 998/998 (0 errors) | PASS |
| JSON SBOM | 998/998 (0 errors) | PASS |
| .dockerignore | 998/998 (100%) | PASS |
| README.md | 998/998 (100%) | PASS |
| manifest.toml | 998/998 (100%) | PASS |
| sbom.spdx.json | 998/998 (100%) | PASS |
| Anti-patterns | 0 real (1 false positive) | PASS |
| OCI title | 998/998 (100%) | PASS |
| OCI description | 997/998 (99.9%) | PASS |
| OCI source | 995/998 (99.7%) | PASS |
| OCI version | 996/998 (99.8%) | PASS |
| Non-root USER | 993/998 (99.5%) | PASS |
| ENTRYPOINT | 956/998 (95.8%) | PASS |
| STOPSIGNAL | 994/998 (99.6%) | PASS |
| HEALTHCHECK NONE | 438/998 (43.9%) | EXPECTED (scratch) |
| HEALTHCHECK real | 559/998 (56.0%) | PASS |
| FROM digest pin | 1522/2020 (75.3%) | PASS |
| Multi-arch TARGETARCH | 249 declared + 391 scratch | PASS |
| Dockerfile syntax | 0 errors | PASS |
| Orphaned commands | 0 | PASS |
| Determinism | Zstd + SOURCE_DATE_EPOCH | PASS |
| Rigor (real binary) | 99.8% (996/998) | PASS |
| wolfi package compat | g++/redis/cpp/pkgconfig fixed | PASS |

## Code Quality Audit (2026-05-12)
| Metric | Value | Status |
|--------|-------|--------|
| Rust tests | 53/53 unit + 8/8 integration | PASS |
| Rust clippy | 0 warnings | PASS |
| Rust fmt | PASS | PASS |
| Rust release build | PASS | PASS |
| Python syntax | 29/29 scripts | PASS |
| Shell syntax | 25/25 scripts | PASS |
| Shell shellcheck | 0 errors (1 info) | PASS |
| Manifest TOML | 998/998 | PASS |
| SBOM JSON | 998/998 | PASS |
| Documentation emojis | 0 (archive-only) | PASS |
| Broken refs | 0 | PASS |
| Pre-commit hook | 5 std + 4 custom | PASS |
| Pre-push gate | 8-gate (9 checks) | PASS |

## Git Hooks
- **Pre-commit:** trailing-whitespace, EOF fixer, YAML/JSON lint, merge-conflict, hadolint, constraints, no-alpine, fast-tests (clippy+fmt+py+sh)
- **Pre-push:** 8-gate: Rust tests, clippy, fmt, Python syntax, Shell syntax, Manifest TOML, SBOM JSON, Dockerfile constraints, Rust release build

## CI Pipeline
- Gate/Lint/Discover: 100% pass
- Remaining build failures: ALL upstream issues (0 code bugs)
- See ROADMAP.md and ROADMAP_FORWARD.md for full upstream failure catalog
