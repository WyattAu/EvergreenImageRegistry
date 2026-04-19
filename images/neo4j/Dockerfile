# =============================================================================
# SOVEREIGN HARDENED NEO4J
# Generated from template - Version: 5.20.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.20.0
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends neo4j ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' neo4j 2>/dev/null || true
RUN mkdir -p /app /var/log/neo4j /var/cache/neo4j && chown -R neo4j:neo4j /app /var/log/neo4j /var/cache/neo4j 2>/dev/null || true
USER neo4j
WORKDIR /app
EXPOSE 7474 7687
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD neo4j curl -s localhost:7474
ENTRYPOINT ["neo4j"]
LABEL org.opencontainers.image.title="neo4j" \
      org.opencontainers.image.version="5.20.0" \
      org.opencontainers.image.vendor="Neo4j" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
