ARG VERSION=1.21.0

FROM ghcr.io/banzaicloud/bank-vaults:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /bank-vaults /usr/local/bin/bank-vaults
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8200

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/bank-vaults"]
LABEL org.opencontainers.image.title="vault-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Banzai Cloud" \
      org.opencontainers.image.source="https://github.com/banzaicloud/bank-vaults" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
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
