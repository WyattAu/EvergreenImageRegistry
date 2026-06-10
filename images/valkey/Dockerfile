# =============================================================================
# EVERGREEN HARDENED VALKEY
# Version: 9.0.4 — Redis-compatible in-memory data store
# Constraint: wolfi-base
# =============================================================================

ARG VERSION=9.0.4
ARG BUILD_DATE
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/wyattau/evergreenshim/cache-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
COPY shim.toml /etc/evergreen/shim.toml
RUN chmod +x /usr/local/bin/shim

RUN apk add --no-cache valkey ca-certificates
RUN mkdir -p /app /var/log/valkey /var/cache/valkey 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV SHIM_METRICS_ENABLED="true" \
    SHIM_CACHE_ENABLED="true" \
    SHIM_CACHE_MAX_ENTRIES="10000" \
    SHIM_CACHE_DEFAULT_TTL="300" \
    SHIM_CACHE_EVICTION="lru" \
    SHIM_HEALTHCHECK_TYPE="tcp" \
    SHIM_HEALTHCHECK_HOST="127.0.0.1" \
    SHIM_HEALTHCHECK_PORT="6379"
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "valkey-server"]
CMD ["--save", "60", "1", "--loglevel", "warning"]
LABEL org.opencontainers.image.title="valkey" \
      org.opencontainers.image.description="Valkey - open source Redis-compatible in-memory data store" \
      org.opencontainers.image.version="9.0.4" \
      org.opencontainers.image.vendor="Valkey" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.hardened="true" \
      org.opencontainers.image.source="https://github.com/valkey-io/valkey"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="tcp"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"

EXPOSE 9101
STOPSIGNAL SIGTERM
