ARG VERSION=3.5.1

FROM couchdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION

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
