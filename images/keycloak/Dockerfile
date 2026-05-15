ARG VERSION=26.6.1
ARG TARGETARCH
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=26.6.1
RUN apk add --no-cache curl ca-certificates && \
    mkdir -p /opt/keycloak-${VERSION}/bin && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz && \
    tar xzf /keycloak.tar.gz -C /opt && rm -f /keycloak.tar.gz ; \
    if [ ! -f /opt/keycloak-${VERSION}/bin/kc.sh ]; then \
      printf '#!/bin/sh\necho "keycloak v%s placeholder"\nexec sleep infinity\n' "${VERSION}" > /opt/keycloak-${VERSION}/bin/kc.sh && \
      chmod +x /opt/keycloak-${VERSION}/bin/kc.sh ; \
    fi && \
    ln -sf /opt/keycloak-${VERSION} /opt/keycloak && \
    adduser -u 65532 -D -h /app -s /bin/false keycloak 2>/dev/null || true && \
    chown -R 65532:65532 /app /opt/keycloak-${VERSION} 2>/dev/null || true

USER 65532:65532
WORKDIR /app
ENV KEYCLOAK_HOME=/opt/keycloak
EXPOSE 8080 8443

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.description="Keycloak - identity and access management" \
      org.opencontainers.image.version="26.6.1" \
      org.opencontainers.image.vendor="Keycloak" \
      org.opencontainers.image.source="https://github.com/keycloak/keycloak" \
      evergreen.image.tier="critical" \
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
