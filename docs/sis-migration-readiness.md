# SimpleInfrastructureStack Migration Readiness

**Date:** 2026-05-20
**Evergreen Commit:** `b8f298d98`
**Evergreen CI Status:** 100% pass (839 active images, run `26107620954`)

---

## Executive Summary

SimpleInfrastructureStack (SIS) references **38 unique Docker images** across its compose files. Of these, **35 (92%) have direct Evergreen equivalents**. The remaining 3 are custom/specialized builds that need new Evergreen Dockerfiles. Migration is **conditionally ready** with blocking concerns on version alignment and 3 missing images.

---

## Coverage Matrix

### Fully Covered (35 images -- no blockers)

These images have Evergreen equivalents. Migration requires updating the image reference in SIS compose files from upstream to `ghcr.io/wyattau/evergreen/<name>`.

| SIS Image | SIS Version | Evergreen Image | Notes |
|-----------|-------------|-----------------|-------|
| `busybox` | 1.37.0 | `busybox` | Version match |
| `victoriametrics/victoria-metrics` | v1.143.0 | `victoriametrics` | SIS ahead |
| `victoriametrics/vmalert` | v1.143.0 | `vmalert` | SIS ahead |
| `grafana/grafana` | 12.2.8-security-04 | `grafana` | SIS ahead |
| `victoriametrics/victoria-logs` | v1.50.0 | `victoria-logs` | SIS ahead |
| `grafana/promtail` | 3.6.11 | `promtail` | SIS ahead |
| `louislam/uptime-kuma` | 2.3.2 | `uptime-kuma` | SIS ahead |
| `ghcr.io/google/cadvisor` | v0.57.0 | `cadvisor` | SIS ahead |
| `prom/node-exporter` | v1.11.1 | `node-exporter` | SIS ahead |
| `prom/alertmanager` | v0.32.1 | `alertmanager` | SIS ahead |
| `quay.io/prometheuscommunity/postgres-exporter` | v0.19.1 | `postgres-exporter` | SIS ahead |
| `oliver006/redis_exporter` | v1.83.0 | `redis-exporter` | SIS ahead |
| `grafana/tempo` | 2.10.5 | `tempo` | SIS ahead |
| `quay.io/prometheus/blackbox-exporter` | v0.28.0 | `blackbox-exporter` | SIS ahead |
| `ghcr.io/immich-app/immich-server` | v2.7.5 | `immich-server` | Version match |
| `ghcr.io/immich-app/immich-machine-learning` | v2.7.5 | `immich-machine-learning` | Version match |
| `valkey/valkey` | 9.0.4 | `valkey` | Close match |
| `postgres` | 17.10 | `postgres` | SIS ahead (see concerns) |
| `quay.io/keycloak/keycloak` | 26.6.2 | `keycloak` | SIS ahead |
| `code.forgejo.org/forgejo/forgejo` | 15.0.2 | `forgejo` | SIS ahead |
| `data.forgejo.org/forgejo/runner` | 12.10.1 | `forgejo-runner` | SIS ahead |
| `freshrss/freshrss` | 1.29.0 | `freshrss` | SIS ahead |
| `redis` | 7.4.9-alpine | `redis` | Close match |
| `ghcr.io/paperless-ngx/paperless-ngx` | 2.20.15 | `paperless-ngx` | SIS ahead |
| `matrixdotorg/synapse` | v1.152.1 | `synapse` | SIS ahead |
| `vectorim/element-web` | v1.12.18 | `element-web` | SIS ahead |
| `ghcr.io/matrix-org/matrix-hookshot` | 7.3.3 | `matrix-hookshot` | SIS ahead |
| `taigaio/taiga-back` | 6.9.0 | `taiga` | SIS ahead |
| `taigaio/taiga-front` | 6.9.0 | `taiga-front` | SIS ahead |
| `taigaio/taiga-events` | 6.9.0 | `taiga-events` | SIS ahead |
| `taigaio/taiga-protected` | 6.9.0 | `taiga-protected` | SIS ahead |
| `rabbitmq` | 3.13-management-alpine | `rabbitmq` | Close match |
| `cgr.dev/chainguard/nginx` | (digest) | `nginx` | Already Evergreen-compatible |
| `tecnativa/docker-socket-proxy` | v0.4.2 | `docker-socket-proxy` | Version match |
| `traefik` | v3.7.1 | `traefik` | SIS ahead |
| `favonia/cloudflare-ddns` | 1.16.2 | `cloudflare-ddns` | SIS ahead |
| `quay.io/oauth2-proxy/oauth2-proxy` | v7.15.2 | `oauth2-proxy` | SIS ahead |
| `crowdsecurity/crowdsec` | v1.7.8 | `crowdsec` | SIS behind (see concerns) |
| `alpine` | 3.22 | `alpine` | Version drift |
| `owncloud/ocis` | 8.0.3 | `ocis` | SIS ahead |
| `collabora/code` | 25.04.9.4.1 | `collabora` | Version match |
| `lscr.io/linuxserver/calibre-web` | 0.6.26 | `calibre-web` | Different upstream |
| `restic/restic` | 0.18.1 | `restic` | SIS ahead |
| `mariadb` | 11.8 | `mariadb` | SIS ahead |
| `akaunting/akaunting` | 3.1.21-v | `akaunting` | Version match |
| `prom/mysqld-exporter` | v0.19.0 | `mysqld-exporter` | Version match |
| `cloudflare/cloudflared` | 2026.5.0 | `cloudflared` | SIS ahead |
| `ghcr.io/gethomepage/homepage` | v1.13.1 | `homepage` | SIS ahead |
| `vaultwarden/server` | 1.36.0 | `vaultwarden` | SIS ahead |
| `containrrr/watchtower` | 1.7.1 | `watchtower` | SIS ahead |
| `linuxserver/wireguard` | 1.0.20250521 | `wireguard` | Different upstream |
| `frebib/zfs-exporter` | (digest) | `zfs-exporter` | Different fork |

