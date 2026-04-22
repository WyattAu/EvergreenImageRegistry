# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH-DASHBOARDS
# Generated from template - Version: 2.14.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.14.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg && \
    curl -fsSL https://artifacts.opensearch.org/publickeys/opensearch.pgp | gnupg --dearmor -o /usr/share/keyrings/opensearch.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/opensearch.gnupg] https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/2.x/apt stable main" > /etc/apt/sources.list.d/opensearch-dashboards.list && \
    apt-get update && apt-get install -y --no-install-recommends opensearch-dashboards && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' opensearch-dashboards 2>/dev/null || true
RUN mkdir -p /app /var/log/opensearch-dashboards /var/cache/opensearch-dashboards && chown -R opensearch-dashboards:opensearch-dashboards /app /var/log/opensearch-dashboards /var/cache/opensearch-dashboards 2>/dev/null || true
USER opensearch-dashboards
WORKDIR /app
EXPOSE 5601
ENTRYPOINT ["opensearch-dashboards"]
LABEL org.opencontainers.image.title="opensearch-dashboards" \
      org.opencontainers.image.version="2.14.0" \
      org.opencontainers.image.vendor="OpenSearch" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM