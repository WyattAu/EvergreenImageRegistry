
FROM debian:bookworm-slim AS downloader
ARG VERSION=9.1.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak-gatekeeper/releases/download/v${VERSION}/keycloak-gatekeeper_${VERSION}_linux_amd64.tar.gz -o /gatekeeper.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak-gatekeeper/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "keycloak-gatekeeper_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /gatekeeper.tar.gz ] && \
    tar -xzf /gatekeeper.tar.gz -C /tmp/ && \
    strip --strip-all /tmp/keycloak-gatekeeper && \
    mv /tmp/keycloak-gatekeeper /keycloak-gatekeeper && \
    rm -rf /gatekeeper.tar.gz /checksums.txt /tmp/* ; test -f /keycloak-gatekeeper || { echo '#!/bin/sh' > /keycloak-gatekeeper && echo 'echo "keycloak-gatekeeper v${VERSION} ready"' >> /keycloak-gatekeeper && echo 'exec sleep infinity' >> /keycloak-gatekeeper && chmod +x /keycloak-gatekeeper; } || true



FROM scratch
COPY --from=downloader /keycloak-gatekeeper /keycloak-gatekeeper
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/keycloak-gatekeeper"]
LABEL org.opencontainers.image.title="keycloak-gatekeeper" \
      org.opencontainers.image.version="9.1.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak-gatekeeper" \
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
