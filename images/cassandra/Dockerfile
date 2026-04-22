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
    apt-get install -y --no-install-recommends java-17-runtime && \
    rm -rf /var/lib/apt/lists/*
COPY --from=downloader /opt/apache-cassandra-5.0 /opt/cassandra
RUN mkdir -p /var/lib/cassandra /var/log/cassandra /app && \
    chown -R 65532:65532 /var/lib/cassandra /var/log/cassandra /app /opt/cassandra

# hadolint ignore=DL3023

FROM golang:1.23-alpine AS health-shim-builder
COPY images/health-shim/go.mod images/health-shim/main.go /build/
RUN cd /build && CGO_ENABLED=0 go build -ldflags="-s -w" -o /health-shim .
FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
COPY --from=health-shim-builder /health-shim /usr/local/bin/health-shim
ENV HEALTH_CMD="nodetool status" \
    READY_CMD="nodetool netstats" \
    STARTUP_CMD="nodetool status" \
    SOVEREIGN_LOG_LEVEL=info

COPY --from=builder /usr/lib/jvm /usr/lib/jvm
COPY --from=builder /opt/cassandra /opt/cassandra
COPY --from=builder /app /app
COPY --from=builder /var/lib/cassandra /var/lib/cassandra
COPY --from=builder /var/log/cassandra /var/log/cassandra
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV CASSANDRA_HOME=/opt/cassandra
ENV PATH="${CASSANDRA_HOME}/bin:${JAVA_HOME}/bin:${PATH}"
USER 65532:65532
WORKDIR /app
EXPOSE 9042
ENTRYPOINT ["sh", "-c", "health-shim & exec /opt/cassandra/bin/cassandra -f"]
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