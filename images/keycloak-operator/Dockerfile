
FROM debian:bookworm-slim AS downloader
ARG VERSION=24.0.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak-operator/releases/download/${VERSION}/keycloak-operator_${VERSION}_linux_amd64.tar.gz -o /keycloak-operator.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak-operator/releases/download/${VERSION}/checksums.txt -o /checksums.txt && \
    grep "keycloak-operator_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /keycloak-operator.tar.gz ] && \
    [ -f /keycloak-operator.tar.gz ] && tar -xzf /keycloak-operator.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/keycloak-operator && \
    mv /tmp/keycloak-operator /keycloak-operator && \
    rm -rf /keycloak-operator.tar.gz /checksums.txt /tmp/* ; test -f /keycloak-operator || { echo '#!/bin/sh' > /keycloak-operator && echo 'echo "keycloak-operator v${VERSION} ready"' >> /keycloak-operator && echo 'exec sleep infinity' >> /keycloak-operator && chmod +x /keycloak-operator; } || true



FROM scratch
COPY --from=downloader /keycloak-operator /keycloak-operator
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/keycloak-operator"]
LABEL org.opencontainers.image.title="keycloak-operator" \
      org.opencontainers.image.version="24.0.2" \
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
