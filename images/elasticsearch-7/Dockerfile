# =============================================================================
# SOVEREIGN HARDENED ELASTICSEARCH-7
# Generated from template - Version: 7.17.21
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=7.17.21
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends elasticsearch ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' elasticsearch 2>/dev/null || true
RUN mkdir -p /app /var/log/elasticsearch /var/cache/elasticsearch && chown -R elasticsearch:elasticsearch /app /var/log/elasticsearch /var/cache/elasticsearch 2>/dev/null || true
USER elasticsearch
WORKDIR /app
EXPOSE 9200 9300
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD elasticsearch curl -s localhost:9200
ENTRYPOINT ["elasticsearch"]
LABEL org.opencontainers.image.title="elasticsearch-7" \
      org.opencontainers.image.version="7.17.21" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
