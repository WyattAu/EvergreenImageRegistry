# =============================================================================
# SOVEREIGN HARDENED OPENHAB
# Generated from template - Version: 4.1.2
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.1.2
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openhab ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' openhab 2>/dev/null || true
RUN mkdir -p /app /var/log/openhab /var/cache/openhab && chown -R openhab:openhab /app /var/log/openhab /var/cache/openhab 2>/dev/null || true
USER openhab
WORKDIR /app
EXPOSE 8080 8443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD openhab curl -s localhost:8080/rest/about
ENTRYPOINT ["openhab"]
LABEL org.opencontainers.image.title="openhab" \
      org.opencontainers.image.version="4.1.2" \
      org.opencontainers.image.vendor="OpenHAB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
