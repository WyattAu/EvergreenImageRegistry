ARG VERSION=0.90.1

FROM quay.io/prometheus-operator/prometheus-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /bin/operator /usr/local/bin/prometheus-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/prometheus-operator"]
LABEL org.opencontainers.image.title="prometheus-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Sovereign hardened prometheus-operator - Kubernetes Prometheus operator" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
