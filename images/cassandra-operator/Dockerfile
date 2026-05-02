ARG VERSION=1.20.0

FROM ghcr.io/k8ssandra/cass-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/cass-operator
COPY --from=upstream /etc/pki/tls/certs/ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/cass-operator"]
LABEL org.opencontainers.image.title="cassandra-operator" \
      org.opencontainers.image.description="Sovereign hardened cass-operator - Kubernetes operator for Apache Cassandra" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="k8ssandra" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
