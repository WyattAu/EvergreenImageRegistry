# =============================================================================
# SOVEREIGN HARDENED MQTT
# Generated from template - Version: 2.0.18
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=2.0.18
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:2.0.18
RUN apk add --no-cache mosquitto ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 mosquitto 2>/dev/null || true
RUN mkdir -p /app /var/log/mqtt /var/cache/mqtt && chown -R mosquitto:mosquitto /app /var/log/mqtt /var/cache/mqtt 2>/dev/null || true
USER mosquitto:mosquitto
WORKDIR /app
EXPOSE 1883 9001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD mosquitto_sub
ENTRYPOINT ["mosquitto"]
LABEL org.opencontainers.image.title="mqtt" \
      org.opencontainers.image.version="2.0.18" \
      org.opencontainers.image.vendor="Eclipse" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
