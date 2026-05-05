ARG VERSION=1.11.0

FROM cockroachdb/cockroach-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/cockroach-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/cockroach-operator"]
LABEL org.opencontainers.image.title="crdb-operator" \
      org.opencontainers.image.description="Evergreen hardened CockroachDB Operator - Kubernetes operator for CockroachDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/cockroachdb/cockroach"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
