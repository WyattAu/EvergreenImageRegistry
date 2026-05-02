ARG VERSION=1.12.0

FROM registry.opensource.zalan.do/acid/postgres-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /postgres-operator /usr/local/bin/postgres-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/postgres-operator"]
LABEL org.opencontainers.image.title="postgres-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Zalando PostgreSQL Operator for Kubernetes" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/zalando/postgres-operator" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
