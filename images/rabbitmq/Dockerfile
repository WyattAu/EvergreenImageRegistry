# =============================================================================
# SOVEREIGN HARDENED RABBITMQ
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG BUILD_DATE

FROM golang:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="rabbitmq-diagnostics -q ping" \
    READY_CMD="rabbitmq-diagnostics -q check_running" \
    STARTUP_CMD="rabbitmq-diagnostics -q ping" \
    SOVEREIGN_LOG_LEVEL=info
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -g '' rabbitmq 2>/dev/null || true
RUN mkdir -p /app /var/log/rabbitmq-server /var/cache/rabbitmq-server && chown -R rabbitmq:rabbitmq /app /var/log/rabbitmq-server /var/cache/rabbitmq-server 2>/dev/null || true
USER rabbitmq
WORKDIR /app
EXPOSE 5672 15672
ENTRYPOINT ["sh", "-c", "health-shim & exec rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM