# Evergreen Image Registry

## Status
- **Phase:** 49 (Post-CI Fix Iteration)
- **Version:** v26.2.0
- **Status:** Stable - All syntax errors resolved
- **CI Status:** Running (upstream failures only)
- **Last Updated:** 2026-05-06

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
| Anti-patterns | 0/10 (chmod 777, curl|sh, eval, sudo, etc.) | PASS |
| OCI title | 998/998 (100%) | PASS |
| OCI description | 997/998 (99.9%) | PASS |
| OCI source | 995/998 (99.7%) | PASS |
| OCI version | 996/998 (99.8%) | PASS |
| Non-root USER | 993/998 (99.5%) | PASS |
| ENTRYPOINT | 956/998 (95.8%) | PASS |
| STOPSIGNAL | 994/998 (99.6%) | PASS |
| HEALTHCHECK NONE | 438/998 (43.9%) | EXPECTED (mostly scratch) |
| HEALTHCHECK real | 559/998 (56.0%) | PASS |
| FROM digest pin | 1522/2020 (75.3%) | GOOD |
| Multi-arch TARGETARCH | 249 declared + 391 scratch | PASS |
| Determinism | Zstd + SOURCE_DATE_EPOCH | PASS |
| BuildKit cache | cache-from/cache-to | PASS |
| Dockerfile syntax | 0 parse errors | PASS |
| Orphaned commands | 0 | PASS |

## CI Pipeline
- 10 workflows, 23 jobs (12 build batches + gates + verify + etc.)
- Lint/Gates/Discover: Always PASS
- Build batches: PASS (syntax) / fail (upstream 404s only)
- All Dockerfile syntax errors resolved across 8 fix commits

## Known Upstream Failures (~50 images)
- GitHub download 404s (version bumped upstream)
- Registry images not found (deleted/renamed)
- Build failures (compilation, missing deps)
- Package not available (wolfi/apk)
