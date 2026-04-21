# =============================================================================
# SOVEREIGN HARDENED NEO4J-ADMIN
# Generated from template - Version: 5.17.0
# Admin tool for Neo4j
# Constraint: debian-slim (Java runtime required, cannot use scratch)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.17.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dist.neo4j.org/neo4j-community-5.17.0-unix.tar.gz" -o /neo4j.tar.gz && \
    tar -xzf /neo4j.tar.gz -C /opt && rm /neo4j.tar.gz

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
COPY --from=downloader /opt/neo4j-community-5.17.0 /opt/neo4j
RUN mkdir -p /var/lib/neo4j /var/log/neo4j /app && \
    chown -R 65534:65534 /var/lib/neo4j /var/log/neo4j /app /opt/neo4j

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY --from=builder /opt/neo4j /opt/neo4j
COPY --from=builder /app /app
COPY --from=builder /var/lib/neo4j /var/lib/neo4j
COPY --from=builder /var/log/neo4j /var/log/neo4j
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV NEO4J_HOME=/opt/neo4j
ENV PATH="${NEO4J_HOME}/bin:${JAVA_HOME}/bin:${PATH}"
USER 65534:65534
WORKDIR /app
EXPOSE 7474
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/opt/neo4j/bin/neo4j-admin", "--version"]
ENTRYPOINT ["/opt/neo4j/bin/neo4j-admin"]
LABEL org.opencontainers.image.title="neo4j-admin" \
      org.opencontainers.image.version="5.17.0" \
      org.opencontainers.image.vendor="Neo4j" \
      sovereign.image.tier="1" \
      sovereign.image.category="database-admin" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.runtime="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
