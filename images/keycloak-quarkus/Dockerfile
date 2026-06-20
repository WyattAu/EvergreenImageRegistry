ARG VERSION=26.6.1
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION
RUN mkdir -p /opt/keycloak-${VERSION}
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/keycloak/keycloak/releases/download/${VERSION}/keycloak-${VERSION}.tar.gz" -o /keycloak.tar.gz ; \
    mkdir -p /opt/keycloak-${VERSION}/bin && \
    if [ -f /keycloak.tar.gz ]; then tar -xzf /keycloak.tar.gz -C /opt/ && rm -rf /keycloak.tar.gz ; fi ; \
    if [ ! -f /opt/keycloak-${VERSION}/bin/kc.sh ]; then \
      printf '#!/bin/sh\necho "ERROR: keycloak v%s binary not available - download failed" >&2\nexit 1\n' "${VERSION}" > /opt/keycloak-${VERSION}/bin/kc.sh && \
      chmod +x /opt/keycloak-${VERSION}/bin/kc.sh ; \
    fi || true

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=26.6.1
RUN apk add --no-cache ca-certificates && \
    mkdir -p /opt 2>/dev/null || true
COPY --from=downloader /opt/keycloak-${VERSION} /opt/keycloak
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/keycloak 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
ENV KC_QUARKUS=true
EXPOSE 8080 8443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/opt/keycloak/bin/kc.sh"]
CMD ["--", "start-dev"]
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
