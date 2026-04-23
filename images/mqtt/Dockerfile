# =============================================================================
# SOVEREIGN HARDENED MQTT
# Generated from template - Version: 2.0.18
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.0.18
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache ca-certificates
RUN adduser -u 65532 -G '' -D mosquitto 2>/dev/null || true
RUN mkdir -p /app /var/log/mosquitto /var/cache/mosquitto && chown -R mosquitto:mosquitto /app /var/log/mosquitto /var/cache/mosquitto 2>/dev/null || true
USER mosquitto
WORKDIR /app
EXPOSE 1883 9001
ENTRYPOINT ["mosquitto"]
LABEL org.opencontainers.image.title="mqtt" \
      org.opencontainers.image.version="2.0.18" \
      org.opencontainers.image.vendor="Eclipse" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM