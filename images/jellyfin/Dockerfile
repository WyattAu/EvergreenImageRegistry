# =============================================================================
# SOVEREIGN HARDENED JELLYFIN
# Generated from template - Version: 10.9.7
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=10.9.7
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends jellyfin ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' jellyfin 2>/dev/null || true
RUN mkdir -p /app /var/log/jellyfin /var/cache/jellyfin && chown -R jellyfin:jellyfin /app /var/log/jellyfin /var/cache/jellyfin 2>/dev/null || true
USER jellyfin
WORKDIR /app
EXPOSE 8096
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD jellyfin curl -s localhost:8096/health
ENTRYPOINT ["jellyfin"]
LABEL org.opencontainers.image.title="jellyfin" \
      org.opencontainers.image.version="10.9.7" \
      org.opencontainers.image.vendor="Jellyfin" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
