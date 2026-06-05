
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.3.3
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/couchdb/source/3.3.3/apache-couchdb-3.3.3.tar.gz" -o /couchdb.tar.gz && { echo "Binary not available - download failed" >&2; exit 1; }
    echo "7a2007b5f673d4be22a25c9a111d9066919d872ddb9135a7dcec0122299bd39e  /couchdb.tar.gz" | sha256sum -c
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN touch /tmp/couchdb.tar.gz
COPY --from=downloader /couchdb.tar.gz /tmp/couchdb.tar.gz
RUN mkdir -p /opt/couchdb || true
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
        make && \
        gcc \
        g++ && \
    rm -rf /var/lib/apt/lists/* || true && \
    [ -f /tmp/couchdb.tar.gz ] && tar -xzf /tmp/couchdb.tar.gz -C /tmp ; \
    cd /tmp/apache-couchdb-3.3.3 &&  \./configure --disable-docs --spidermonkey-version=78 && \
     make release ; \
    strip --strip-all /tmp/apache-couchdb-3.3.3/rel/couchdb/bin/* 2>/dev/null && \
    mkdir -p /opt/couchdb && \
    cp -a /tmp/apache-couchdb-3.3.3/rel/couchdb/. /opt/couchdb/
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


RUN apk add --no-cache procps \
    mkdir -p /opt 2>/dev/null || true
RUN mkdir -p /opt/couchdb || true
COPY --from=builder /opt/couchdb /opt/couchdb
RUN mkdir -p /var/lib/couchdb /var/log/couchdb /app  || true ; \
    chown -R 65532:65532 /var/lib/couchdb /var/log/couchdb /app /opt/couchdb
ENV COUCHDB_HOME=/opt/couchdb
ENV PATH="${COUCHDB_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 5984

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5984"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
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