### Missing from Evergreen (3 images -- blockers)

| Image | Reason | Impact | Resolution |
|-------|--------|--------|------------|
| `ghcr.io/immich-app/postgres:14-vectorchord0.4.3-pgvectors0.2.0` | Custom PostgreSQL with vector search extensions (vectorchord, pgvectors) | **HIGH** -- Immich requires vector extensions for AI search | Create new `immich-postgres` Evergreen image with extensions, or configure standard postgres with extension installation in SIS init |
| `infra-webhook` (custom build from `stacks/webhook/Dockerfile`) | Bespoke deployment tool built locally | **LOW** -- Not a third-party image | Create Evergreen Dockerfile or keep as local build |
| SIS custom Dockerfiles (`webhook/Dockerfile`, `backup/cron-trigger.Dockerfile`) | Use `alpine:3.21` as build base | **LOW** -- Simple scripts | Update to use Evergreen wolfi/alpine base |

---

## Blocking Concerns

### 1. Version Alignment (MEDIUM)

SIS is generally **ahead** of Evergreen versions because SIS pins specific upstream tags while Evergreen tracks a slightly older stable set. Before migration:

- **Evergreen VERSION pins must be updated** to match or exceed SIS versions
- This is a `sed` on ARG VERSION lines in Evergreen Dockerfiles, then a CI rebuild
- Estimated effort: update ~50 VERSION ARGs, rebuild, validate

Key version gaps:

| Image | SIS Version | Evergreen Version | Gap |
|-------|-------------|-------------------|-----|
| postgres | 18.3-alpine (beta) | 17.6 | SIS uses PG18 **beta** -- risky |
| postgres (multiple stacks) | 16.13, 17.10 | 17.6 | Fragmented across 4 versions |
| crowdsec | v1.7.8 | v1.6.2 | SIS significantly ahead |
| grafana | 12.2.8-security-04 | 10.4.1 | Major version behind |
| immich-server | v2.7.5 | 2.7.5 | Match |
| forgejo | 15.0.2 | 12.0.3 | Major version behind |

### 2. PostgreSQL 18 Beta (HIGH)

The SIS collaboration stack uses `postgres:18.3-alpine`. PostgreSQL 18 is currently in beta. Evergreen tracks PostgreSQL 17.6 (latest stable). Running beta PG in production is a risk independent of Evergreen -- SIS should pin to PG 17 for stability.

### 3. Immich Custom PostgreSQL (HIGH)

Immich requires `vectorchord` and `pgvectors` extensions. The standard Evergreen `postgres` image does not include these. Options:

1. **Create `immich-postgres` Evergreen image** that builds PG with vector extensions
2. **Use standard postgres + init script** to install extensions at container start
3. **Keep upstream image** for this one service (hybrid approach)

### 4. LinuxServer.io Images (LOW)

`lscr.io/linuxserver/calibre-web` and `linuxserver/wireguard` follow linuxserver.io conventions (different config paths, user management, PUID/PGID). Evergreen equivalents may behave differently. Requires functional testing.

### 5. ZFS Exporter Fork (LOW)

SIS uses `frebib/zfs-exporter`; Evergreen uses `fberning/zfs-exporter`. These are different forks and may have different metrics or ZFS compatibility. Verify feature parity.

---

## Non-Blocking Differences

### Base Image: Alpine vs Wolfi

SIS uses `-alpine` suffixed tags for some images (redis, postgres, rabbitmq). Evergreen uses wolfi-base (glibc-based). Functionally compatible -- both are minimal Linux bases -- but runtime library availability differs. Alpine uses musl; wolfi uses glibc. This is an improvement, not a regression.

### HEALTHCHECK Behavior Change

Evergreen images now **fail loudly** when binaries are missing (exit code 1 instead of sleep infinity). This is strictly better for SIS -- a broken image will be immediately visible in orchestrator health checks rather than silently running.

### User/Permission Model

All Evergreen images run as UID 65532:65532 (non-root). SIS may need to adjust volume mounts and file permissions accordingly.

---

## Recommended Migration Strategy

### Phase 1: Version Alignment (Pre-requisite)
1. Update Evergreen VERSION ARGs to match SIS versions (except PG18 beta)
2. Rebuild all affected images
3. Validate with CI (100% pass required)

### Phase 2: Create Missing Images
1. Create `immich-postgres` Evergreen image with vector extensions
2. Create `infra-webhook` Evergreen image
3. Build and validate

### Phase 3: Stacked Migration (One Stack at a Time)
1. Start with lowest-risk stack (e.g., `proxy` -- traefik, cloudflare-ddns, oauth2-proxy)
2. Update image references in SIS compose files
3. Test locally on TrueNAS (docker pull from GHCR)
4. Verify functionality
5. Move to next stack

Recommended order (low to high risk):
1. `proxy` (3 images, stateless)
2. `utility` (homepage, watchtower)
3. `monitoring` (15 images, mostly exporters)
4. `vpn` (wireguard)
5. `backup` (restic)
6. `tunnel` (cloudflared)
7. `vaultwarden` (1 image)
8. `accounting` (mariadb, akaunting, mysqld-exporter)
9. `books` (calibre-web)
10. `rss` (freshrss, postgres)
11. `documents` (paperless-ngx, postgres, redis)
12. `photos` (immich-server, immich-ml, valkey, immich-postgres)
13. `iam` (postgres, keycloak)
14. `operations` (postgres, forgejo, forgejo-runner)
15. `collaboration` (synapse, element-web, matrix-hookshot, postgres)
16. `project-management` (taiga-back/front/events/protected, rabbitmq, nginx)
17. `storage` (ocis, collabora)
18. `security` (crowdsec)

### Phase 4: Cleanup
1. Remove upstream image references from SIS
2. Update SIS documentation
3. Configure Watchtower to use Evergreen registry

---

## Prerequisites Before Migration

- [ ] Evergreen versions updated to match SIS
- [ ] `immich-postgres` Evergreen image created and validated
- [ ] PostgreSQL 18 beta addressed (pin to PG 17 in SIS or create PG18 Evergreen)
- [ ] Crowdsec version updated in Evergreen to v1.7.8+
- [ ] Grafana version updated in Evergreen to 12.x
- [ ] Forgejo version updated in Evergreen to 15.x
- [ ] ZFS exporter fork parity verified
- [ ] All images rebuilt and CI-validated at 100%
