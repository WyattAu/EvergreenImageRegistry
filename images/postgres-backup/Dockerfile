# =============================================================================
# EVERGREEN HARDENED POSTGRES BACKUP
# Generated from template - Version: 17
# Constraint: debian-slim - pg_dump and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=17
RUN mkdir -p /app /backups /var/log/postgres-backup /var/cache/postgres-backup || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION}-client xz-utils && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /backups /var/log/postgres-backup /var/cache/postgres-backup || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client wget ca-certificates || true
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/postgres-backup /var/log/postgres-backup
COPY --from=builder --chown=65532:65532 /var/cache/postgres-backup /var/cache/postgres-backup
WORKDIR /app
COPY <<'SCRIPT' /app/backup.sh
#!/bin/sh
set -eu
: "${PGHOST:?PGHOST is required}"
: "${PGUSER:?PGUSER is required}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
DB="${PGDATABASE:-all}"
OUTPUT="/backups/${DB}_${TIMESTAMP}.dump.xz"
if [ "$DB" = "all" ]; then
    pg_dumpall --host="$PGHOST" --user="$PGUSER" | xz -9 > "$OUTPUT"
else
    pg_dump --host="$PGHOST" --user="$PGUSER" --format=directory --jobs=4 --file="/backups/${DB}_${TIMESTAMP}" "$DB" && \
    tar -cf - "/backups/${DB}_${TIMESTAMP}" | xz -9 > "$OUTPUT" && \
    rm -rf "/backups/${DB}_${TIMESTAMP}"
fi
echo "Backup complete: $OUTPUT"
SCRIPT
RUN chmod +x /app/backup.sh && chown 65532:65532 /app/backup.sh
USER 65532:65532

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/backup.sh"]
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
