# =============================================================================
# EVERGREEN HARDENED REDIS
# Wolfi-based with health-shim as PID 1
# =============================================================================
ARG VERSION=8.6
ARG TARGETARCH
ARG SHIM_VERSION=v0.3.0

FROM redis:${VERSION} AS upstream


FROM ghcr.io/wyattau/evergreenshim/cache-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ENV HEALTH_CMD="redis-cli ping" \
    READY_CMD="redis-cli ping" \
    STARTUP_CMD="redis-cli ping" \
    EVERGREEN_LOG_LEVEL=info

RUN apk add --no-cache ca-certificates

COPY --from=upstream /usr/local/bin/redis-server /usr/local/bin/redis-server
COPY --from=upstream /usr/local/bin/redis-cli /usr/local/bin/redis-cli
COPY --from=shim /shim /usr/local/bin/shim
COPY shim.toml /etc/evergreen/shim.toml
RUN chmod +x /usr/local/bin/shim

RUN adduser -D -u 65532 -s /bin/false redis 2>/dev/null || true && \
    mkdir -p /app /var/log/redis /var/cache/redis && \
    chown -R 65532:65532 /app /var/log/redis /var/cache/redis

USER 65532:65532
ENV SHIM_CACHE_ENABLED="true" \
    SHIM_CACHE_MAX_ENTRIES="10000" \
    SHIM_CACHE_DEFAULT_TTL="300" \
    SHIM_CACHE_EVICTION="lru" \
    SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 6379 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "redis-server", "--", "--bind", "0.0.0.0", "--protected-mode", "no"]
LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.description="Redis - in-memory data structure store and cache" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/redis/redis"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.health.endpoint="/livez"
LABEL evergreen.health.listen="0.0.0.0:9101"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
