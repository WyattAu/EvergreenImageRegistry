# =============================================================================
# SOVEREIGN HARDENED NEO4J
# Generated from template - Version: 5.20.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.20.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=5.20.0
RUN apk add --no-cache curl ca-certificates \
    curl --retry 3 --retry-delay 5 -fsSL "https://dist.neo4j.org/neo4j-community-${VERSION}-unix.tar.gz" | \
    tar xz -C /opt && \
    ln -s /opt/neo4j-community-${VERSION} /opt/neo4j && \
    ln -s /opt/neo4j/bin/neo4j /usr/local/bin/neo4j
RUN adduser -u 65532 -D neo4j 2>/dev/null || true
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
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM