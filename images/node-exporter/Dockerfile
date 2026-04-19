# =============================================================================
# SOVEREIGN HARDENED NODE-EXPORTER
# Generated from template - Version: 1.8.0
# =============================================================================

ARG VERSION=1.8.0
ARG BUILD_DATE

FROM alpine:1.8.0-alpine
RUN apk add --no-cache node_exporter ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id node-exporter 2>/dev/null || adduser -D -u 65534 node-exporter
RUN mkdir -p /app /var/log/node-exporter /var/cache/node-exporter && chown -R node-exporter:node-exporter /app /var/log/node-exporter /var/cache/node-exporter
USER node-exporter:node-exporter
WORKDIR /app
EXPOSE 9100
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /metrics
ENTRYPOINT ["node_exporter"]
LABEL org.opencontainers.image.title="node-exporter" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Prometheus" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
