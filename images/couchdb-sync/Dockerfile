# =============================================================================
# SOVEREIGN HARDENED COUCHDB-SYNC
# Generated from template - Version: 3.3.3
# Erlang-based, sync entrypoint variant
# Constraint: debian-slim (Erlang runtime required, cannot use scratch)
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.3.3
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dlcdn.apache.org/couchdb/source/3.3.3/apache-couchdb-3.3.3.tar.gz" -o /couchdb.tar.gz

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
COPY --from=downloader /couchdb.tar.gz /tmp/couchdb.tar.gz
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        erlang-dev \
        erlang-base \
        erlang-asn1 \
        erlang-crypto \
        erlang-ssl \
        erlang-public-key \
        erlang-syntax-tools \
        erlang-tools \
        libmozjs-78-dev \
        libicu-dev \
        curl \
        ca-certificates \
        make \
        gcc \
        g++ && \
    rm -rf /var/lib/apt/lists/*
RUN tar -xzf /tmp/couchdb.tar.gz -C /tmp && \
    cd /tmp/apache-couchdb-3.3.3 && \
    ./configure --disable-docs --spidermonkey-version=78 && \
    make release && \
    strip --strip-all /tmp/apache-couchdb-3.3.3/rel/couchdb/bin/* || true && \
    mkdir -p /opt/couchdb && \
    cp -a /tmp/apache-couchdb-3.3.3/rel/couchdb/. /opt/couchdb/

# hadolint ignore=DL3023
FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        erlang-base \
        erlang-asn1 \
        erlang-crypto \
        erlang-ssl \
        erlang-public-key \
        erlang-syntax-tools \
        erlang-tools \
        libmozjs-78-0 \
        libicu72 \
        procps && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY --from=builder /opt/couchdb /opt/couchdb
RUN mkdir -p /var/lib/couchdb /var/log/couchdb /app && \
    chown -R 65534:65534 /var/lib/couchdb /var/log/couchdb /app /opt/couchdb
ENV COUCHDB_HOME=/opt/couchdb
ENV PATH="${COUCHDB_HOME}/bin:${PATH}"
USER 65534:65534
WORKDIR /app
EXPOSE 5984
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/opt/couchdb/bin/couchdb", "--version"]
ENTRYPOINT ["/opt/couchdb/bin/couchdb", "--with-sync-design-doc"]
LABEL org.opencontainers.image.title="couchdb-sync" \
      org.opencontainers.image.version="3.3.3" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="CouchDB with sync/replication entrypoint for multi-master deployments" \
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
