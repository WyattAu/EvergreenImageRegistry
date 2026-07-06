# Evergreen Image Registry

**Version:** v31.1.0  
**Phase:** 114  
**Date:** 2026-07-06

## Registry Status

| Metric | Value |
|--------|-------|
| Active images | 673 |
| Archived images | 339 |
| Health-shim version | v1.3.0 |
| Build type | Repack-from-upstream (GHCR) |
| CI Pipeline | ✅ 30/30 nightly jobs passing |
| GHCR | All 673 images available |
| Lint | ✅ 15/15 checks passing |
| SIS Stacks Deployed | 11+ |

## Image Pattern

All active images use the repack-from-upstream pattern:

```dockerfile
FROM ghcr.io/wyattau/evergreenshim/health-shim:v1.3.0 AS shim
FROM <upstream>:<pinned-version>
COPY --from=shim /shim /usr/local/bin/shim
HEALTHCHECK CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:<port>"]
```

Key principles:
- No ENTRYPOINT override (inherit upstream)
- Shim for HEALTHCHECK only
- USER root for apps with complex entrypoints (paperless-ngx, freshrss)
- Security labels as metadata (not yet enforced)
- Version-pinned upstreams for reproducibility

## CI Pipeline

- **Nightly:** Builds all 673 images, pushes to GHCR
- **Build:** Plain `docker build` (inherits Docker Hub credentials)
- **Push:** GHCR only (30/30 batches pass)
- **Smoke test:** Post-build runtime check
- **Docker Hub:** Login for pulling upstreams only
