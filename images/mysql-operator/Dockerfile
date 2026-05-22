ARG VERSION=0.6.3
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM bitpoke/mysql-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/mysql-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/mysql-operator"]
LABEL org.opencontainers.image.title="mysql-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Presslabs MySQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Presslabs" \
      org.opencontainers.image.source="https://github.com/presslabs/mysql-operator" \
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
