# =============================================================================
# SOVEREIGN HARDENED OUTLINE
# Generated from template - Version: 0.77.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.77.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm postgresql-client ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' outline 2>/dev/null || true
RUN mkdir -p /app /var/log/node /var/cache/node && chown -R outline:outline /app /var/log/node /var/cache/node 2>/dev/null || true
USER outline
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node curl -s localhost:3000/api/status
ENTRYPOINT ["node"]
LABEL org.opencontainers.image.title="outline" \
      org.opencontainers.image.version="0.77.0" \
      org.opencontainers.image.vendor="Outline" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
