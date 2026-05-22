# =============================================================================
# EVERGREEN HARDENED MYSQL BACKUP
# Generated from template - Version: 8.0
# Wolfi-base provides glibc; mysqldump and xz from upstream debs
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
    mkdir -p /app /backups /var/log/mysql-backup /var/cache/mysql-backup || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache wget ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/mysql-backup /var/log/mysql-backup
COPY --from=builder --chown=65532:65532 /var/cache/mysql-backup /var/cache/mysql-backup
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
RUN chmod +x /app/backup.sh 2>/dev/null || true && chown 65532:65532 /app/backup.sh 2>/dev/null || true

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/backup.sh"]
LABEL org.opencontainers.image.title="mysql-backup" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Backup Container with mysqldump + xz compression" \
      org.opencontainers.image.vendor="Oracle" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/databack/mysql-backup4sh"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
