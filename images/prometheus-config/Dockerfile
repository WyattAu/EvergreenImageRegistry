ARG VERSION=0.90.1

FROM quay.io/prometheus-operator/prometheus-operator:v0.90.1 AS upstream

FROM scratch
COPY --from=upstream /prometheus-operator /prometheus-config-reloader
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/prometheus-config-reloader"]
LABEL org.opencontainers.image.title="prometheus-config" \
      org.opencontainers.image.version="0.90.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Evergreen hardened prometheus-config - Prometheus config reloader" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"

EXPOSE 9101
STOPSIGNAL SIGTERM
