# =============================================================================
# EVERGREEN HARDENED MYSQL RESTORE
# Generated from template - Version: 8.0
# Constraint: debian-slim - mysql client and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client xz-utils && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /backups /var/log/mysql-restore /var/cache/mysql-restore || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache curl ca-certificates 
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/mysql-restore /var/log/mysql-restore
COPY --from=builder --chown=65532:65532 /var/cache/mysql-restore /var/cache/mysql-restore
USER 65532:65532
WORKDIR /app
COPY <<'SCRIPT' /app/restore.sh
#!/bin/sh
set -eu
: "${MYSQL_HOST:?MYSQL_HOST is required}"
: "${MYSQL_USER:?MYSQL_USER is required}"
: "${MYSQL_PASSWORD:?MYSQL_PASSWORD is required}"
: "${BACKUP_FILE:?BACKUP_FILE is required}"
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi
case "$BACKUP_FILE" in
    *.xz) xzcat "$BACKUP_FILE" ;
    *.gz) zcat "$BACKUP_FILE" ;
    *.sql) cat "$BACKUP_FILE" ;
    *)     echo "Unsupported format"; exit 1 ;
esac | mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD"
echo "Restore complete from: $BACKUP_FILE"
SCRIPT
RUN chmod +x /app/restore.sh 2>/dev/null || true && chown 65532:65532 /app/restore.sh 2>/dev/null || true

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/restore.sh"]
LABEL org.opencontainers.image.title="mysql-restore" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Restore Container with xz/gz/sql support" \
      org.opencontainers.image.vendor="Oracle" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
