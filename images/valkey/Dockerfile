# =============================================================================
# SOVEREIGN HARDENED VALKEY
# Generated from template - Version: 7.2.4
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.2.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends valkey ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' valkey 2>/dev/null || true
RUN mkdir -p /app /var/log/valkey-server /var/cache/valkey-server && chown -R valkey:valkey /app /var/log/valkey-server /var/cache/valkey-server 2>/dev/null || true
USER valkey
WORKDIR /app
EXPOSE 6379
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD valkey-server valkey-cli ping
ENTRYPOINT ["valkey-server"]
LABEL org.opencontainers.image.title="valkey" \
      org.opencontainers.image.version="7.2.4" \
      org.opencontainers.image.vendor="Valkey" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
