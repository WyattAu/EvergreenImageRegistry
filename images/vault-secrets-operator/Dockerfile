ARG VERSION=1.4.0
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

FROM hashicorp/vault-secrets-operator:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /vault-secrets-operator /usr/local/bin/vault-secrets-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets-operator" \
      org.opencontainers.image.description="vault-secrets-operator container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" \
      evergreen.image.tier="2" \
      evergreen.image.category="secrets" \
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
