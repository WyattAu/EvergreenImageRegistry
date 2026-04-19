# =============================================================================
# SOVEREIGN HARDENED UPTIME-KUMA
# Generated from template - Version: 1.23.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.23.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' node 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R node:node /app /var/log/node /var/cache/node 2>/dev/null || true
USER node
WORKDIR /app
EXPOSE 3001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node curl -s localhost:3001/api/status
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="uptime-kuma" \
      org.opencontainers.image.version="1.23.1" \
      org.opencontainers.image.vendor="Uptime Kuma" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
