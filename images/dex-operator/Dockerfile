ARG VERSION=0.18.0

FROM ghcr.io/dexidp/dex-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/dex-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/usr/local/bin/dex-operator"]
LABEL org.opencontainers.image.title="dex-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="DexIDP" \
      org.opencontainers.image.source="https://github.com/dexidp/dex-operator" \
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

EXPOSE 9101
STOPSIGNAL SIGTERM
