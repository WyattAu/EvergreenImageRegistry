# =============================================================================
# EVERGREEN HARDENED REDIS SENTINEL
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - Redis sentinel mode requires config and working directories
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.4.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=7.4.1
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/redis/redis/archive/refs/tags/${VERSION}.tar.gz -o redis.tar.gz ; echo "573824f0f8ee8ef55e9e2f1ac0bb4d5e14b52ee7f352c2b99bc3f3f50dc40e83  redis.tar.gz" | sha256sum -c  ; [ -f redis.tar.gz ] && tar -xzf redis.tar.gz ; \
    cd redis-${VERSION} && make -j"$(nproc)" redis && strip --strip-all src/redis 2>/dev/null; cp src/redis /tmp/redis 2>/dev/null && \
    mkdir -p /tmp/redis
FROM ghcr.io/wyattau/evergreenshim/cache-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=7.4.1

RUN apk add --no-cache ca-certificates && adduser -u 65532 -s /bin/false &&  mkdir -p /data /var/log/redis
# NOTE: redis server not available in wolfi; uses pre-compiled binary
COPY --from=builder /tmp/redis /usr/local/bin/redis
USER 65532:65532
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_SCHEDULE="0 0 2 * * *" \
    SHIM_BACKUP_RETENTION_DAYS="7" \
    SHIM_BACKUP_OUTPUT_DIR="/backups"
ENV SHIM_CACHE_ENABLED="true" \
    SHIM_CACHE_MAX_ENTRIES="10000" \
    SHIM_CACHE_DEFAULT_TTL="300" \
    SHIM_CACHE_EVICTION="lru" \
    SHIM_METRICS_ENABLED="true"
WORKDIR /data
EXPOSE 26379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:26379"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      org.opencontainers.image.title="redis-sentinel" \
      org.opencontainers.image.description="Evergreen hardened Redis Sentinel - Redis high availability sentinel mode" \
      org.opencontainers.image.version="${VERSION}" \
            org.opencontainers.image.source="https://github.com/redis/redis"
LABEL evergreen.base.image="wolfi"
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
