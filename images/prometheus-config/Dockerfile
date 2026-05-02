ARG VERSION=0.90.1

FROM quay.io/prometheus-operator/prometheus-operator:v0.90.1 AS upstream

FROM scratch
COPY --from=upstream /prometheus-operator /prometheus-config-reloader
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/prometheus-config-reloader"]
LABEL org.opencontainers.image.title="prometheus-config" \
      org.opencontainers.image.version="0.90.1" \
      org.opencontainers.image.vendor="Prometheus" \
      org.opencontainers.image.description="Sovereign hardened prometheus-config - Prometheus config reloader" \
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
