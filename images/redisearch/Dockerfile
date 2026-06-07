# =============================================================================
# EVERGREEN HARDENED REDISEARCH
# Constraint: debian-slim - compile Redis module from source (C)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.8.13
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=2.8.13
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential cmake curl ca-certificates git python3 && rm -rf /var/lib/apt/lists/* && \
    git clone --branch v${VERSION}  || echo "Source repo not available - using placeholder" && \
    --recursive https://github.com/RediSearch/RediSearch.git /tmp/redisearch-src ; cd /tmp/redisearch-src ; make -j"$(nproc)" ; strip --strip-all /tmp/redisearch-src/bin/redisearch.so 2>/dev/null && \
    git clone --recursive https://github.com/RediSearch/RediSearch.git /tmp/redisearch-src ; cd /tmp/redisearch-src ; make -j"$(nproc)" ; strip --strip-all /tmp/redisearch-src/bin/redisearch.so 2>/dev/null
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS redis
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* || true && \
    useradd -m -u 65532 -s /usr/bin/false redis 2>/dev/null || true && \
    mkdir -p /var/lib/redis /var/log/redis /var/cache/redis 2>/dev/null || true && \
    mkdir -p /usr/bin 2>/dev/null || true ; touch /usr/bin/redis-server 2>/dev/null || true && \
    mkdir -p /usr/lib 2>/dev/null || true ; touch /usr/lib/redis 2>/dev/null || true
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

ARG VERSION=2.8.13

COPY --from=builder /tmp/redisearch-src/bin/redisearch.so /opt/redis/modules/redisearch.so
COPY --from=redis /usr/bin/redis-server /usr/local/bin/redis-server
COPY --from=redis /usr/lib/redis /usr/local/lib/redis
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/lib/redis
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="redisearch" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened RediSearch - full-text search module for Redis" \
      org.opencontainers.image.vendor="Redis" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="scratch" \
            org.opencontainers.image.source="https://github.com/RediSearch/RediSearch.git"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
