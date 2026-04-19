# =============================================================================
# SOVEREIGN HARDENED CONSUL
# Generated from template - Version: 1.18.1
# Constraint: debian-slim - fallback when scratch/distroless/wolfi not available
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.18.1
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends consul ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' consul 2>/dev/null || true
RUN mkdir -p /app /var/log/consul /var/cache/consul && chown -R consul:consul /app /var/log/consul /var/cache/consul 2>/dev/null || true
USER consul:consul
WORKDIR /app
EXPOSE 8500
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD consul members
ENTRYPOINT ["consul"]
LABEL org.opencontainers.image.title="consul" \
      org.opencontainers.image.version="1.18.1" \
      org.opencontainers.image.vendor="HashiCorp" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
