# Evergreen Image Registry

**Version:** v32.0.0  
**Phase:** 116  
**Date:** 2026-07-08

## Registry Status

| Metric | Value |
|--------|-------|
| Active images | 706 |
| Archived images | 305 |
| Hardened images | 10 |
| Docker Hub mirrors | 22 (124 Dockerfiles updated) |
| Health-shim version | v1.3.0 |
| Build type | Repack + Hardened + Mirrored |
| CI Pipeline | ✅ Nightly + multi-arch (critical + standard) |
| GHCR | All 706 images available |
| Lint | ✅ 15/15 checks passing |
| SIS Stacks Deployed | 11+ |

## Hardened Images (10)

True wolfi-base/scratch, non-root, runtime-verified:

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
| postgresql-16 | Chainguard wolfi | non-root UID 70 | ✅ SELECT 1 |
| mariadb | Chainguard wolfi | non-root UID 65532 | ✅ mysqladmin alive |

## Restored Images (31)

Previously archived due to missing Docker Hub namespace. Fixed upstream references:

audiobookshelf, cloudflared, cryptpad, dex, docker-socket-proxy, elasticsearch,
element-web, envoy, ferretdb, freshrss-minimal, gitea-actions, koel, lidarr,
lychee, mailhog, metricbeat, mosquitto, n8n, outline, packetbeat, photoview,
piwigo, planka, postgis, privatebin, tempo, valkey, watchtower, whisparr,
woodpecker-agent, woodpecker-server

## CI Pipeline

- **Nightly:** Builds all 706 images, pushes to GHCR
- **Multi-arch:** Critical + Standard tiers: amd64 + arm64 (QEMU + buildx)
- **Build:** Plain `docker build` (single-arch) or `docker buildx build --push` (multi-arch)
- **Push:** GHCR only
- **Smoke test:** Post-build runtime check (shim binary presence)
- **Docker Hub:** Login for pulling remaining upstreams (22 mirrored to GHCR)

## Changelog (v31.1.0 → v32.0.0)

1. **Standardized shim v1.3.0** across all hardened images
2. **Hardened 5 new images**: grafana, oauth2-proxy, keycloak, postgresql-16, mariadb
3. **Mirrored 22 Docker Hub upstreams** to GHCR (124 Dockerfiles updated)
4. **Re-enabled ARM64 multi-arch** for critical + standard tiers
5. **Restored 31 archived images** with correct upstream Docker Hub paths
6. **Added QEMU setup** for cross-compilation in CI
