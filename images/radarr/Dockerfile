# =============================================================================
# SOVEREIGN HARDENED RADARR
# Generated from template - Version: 5.6.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.6.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends radarr ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' radarr 2>/dev/null || true
RUN mkdir -p /app /var/log/radarr /var/cache/radarr && chown -R radarr:radarr /app /var/log/radarr /var/cache/radarr 2>/dev/null || true
USER radarr
WORKDIR /app
EXPOSE 7878
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD radarr curl -s localhost:7878/api/v3/health
ENTRYPOINT ["radarr"]
LABEL org.opencontainers.image.title="radarr" \
      org.opencontainers.image.version="5.6.1" \
      org.opencontainers.image.vendor="Radarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
