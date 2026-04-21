# =============================================================================
# SOVEREIGN HARDENED REDIS CLUSTER
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - Redis cluster mode requires config and working directories
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/redis/redis/archive/refs/tags/${VERSION}.tar.gz" -o redis.tar.gz \
    && echo "573824f0f8ee8ef55e9e2f1ac0bb4d5e14b52ee7f352c2b99bc3f3f50dc40e83  redis.tar.gz" | sha256sum -c - \
    && tar -xzf redis.tar.gz \
    && cd redis-${VERSION} && make -j"$(nproc)" redis-server && strip --strip-all src/redis-server \
    && cp src/redis-server /tmp/redis-server

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin redis 2>/dev/null || true
RUN mkdir -p /data /var/log/redis
COPY --from=builder /tmp/redis-server /usr/local/bin/redis-server
USER 65534:65534
WORKDIR /data
EXPOSE 6379 16379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/redis-server", "--version"]
ENTRYPOINT ["/usr/local/bin/redis-server", "--cluster-enabled", "yes", "--cluster-config-file", "/data/nodes.conf"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      org.opencontainers.image.title="redis-cluster" \
      org.opencontainers.image.description="Sovereign hardened Redis Cluster - Redis with cluster mode pre-enabled" \
      org.opencontainers.image.version="${VERSION}"
