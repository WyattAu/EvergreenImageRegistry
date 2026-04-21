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
    mkdir -p /app /backups /var/log/mysql-restore /var/cache/mysql-restore

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client xz-utils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /backups /backups
COPY --from=builder --chown=65534:65534 /var/log/mysql-restore /var/log/mysql-restore
COPY --from=builder --chown=65534:65534 /var/cache/mysql-restore /var/cache/mysql-restore
USER 65534:65534
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
RUN chmod +x /app/restore.sh && chown 65534:65534 /app/restore.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["mysql", "--version"]
ENTRYPOINT ["/app/restore.sh"]
LABEL org.opencontainers.image.title="mysql-restore" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Restore Container with xz/gz/sql support" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
