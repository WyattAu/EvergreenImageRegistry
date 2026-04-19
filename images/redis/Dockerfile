# =============================================================================
# SOVEREIGN HARDENED REDIS
# Generated from template - Version: 7.4.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.4.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends redis-server ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' redis 2>/dev/null || true
RUN mkdir -p /app /var/log/redis-server /var/cache/redis-server && chown -R redis:redis /app /var/log/redis-server /var/cache/redis-server 2>/dev/null || true
USER redis
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD redis-server redis-cli ping
ENTRYPOINT ["redis-server"]
LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.version="7.4.1" \
      org.opencontainers.image.vendor="Redis" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
