ARG VERSION=0.45.0

FROM ghcr.io/victoriametrics/operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /usr/local/bin/manager /usr/local/bin/vm-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080 8443

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/vm-operator"]
LABEL org.opencontainers.image.title="vm-operator" \
      org.opencontainers.image.description="Evergreen hardened VictoriaMetrics Operator - Kubernetes operator for VictoriaMetrics" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="VictoriaMetrics" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="monitoring" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
