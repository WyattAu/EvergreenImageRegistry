# =============================================================================
# SOVEREIGN HARDENED RABBITMQ
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ENV HEALTH_CMD="rabbitmq-diagnostics -q ping" \
    READY_CMD="rabbitmq-diagnostics -q check_running" \
    STARTUP_CMD="rabbitmq-diagnostics -q ping" \
    SOVEREIGN_LOG_LEVEL=info
RUN apk add --no-cache ca-certificates 
RUN adduser -u 65532 -D rabbitmq 2>/dev/null || true
RUN mkdir -p /app /var/log/rabbitmq-server /var/cache/rabbitmq-server && chown -R rabbitmq:rabbitmq /app /var/log/rabbitmq-server /var/cache/rabbitmq-server 2>/dev/null || true
USER rabbitmq
WORKDIR /app
EXPOSE 5672 15672
ENTRYPOINT ["sh", "-c", "rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
