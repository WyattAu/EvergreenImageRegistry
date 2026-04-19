# =============================================================================
# SOVEREIGN HARDENED MQTT
# Generated from template - Version: 2.0.18
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.0.18
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends mosquitto ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' mosquitto 2>/dev/null || true
RUN mkdir -p /app /var/log/mosquitto /var/cache/mosquitto && chown -R mosquitto:mosquitto /app /var/log/mosquitto /var/cache/mosquitto 2>/dev/null || true
USER mosquitto
WORKDIR /app
EXPOSE 1883 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mosquitto mosquitto_sub -C 1 -t $SYS/#
ENTRYPOINT ["mosquitto"]
LABEL org.opencontainers.image.title="mqtt" \
      org.opencontainers.image.version="2.0.18" \
      org.opencontainers.image.vendor="Eclipse" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
