# =============================================================================
# SOVEREIGN HARDENED ACTIVEMQ
# Generated from template - Version: 6.1.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=6.1.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends activemq ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' activemq 2>/dev/null || true
RUN mkdir -p /app /var/log/activemq /var/cache/activemq && chown -R activemq:activemq /app /var/log/activemq /var/cache/activemq 2>/dev/null || true
USER activemq
WORKDIR /app
EXPOSE 61616 8161
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD activemq curl -s localhost:8161
ENTRYPOINT ["activemq"]
LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.version="6.1.2" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
