ARG VERSION=0.5.0

FROM bitpoke/mysql-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/mysql-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/mysql-operator"]
LABEL org.opencontainers.image.title="mysql-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Presslabs MySQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Presslabs" \
      org.opencontainers.image.source="https://github.com/presslabs/mysql-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
