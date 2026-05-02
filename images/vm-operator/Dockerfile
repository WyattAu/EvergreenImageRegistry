ARG VERSION=0.45.0

FROM ghcr.io/victoriametrics/operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /usr/local/bin/manager /usr/local/bin/vm-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443
ENTRYPOINT ["/usr/local/bin/vm-operator"]
LABEL org.opencontainers.image.title="vm-operator" \
      org.opencontainers.image.description="Sovereign hardened VictoriaMetrics Operator - Kubernetes operator for VictoriaMetrics" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      sovereign.image.status="functional" \
      sovereign.image.tier="1" \
      sovereign.image.category="monitoring" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
