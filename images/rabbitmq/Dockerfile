# =============================================================================
# SOVEREIGN HARDENED RABBITMQ
# Generated from template - Version: 3.13.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=3.13.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:3.13.0
RUN apk add --no-cache rabbitmq ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 rabbitmq 2>/dev/null || true
RUN mkdir -p /app /var/log/rabbitmq /var/cache/rabbitmq && chown -R rabbitmq:rabbitmq /app /var/log/rabbitmq /var/cache/rabbitmq 2>/dev/null || true
USER rabbitmq:rabbitmq
WORKDIR /app
EXPOSE 5672 15672
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD rabbitmq-diagnostics ping
ENTRYPOINT ["rabbitmq-server"]
LABEL org.opencontainers.image.title="rabbitmq" \
      org.opencontainers.image.version="3.13.0" \
      org.opencontainers.image.vendor="RabbitMQ" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
