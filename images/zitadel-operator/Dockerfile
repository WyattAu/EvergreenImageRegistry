ARG VERSION=0.5.0
ARG TARGETARCH

FROM ghcr.io/zitadel/zitadel-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/zitadel-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/zitadel-operator"]
LABEL org.opencontainers.image.title="zitadel-operator" \
      org.opencontainers.image.description="zitadel-operator container image" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel-operator" \
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
