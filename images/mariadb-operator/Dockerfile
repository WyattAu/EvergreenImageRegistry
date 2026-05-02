ARG VERSION=0.35.0

FROM ghcr.io/mariadb-operator/mariadb-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /bin/mariadb-operator /usr/local/bin/mariadb-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/mariadb-operator"]
LABEL org.opencontainers.image.title="mariadb-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="MariaDB Operator for Kubernetes" \
      org.opencontainers.image.vendor="mariadb-operator" \
      org.opencontainers.image.source="https://github.com/mariadb-operator/mariadb-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
