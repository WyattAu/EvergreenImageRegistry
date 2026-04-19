# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH-DASHBOARDS
# Generated from template - Version: 2.14.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.14.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends opensearch-dashboards ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' opensearch-dashboards 2>/dev/null || true
RUN mkdir -p /app /var/log/opensearch-dashboards /var/cache/opensearch-dashboards && chown -R opensearch-dashboards:opensearch-dashboards /app /var/log/opensearch-dashboards /var/cache/opensearch-dashboards 2>/dev/null || true
USER opensearch-dashboards
WORKDIR /app
EXPOSE 5601
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:5601/api/status
ENTRYPOINT ["opensearch-dashboards"]
LABEL org.opencontainers.image.title="opensearch-dashboards" \
      org.opencontainers.image.version="2.14.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
