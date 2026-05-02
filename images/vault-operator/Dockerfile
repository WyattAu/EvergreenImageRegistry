ARG VERSION=1.21.0

FROM ghcr.io/banzaicloud/bank-vaults:v${VERSION} AS upstream

FROM scratch
COPY --from=upstream /bank-vaults /usr/local/bin/bank-vaults
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8200
ENTRYPOINT ["/usr/local/bin/bank-vaults"]
LABEL org.opencontainers.image.title="vault-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Banzai Cloud" \
      org.opencontainers.image.source="https://github.com/banzaicloud/bank-vaults" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
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
