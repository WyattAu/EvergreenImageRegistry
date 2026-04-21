# =============================================================================
# SOVEREIGN HARDENED MYSQL BACKUP
# Generated from template - Version: 8.0
# Constraint: debian-slim - mysqldump and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client xz-utils && \
    mkdir -p /app /backups /var/log/mysql-backup /var/cache/mysql-backup

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client xz-utils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /backups /backups
COPY --from=builder --chown=65534:65534 /var/log/mysql-backup /var/log/mysql-backup
COPY --from=builder --chown=65534:65534 /var/cache/mysql-backup /var/cache/mysql-backup
USER 65534:65534
WORKDIR /app
COPY <<'SCRIPT' /app/backup.sh
#!/bin/sh
set -eu
: "${MYSQL_HOST:?MYSQL_HOST is required}"
: "${MYSQL_USER:?MYSQL_USER is required}"
: "${MYSQL_PASSWORD:?MYSQL_PASSWORD is required}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
OUTPUT="/backups/${MYSQL_DATABASE:-all}_${TIMESTAMP}.sql.xz"
mysqldump --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" \
    --single-transaction --routines --triggers ${MYSQL_DATABASE:+"$MYSQL_DATABASE"} \
    ${MYSQL_DATABASE:---all-databases} | xz -9 > "$OUTPUT"
echo "Backup complete: $OUTPUT"
SCRIPT
RUN chmod +x /app/backup.sh && chown 65534:65534 /app/backup.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["mysqldump", "--version"]
ENTRYPOINT ["/app/backup.sh"]
LABEL org.opencontainers.image.title="mysql-backup" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Backup Container with mysqldump + xz compression" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
