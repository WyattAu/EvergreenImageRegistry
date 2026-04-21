# =============================================================================
# SOVEREIGN HARDENED POSTGRES BACKUP
# Generated from template - Version: 17
# Constraint: debian-slim - pg_dump and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-${VERSION} xz-utils && \
    mkdir -p /app /backups /var/log/postgres-backup /var/cache/postgres-backup

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-${VERSION} xz-utils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /backups /backups
COPY --from=builder --chown=65534:65534 /var/log/postgres-backup /var/log/postgres-backup
COPY --from=builder --chown=65534:65534 /var/cache/postgres-backup /var/cache/postgres-backup
USER 65534:65534
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
RUN chmod +x /app/backup.sh && chown 65534:65534 /app/backup.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["pg_dump", "--version"]
ENTRYPOINT ["/app/backup.sh"]
LABEL org.opencontainers.image.title="postgres-backup" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Backup Container with pg_dump + xz compression" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
