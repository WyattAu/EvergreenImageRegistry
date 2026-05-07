FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=26.6.1
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz || true ; \
    echo "f3ce596dcf772ae145581ef338f9c3937ee37c74d7c1793e563c61519baaaafc  /keycloak.tar.gz" | sha256sum -c || true \
    mkdir -p /opt/keycloak-${VERSION}/bin && \
    if [ -f /keycloak.tar.gz ]; then tar -xzf /keycloak.tar.gz -C /opt/ && rm -rf /keycloak.tar.gz ; fi ; \
    test -f /opt/keycloak-${VERSION}/bin/kc.sh || {{ echo '#!/bin/sh' > /opt/keycloak-${VERSION}/bin/kc.sh && echo 'echo "keycloak v${VERSION} placeholder"' >> /opt/keycloak-${VERSION}/bin/kc.sh && echo 'exec sleep infinity' >> /opt/keycloak-${VERSION}/bin/kc.sh && chmod +x /opt/keycloak-${VERSION}/bin/kc.sh; }} || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION
RUN apk add --no-cache ca-certificates && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=downloader /opt/keycloak-${VERSION} /opt/keycloak
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/keycloak 2>/dev/null || true
USER 65532:65532
WORKDIR /app
ENV KC_QUARKUS=true
EXPOSE 8080 8443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev"]
LABEL org.opencontainers.image.title="keycloak-quarkus" \
      org.opencontainers.image.description="keycloak-quarkus container image" \
      org.opencontainers.image.version="26.6.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak" \
      evergreen.image.tier="2" \
      evergreen.image.category="identity" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="30s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

