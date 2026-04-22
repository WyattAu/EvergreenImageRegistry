# =============================================================================
# SOVEREIGN HARDENED REDIS SENTINEL
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - Redis sentinel mode requires config and working directories
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
    && cd redis-${VERSION} && make -j"$(nproc)" redis && strip --strip-all src/redis \
    && cp src/redis /tmp/redis

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /usr/sbin/nologin redis 2>/dev/null || true
RUN mkdir -p /data /var/log/redis
COPY --from=builder /tmp/redis /usr/local/bin/redis
USER 65532:65532
WORKDIR /data
EXPOSE 26379
ENTRYPOINT ["/usr/local/bin/redis", "--sentinel"]
LABEL sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      org.opencontainers.image.title="redis-sentinel" \
      org.opencontainers.image.description="Sovereign hardened Redis Sentinel - Redis high availability sentinel mode" \
      org.opencontainers.image.version="${VERSION}"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM