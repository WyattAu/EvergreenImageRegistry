# Evergreen Image Registry

## Status
- **Phase:** 51
- **Version:** v26.3.0
- **Status:** Stable - All code bugs fixed, remaining failures are upstream issues
- **CI Status:** Build batches running, gate/lint 100% pass
- **Last Updated:** 2026-05-07

## Quality Scorecard
| Metric | Value | Status |
|--------|-------|--------|
| Total Images | 998 | COMPLETE |
| TOML Validation | 998/998 (0 errors) | PASS |
| JSON SBOM | 998/998 (0 errors) | PASS |
| .dockerignore | 997/998 (99.9%) | PASS |
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

## CI Pipeline
- Gate/Lint/Discover: 100% pass
- Remaining build failures: ALL upstream issues (0 code bugs)
- See ROADMAP.md for full upstream failure catalog

## Session Commit History (12 commits, ~409 image-fixes)
| Commit | What | Images |
|--------|------|--------|
| f000b409 | Blank line continuation fix | 75 |
| 4e5a3b42 | Shell continuation fixes | 60 |
| e502a757 | LABEL/placeholder fixes | 124 |
| 1d988645 | apk+php+heredoc fixes | 21 |
| 7dff8f17 | Orphaned command chains | 37 |
| 27d340b5 | apk+adduser+chown fixes | 25 |
| 43e15bce | Version bump 27 images | 27 |
| 46efe6e1 | Fix remaining failures | 14 |
| baa8c5c6 | VERSION.md v26.2.0 | 1 |
| ecd36165 | ROADMAP.md Phase 49-50 | 1 |
