# =============================================================================
# SOVEREIGN HARDENED CASSANDRA
# Generated from template - Version: 5.0
# Java-based, requires JRE runtime
# Constraint: debian-slim (Java runtime required, cannot use scratch)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=5.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dlcdn.apache.org/cassandra/5.0/apache-cassandra-5.0-bin.tar.gz" -o /cassandra.tar.gz && \
    tar -xzf /cassandra.tar.gz -C /opt && rm /cassandra.tar.gz

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/apache-cassandra-5.0 /opt/cassandra
RUN mkdir -p /var/lib/cassandra /var/log/cassandra /app && \
    chown -R 65534:65534 /var/lib/cassandra /var/log/cassandra /app /opt/cassandra

# hadolint ignore=DL3023
FROM debian:bookworm-slim
COPY --from=builder /usr/lib/jvm /usr/lib/jvm
COPY --from=builder /opt/cassandra /opt/cassandra
COPY --from=builder /app /app
COPY --from=builder /var/lib/cassandra /var/lib/cassandra
COPY --from=builder /var/log/cassandra /var/log/cassandra
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV CASSANDRA_HOME=/opt/cassandra
ENV PATH="${CASSANDRA_HOME}/bin:${JAVA_HOME}/bin:${PATH}"
USER 65534:65534
WORKDIR /app
EXPOSE 9042
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["/opt/cassandra/bin/nodetool", "version"]
ENTRYPOINT ["/opt/cassandra/bin/cassandra", "-f"]
LABEL org.opencontainers.image.title="cassandra" \
      org.opencontainers.image.version="5.0" \
      org.opencontainers.image.vendor="Apache" \
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
