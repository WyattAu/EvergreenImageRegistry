ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:0104b334637a5f19aa9c983a91b54c89887c0984081f2068983107a6f6c21eeb AS downloader
ARG TARGETARCH
ARG VERSION=v7.15.2
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/oauth2-proxy/oauth2-proxy/releases/download/${VERSION}/oauth2-proxy-${VERSION}.linux-${TARGETARCH}.tar.gz -o /oauth2-proxy.tar.gz ; \
    mkdir -p /tmp/extract && tar -xzf /oauth2-proxy.tar.gz -C /tmp/extract && rm -f /oauth2-proxy.tar.gz && \
    mv /tmp/extract/oauth2-proxy-*/oauth2-proxy /tmp/oauth2-proxy && chmod +x /tmp/oauth2-proxy 2>/dev/null ; \binary not available - download failed" >&2"' >> /tmp/oauth2-proxy && echo 'exit 1' >> /tmp/oauth2-proxy && chmod +x /tmp/oauth2-proxy; }


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tmp/oauth2-proxy /oauth2-proxy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
WORKDIR /app
EXPOSE 80 443

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:80"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="oauth2-proxy" \
      org.opencontainers.image.version="v7.15.2" \
      org.opencontainers.image.vendor="OAuth2 Proxy" \
      org.opencontainers.image.description="OAuth2 Proxy - reverse proxy with authentication provider" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/oauth2-proxy/oauth2-proxy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
