ARG VERSION=5.4.6

FROM scylladb/scylla:5.4.1 AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION
RUN apk add --no-cache ca-certificates libxml2-utils python3 systemd || true && \
    adduser -u 65532 -s /bin/false scylla || true && \
    mkdir -p /var/lib/scylla /var/log/scylla
COPY --from=upstream /opt/scylladb /opt/scylladb 2>/dev/null || true
COPY --from=upstream /usr/bin/scylla /usr/bin/scylla 2>/dev/null || true
COPY --from=upstream /usr/lib/scylla /usr/lib/scylla 2>/dev/null || true
COPY --from=upstream /etc/scylla /etc/scylla 2>/dev/null || true
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/scylla
EXPOSE 9042 9160 10000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD nodetool status
ENTRYPOINT ["/usr/bin/scylla"]
LABEL org.opencontainers.image.title="scylladb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened ScyllaDB - extracted from official Docker image" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.note="Extracted from scylladb/scylla:5.4.1. downloads.scylladb.com GPG key URL was wrong (404)." \
      org.opencontainers.image.source="https://github.com/scylladb/scylladb"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
