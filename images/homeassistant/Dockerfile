# =============================================================================
# SOVEREIGN HARDENED HOMEASSISTANT
# Generated from template - Version: 2024.4.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2024.4.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' homeassistant 2>/dev/null || true
RUN mkdir -p /app /var/log/python /var/cache/python && chown -R homeassistant:homeassistant /app /var/log/python /var/cache/python 2>/dev/null || true
USER homeassistant
WORKDIR /app
EXPOSE 8123
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:8123/api/
ENTRYPOINT ["python"]
LABEL org.opencontainers.image.title="homeassistant" \
      org.opencontainers.image.version="2024.4.2" \
      org.opencontainers.image.vendor="Home Assistant" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
