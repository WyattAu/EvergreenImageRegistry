ARG VERSION=1.11.0

FROM cockroachdb/cockroach-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/cockroach-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/cockroach-operator"]
LABEL org.opencontainers.image.title="crdb-operator" \
      org.opencontainers.image.description="Sovereign hardened CockroachDB Operator - Kubernetes operator for CockroachDB" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Cockroach Labs" \
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
