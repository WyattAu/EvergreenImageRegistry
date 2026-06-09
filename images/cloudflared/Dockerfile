ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian:bookworm-slim AS downloader
ARG VERSION=2026.5.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://github.com/cloudflare/cloudflared/releases/download/${VERSION}/cloudflared-linux-$(echo $TARGETPLATFORM | sed "s|linux/||")" -o /cloudflared && \
    chmod +x /cloudflared

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=downloader /cloudflared /cloudflared
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /
EXPOSE 7844 9101
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:7844"]
ENTRYPOINT ["/shim", "run", "-c", "/cloudflared"]
LABEL org.opencontainers.image.title="cloudflared" \
      org.opencontainers.image.description="Cloudflare Tunnel client" \
      org.opencontainers.image.version="2026.5.0" \
      org.opencontainers.image.vendor="Cloudflare" \
      org.opencontainers.image.platforms="linux/amd64,linux/arm64" \
      org.opencontainers.image.source="https://github.com/cloudflare/cloudflared" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="binary-download" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="http" \
      evergreen.health.endpoint="/livez" \
      evergreen.health.listen="0.0.0.0:9101" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
