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
    default-php84-mysql-client && \
    mkdir -p /app /var/log/php84-mysql-init /var/cache/php84-mysql-init


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache curl ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/php84-mysql-init /var/log/php84-mysql-init
COPY --from=builder --chown=65532:65532 /var/cache/php84-mysql-init /var/cache/php84-mysql-init
USER 65532:65532
WORKDIR /app
COPY <<'SCRIPT' /app/init.sh
#!/bin/sh
set -eu
: "${MYSQL_HOST:?MYSQL_HOST is required}"
: "${MYSQL_DATABASE:?MYSQL_DATABASE is required}"
if [ -d "/docker-entrypoint-initdb.d" ]; then
    for f in /docker-entrypoint-initdb.d/*; do
        case "$f" in
            *.sql)    echo "Running $f"; php84-mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$f" ;;
            *.sh)     echo "Running $f"; . "$f" ;;
            *)        echo "Ignoring $f" ;;
        esac
    done
fi
SCRIPT
RUN chmod +x /app/init.sh && chown 65532:65532 /app/init.sh
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="php84-mysql-init" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Initialization Container" \
      org.opencontainers.image.vendor="Oracle" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM