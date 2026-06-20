# =============================================================================
# EVERGREEN HARDENED MYSQL RESTORE
# Generated from template - Version: 8.0
# Wolfi-base provides glibc; MySQL client and xz from upstream debs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client xz-utils && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /backups /var/log/mysql-restore /var/cache/mysql-restore || true


ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim

RUN apk add --no-cache wget ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/mysql-restore /var/log/mysql-restore
COPY --from=builder --chown=65532:65532 /var/cache/mysql-restore /var/cache/mysql-restore
USER 65532:65532
WORKDIR /app
RUN echo '#!/bin/sh' > /app/restore.sh && \
    echo 'set -eu' >> /app/restore.sh && \
    echo ': "${MYSQL_HOST:?MYSQL_HOST is required}"' >> /app/restore.sh && \
    echo ': "${MYSQL_USER:?MYSQL_USER is required}"' >> /app/restore.sh && \
    echo ': "${MYSQL_PASSWORD:?MYSQL_PASSWORD is required}"' >> /app/restore.sh && \
    echo ': "${BACKUP_FILE:?BACKUP_FILE is required}"' >> /app/restore.sh && \
    echo 'if [ ! -f "$BACKUP_FILE" ]; then' >> /app/restore.sh && \
    echo '    echo "Backup file not found: $BACKUP_FILE"' >> /app/restore.sh && \
    echo '    exit 1' >> /app/restore.sh && \
    echo 'fi' >> /app/restore.sh && \
    echo 'case "$BACKUP_FILE" in' >> /app/restore.sh && \
    echo '    *.xz) xzcat "$BACKUP_FILE" ;;' >> /app/restore.sh && \
    echo '    *.gz) zcat "$BACKUP_FILE" ;;' >> /app/restore.sh && \
    echo '    *.sql) cat "$BACKUP_FILE" ;;' >> /app/restore.sh && \
    echo '    *)     echo "Unsupported format"; exit 1 ;;' >> /app/restore.sh && \
    echo 'esac | mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD"' >> /app/restore.sh && \
    echo 'echo "Restore complete from: $BACKUP_FILE"' >> /app/restore.sh
RUN chmod +x /app/restore.sh 2>/dev/null && chown 65532:65532 /app/restore.sh 2>/dev/null

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/app/restore.sh"]
LABEL org.opencontainers.image.title="mysql-restore" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Restore Container with xz/gz/sql support" \
      org.opencontainers.image.vendor="Oracle" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/mysql/mysql-server"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
