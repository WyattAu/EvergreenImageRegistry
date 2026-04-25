# =============================================================================
# SOVEREIGN HARDENED POSTGRES RESTORE
# Generated from template - Version: 17
# Constraint: debian-slim - pg_restore and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG VERSION=17
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION}-client xz-utils && \
    mkdir -p /app /backups /var/log/postgres-restore /var/cache/postgres-restore || true


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client curl ca-certificates || true
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/postgres-restore /var/log/postgres-restore
COPY --from=builder --chown=65532:65532 /var/cache/postgres-restore /var/cache/postgres-restore
USER 65532:65532
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
RUN chmod +x /app/restore.sh && chown 65532:65532 /app/restore.sh
ENTRYPOINT ["/app/restore.sh"]
LABEL org.opencontainers.image.title="postgres-restore" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Restore Container with pg_restore + xz support" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM