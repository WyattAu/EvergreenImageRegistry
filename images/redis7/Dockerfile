# =============================================================================
# EVERGREEN HARDENED REDIS7
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=7.4.1
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.1.0

FROM ghcr.io/wyattau/evergreenshim/cache-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache ca-certificates && adduser -u 65532 -D 2>/dev/null &&  mkdir -p /app /var/log/redis7 /var/cache/redis7 && chown -R redis:redis /app /var/log/redis7 /var/cache/redis7 2>/dev/null
# NOTE: redis server not available in wolfi; uses pre-compiled binary
USER redis:redis
ENV SHIM_BACKUP_ENABLED="true" \
    SHIM_BACKUP_SCHEDULE="0 0 2 * * *" \
    SHIM_BACKUP_RETENTION_DAYS="7" \
    SHIM_BACKUP_OUTPUT_DIR="/backups"
ENV SHIM_CACHE_ENABLED="true" \
    SHIM_CACHE_MAX_ENTRIES="10000" \
    SHIM_CACHE_DEFAULT_TTL="300" \
    SHIM_CACHE_EVICTION="lru"
WORKDIR /app
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="redis7" \
      org.opencontainers.image.description="redis7 container image" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/redis/redis"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
ENV SHIM_CACHE_ENABLED="true" \
    SHIM_CACHE_MAX_ENTRIES="10000" \
    SHIM_CACHE_DEFAULT_TTL="300" \
    SHIM_CACHE_EVICTION="lru" \
    SHIM_METRICS_ENABLED="true"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
