# =============================================================================
# SOVEREIGN HARDENED DRONE
# Generated from template - Version: 2.16.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.16.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends drone ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' drone 2>/dev/null || true
RUN mkdir -p /app /var/log/drone /var/cache/drone && chown -R drone:drone /app /var/log/drone /var/cache/drone 2>/dev/null || true
USER drone
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD drone curl -s localhost:80/healthz
ENTRYPOINT ["drone"]
LABEL org.opencontainers.image.title="drone" \
      org.opencontainers.image.version="2.16.0" \
      org.opencontainers.image.vendor="Drone" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
