# =============================================================================
# SOVEREIGN HARDENED NATS
# Generated from template - Version: 2.10.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2.10.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2.10.0
RUN apk add --no-cache nats ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 nats 2>/dev/null || true
RUN mkdir -p /app /var/log/nats /var/cache/nats && chown -R nats:nats /app /var/log/nats /var/cache/nats 2>/dev/null || true
USER nats:nats
WORKDIR /app
EXPOSE 4222 8222
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD nats-server -v
ENTRYPOINT ["nats-server"]
LABEL org.opencontainers.image.title="nats" \
      org.opencontainers.image.version="2.10.0" \
      org.opencontainers.image.vendor="NATS" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
