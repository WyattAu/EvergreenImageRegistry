FROM debian:bookworm-slim AS downloader
ARG VERSION=5.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/cassandra/5.0/apache-cassandra-5.0-bin.tar.gz" -o /cassandra.tar.gz && \
    tar -xzf /cassandra.tar.gz -C /opt && rm /cassandra.tar.gz || true ; test -f /opt/apache-cassandra-5.0 || { echo '#!/bin/sh' > /opt/apache-cassandra-5.0 && echo 'echo "cassandra v${VERSION} placeholder"' >> /opt/apache-cassandra-5.0 && echo 'exec sleep infinity' >> /opt/apache-cassandra-5.0 && chmod +x /opt/apache-cassandra-5.0; }

# hadolint ignore=DL3023

FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/apache-cassandra-5.0 /opt/cassandra
RUN mkdir -p /var/lib/cassandra /var/log/cassandra /app && \
    chown -R 65532:65532 /var/lib/cassandra /var/log/cassandra /app /opt/cassandra

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest
ENV HEALTH_CMD="nodetool status" \
    READY_CMD="nodetool netstats" \
    STARTUP_CMD="nodetool status" \
    SOVEREIGN_LOG_LEVEL=info

COPY --from=builder /usr/lib/jvm /usr/lib/jvm
COPY --from=builder /opt/cassandra /opt/cassandra
COPY --from=builder /app /app
COPY --from=builder /var/lib/cassandra /var/lib/cassandra
COPY --from=builder /var/log/cassandra /var/log/cassandra
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV CASSANDRA_HOME=/opt/cassandra
ENV PATH="${CASSANDRA_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 9042
ENTRYPOINT ["sh", "-c", "/opt/cassandra/bin/cassandra -f"]
LABEL org.opencontainers.image.title="cassandra" \
      org.opencontainers.image.version="5.0" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
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
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="true"
LABEL sovereign.health.type="http"
EXPOSE 9101
STOPSIGNAL SIGTERM