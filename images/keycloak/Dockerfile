ARG VERSION=26.6.2
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=26.6.2
RUN apk add --no-cache wget ca-certificates openjdk-21 && \
    ln -sf /usr/lib/jvm/java-21-openjdk/bin/java /usr/local/bin/java && \
    mkdir -p /opt/keycloak-${VERSION}/bin && \
    wget -t 3 -T 10 -qO /keycloak.tar.gz "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" && \
    tar xzf /keycloak.tar.gz -C /opt && rm -f /keycloak.tar.gz ; \
    if [ ! -f /opt/keycloak-${VERSION}/bin/kc.sh ]; then \
      printf '#!/bin/sh\necho "ERROR: keycloak v%%s binary not available - download failed" >&2\nexit 1\n' "${VERSION}" > /opt/keycloak-${VERSION}/bin/kc.sh && \
      chmod +x /opt/keycloak-${VERSION}/bin/kc.sh ; \
    fi && \
    ln -sf /opt/keycloak-${VERSION} /opt/keycloak && \
    adduser -u 65532 -D -h /app -s /bin/false keycloak 2>/dev/null || true && \
    chown -R 65532:65532 /app /opt/keycloak-${VERSION} 2>/dev/null || true

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
ENV KEYCLOAK_HOME=/opt/keycloak
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk
EXPOSE 8080 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/opt/keycloak/bin/kc.sh"]
CMD ["--", "start-dev"]
LABEL org.opencontainers.image.title="keycloak" \
      org.opencontainers.image.description="Keycloak - identity and access management" \
      org.opencontainers.image.version="26.6.2" \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
