# Evergreen Image Registry

**Version:** v32.0.0  
**Phase:** 115  
**Date:** 2026-07-07

## Registry Status

| Metric | Value |
|--------|-------|
| Active images | 675 |
| Archived images | 336 |
| Hardened images | 8 |
| Docker Hub mirrors | 22 (124 Dockerfiles updated) |
| Health-shim version | v1.3.0 |
| Build type | Repack + Hardened + Mirrored |
| CI Pipeline | ✅ Nightly + multi-arch (critical tier) |
| GHCR | All 675 images available |
| Lint | ✅ 15/15 checks passing |
| SIS Stacks Deployed | 11+ |

## Hardened Images (8)

True scratch/wolfi-base, non-root (UID 65532), runtime-verified:

| Image | Base | Method | Verified |
|-------|------|--------|----------|
| redis | scratch | source-build | ✅ PONG |
| nginx | wolfi-base | apk-install | ✅ HTTP 200 |
| traefik | scratch | binary-download | ✅ HTTP 301 |
| prometheus | scratch | binary-download | ✅ HTTP 200 |
| alertmanager | scratch | binary-download | ✅ HTTP 200 |
| grafana | scratch | binary-extraction | ✅ HTTP 200 |
| oauth2-proxy | scratch | Go-binary | ✅ HTTP 403 (correct) |
| keycloak | upstream-repack | non-root UID 1000 | ✅ HTTP 200 |

## Docker Hub Mirrors (22)

Top 22 most-referenced Docker Hub upstreams mirrored to GHCR to eliminate rate limiting:

```
ghcr.io/wyattau/evergreenimageregistry/mirror-<name>:latest
```

Including: debian, python, golang, rust, redis, traefik, rabbitmq, argoproj/argocd, beryju/authentik, envoyproxy/envoy, jellyfin, homeassistant, minio, neo4j, thanos, adguardhome, etc.

124 Dockerfiles updated to use GHCR mirrors instead of Docker Hub.

## CI Pipeline

- **Nightly:** Builds all 675 images, pushes to GHCR
- **Multi-arch:** Critical tier now builds amd64 + arm64
- **Build:** Plain `docker build` (single-arch) or `docker buildx build --push` (multi-arch)
- **Push:** GHCR only
- **Smoke test:** Post-build runtime check (shim binary presence)
- **Docker Hub:** Login for pulling remaining upstreams (rate-limit mitigation via mirrors)

## Image Pattern

All active images use the repack-from-upstream pattern:

```dockerfile
FROM ghcr.io/wyattau/evergreenshim/health-shim:v1.3.0 AS shim
FROM ghcr.io/wyattau/evergreenimageregistry/mirror-<upstream>:latest
COPY --from=shim /shim /usr/local/bin/shim
HEALTHCHECK CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:<port>"]
```

Hardened images use source-build or binary-download to scratch:

```dockerfile
FROM debian:bookworm-slim AS downloader
RUN curl <binary> && tar -xzf ...
FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=downloader /app /app
USER 65532:65532
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/app"]
```

## Changelog (v31.1.0 → v32.0.0)

1. **Standardized shim v1.3.0** across all hardened images (v1.2.0/v1.3.0 split was a misunderstanding)
2. **Hardened 3 new images**: grafana, oauth2-proxy, keycloak
3. **Mirrored 22 Docker Hub upstreams** to GHCR (124 Dockerfiles updated)
4. **Re-enabled ARM64 multi-arch** for critical tier
5. **Added QEMU setup** for cross-compilation in CI
6. **4 images restored** from archive: grafana, oauth2-proxy, keycloak (3 new harden)
