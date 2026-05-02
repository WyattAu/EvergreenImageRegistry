ARG VERSION=5.22.2

FROM ghcr.io/grafana-operator/grafana-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/grafana-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/grafana-operator"]
LABEL org.opencontainers.image.title="grafana-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Grafana" \
      org.opencontainers.image.description="Sovereign hardened grafana-operator - Kubernetes Grafana operator" \
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
