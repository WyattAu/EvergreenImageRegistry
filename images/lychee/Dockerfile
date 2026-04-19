# =============================================================================
# SOVEREIGN HARDENED LYCHEE
# Generated from template - Version: 0.15.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=0.15.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends lychee ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' lychee 2>/dev/null || true
RUN mkdir -p /app /var/log/lychee /var/cache/lychee && chown -R lychee:lychee /app /var/log/lychee /var/cache/lychee 2>/dev/null || true
USER lychee
WORKDIR /app
EXPOSE 8089
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8089/health
ENTRYPOINT ["lychee"]
LABEL org.opencontainers.image.title="lychee" \
      org.opencontainers.image.version="0.15.1" \
      org.opencontainers.image.vendor="Lychee" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
