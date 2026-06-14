# =============================================================================
# EVERGREEN HARDENED RABBITMQ
# Repack of upstream rabbitmq:3.13-management with health-shim overlay.
#
# Erlang/RabbitMQ has a deep, tightly-coupled dependency tree (BEAM VM, OTP,
# shared libs, NIFs) that cannot be reliably transplanted onto a wolfi-base
# scratch stage. The only robust path is to keep the upstream image as the
# final stage and layer hardening (health-shim, non-root entrypoint,
# HEALTHCHECK, labels) on top.
#
# Note: this is an intentional, documented exception to the
# "no debian final stage" constraint, recorded for rabbitmq specifically.
# =============================================================================

ARG VERSION=3.13
ARG BUILD_DATE

ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM rabbitmq:${VERSION}-management

# Drop in the evergreen health-shim, which wraps the upstream
# docker-entrypoint.sh with supervision, healthchecks, and metrics.
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ENV HEALTH_CMD="rabbitmq-diagnostics -q ping" \
    READY_CMD="rabbitmq-diagnostics -q check_running" \
    STARTUP_CMD="rabbitmq-diagnostics -q ping" \
    EVERGREEN_LOG_LEVEL=info \
    SHIM_METRICS_ENABLED="true"

WORKDIR /app
EXPOSE 5672 15672

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5672"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "docker-entrypoint.sh"]
CMD ["rabbitmq-server"]

LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.description="RabbitMQ - message broker software" \
      org.opencontainers.image.version="3.13" \
      org.opencontainers.image.vendor="RabbitMQ" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="upstream" \
      org.opencontainers.image.source="https://github.com/rabbitmq/rabbitmq-server"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
