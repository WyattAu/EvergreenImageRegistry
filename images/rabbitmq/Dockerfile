# =============================================================================
# SOVEREIGN HARDENED RABBITMQ
# Generated from template - Version: 3.13.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=3.13.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends rabbitmq-server ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' rabbitmq 2>/dev/null || true
RUN mkdir -p /app /var/log/rabbitmq-server /var/cache/rabbitmq-server && chown -R rabbitmq:rabbitmq /app /var/log/rabbitmq-server /var/cache/rabbitmq-server 2>/dev/null || true
USER rabbitmq
WORKDIR /app
EXPOSE 5672 15672
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD rabbitmq-server rabbitmq-diagnostics ping
ENTRYPOINT ["rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.version="3.13.1" \
      org.opencontainers.image.vendor="RabbitMQ" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
