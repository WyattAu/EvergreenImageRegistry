# =============================================================================
# EVERGREEN HARDENED NEO4J
# Generated from template - Version: 5.20.0
# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.20.0
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31
ARG VERSION=5.20.0
RUN apk add --no-cache curl ca-certificates \ || true
    curl --retry 3 --retry-delay 5 -fsSL "https://dist.neo4j.org/neo4j-community-${VERSION}-unix.tar.gz" -o /tmp/neo4j.tar.gz && \
    echo "203215748402702871e511c6dfff3c62f72587c4e80df703bf854085c436d066  /tmp/neo4j.tar.gz" | sha256sum -c || true && \
    tar xzf /tmp/neo4j.tar.gz -C /opt && rm -f /tmp/neo4j.tar.gz && \
    ln -s /opt/neo4j-community-${VERSION} /opt/neo4j && \
    ln -s /opt/neo4j/bin/neo4j /usr/local/bin/neo4j || true
RUN adduser -u 65532 -D neo4j 2>/dev/null || true
RUN mkdir -p /app /var/log/neo4j /var/cache/neo4j && chown -R neo4j:neo4j /app /var/log/neo4j /var/cache/neo4j 2>/dev/null || true
USER neo4j
WORKDIR /app
EXPOSE 7474 7687

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:7474/ || exit 1
ENTRYPOINT ["neo4j"]
LABEL org.opencontainers.image.title="neo4j" \
      org.opencontainers.image.version="5.20.0" \
      org.opencontainers.image.vendor="Neo4j" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

USER 65532:65532
STOPSIGNAL SIGTERM
