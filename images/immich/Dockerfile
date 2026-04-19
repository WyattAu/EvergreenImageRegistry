# =============================================================================
# SOVEREIGN HARDENED IMMICH
# Generated from template - Version: 1.106.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.106.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nodejs ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' immich 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R immich:immich /app /var/log/node /var/cache/node 2>/dev/null || true
USER immich
WORKDIR /app
EXPOSE 2283
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:2283/api/server-info/ping
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="immich" \
      org.opencontainers.image.version="1.106.0" \
      org.opencontainers.image.vendor="Immich" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
