# =============================================================================
# EVERGREEN HARDENED MYSQL INIT
# Generated from template - Version: 8.0
# Constraint: debian-slim - MySQL client tools require glibc
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client && \
    mkdir -p /app /var/log/mysql-init /var/cache/mysql-init || true


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache curl ca-certificates 
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mysql-init /var/log/mysql-init
COPY --from=builder --chown=65532:65532 /var/cache/mysql-init /var/cache/mysql-init
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
            *.sql)    echo "Running $f"; mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$f" ;
            *.sh)     echo "Running $f"; . "$f" ;
            *)        echo "Ignoring $f" ;
        esac
    done
fi
SCRIPT
RUN chmod +x /app/init.sh 2>/dev/null || true && chown 65532:65532 /app/init.sh 2>/dev/null || true

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="mysql-init" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Initialization Container" \
      org.opencontainers.image.vendor="Oracle" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
