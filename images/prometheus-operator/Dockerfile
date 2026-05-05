ARG VERSION=0.90.1

FROM quay.io/prometheus-operator/prometheus-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /bin/operator /usr/local/bin/prometheus-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/prometheus-operator"]
LABEL org.opencontainers.image.title="prometheus-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Evergreen hardened prometheus-operator - Kubernetes Prometheus operator" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
            org.opencontainers.image.source="https://github.com/prometheus-operator/prometheus-operator"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
