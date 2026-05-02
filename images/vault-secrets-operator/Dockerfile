ARG VERSION=1.18.0

FROM hashicorp/vault-secrets-operator:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /vault-secrets-operator /usr/local/bin/vault-secrets-operator
COPY --from=upstream /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/vault-secrets-operator"]
LABEL org.opencontainers.image.title="vault-secrets-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="HashiCorp" \
      org.opencontainers.image.source="https://github.com/hashicorp/vault-secrets-operator" \
      sovereign.image.tier="2" \
      sovereign.image.category="secrets" \
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
