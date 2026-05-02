ARG VERSION=24.0.2

FROM quay.io/keycloak/keycloak-operator:${VERSION} AS upstream

FROM scratch
COPY --from=upstream /usr/local/bin/keycloak-operator /usr/local/bin/keycloak-operator
COPY --from=upstream /etc/pki/tls/certs/ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/keycloak-operator"]
LABEL org.opencontainers.image.title="keycloak-operator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak-operator" \
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
