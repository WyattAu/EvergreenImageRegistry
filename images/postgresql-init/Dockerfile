# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL INIT
# Generated from template - Version: 17
# Constraint: debian-slim - PostgreSQL client tools require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=17
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client && \
    mkdir -p /app /var/log/postgresql-init /var/cache/postgresql-init

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache postgresql-client-${VERSION} curl ca-certificates
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
            *.sql)    echo "Running $f"; psql -v ON_ERROR_STOP=1 --username "$PGUSER" -f "$f" ;;
            *.sh)     echo "Running $f"; . "$f" ;;
            *)        echo "Ignoring $f" ;;
        esac
    done
fi
SCRIPT
RUN chmod +x /app/init.sh && chown 65532:65532 /app/init.sh
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="postgresql-init" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Initialization Container" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM