# =============================================================================
# SOVEREIGN HARDENED SONARR
# Generated from template - Version: 4.0.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends sonarr ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' sonarr 2>/dev/null || true
RUN mkdir -p /app /var/log/sonarr /var/cache/sonarr && chown -R sonarr:sonarr /app /var/log/sonarr /var/cache/sonarr 2>/dev/null || true
USER sonarr
WORKDIR /app
EXPOSE 8989
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD sonarr curl -s localhost:8989/api/v3/health
ENTRYPOINT ["sonarr"]
LABEL org.opencontainers.image.title="sonarr" \
      org.opencontainers.image.version="4.0.2" \
      org.opencontainers.image.vendor="Sonarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
