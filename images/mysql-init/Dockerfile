# =============================================================================
# EVERGREEN HARDENED MYSQL INIT
# Generated from template - Version: 8.0
# Wolfi-base provides glibc; MySQL client tools from upstream debs
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=8.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app /var/log/mysql-init /var/cache/mysql-init || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache wget ca-certificates
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/mysql-init /var/log/mysql-init
COPY --from=builder --chown=65532:65532 /var/cache/mysql-init /var/cache/mysql-init
USER 65532:65532
WORKDIR /app
RUN echo '#!/bin/sh' > /app/init.sh && \
    echo 'set -eu' >> /app/init.sh && \
    echo ': "${MYSQL_HOST:?MYSQL_HOST is required}"' >> /app/init.sh && \
    echo ': "${MYSQL_DATABASE:?MYSQL_DATABASE is required}"' >> /app/init.sh && \
    echo 'if [ -d "/docker-entrypoint-initdb.d" ]; then' >> /app/init.sh && \
    echo '    for f in /docker-entrypoint-initdb.d/*; do' >> /app/init.sh && \
    echo '        case "$f" in' >> /app/init.sh && \
    echo '            *.sql)    echo "Running $f"; mysql --host="$MYSQL_HOST" --user="$MYSQL_USER" --password="$MYSQL_PASSWORD" "$MYSQL_DATABASE" < "$f" ;;' >> /app/init.sh && \
    echo '            *.sh)     echo "Running $f"; . "$f" ;;' >> /app/init.sh && \
    echo '            *)        echo "Ignoring $f" ;;' >> /app/init.sh && \
    echo '        esac' >> /app/init.sh && \
    echo '    done' >> /app/init.sh && \
    echo 'fi' >> /app/init.sh
RUN chmod +x /app/init.sh 2>/dev/null && chown 65532:65532 /app/init.sh 2>/dev/null

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
ENTRYPOINT ["/app/init.sh"]
LABEL org.opencontainers.image.title="mysql-init" \
      org.opencontainers.image.version="8.0" \
      org.opencontainers.image.description="MySQL Initialization Container" \
      org.opencontainers.image.vendor="Oracle" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/mysql/mysql-server"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
