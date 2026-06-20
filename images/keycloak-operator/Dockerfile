ARG VERSION=26.6.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM quay.io/keycloak/keycloak-operator:${VERSION} AS upstream

ARG SHIM_VERSION=v1.2.0
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=upstream /usr/local/bin/keycloak-operator /usr/local/bin/keycloak-operator
COPY --from=upstream /etc/pki/tls/certs/ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/keycloak-operator"]
LABEL org.opencontainers.image.title="keycloak-operator" \
      org.opencontainers.image.description="keycloak-operator container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak-operator" \
      evergreen.image.tier="2" \
      evergreen.image.category="identity" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
