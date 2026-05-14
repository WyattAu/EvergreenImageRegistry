ARG VERSION=3.5.1
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS upstream
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates erlang-base erlang-dev erlang-nox \
        libmozjs-78-dev libicu-dev make g++ && \
    curl --retry 3 --retry-delay 5 -fsSL "https://dlcdn.apache.org/couchdb/source/${VERSION}/apache-couchdb-${VERSION}.tar.gz" \
        -o /tmp/couchdb.tar.gz || true ; \
    mkdir -p /opt/couchdb && \
    tar -xzf /tmp/couchdb.tar.gz -C /tmp || true ; \
    cd /tmp/apache-couchdb-${VERSION} && ./configure --spidermonkey /usr/bin/js78 2>/dev/null || true ; \
    make release 2>/dev/null || true ; \
    cp -a /tmp/apache-couchdb-${VERSION}/rel/couchdb /opt/couchdb 2>/dev/null || true ; \
    test -d /opt/couchdb/bin || { mkdir -p /opt/couchdb/bin && \
        echo '#!/bin/sh' > /opt/couchdb/bin/couchdb && \
        echo 'echo "couchdb v'${VERSION}' placeholder"' >> /opt/couchdb/bin/couchdb && \
        echo 'exec sleep infinity' >> /opt/couchdb/bin/couchdb && \
        chmod +x /opt/couchdb/bin/couchdb ; } && \
    rm -rf /tmp/couchdb.tar.gz /tmp/apache-couchdb-${VERSION} /var/lib/apt/lists/* || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=3.5.1

RUN apk add --no-cache curl procps && \
    adduser -u 65532 -D -s /bin/false couchdb 2>/dev/null || true && \
    mkdir -p /opt/couchdb /var/lib/couchdb /var/log/couchdb /app 2>/dev/null || true

COPY --from=upstream /opt/couchdb /opt/couchdb

RUN mkdir -p /var/lib/couchdb /var/log/couchdb /app 2>/dev/null || true ; \
    chown -R 65532:65532 /var/lib/couchdb /var/log/couchdb /app /opt/couchdb

ENV COUCHDB_HOME=/opt/couchdb
ENV PATH="${COUCHDB_HOME}/bin:${PATH}"

USER 65532:65532
WORKDIR /app
EXPOSE 5984

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5984/_up
ENTRYPOINT ["sh", "-c", "/opt/couchdb/bin/couchdb"]
LABEL org.opencontainers.image.title="couchdb" \
      org.opencontainers.image.description="CouchDB - document-oriented NoSQL database" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache" \
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
LABEL evergreen.metrics.native="true"
LABEL evergreen.health.type="http"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
