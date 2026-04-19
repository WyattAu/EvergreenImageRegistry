# =============================================================================
# SOVEREIGN HARDENED TRANSMISSION
# Generated from template - Version: 4.0.6
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.6
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends transmission-daemon ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' transmission 2>/dev/null || true
RUN mkdir -p /app /var/log/transmission-daemon /var/cache/transmission-daemon && chown -R transmission:transmission /app /var/log/transmission-daemon /var/cache/transmission-daemon 2>/dev/null || true
USER transmission
WORKDIR /app
EXPOSE 9091
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD transmission-daemon curl -s localhost:9091/transmission/rpc
ENTRYPOINT ["transmission-daemon"]
LABEL org.opencontainers.image.title="transmission" \
      org.opencontainers.image.version="4.0.6" \
      org.opencontainers.image.vendor="Transmission" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
