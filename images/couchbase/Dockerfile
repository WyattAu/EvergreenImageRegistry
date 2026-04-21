# =============================================================================
# SOVEREIGN HARDENED COUCHBASE
# Generated from template - Version: 7.6.1
# Complex install from Couchbase repository
# Constraint: debian-slim (runtime dependencies required, cannot use scratch)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=7.6.1
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg && \
    rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://packages.couchbase.com/ubuntu/couchbase.key" | gpg --dearmor -o /usr/share/keyrings/couchbase-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/couchbase-archive-keyring.gpg] https://packages.couchbase.com/ubuntu jammy main" > /etc/apt/sources.list.d/couchbase.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends couchbase-server-community && \
    rm -rf /var/lib/apt/lists/*

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libstdc++6 \
        libssl3 \
        libcurl4 \
        zlib1g \
        libevent-2.1-7 \
        libsnappy1v5 \
        procps && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY --from=builder /opt/couchbase /opt/couchbase
RUN mkdir -p /var/lib/couchbase /var/log/couchbase /app && \
    chown -R 65534:65534 /var/lib/couchbase /var/log/couchbase /app /opt/couchbase
ENV COUCHBASE_HOME=/opt/couchbase
ENV PATH="${COUCHBASE_HOME}/bin:${PATH}"
USER 65534:65534
WORKDIR /app
EXPOSE 8091
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["/opt/couchbase/bin/couchbase-cli", "server-info", "-c", "127.0.0.1:8091"]
ENTRYPOINT ["/opt/couchbase/bin/couchbase-server"]
LABEL org.opencontainers.image.title="couchbase" \
      org.opencontainers.image.version="7.6.1" \
      org.opencontainers.image.vendor="Couchbase" \
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
