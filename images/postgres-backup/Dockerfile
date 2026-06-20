# =============================================================================
# EVERGREEN HARDENED POSTGRES BACKUP
# Generated from template - Version: 17
# Wolfi-base provides glibc; pg_dump and xz from upstream debs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=17
RUN mkdir -p /app /backups /var/log/postgres-backup /var/cache/postgres-backup || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION}-client xz-utils && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /backups /var/log/postgres-backup /var/cache/postgres-backup || true


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client wget ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/postgres-backup /var/log/postgres-backup
COPY --from=builder --chown=65532:65532 /var/cache/postgres-backup /var/cache/postgres-backup
WORKDIR /app
RUN echo '#!/bin/sh' > /app/backup.sh && \
    echo 'set -eu' >> /app/backup.sh && \
    echo ': "${PGHOST:?PGHOST is required}"' >> /app/backup.sh && \
    echo ': "${PGUSER:?PGUSER is required}"' >> /app/backup.sh && \
    echo 'TIMESTAMP="$(date +%Y%m%d_%H%M%S)"' >> /app/backup.sh && \
    echo 'DB="${PGDATABASE:-all}"' >> /app/backup.sh && \
    echo 'OUTPUT="/backups/${DB}_${TIMESTAMP}.dump.xz"' >> /app/backup.sh && \
    echo 'if [ "$DB" = "all" ]; then' >> /app/backup.sh && \
    echo '    pg_dumpall --host="$PGHOST" --user="$PGUSER" | xz -9 > "$OUTPUT"' >> /app/backup.sh && \
    echo 'else' >> /app/backup.sh && \
    echo '    pg_dump --host="$PGHOST" --user="$PGUSER" --format=directory --jobs=4 --file="/backups/${DB}_${TIMESTAMP}" "$DB" && \' >> /app/backup.sh && \
    echo '    tar -cf - "/backups/${DB}_${TIMESTAMP}" | xz -9 > "$OUTPUT" && \' >> /app/backup.sh && \
    echo '    rm -rf "/backups/${DB}_${TIMESTAMP}"' >> /app/backup.sh && \
    echo 'fi' >> /app/backup.sh && \
    echo 'echo "Backup complete: $OUTPUT"' >> /app/backup.sh
RUN chmod +x /app/backup.sh && chown 65532:65532 /app/backup.sh
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="false" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/app/backup.sh"]
LABEL org.opencontainers.image.title="postgres-backup" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Backup Container with pg_dump + xz compression" \
      org.opencontainers.image.vendor="PostgreSQL" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/postgres/postgres"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
