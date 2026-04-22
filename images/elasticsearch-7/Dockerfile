# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH-7
# Generated from template - Version: 7.17.21
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.17.21
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg && \
    curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | gnupg --dearmor -o /usr/share/keyrings/elasticsearch.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/elasticsearch.gnupg] https://artifacts.elastic.co/packages/7.x/apt stable main" > /etc/apt/sources.list.d/elastic-7.x.list && \
    apt-get update && apt-get install -y --no-install-recommends elasticsearch && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' elasticsearch 2>/dev/null || true
RUN mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch 2>/dev/null || true
USER elasticsearch
WORKDIR /app
EXPOSE 9200 9300
ENTRYPOINT ["elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-7" \
      org.opencontainers.image.version="7.17.21" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM