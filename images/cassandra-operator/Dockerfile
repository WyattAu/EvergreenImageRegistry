ARG VERSION=1.20.0

FROM ghcr.io/k8ssandra/cass-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/cass-operator
COPY --from=upstream /etc/pki/tls/certs/ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/cass-operator"]
LABEL org.opencontainers.image.title="cassandra-operator" \
      org.opencontainers.image.description="Evergreen hardened cass-operator - Kubernetes operator for Apache Cassandra" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="k8ssandra" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
