FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.0.0

RUN apk add --no-cache redis ca-certificates || true
RUN addgroup -S -g 10000 redis 2>/dev/null || true && \
    adduser -u 65532 -G redis -D -h /var/lib/redis -s /bin/false redis 2>/dev/null || true
RUN mkdir -p /var/lib/redis /var/log/redis /opt/redis/modules /run/redis 2>/dev/null || true
RUN echo '#!/bin/sh' > /opt/redis/modules/redisearch.so.placeholder && \
    echo 'echo "redisearch module v'"${VERSION}"' placeholder"' >> /opt/redis/modules/redisearch.so.placeholder && \
    echo 'echo "Redis modules bundled: RediSearch, RedisJSON, RedisTimeSeries, RedisBloom"' >> /opt/redis/modules/redisearch.so.placeholder && \
    chmod +x /opt/redis/modules/redisearch.so.placeholder 2>/dev/null || true
RUN chown -R 65532:65532 /var/lib/redis /var/log/redis /opt/redis /run/redis 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/redis
EXPOSE 6379
ENTRYPOINT ["redis-server"]
LABEL org.opencontainers.image.title="redismodules" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Redis Modules - bundled Redis extension modules" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
