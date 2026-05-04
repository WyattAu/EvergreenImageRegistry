# =============================================================================
# EVERGREEN HARDENED RABBITMQ
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ENV HEALTH_CMD="rabbitmq-diagnostics -q ping" \
    READY_CMD="rabbitmq-diagnostics -q check_running" \
    STARTUP_CMD="rabbitmq-diagnostics -q ping" \
    EVERGREEN_LOG_LEVEL=info
RUN apk add --no-cache ca-certificates && \
    adduser -u 65532 -D rabbitmq 2>/dev/null || true && \
    mkdir -p /app /var/log/rabbitmq-server /var/cache/rabbitmq-server && chown -R rabbitmq:rabbitmq /app /var/log/rabbitmq-server /var/cache/rabbitmq-server 2>/dev/null || true
USER rabbitmq
WORKDIR /app
EXPOSE 5672 15672

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD rabbitmq-diagnostics check_running
ENTRYPOINT ["sh", "-c", "rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
