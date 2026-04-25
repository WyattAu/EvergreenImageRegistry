# =============================================================================
# SOVEREIGN HARDENED MYSQL RESTORE
# Generated from template - Version: 8.0
# Constraint: debian-slim - mysql client and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client xz-utils && \
    mkdir -p /app /backups /var/log/mysql-restore /var/cache/mysql-restore || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates || true
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
    *.xz) xzcat "$BACKUP_FILE" ;;
    *.gz) zcat "$BACKUP_FILE" ;;
    *.sql) cat "$BACKUP_FILE" ;;
    *)     echo "Unsupported format"; exit 1 ;;
esac | mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD"
echo "Restore complete from: $BACKUP_FILE"
SCRIPT
RUN chmod +x /app/restore.sh && chown 65532:65532 /app/restore.sh
ENTRYPOINT ["/app/restore.sh"]
LABEL org.opencontainers.image.title="mysql-restore" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Restore Container with xz/gz/sql support" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM