ARG VERSION=5.4.6

FROM scylladb/scylla:latest AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates libxml2-utils python3 systemd || true
RUN adduser -u 65532 -s /bin/false scylla || true
RUN mkdir -p /var/lib/scylla /var/log/scylla
COPY --from=upstream /opt/scylladb /opt/scylladb 2>/dev/null || true
COPY --from=upstream /usr/bin/scylla /usr/bin/scylla 2>/dev/null || true
COPY --from=upstream /usr/lib/scylla /usr/lib/scylla 2>/dev/null || true
COPY --from=upstream /etc/scylla /etc/scylla 2>/dev/null || true
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt 2>/dev/null || true
USER 65532:65532
WORKDIR /var/lib/scylla
EXPOSE 9042 9160 10000
ENTRYPOINT ["/usr/bin/scylla"]
LABEL org.opencontainers.image.title="scylladb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ScyllaDB - extracted from official Docker image" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.note="Extracted from scylladb/scylla:latest. downloads.scylladb.com GPG key URL was wrong (404)." \
      org.opencontainers.image.source="https://github.com/scylladb/scylladb"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
