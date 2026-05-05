ARG VERSION=0.90.1

FROM quay.io/prometheus-operator/prometheus-operator@sha256:52a6a92d915ea2fa94314748d99db7a94922e3fe63274f6182fc033b9126b573 AS upstream

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
