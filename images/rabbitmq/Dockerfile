# =============================================================================
# EVERGREEN HARDENED RABBITMQ
# Generated from template - Version: 3.13
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM scratch AS entrypoint
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV HEALTH_CMD="rabbitmq-diagnostics -q ping" \
    READY_CMD="rabbitmq-diagnostics -q check_running" \
    STARTUP_CMD="rabbitmq-diagnostics -q ping" \
    EVERGREEN_LOG_LEVEL=info
RUN apk add --no-cache bash ca-certificates && \
    adduser -u 65532 -D rabbitmq 2>/dev/null || true && \
    mkdir -p /app /var/log/rabbitmq-server /var/cache/rabbitmq-server && chown -R rabbitmq:rabbitmq /app /var/log/rabbitmq-server /var/cache/rabbitmq-server 2>/dev/null || true
COPY --from=entrypoint /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh
WORKDIR /app
EXPOSE 5672 15672

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5672"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
CMD ["-c", "/usr/local/bin/docker-entrypoint.sh", "--", "rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.description="RabbitMQ - message broker software" \
      org.opencontainers.image.version="3.13" \
      org.opencontainers.image.vendor="RabbitMQ" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/rabbitmq/rabbitmq-server"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
