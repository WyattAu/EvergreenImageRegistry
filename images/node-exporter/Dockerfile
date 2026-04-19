# =============================================================================
# SOVEREIGN HARDENED NODE-EXPORTER
# Generated from template - Version: 1.8.0
# Constraint: debian-slim - minimal base, CVE scanning friendly
# =============================================================================

ARG VERSION=1.8.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends node_exporter ca-certificates && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -m -u 65534 -g '' node-exporter 2>/dev/null || true
RUN mkdir -p /app /var/log/node-exporter /var/cache/node-exporter && chown -R node-exporter:node-exporter /app /var/log/node-exporter /var/cache/node-exporter 2>/dev/null || true
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
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
