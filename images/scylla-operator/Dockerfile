ARG VERSION=1.20.2
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM docker.io/scylladb/scylla-operator:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /usr/bin/scylla-operator /usr/local/bin/scylla-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/scylla-operator"]
LABEL org.opencontainers.image.title="scylla-operator" \
      org.opencontainers.image.description="Evergreen hardened ScyllaDB Operator - Kubernetes operator for ScyllaDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ScyllaDB" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
            org.opencontainers.image.source="https://github.com/scylladb/scylla-operator"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
