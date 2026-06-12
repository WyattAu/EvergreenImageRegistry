ARG VERSION=0.6.26
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:0104b334637a5f19aa9c983a91b54c89887c0984081f2068983107a6f6c21eeb AS downloader
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/janeczku/calibre-web/releases/download/${VERSION}/calibreweb-${VERSION}-linux-${TARGETARCH}.tar.gz" -o /calibre-web.tar.gz && \
    mkdir -p /tmp/extract && tar -xzf /calibre-web.tar.gz -C /tmp/extract && rm -f /calibre-web.tar.gz && \
    mv /tmp/extract/calibreweb-* /tmp/calibre-web && chmod +x /tmp/calibre-web 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim

COPY --from=downloader /tmp/calibre-web /calibre-web
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8083

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8083"]

ENTRYPOINT ["/shim", "run", "-c", "/calibre-web"]
LABEL org.opencontainers.image.title="calibre-web" \
      org.opencontainers.image.description="calibre-web container image" \
      org.opencontainers.image.version="0.6.26" \
      org.opencontainers.image.vendor="Calibre-Web" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/janeczku/calibre-web"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
