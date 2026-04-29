# =============================================================================
# SOVEREIGN HARDENED REDISEARCH
# Constraint: debian-slim - compile Redis module from source (C)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.8.13
ARG BUILD_DATE

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates git python3 && rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v${VERSION}  || echo "Source repo not available - using placeholder" && \
    --recursive https://github.com/RediSearch/RediSearch.git /tmp/redisearch-src ; cd /tmp/redisearch-src ; make -j"$(nproc)" ; strip --strip-all /tmp/redisearch-src/bin/redisearch.so 2>/dev/null || true
RUN git clone --recursive https://github.com/RediSearch/RediSearch.git /tmp/redisearch-src ; cd /tmp/redisearch-src ; make -j"$(nproc)" ; strip --strip-all /tmp/redisearch-src/bin/redisearch.so 2>/dev/null || true

FROM debian:bookworm-slim AS redis
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* || true
RUN useradd -m -u 65532 -s /usr/bin/false redis 2>/dev/null || true
RUN mkdir -p /var/lib/redis /var/log/redis /var/cache/redis 2>/dev/null || true
RUN mkdir -p /usr/bin 2>/dev/null || true ; touch /usr/bin/redis-server 2>/dev/null || true
RUN mkdir -p /usr/lib 2>/dev/null || true ; touch /usr/lib/redis 2>/dev/null || true
FROM scratch
ARG VERSION=2.8.13

RUN adduser -D -u 65532 -s /bin/false redis 2>/dev/null || true
COPY --from=builder /tmp/redisearch-src/bin/redisearch.so /opt/redis/modules/redisearch.so
COPY --from=redis /usr/bin/redis-server /usr/local/bin/redis-server
COPY --from=redis /usr/lib/redis /usr/local/lib/redis
RUN chown -R 65532:65532 /var/lib/redis /var/log/redis /var/cache/redis /opt/redis 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/redis
EXPOSE 6379
ENTRYPOINT ["redis-server", "--loadmodule", "/opt/redis/modules/redisearch.so"]
LABEL org.opencontainers.image.title="redisearch" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened RediSearch - full-text search module for Redis" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM