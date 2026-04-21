# =============================================================================
# SOVEREIGN HARDENED MYSQL INIT
# Generated from template - Version: 8.0
# Constraint: debian-slim - MySQL client tools require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client && \
    mkdir -p /app /var/log/mysql-init /var/cache/mysql-init

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder --chown=65534:65534 /app /app
COPY --from=builder --chown=65534:65534 /var/log/mysql-init /var/log/mysql-init
COPY --from=builder --chown=65534:65534 /var/cache/mysql-init /var/cache/mysql-init
USER 65534:65534
WORKDIR /app
COPY <<'SCRIPT' /app/init.sh
#!/bin/sh
set -eu
: "${MYSQL_HOST:?MYSQL_HOST is required}"
: "${MYSQL_DATABASE:?MYSQL_DATABASE is required}"
if [ -d "/docker-entrypoint-initdb.d" ]; then
    for f in /docker-entrypoint-initdb.d/*; do
        case "$f" in
            *.sql)    echo "Running $f"; mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$f" ;;
            *.sh)     echo "Running $f"; . "$f" ;;
            *)        echo "Ignoring $f" ;;
        esac
    done
fi
SCRIPT
RUN chmod +x /app/init.sh && chown 65534:65534 /app/init.sh
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["mysql", "--version"]
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="mysql-init" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Initialization Container" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
