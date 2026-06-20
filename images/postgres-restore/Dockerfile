# =============================================================================
# EVERGREEN HARDENED POSTGRES RESTORE
# Generated from template - Version: 17
# Wolfi-base provides glibc; pg_restore and xz from upstream debs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=17
RUN mkdir -p /app /backups /var/log/postgres-restore /var/cache/postgres-restore || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION}-client xz-utils && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /backups /var/log/postgres-restore /var/cache/postgres-restore || true


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client wget ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/postgres-restore /var/log/postgres-restore
COPY --from=builder --chown=65532:65532 /var/cache/postgres-restore /var/cache/postgres-restore
WORKDIR /app
RUN echo '#!/bin/sh' > /app/restore.sh && \
    echo 'set -eu' >> /app/restore.sh && \
    echo ': "${PGHOST:?PGHOST is required}"' >> /app/restore.sh && \
    echo ': "${PGUSER:?PGUSER is required}"' >> /app/restore.sh && \
    echo ': "${PGDATABASE:?PGDATABASE is required}"' >> /app/restore.sh && \
    echo ': "${BACKUP_FILE:?BACKUP_FILE is required}"' >> /app/restore.sh && \
    echo 'if [ ! -f "$BACKUP_FILE" ]; then' >> /app/restore.sh && \
    echo '    echo "Backup file not found: $BACKUP_FILE"' >> /app/restore.sh && \
    echo '    exit 1' >> /app/restore.sh && \
    echo 'fi' >> /app/restore.sh && \
    echo 'case "$BACKUP_FILE" in' >> /app/restore.sh && \
    echo '    *.dump.xz)' >> /app/restore.sh && \
    echo '        TEMP_DIR="$(mktemp -d)"' >> /app/restore.sh && \
    echo '        xzcat "$BACKUP_FILE" | tar -xf - -C "$TEMP_DIR"' >> /app/restore.sh && \
    echo '        pg_restore --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE" --clean --if-exists --jobs=4 "$TEMP_DIR"/*' >> /app/restore.sh && \
    echo '        rm -rf "$TEMP_DIR"' >> /app/restore.sh && \
    echo '        ;;' >> /app/restore.sh && \
    echo '    *.xz)' >> /app/restore.sh && \
    echo '        xzcat "$BACKUP_FILE" | psql --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE"' >> /app/restore.sh && \
    echo '        ;;' >> /app/restore.sh && \
    echo '    *.sql)' >> /app/restore.sh && \
    echo '        psql --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE" < "$BACKUP_FILE"' >> /app/restore.sh && \
    echo '        ;;' >> /app/restore.sh && \
    echo '    *)' >> /app/restore.sh && \
    echo '        echo "Unsupported format"; exit 1' >> /app/restore.sh && \
    echo '        ;;' >> /app/restore.sh && \
    echo 'esac' >> /app/restore.sh && \
    echo 'echo "Restore complete from: $BACKUP_FILE"' >> /app/restore.sh
RUN chmod +x /app/restore.sh && chown 65532:65532 /app/restore.sh
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="false" \
    SHIM_BACKUP_DB_HOST="localhost" \
    SHIM_BACKUP_DB_PORT="5432" \
    SHIM_REPLICATION_ENABLED="false" \
    SHIM_MIGRATION_ENABLED="false" \
    SHIM_VAULT_ENABLED="false" \
    SHIM_AUDIT_ENABLED="true"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/app/restore.sh"]
LABEL org.opencontainers.image.title="postgres-restore" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Restore Container with pg_restore + xz support" \
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
