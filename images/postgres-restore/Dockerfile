# =============================================================================
# EVERGREEN HARDENED POSTGRES RESTORE
# Generated from template - Version: 17
# Constraint: debian-slim - pg_restore and xz require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=17
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-${VERSION}-client xz-utils && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /backups /var/log/postgres-restore /var/cache/postgres-restore || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client wget ca-certificates || true
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /backups /backups
COPY --from=builder --chown=65532:65532 /var/log/postgres-restore /var/log/postgres-restore
COPY --from=builder --chown=65532:65532 /var/cache/postgres-restore /var/cache/postgres-restore
WORKDIR /app
COPY <<'SCRIPT' /app/restore.sh
#!/bin/sh
set -eu
: "${PGHOST:?PGHOST is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGDATABASE:?PGDATABASE is required}"
: "${BACKUP_FILE:?BACKUP_FILE is required}"
if [ ! -f "$BACKUP_FILE" ]; then
RUN echo "Backup file not found: $BACKUP_FILE" \
    exit 1
fi
case "$BACKUP_FILE" in
    *.dump.xz)
        TEMP_DIR="$(mktemp -d)"
        xzcat "$BACKUP_FILE" | tar -xf - -C "$TEMP_DIR"
        pg_restore --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE" --clean --if-exists --jobs=4 "$TEMP_DIR"/*
RUN rm -rf "$TEMP_DIR" \
    ;;
    *.xz)
        xzcat "$BACKUP_FILE" | psql --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE"
        ;;
    *.sql)
        psql --host="$PGHOST" --user="$PGUSER" --dbname="$PGDATABASE" < "$BACKUP_FILE"
        ;;
    *)
RUN echo "Unsupported format"; exit 1 ;
esac
echo "Restore complete from: $BACKUP_FILE"
SCRIPT
RUN chmod +x /app/restore.sh && chown 65532:65532 /app/restore.sh
USER 65532:65532

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/restore.sh"]
LABEL org.opencontainers.image.title="postgres-restore" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Restore Container with pg_restore + xz support" \
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
