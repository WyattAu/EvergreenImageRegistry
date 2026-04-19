# =============================================================================
# SOVEREIGN HARDENED NATS
# Generated from template - Version: 2.10.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=2.10.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nats ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' nats 2>/dev/null || true
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
      sovereign.constraint.debian_slim="true"
