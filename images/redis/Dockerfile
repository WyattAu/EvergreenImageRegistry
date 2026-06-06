# =============================================================================
# EVERGREEN HARDENED REDIS
# Static build from source - scratch final stage
# =============================================================================
ARG VERSION=8.0.2
ARG TARGETARCH
ARG SHIM_VERSION=v0.3.0

FROM debian:bookworm-slim AS builder
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential linux-headers ca-certificates wget && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN wget -q "https://download.redis.io/releases/redis-${VERSION}.tar.gz" -O redis.tar.gz && \
    tar -xzf redis.tar.gz && rm redis.tar.gz
RUN cd redis-${VERSION} && \
    make -j$(nproc) \
        CFLAGS="-static -O2 -fstack-protector-strong" \
        LDFLAGS="-static" \
        MALLOC=jemalloc \
        BUILD_TLS=yes \
        install

FROM ghcr.io/wyattau/evergreenshim/cache-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /usr/local/bin/redis-server /usr/local/bin/redis-server
COPY --from=builder /usr/local/bin/redis-cli /usr/local/bin/redis-cli
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

RUN ["/bin/sh", "-c", "mkdir -p /app /var/log/redis /var/cache/redis"]

USER 65532:65532
ENV SHIM_CACHE_ENABLED="true" \
    SHIM_CACHE_MAX_ENTRIES="10000" \
    SHIM_CACHE_DEFAULT_TTL="300" \
    SHIM_CACHE_EVICTION="lru" \
    SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 6379 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/shim", "run"]
CMD ["-c", "redis-server", "--", "--bind", "0.0.0.0", "--protected-mode", "no"]
LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.description="Redis - in-memory data structure store and cache (static build)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.source="https://github.com/redis/redis" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="musl-source" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="exec" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
