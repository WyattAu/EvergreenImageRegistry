# =============================================================================
# SOVEREIGN HARDENED SYNAPSE
# Generated from template - Version: 1.105.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.105.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends synapse python3 ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' synapse 2>/dev/null || true
RUN mkdir -p /app /var/log/synapse /var/cache/synapse && chown -R synapse:synapse /app /var/log/synapse /var/cache/synapse 2>/dev/null || true
USER synapse
WORKDIR /app
EXPOSE 8008
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD synapse curl -s localhost:8008/_matrix/client/versions
ENTRYPOINT ["synapse"]
LABEL org.opencontainers.image.title="synapse" \
      org.opencontainers.image.version="1.105.0" \
      org.opencontainers.image.vendor="Matrix" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
