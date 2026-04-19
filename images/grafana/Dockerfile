# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Generated from template - Version: 11.0.0
# Constraint: wolfi-os - minimal, CVE-free base
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:11.0.0
RUN apk add --no-cache grafana ca-certificates && rm -rf /var/cache/apk/*
# Create non-root user
RUN adduser -D -u 65534 grafana 2>/dev/null || true
RUN mkdir -p /app /var/log/grafana /var/cache/grafana && chown -R grafana:grafana /app /var/log/grafana /var/cache/grafana 2>/dev/null || true
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
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.wolfi="true"
