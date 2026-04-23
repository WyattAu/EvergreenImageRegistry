# =============================================================================
# SOVEREIGN HARDENED OPENSEARCH-DASHBOARDS
# Generated from template - Version: 2.14.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.14.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache curl ca-certificates && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/${VERSION}/opensearch-dashboards-${VERSION}-linux-x64.tar.gz" | \
    tar xz -C /opt && \
    ln -s /opt/opensearch-dashboards-${VERSION} /opt/opensearch-dashboards && \
    ln -s /opt/opensearch-dashboards/bin/opensearch-dashboards /usr/local/bin/opensearch-dashboards
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
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM