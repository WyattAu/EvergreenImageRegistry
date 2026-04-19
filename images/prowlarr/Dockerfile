# =============================================================================
# SOVEREIGN HARDENED PROWLARR
# Generated from template - Version: 1.23.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.23.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends prowlarr ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' prowlarr 2>/dev/null || true
RUN mkdir -p /app /var/log/prowlarr /var/cache/prowlarr && chown -R prowlarr:prowlarr /app /var/log/prowlarr /var/cache/prowlarr 2>/dev/null || true
USER prowlarr
WORKDIR /app
EXPOSE 9696
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD prowlarr curl -s localhost:9696/api/v1/health
ENTRYPOINT ["prowlarr"]
LABEL org.opencontainers.image.title="prowlarr" \
      org.opencontainers.image.version="1.23.0" \
      org.opencontainers.image.vendor="Prowlarr" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
