# =============================================================================
# SOVEREIGN HARDENED POSTGRES RESTORE
# Generated from template - Version: 17
# Constraint: debian-slim - pg_restore and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-${VERSION} xz-utils && \
    mkdir -p /app /backups /var/log/postgres-restore /var/cache/postgres-restore

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-${VERSION} xz-utils curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /backups /backups
COPY --from=builder --chown=65534:65534 /var/log/postgres-restore /var/log/postgres-restore
COPY --from=builder --chown=65534:65534 /var/cache/postgres-restore /var/cache/postgres-restore
USER 65534:65534
WORKDIR /app
COPY <<'SCRIPT' /app/restore.sh
#!/bin/sh
set -eu
: "${PGHOST:?PGHOST is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGDATABASE:?PGDATABASE is required}"
: "${BACKUP_FILE:?BACKUP_FILE is required}"
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi
case "$BACKUP_FILE" in
    *.dump.xz)
        TEMP_DIR="$(mktemp -d)"
        xzcat "$BACKUP_FILE" | tar -xf - -C "$TEMP_DIR"
        pg_restore --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE" --clean --if-exists --jobs=4 "$TEMP_DIR"/*
        rm -rf "$TEMP_DIR"
        ;;
    *.xz)
        xzcat "$BACKUP_FILE" | psql --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE"
        ;;
    *.sql)
        psql --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE" < "$BACKUP_FILE"
        ;;
    *)
        echo "Unsupported format"; exit 1 ;;
esac
echo "Restore complete from: $BACKUP_FILE"
SCRIPT
RUN chmod +x /app/restore.sh && chown 65534:65534 /app/restore.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["pg_restore", "--version"]
ENTRYPOINT ["/app/restore.sh"]
LABEL org.opencontainers.image.title="postgres-restore" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Restore Container with pg_restore + xz support" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
