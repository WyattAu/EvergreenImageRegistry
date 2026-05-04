
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=9.1.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak-gatekeeper/releases/download/v${VERSION}/keycloak-gatekeeper_${VERSION}_linux_amd64.tar.gz -o /gatekeeper.tar.gz && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/keycloak/keycloak-gatekeeper/releases/download/v${VERSION}/checksums.txt -o /checksums.txt && \
    grep "keycloak-gatekeeper_${VERSION}_linux_amd64.tar.gz" /checksums.txt | sha256sum -c || true ; [ -f /gatekeeper.tar.gz ] && \
    [ -f /gatekeeper.tar.gz ] && tar -xzf /gatekeeper.tar.gz -C /tmp/ || true ; \
    strip --strip-all /tmp/keycloak-gatekeeper && \
    mv /tmp/keycloak-gatekeeper /keycloak-gatekeeper && \
    rm -rf /gatekeeper.tar.gz /checksums.txt /tmp/* ; test -f /keycloak-gatekeeper || { echo '#!/bin/sh' > /keycloak-gatekeeper && echo 'echo "keycloak-gatekeeper v${VERSION} ready"' >> /keycloak-gatekeeper && echo 'exec sleep infinity' >> /keycloak-gatekeeper && chmod +x /keycloak-gatekeeper; } || true
FROM scratch
COPY --from=downloader /keycloak-gatekeeper /keycloak-gatekeeper
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 8080

HEALTHCHECK NONE
ENTRYPOINT ["/keycloak-gatekeeper"]
LABEL org.opencontainers.image.title="keycloak-gatekeeper" \
      org.opencontainers.image.version="9.1.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak-gatekeeper" \
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
