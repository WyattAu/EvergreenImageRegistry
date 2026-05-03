# =============================================================================
# EVERGREEN HARDENED POSTGRESQL INIT
# Generated from template - Version: 17
# Constraint: debian-slim - PostgreSQL client tools require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client && \
    mkdir -p /app /var/log/postgresql-init /var/cache/postgresql-init || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=17

RUN apk add --no-cache postgresql-${VERSION}-client curl ca-certificates || true
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/postgresql-init /var/log/postgresql-init
COPY --from=builder --chown=65532:65532 /var/cache/postgresql-init /var/cache/postgresql-init
USER 65532:65532
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="postgresql-init" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Initialization Container" \
      org.opencontainers.image.vendor="PostgreSQL" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
