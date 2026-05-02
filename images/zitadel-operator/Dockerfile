ARG VERSION=0.5.0

FROM ghcr.io/zitadel/zitadel-operator:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /manager /usr/local/bin/zitadel-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/zitadel-operator"]
LABEL org.opencontainers.image.title="zitadel-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="ZITADEL" \
      org.opencontainers.image.source="https://github.com/zitadel/zitadel-operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
