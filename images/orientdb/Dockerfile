# =============================================================================
# SOVEREIGN HARDENED ORIENTDB
# Generated from template - Version: 3.2.34
# Java-based graph/document database
# Constraint: debian-slim (Java runtime required, cannot use scratch)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.2.34
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/orientechnologies/orientdb/releases/download/3.2.34/orientdb-community-3.2.34.tar.gz" -o /orientdb.tar.gz && \
    tar -xzf /orientdb.tar.gz -C /opt && rm /orientdb.tar.gz

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
COPY --from=downloader /opt/orientdb-community-3.2.34 /opt/orientdb
RUN mkdir -p /var/lib/orientdb /var/log/orientdb /app && \
    chown -R 65534:65534 /var/lib/orientdb /var/log/orientdb /app /opt/orientdb

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY --from=builder /opt/orientdb /opt/orientdb
COPY --from=builder /app /app
COPY --from=builder /var/lib/orientdb /var/lib/orientdb
COPY --from=builder /var/log/orientdb /var/log/orientdb
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV ORIENTDB_HOME=/opt/orientdb
ENV PATH="${ORIENTDB_HOME}/bin:${JAVA_HOME}/bin:${PATH}"
USER 65534:65534
WORKDIR /app
EXPOSE 2480
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["sh", "-c", "/opt/orientdb/bin/console.sh 'SELECT 1'"]
ENTRYPOINT ["/opt/orientdb/bin/server.sh"]
LABEL org.opencontainers.image.title="orientdb" \
      org.opencontainers.image.version="3.2.34" \
      org.opencontainers.image.vendor="Orientechnologies" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.runtime="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"
