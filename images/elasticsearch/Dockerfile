# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH
# Generated from template - Version: 8.14.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.14.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=8.14.0
ENV HEALTH_CMD="curl -sf http://localhost:9200/_cluster/health" \
    READY_CMD="curl -sf http://localhost:9200/_cluster/health" \
    STARTUP_CMD="curl -sf http://localhost:9200/_cluster/health" \
    SOVEREIGN_LOG_LEVEL=info
RUN apk add --no-cache curl ca-certificates && || true ; \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${VERSION}-linux-x86_64.tar.gz" | \
    tar xz -C /opt && \
    ln -s /opt/elasticsearch-${VERSION} /opt/elasticsearch && \
    ln -s /opt/elasticsearch/bin/elasticsearch /usr/local/bin/elasticsearch
RUN adduser -u 65532 -D elasticsearch 2>/dev/null || true
RUN mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch 2>/dev/null || true
USER elasticsearch
WORKDIR /app
EXPOSE 9200 9300
ENTRYPOINT ["sh", "-c", "elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch" \
      org.opencontainers.image.version="8.14.0" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM