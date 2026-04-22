# =============================================================================
# SOVEREIGN HARDENED NEO4J
# Generated from template - Version: 5.20.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.20.0
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg && \
    curl -fsSL https://debian.neo4j.com/neotechnology.gnupg.key | gnupg --dearmor -o /usr/share/keyrings/neo4j.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/neo4j.gnupg] https://debian.neo4j.com stable 4.4" > /etc/apt/sources.list.d/neo4j.list && \
    apt-get update && apt-get install -y --no-install-recommends neo4j && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65532 -g '' neo4j 2>/dev/null || true
RUN mkdir -p /app /var/log/neo4j /var/cache/neo4j && chown -R neo4j:neo4j /app /var/log/neo4j /var/cache/neo4j 2>/dev/null || true
USER neo4j
WORKDIR /app
EXPOSE 7474 7687
ENTRYPOINT ["neo4j"]
LABEL org.opencontainers.image.title="neo4j" \
      org.opencontainers.image.version="5.20.0" \
      org.opencontainers.image.vendor="Neo4j" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
USER 65532:65532
STOPSIGNAL SIGTERM