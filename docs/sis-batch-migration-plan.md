# SIS Batch Migration Plan

**Date:** 2026-06-14 | **EIR Version:** v30.1.0 | **Shim:** v1.2.0

## Verified Working (Phase 112)

| Image        | Tested On        | Result                                                    |
| ------------ | ---------------- | --------------------------------------------------------- |
| prometheus   | Runner + TrueNAS | Healthy, flags pass through shim                          |
| alertmanager | Runner + TrueNAS | Healthy, flags pass through shim                          |
| grafana      | Runner + TrueNAS | Healthy, provisioning + dashboards loaded                 |
| oauth2-proxy | Runner           | --version and --help pass through (flag bug fixed)        |
| keycloak     | Runner           | Fully boots (JVM + Quarkus + DB schema), start-dev via -- |

## Batch Migration Groups

### Batch 1: Stateless Services (Lowest Risk)

**Pre-req:** None **Estimated time:** 2 hours

| Stack   | Images                   | Notes                                                   |
| ------- | ------------------------ | ------------------------------------------------------- |
| proxy   | traefik, cloudflare-ddns | oauth2-proxy blocked LESSON-002 (now fixed with v1.2.0) |
| utility | homepage, watchtower     | Stateless, easy rollback                                |
| tunnel  | cloudflared              | Single image, stateless                                 |

**Total:** 5 images

### Batch 2: Simple Stateful (Low Risk)

**Pre-req:** Batch 1 validated **Estimated time:** 2 hours

| Stack       | Images                              | Notes                |
| ----------- | ----------------------------------- | -------------------- |
| vaultwarden | vaultwarden                         | Single image, SQLite |
| backup      | restic                              | Single image         |
| accounting  | mariadb, akaunting, mysqld-exporter | DB + app + exporter  |
| rss         | freshrss, postgres                  | DB + app             |

**Total:** 7 images

### Batch 3: Documents & Media (Medium Risk)

**Pre-req:** Batch 2 validated **Estimated time:** 3 hours

| Stack     | Images                                            | Notes                   |
| --------- | ------------------------------------------------- | ----------------------- |
| documents | paperless-ngx, postgres, redis                    | Requires data migration |
| photos    | immich-server, immich-ml, valkey, immich-postgres | Custom PG with pgvector |

**Total:** 7 images

### Batch 4: Identity & Operations (Higher Risk)

**Pre-req:** Batches 1-3 validated **Estimated time:** 4 hours

| Stack      | Images                            | Notes                     |
| ---------- | --------------------------------- | ------------------------- |
| iam        | postgres, keycloak                | Keycloak verified working |
| operations | postgres, forgejo, forgejo-runner | CI/CD critical            |

**Total:** 5 images

### Batch 5: Collaboration & Security (Highest Risk)

**Pre-req:** Batches 1-4 validated **Estimated time:** 4 hours

| Stack         | Images                                             | Notes                     |
| ------------- | -------------------------------------------------- | ------------------------- |
| collaboration | synapse, element-web, matrix-hookshot, postgres    | Complex federation        |
| project-mgmt  | taiga-back/front/events/protected, rabbitmq, nginx | Multi-service             |
| storage       | ocis, collabora                                    | Microservice architecture |
| security      | crowdsec                                           | Needs cscli/LAPI config   |

**Total:** 12 images

### Known Exceptions (Keep Upstream)

| Image                      | Reason                                                    |
| -------------------------- | --------------------------------------------------------- |
| vpn/wireguard              | Kernel WireGuard vs userspace wireguard-go (not feasible) |
| zfs-exporter (frebib fork) | Different fork, verify parity first                       |

## Per-Stack Migration Checklist

For each stack:

1. Pull EIR images on TrueNAS
2. Stop existing containers (keep volumes)
3. chown volumes to 65532:65532
4. Update SIS compose to use EIR image references
5. Start containers with docker compose up
6. Verify healthchecks pass
7. Test functionality (login, CRUD, API)
8. Monitor for 24 hours before next batch

## Rollback Plan

For each batch:

- Keep old compose file as `docker-compose.yml.pre-eir`
- Old images remain in local Docker cache
- Rollback: `docker compose -f docker-compose.yml.pre-eir up -d`
- Volume data preserved (no destructive changes)
