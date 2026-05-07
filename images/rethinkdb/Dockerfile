ARG VERSION=latest

FROM rethinkdb/rethinkdb:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION
RUN apk add --no-cache ca-certificates libstdc++ && \
    adduser -u 65532 -s /bin/false rethinkdb || true && \
    mkdir -p /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data /opt 2>/dev/null || true
COPY --from=upstream /rethinkdb /opt/rethinkdb
RUN chown -R 65532:65532 /opt/rethinkdb /var/lib/rethinkdb /var/log/rethinkdb /var/cache/rethinkdb /data

WORKDIR /data

EXPOSE 28015 29015 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="rethinkdb" org.opencontainers.image.version="${VERSION}" org.opencontainers.image.description="Evergreen hardened RethinkDB - real-time NoSQL database" org.opencontainers.image.vendor="RethinkDB" evergreen.image.tier="1" evergreen.image.category="database" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.base.image="wolfi" \
      org.opencontainers.image.source="https://github.com/rethinkdb/rethinkdb"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/rethinkdb/bin/rethinkdb", "--bind", "all", "--directory", "/data"]
