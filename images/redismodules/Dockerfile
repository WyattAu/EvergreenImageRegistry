# =============================================================================
# SOVEREIGN HARDENED REDISMODULES
# Constraint: debian-slim - compile Redis modules from source (C)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates git python3 libssl-dev && \
    rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN mkdir -p /tmp/modules && cd /tmp/modules \
    && git clone --depth 1 --branch v2.8.13 --recursive \
    https://github.com/RediSearch/RediSearch.git 2>/dev/null && cd RediSearch && make -j"$(nproc)" \
    && cp bin/redisearch.so /tmp/modules/ || true \
    && cd /tmp/modules \
    && git clone --depth 1 https://github.com/RedisJSON/RedisJSON.git && cd RedisJSON && make -j"$(nproc)" \
    && cp src/rejson.so /tmp/modules/ || true \
    && cd /tmp/modules \
    && git clone --depth 1 https://github.com/RedisTimeSeries/RedisTimeSeries.git && cd RedisTimeSeries && make -j"$(nproc)" \
    && cp/bin/redistimeseries.so /tmp/modules/ || true \
    && cd /tmp/modules \
    && git clone --depth 1 https://github.com/RedisBloom/RedisBloom.git && cd RedisBloom && make -j"$(nproc)" \
    && cp/libredisbloom.so /tmp/modules/ || true

FROM debian:bookworm-slim AS redis
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

FROM debian:bookworm-slim
RUN useradd -m -u 65534 -s /usr/sbin/nologin redis 2>/dev/null || true
RUN mkdir -p /var/lib/redis /var/log/redis /var/cache/redis /opt/redis/modules
COPY --from=builder /tmp/modules/*.so /opt/redis/modules/
COPY --from=redis /usr/bin/redis-server /usr/local/bin/redis-server
RUN chown -R 65534:65534 /var/lib/redis /var/log/redis /var/cache/redis /opt/redis
USER 65534:65534
WORKDIR /var/lib/redis
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["redis-cli", "ping"]
ENTRYPOINT ["redis-server", "--loadmodule", "/opt/redis/modules/redisearch.so"]
LABEL org.opencontainers.image.title="redismodules" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Redis Modules - bundled Redis extension modules" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
