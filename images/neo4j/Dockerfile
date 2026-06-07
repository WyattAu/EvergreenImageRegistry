# =============================================================================







# EVERGREEN HARDENED NEO4J







# Generated from template - Version: 5.20.0







# Constraint: debian-slim - fallback when scratch/distroless/wolfi unavailable







# Priority: scratch > distroless > wolfi > debian-slim (last resort)







# =============================================================================















ARG VERSION=5.20.0
ARG TARGETARCH







ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532























ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim








ARG VERSION=5.20.0







RUN apk add --no-cache curl ca-certificates \ && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dist.neo4j.org/neo4j-community-${VERSION}-unix.tar.gz" -o /tmp/neo4j.tar.gz && \
    echo "203215748402702871e511c6dfff3c62f72587c4e80df703bf854085c436d066  /tmp/neo4j.tar.gz" | sha256sum -c && \
    tar xzf /tmp/neo4j.tar.gz -C /opt && rm -f /tmp/neo4j.tar.gz && \
    ln -s /opt/neo4j-community-${VERSION} /opt/neo4j && \
    ln -s /opt/neo4j/bin/neo4j /usr/local/bin/neo4j || true







RUN adduser -u 65532 -D neo4j 2>/dev/null || true && \
    mkdir -p /app /var/log/neo4j /var/cache/neo4j && chown -R neo4j:neo4j /app /var/log/neo4j /var/cache/neo4j 2>/dev/null || true







USER neo4j
ENV SHIM_METRICS_ENABLED="true"







WORKDIR /app







EXPOSE 7474 7687






















HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:7474"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]







LABEL org.opencontainers.image.title="neo4j" \
      org.opencontainers.image.description="Neo4j - native graph database" \
      org.opencontainers.image.version="5.20.0" \
      org.opencontainers.image.vendor="Neo4j" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/neo4j/neo4j"







LABEL evergreen.metrics.native="ztunnel"







LABEL evergreen.health.type="exec"







LABEL evergreen.security.cap-drop="ALL"







LABEL evergreen.security.no-new-privileges="true"







LABEL evergreen.security.read-only-rootfs="true"







LABEL evergreen.security.seccomp="runtime-default"















EXPOSE 9101















USER 65532:65532







LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
