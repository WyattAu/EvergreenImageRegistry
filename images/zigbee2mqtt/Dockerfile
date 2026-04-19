# =============================================================================
# SOVEREIGN HARDENED ZIGBEE2MQTT
# Generated from template - Version: 1.37.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.37.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' node 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8080/api/info
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="zigbee2mqtt" \
      org.opencontainers.image.version="1.37.1" \
      org.opencontainers.image.vendor="Zigbee2MQTT" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
