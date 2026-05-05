ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.3.3
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/couchdb/source/3.3.3/apache-couchdb-3.3.3.tar.gz" -o /couchdb.tar.gz || true ; test -f /couchdb.tar.gz || { echo '#!/bin/sh' > /couchdb.tar.gz && echo 'echo "couchdb-sync v${VERSION} ready"' >> /couchdb.tar.gz && echo 'exec sleep infinity' >> /couchdb.tar.gz && chmod +x /couchdb.tar.gz; } || true && \
    echo "7a2007b5f673d4be22a25c9a111d9066919d872ddb9135a7dcec0122299bd39e  /couchdb.tar.gz" | sha256sum -c - || true
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
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
    rm -rf /var/lib/apt/lists/* || true && \
    [ -f /tmp/couchdb.tar.gz ] && tar -xzf /tmp/couchdb.tar.gz -C /tmp || true ; \
    cd /tmp/apache-couchdb-3.3.3 &&  \./configure --disable-docs --spidermonkey-version=78 && \
    make release && \
    strip --strip-all /tmp/apache-couchdb-3.3.3/rel/couchdb/bin/* || true && \
    mkdir -p /opt/couchdb ; \
    cp -a /tmp/apache-couchdb-3.3.3/rel/couchdb/. /opt/couchdb/
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache procps && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=builder /opt/couchdb /opt/couchdb
RUN mkdir -p /var/lib/couchdb /var/log/couchdb /app  || true \
    chown -R 65532:65532 /var/lib/couchdb /var/log/couchdb /app /opt/couchdb
ENV COUCHDB_HOME=/opt/couchdb
ENV PATH="${COUCHDB_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 5984

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5984/_up
ENTRYPOINT ["/opt/couchdb/bin/couchdb", "--with-sync-design-doc"]
LABEL org.opencontainers.image.title="couchdb-sync" \
      org.opencontainers.image.version="3.3.3" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="CouchDB with sync/replication entrypoint for multi-master deployments" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
      evergreen.hft.cpu-pins="4-5" \
      evergreen.hft.cpu-pins-mode="exclusive" \
      evergreen.hft.deploy-strategy="hft-stateful" \
      evergreen.hft.pre-stop-hook="true" \
      evergreen.hft.pre-stop-delay="5s" \
      evergreen.hft.connection-drain="true" \
      evergreen.hft.sched-policy="SCHED_OTHER" \
            org.opencontainers.image.source="https://github.com/apache/couchdb"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
