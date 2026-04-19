# =============================================================================
# SOVEREIGN HARDENED MQTT
# Generated from template - Version: 2.0.18
# =============================================================================

ARG VERSION=2.0.18
ARG BUILD_DATE

FROM alpine:2.0.18-alpine
RUN apk add --no-cache mosquitto ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id mosquitto 2>/dev/null || adduser -D -u 65534 mosquitto
RUN mkdir -p /app /var/log/mqtt /var/cache/mqtt && chown -R mosquitto:mosquitto /app /var/log/mqtt /var/cache/mqtt
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
      sovereign.constraint.nonroot="true"
