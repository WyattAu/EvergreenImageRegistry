# =============================================================================
# SOVEREIGN HARDENED EMQX
# Generated from template - Version: 5.8.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends emqx ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' emqx 2>/dev/null || true
RUN mkdir -p /app /var/log/emqx /var/cache/emqx && chown -R emqx:emqx /app /var/log/emqx /var/cache/emqx 2>/dev/null || true
USER emqx
WORKDIR /app
EXPOSE 1883 8083
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD emqx curl -s localhost:18083/api/v4/status
ENTRYPOINT ["emqx"]
LABEL org.opencontainers.image.title="emqx" \
      org.opencontainers.image.version="5.8.0" \
      org.opencontainers.image.vendor="EMQ" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
