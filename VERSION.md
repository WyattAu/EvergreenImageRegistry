# Evergreen Image Registry

**Version:** v31.0.0  
**Phase:** 113  
**Date:** 2026-07-06  

## Registry Status

| Metric | Value |
|--------|-------|
| Active images | 661 |
| Archived images | 351 |
| Health-shim version | v1.3.0 |
| Build type | Repack-from-upstream (GHCR) |
| CI Pipeline | ✅ 30/30 nightly jobs passing |
| GHCR | All 661 images available |
| Lint | ✅ 15/15 checks passing |
| Alpine references | 0 |
| Stubs/Placeholders | 0 |

## Image Pattern

All active images use the repack-from-upstream pattern:

```dockerfile
ARG SHIM_VERSION=v1.3.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM <upstream-image>
COPY --from=shim /shim /usr/local/bin/shim

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:<port>"]

ENV SHIM_METRICS_ENABLED="true"

LABEL evergreen.entrypoint.pattern="repack-upstream-init"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE <port> 9101
LABEL prometheus.io/scrape="true" prometheus.io/port="9101" prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
```

## CI Pipeline

- **Nightly:** Builds all 661 images, pushes to GHCR
- **Build type:** Plain `docker build` (not buildx)
- **Push:** GHCR only (no Docker Hub push)
- **Docker Hub login:** Used for pulling upstreams only
- **Smoke test:** Post-build runtime check (continue-on-error)
- **Gate checks:** HEALTHCHECK + security labels on all images

## Known Limitations

1. Images inherit upstream's USER (typically root)
2. Security labels are metadata, not enforced at build time
3. No ARM64 support (amd64 only)
4. 351 archived images need manual upstream verification
5. SBOMs generated from directory, not built image
