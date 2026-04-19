# =============================================================================
# SOVEREIGN HARDENED LIDARR
# Generated from template - Version: 2.3.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.3.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends lidarr ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' lidarr 2>/dev/null || true
RUN mkdir -p /app /var/log/lidarr /var/cache/lidarr && chown -R lidarr:lidarr /app /var/log/lidarr /var/cache/lidarr 2>/dev/null || true
USER lidarr
WORKDIR /app
EXPOSE 8686
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD lidarr curl -s localhost:8686/api/v1/health
ENTRYPOINT ["lidarr"]
LABEL org.opencontainers.image.title="lidarr" \
      org.opencontainers.image.version="2.3.1" \
      org.opencontainers.image.vendor="Lidarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
