# =============================================================================
# SOVEREIGN HARDENED GRAFANA
# Generated from template - Version: 11.0.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=11.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends grafana ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' grafana 2>/dev/null || true
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
      sovereign.constraint.debian_slim="true"
