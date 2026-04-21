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

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client-${VERSION} curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/postgresql-init /var/log/postgresql-init
COPY --from=builder --chown=65534:65534 /var/cache/postgresql-init /var/cache/postgresql-init
USER 65534:65534
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
RUN chmod +x /app/init.sh && chown 65534:65534 /app/init.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["psql", "--version"]
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="postgresql-init" \
      org.opencontainers.image.version="17" \
      org.opencontainers.image.description="PostgreSQL Initialization Container" \
      org.opencontainers.image.vendor="PostgreSQL" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
