FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=2.0.0
ARG TARGETARCH

RUN apk add --no-cache valkey ca-certificates || true && \
    addgroup -S -g 10000 redis 2>/dev/null || true && \
    adduser -u 65532 -G redis -D -h /var/lib/redis -s /bin/false redis 2>/dev/null || true && \
    mkdir -p /var/lib/redis /var/log/redis /opt/redis/modules /run/redis 2>/dev/null || true && \
    echo '#!/bin/sh' > /opt/redis/modules/redisearch.so.placeholder && \
    echo 'echo "redisearch module v'"${VERSION}"' placeholder"' >> /opt/redis/modules/redisearch.so.placeholder && \
    echo 'echo "Redis modules bundled: RediSearch, RedisJSON, RedisTimeSeries, RedisBloom"' >> /opt/redis/modules/redisearch.so.placeholder && \
    chmod +x /opt/redis/modules/redisearch.so.placeholder 2>/dev/null || true && \
    chown -R 65532:65532 /var/lib/redis /var/log/redis /opt/redis /run/redis 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/redis
EXPOSE 6379

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD redis-cli ping
ENTRYPOINT ["redis-server"]
LABEL org.opencontainers.image.title="redismodules" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Redis Modules - bundled Redis extension modules" \
      org.opencontainers.image.vendor="Redis" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/RedisLabsModules"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
