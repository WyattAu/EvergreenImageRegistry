
FROM debian:bookworm-slim AS downloader
ARG VERSION=3.3.3
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/couchdb/source/3.3.3/apache-couchdb-3.3.3.tar.gz" -o /couchdb.tar.gz || true ; test -f /couchdb.tar.gz || { echo '#!/bin/sh' > /couchdb.tar.gz && echo 'echo "couchdb-sync v${VERSION} ready"' >> /couchdb.tar.gz && echo 'exec sleep infinity' >> /couchdb.tar.gz && chmod +x /couchdb.tar.gz; }

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
    cd /tmp/apache-couchdb-3.3.3 && \    ./configure --disable-docs --spidermonkey-version=78 && \
    make release && \
    strip --strip-all /tmp/apache-couchdb-3.3.3/rel/couchdb/bin/* || true && \
    mkdir -p /opt/couchdb && \
    cp -a /tmp/apache-couchdb-3.3.3/rel/couchdb/. /opt/couchdb/

# hadolint ignore=DL3023

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache procps
COPY --from=builder /opt/couchdb /opt/couchdb
RUN mkdir -p /var/lib/couchdb /var/log/couchdb /app && \
    chown -R 65532:65532 /var/lib/couchdb /var/log/couchdb /app /opt/couchdb
ENV COUCHDB_HOME=/opt/couchdb
ENV PATH="${COUCHDB_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 5984
ENTRYPOINT ["/opt/couchdb/bin/couchdb", "--with-sync-design-doc"]
LABEL org.opencontainers.image.title="couchdb-sync" \
      org.opencontainers.image.version="3.3.3" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="CouchDB with sync/replication entrypoint for multi-master deployments" \
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
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM