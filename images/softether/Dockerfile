# =============================================================================
# SOVEREIGN HARDENED SOFTETHER
# Generated from template - Version: 4.38-9770
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.38-9770
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' appuser 2>/dev/null || true
RUN mkdir -p /app /var/log/vpnserver /var/cache/vpnserver && chown -R appuser:appuser /app /var/log/vpnserver /var/cache/vpnserver 2>/dev/null || true
USER appuser
WORKDIR /app
EXPOSE 443 992 1194 500 4500 5555
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/bin/vpnserver version
ENTRYPOINT ["vpnserver"]
LABEL org.opencontainers.image.title="softether" \
      org.opencontainers.image.version="4.38-9770" \
      org.opencontainers.image.vendor="SoftEther" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
