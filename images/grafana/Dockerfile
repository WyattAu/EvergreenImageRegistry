# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Generated from template - Version: 11.0.0
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE

FROM alpine:11.0.0-alpine
RUN apk add --no-cache grafana ca-certificates && rm -rf /var/cache/apk/*
RUN rm -f /bin/sh /bin/bash || true
RUN id grafana 2>/dev/null || adduser -D -u 65534 grafana
RUN mkdir -p /app /var/log/grafana /var/cache/grafana && chown -R grafana:grafana /app /var/log/grafana /var/cache/grafana
USER grafana:grafana
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD /api/health
ENTRYPOINT ["grafana"]
LABEL org.opencontainers.image.title="grafana" \
      org.opencontainers.image.version="11.0.0" \
      org.opencontainers.image.vendor="Grafana" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true"
