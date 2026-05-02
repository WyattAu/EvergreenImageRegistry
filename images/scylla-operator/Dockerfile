ARG VERSION=1.13.0

FROM docker.io/scylladb/scylla-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /usr/bin/scylla-operator /usr/local/bin/scylla-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/scylla-operator"]
LABEL org.opencontainers.image.title="scylla-operator" \
      org.opencontainers.image.description="Sovereign hardened ScyllaDB Operator - Kubernetes operator for ScyllaDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ScyllaDB" \
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
