# =============================================================================
# SOVEREIGN HARDENED PLANKA
# Generated from template - Version: 1.17.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.17.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' planka 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R planka:planka /app /var/log/node /var/cache/node 2>/dev/null || true
USER planka
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:3000/api/health
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="planka" \
      org.opencontainers.image.version="1.17.0" \
      org.opencontainers.image.vendor="Planka" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
