# =============================================================================
# EVERGREEN HARDENED POSTGRESQL INIT
# Generated from template - Version: 17
# Wolfi-base provides glibc; PostgreSQL client tools from upstream debs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /var/log/postgresql-init /var/cache/postgresql-init || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client curl ca-certificates || true
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/postgresql-init /var/log/postgresql-init
COPY --from=builder --chown=65532:65532 /var/cache/postgresql-init /var/cache/postgresql-init
WORKDIR /app
COPY <<'SCRIPT' /app/init.sh
#!/bin/sh
set -eu
: "${PGHOST:?PGHOST is required}"
: "${PGDATABASE:?PGDATABASE is required}"
if [ -d "/docker-entrypoint-initdb.d" ]; then
    for f in /docker-entrypoint-initdb.d/*; do
        case "$f" in
            *.sql)    echo "Running $f"; psql -v ON_ERROR_STOP=1 --username "$PGUSER" -f "$f" ;
            *.sh)     echo "Running $f"; . "$f" ;
            *)        echo "Ignoring $f" ;
        esac
    done
fi
SCRIPT
RUN chmod +x /app/init.sh && chown 65532:65532 /app/init.sh
USER 65532:65532

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="postgresql-init" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Initialization Container" \
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
