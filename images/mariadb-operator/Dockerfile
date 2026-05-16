ARG VERSION=26.3.0
ARG TARGETARCH

FROM ghcr.io/mariadb-operator/mariadb-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /bin/mariadb-operator /usr/local/bin/mariadb-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/mariadb-operator"]
LABEL org.opencontainers.image.title="mariadb-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="MariaDB Operator for Kubernetes" \
      org.opencontainers.image.vendor="mariadb-operator" \
      org.opencontainers.image.source="https://github.com/mariadb-operator/mariadb-operator" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
