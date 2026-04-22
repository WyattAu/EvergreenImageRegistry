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
    default-php84-mysql-client xz-utils && \
    mkdir -p /app /backups /var/log/php84-mysql-backup /var/cache/php84-mysql-backup

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache curl ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/php84-mysql-backup /var/log/php84-mysql-backup
COPY --from=builder --chown=65532:65532 /var/cache/php84-mysql-backup /var/cache/php84-mysql-backup
USER 65532:65532
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
RUN chmod +x /app/backup.sh && chown 65532:65532 /app/backup.sh
ENTRYPOINT ["/app/backup.sh"]
LABEL org.opencontainers.image.title="php84-mysql-backup" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Backup Container with mysqldump + xz compression" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM